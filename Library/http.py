import urequests
import time
import random


def http_get(url):
    import socket
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    print(addr)
    s = socket.socket()
    try:
        s.connect(addr)
        s.send(bytes('GET /en/datas/ HTTP/1.1\r\nHost: %s\r\n\r\n' %
                     (host), 'utf8'))
    except OSError as e:
        print(e)
    while True:
        data = s.recv(255)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()


def get_api(url):
    import json

    headers = {'Content-type': 'application/json'}

    url = url

    for i in range(100):
        response = urequests.get(url)
        print(response.json())
        time.sleep(5)
