import os
import sys
import time
import machine
import urequests
import connectWifi
import logging
import client
import dht11
import ujson
# nhấn nút --|BOOT|-- trên esp32 để dừng chương trình
repl_button = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
# led --|XANH|-- onboard
LED = machine.Pin(2, machine.Pin.OUT)
LED.value(1)

# gửi dữ liệu đến API endpoint : http://192.168.1.179:8000/dht11/api/list/


def send_data(post_data):
    if connectWifi.is_connect() is False:
        connectWifi.connect()
    else:
        headers = {'Content-type': 'application/json'}
        request_url = 'http://192.168.1.179:8000/dht11/api/list/'
        datai = ujson.dumps(post_data)
        try:
            response = urequests.post(
                request_url, data=datai, headers=headers)
            response.close()
        except OSError as err:
            print(
                "không kết nối được: \nhttp: // 192.168.1.179: 8000/dht11/api/list/", err)
            pass


'''
def send_data(post_data):
    if connectWifi.is_connect() is False:
        connectWifi.connect()
    else:
        headers = {'Content-type': 'application/json'}
        json = {"query": "mutation{\n  createDht11(input:{temperature:%f, humidity: %f}){\n    temperature\n    humidity\n  }\n}" % post_data.get(
            "temperature") % post_data.get("humidity")}
        #request_url = 'http://192.168.1.179:8000/dht11/api/list/'
        #datai = ujson.dumps(post_data)
        request_url = 'http://192.168.1.179:8000/api/'
        try:
            #response = urequests.post(request_url, data=datai, headers=headers)
            response = urequests.post(request_url, json=json, headers=headers)
            response.close()
        except OSError as err:
            print(
                "không kết nối được: \nhttp: // 192.168.1.179: 8000/api/", err)
            pass
'''

# lấy mẫu cảm biến DHT11
update_0 = dht11.get()
TEMP = update_0.get("temperature")
HUMI = update_0.get("humidity")

while 1:
    with client.connect('ws://192.168.1.179:8000/ws/dht11/') as websocket:
        if repl_button.value() == 0:
            print("Dropping to REPL ", repl_button.value())
            sys.exit()
        else:
            try:
                time.sleep(0.5)
                # lấy data cảm biến DHT11
                update_i = dht11.get()
                ''' nếu có thay đổi giá trị cảm biến thì :
                    1. cập nhật CSDL
                    2. gửi dữ liệu qua frontend qua Socket
                '''
                if update_i.get("temperature") != TEMP or update_i.get("humidity") != HUMI:
                    send_data(update_i)
                    print("cập nhật dữ liệu mới : \n", update_i)
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
                time.sleep(0.5)
                msg = ujson.dumps(msg)
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
            except Exception as e:
                continue
