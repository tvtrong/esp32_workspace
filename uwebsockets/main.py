
import os
import client
import connectWifi
import usocket
import socket
import logging
import json

connectWifi.connect()


def hello():
    with client.connect('ws://192.168.1.6:8000/ws/led/') as websocket:
        msg = websocket.recv()
        print("< {}".format(msg))


hello()


# def updateStats(url):
#    _, _, host, path = url.split('/', 3)
#    connectto = usocket.getaddrinfo(host, 8000)[0][4]
#    s = usocket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    try:
#        s.connect(connectto)
#        print("connected to ", connectto)
#        try:

#            # send some data
#            request = "GET /%s HTTP/1.1\r\nHost:%s\r\n\r\n" % (path, host)
#            # s.send(bytes('GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n' %
#            #             (path, host), 'utf8'))
#            s.send(request.encode())
#            response = s.recv(4096)
#            http_response = repr(response)
#            http_response_len = len(http_response)
#            print(http_response, http_response_len)
#            if response:
#                print(str(response, 'utf8'), end='')
#        except Exception as e:
#            print(e)
#        s.close()
#    except Exception as e:
#        print(e)
#        return


# updateStats('http://192.168.1.10/led/')
