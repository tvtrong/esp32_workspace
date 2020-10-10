# Posty Project: opensocket_server_example.py
# Copyright (c) 2019 Clayton Darwin claytondarwin@gmail.com

# notify
print('RUN: opensocket_server_example.py')

# ----------------------------------------------
# imports
# ----------------------------------------------

# standard library imports
import sys,time,gc,socket

# ----------------------------------------------
# example: run opensocket_server.py
# ----------------------------------------------

# network
from nettools import wlan_connect,wlan_disconnect

# server
import opensocket_server

# run function
def run():

    # end
    print('OpenSocket Server DEMO Starting')

    # network connect
    essid = 'my_essid'
    essid_password = 'my_essid_password'
    from nettools import wlan_connect,wlan_disconnect # must be local
    wlan_connect(essid,essid_password,timeout=15)

    # server setup
    server = opensocket_server.OpenSocket_Server()
    server.server_host = '0.0.0.0'
    server.server_port = 8888
    server.client_timeout = 10

    # server start
    try:
        server.serve()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.print_exception(e)

    # network disconnect
    wlan_disconnect()

    # end
    print('OpenSocket Server DEMO Ended')

if __name__ in ('__main__','opensocket_server_example'):
    run()

# ----------------------------------------------
# end
# ----------------------------------------------

