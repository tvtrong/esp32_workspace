import os
import client
import logging
import time
import urequests
import dht11
import connectWifi
import machine
import ujson
import sys

repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
LED = machine.Pin(2, machine.Pin.OUT)
LED.value(1)


if connectWifi.is_connect() is False:
    connectWifi.connect()


def send_data(post_data):
    headers = {'Content-type': 'application/json'}
    request_url = 'http://192.168.1.179:8000/dht11/api/list/'
    datai = ujson.dumps(post_data)
    try:
        response = urequests.post(request_url, data=datai, headers=headers)
        response.close()
    except OSError as err:
        print("lỗi ở hàm send_data(post_data) --> ", err)
        pass


update_0 = dht11.get()
TEMP = update_0.get("temperature")
HUMI = update_0.get("humidity")


def send_new():
    try:
        # lấy data cảm biến DHT11
        global TEMP, HUMI
        update_i = dht11.get()
        if update_i.get("temperature") != TEMP or update_i.get("humidity") != HUMI:
            send_data(update_i)
            TEMP = update_i.get("temperature")
            HUMI = update_i.get("humidity")
    except OSError as err:
        print("lỗi ở hàm send_new() --> ", err)
        pass


def send_sensor():
    with client.connect('ws://192.168.1.179:8000/ws/dht11/') as websocket:
        # lấy data điều khiển LED
        update_i = dht11.get()
        dht11i = {
            'temperature': update_i.get('temperature'),
            'humidity': update_i.get('humidity')
        }
        msg = {
            "dht11": dht11i,
            "led": 2
        }
        msg = ujson.dumps(msg)
        try:
            websocket.send(msg)
            rep = websocket.recv()
            json_msg = ujson.loads(rep)
            led = json_msg['led']
            if led == 1:
                LED.value(0)
            elif led == 0:
                LED.value(1)
            else:
                pass
        except OSError as err:
            print("lỗi ở hàm send_data() --> ", err)
            pass


with client.connect('ws://192.168.1.179:8000/ws/dht11/') as websocket:
    while True:
        if repl_button.value() == 0:
            print("Dropping to REPL")
            sys.exit()
        else:
            try:
                # lấy data cảm biến DHT11
                update_i = dht11.get()
                try:
                    if update_i.get("temperature") != TEMP or update_i.get("humidity") != HUMI:
                        send_data(update_i)
                        TEMP = update_i.get("temperature")
                        HUMI = update_i.get("humidity")
                except OSError as err:
                    print("send_new()", err)
                    pass
                dht11i = {
                    'temperature': update_i.get('temperature'),
                    'humidity': update_i.get('humidity')
                }
                msg = {
                    "dht11": dht11i,
                    "led": 2
                }
                msg = ujson.dumps(msg)
                try:
                    websocket.send(msg)
                    rep = websocket.recv()
                    json_msg = ujson.loads(rep)
                    led = json_msg['led']
                    if led == 1:
                        LED.value(0)
                    elif led == 0:
                        LED.value(1)
                    else:
                        pass
                except OSError as err:
                    print("send_sensor ", err)
                    pass
                time.sleep(1)
            except Exception as err:
                print("while ", err)
                pass


while 1:
    with client.connect('ws://192.168.1.179:8000/ws/dht11/') as websocket:
        if repl_button.value() == 0:
            print("Dropping to REPL")
            sys.exit()
        else:
            time.sleep(0.3)
            rep = websocket.recv()
            json_msg = ujson.loads(rep)
            led = json_msg['led']
            if led == 1:
                LED.value(0)
            elif led == 0:
                LED.value(1)
            else:
                pass
            try:
                # lấy data cảm biến DHT11
                update_i = dht11.get()
                ''' nếu có thay đổi giá trị cảm biến thì :
                    1. cập nhật CSDL
                    2. gửi dữ liệu qua frontend qua Socket
                '''
                if update_i.get("temperature") != TEMP or update_i.get("humidity") != HUMI:
                    send_data(update_i)
                    print("cập nhật dữ liệu mới : \n", update_i)
                    time.sleep(0.3)
                    TEMP = update_i.get("temperature")
                    HUMI = update_i.get("humidity")
                    dht11i = {
                        'temperature': update_i.get('temperature'),
                        'humidity': update_i.get('humidity')
                    }
                    msg = {
                        "dht11": dht11i,
                        "led": 2
                    }
                    msg = ujson.dumps(msg)
                    websocket.send(msg)
                else:
                    continue
            except Exception as err:
                print("--lỗi--> ", err)
                time.sleep(0.3)
                pass
