# Posty Project: opensocket_client_example.py
# Copyright (c) 2019 Clayton Darwin claytondarwin@gmail.com

# notify
print('LOAD: opensocket_client_example.py')

# ----------------------------------------------
# imports
# ----------------------------------------------

# standard library imports
import sys,time,traceback,socket,select

# ----------------------------------------------
# example: run opensocket_client.py
# ----------------------------------------------

# server variables
server_ip = '192.168.1.10'
server_port = 8000

# client
import opensocket_client

#run function
def run():

    # client setup
    client = opensocket_client.OpenSocket_Client()
    client.server_ip = server_ip
    client.server_port = server_port

    # connect to server
    client.connect()

    # sent line count
    lc = 0

    # catch keyboard interrupt
    try:

        # loop forever (or until EOD)
        while 1:

            # make a data line
            lc += 1
            line = 'Data Line {}.'.format(lc)        

            # send data
            client.sendline(line)
            print('SENT:',line)

            # wait a bit for processing
            time.sleep(0.1)

            # watch for EOD
            eod = False

            # loop to get all available lines
            while 1:

                # get a line
                line = client.getline()

                # no line
                if not line:
                    break

                # got a line
                print(' GET:',line)

                # end of data from server
                if line == b'EOD':
                    eod = True

            # EDO happened
            if eod:
                break

            # wait a bit
            time.sleep(1)

    # close example
    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    # disconnect from server
    client.disconnect()


if __name__ in ('__main__','opensocket_client_example'):
    run()

# ----------------------------------------------
# end
# ----------------------------------------------

