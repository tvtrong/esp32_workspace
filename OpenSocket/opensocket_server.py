# Posty Project: opensocket_server.py
# Copyright (c) 2019 Clayton Darwin claytondarwin@gmail.com

# notify
print('LOAD: opensocket_server.py')

# ----------------------------------------------
# imports
# ----------------------------------------------

# standard library imports
import sys,time,gc,socket

# ----------------------------------------------
# socker server
# ----------------------------------------------

class OpenSocket_Server:

    # ----------------------------------------------

    # creates server socket
    # accepts client sockets 1 at a time
    # opens client socket, keeps it open
    # accepts lines of data delineated by b'\r\n'
    # sends each line to OpenSocket_Server.application
    # sends application return value (should be a line) to client socket
    # repeat until receiving b'EOD\r\n' from client, or a timeout, or a crash
    # sends b'EOD\r\n' to client socket
    # accepts next client socket

    # when a new client socket is opened...
    # send b'_client:client_number' to application
    # send b'_ip:client_ip' to application
    # return values are not sent to client

    # on timeout...
    # send b'TIMEOUT\r\n' to client
    # then close(see below)
    
    # on error and/or close...
    # send b'EOD' to application
    # send b'EOD\r\n' to client socket

    # lines sent to application are bytes.strip()
    # lines received from application are converted with bytes(str(response),'utf-8')
    # lines received from application are stripped and b'\r\n' is added to end
    # i.e. lines sent to client are bytes.strip() + b'\r\n'

    # timeout value is allowable time since last transaction with client
    # client must send data (i.e. b'PING\r\n') to keep socket open
    # application should handle PING by returning 'PING' + application ID (see example below)

    # client should send b'EOD\r\n' to close socket

    # ----------------------------------------------

    # user-defined server variables
    server_host = '0.0.0.0'
    server_port = 8765
    client_timeout = 10 # seconds after last data received

    # EXAMPLE APPLICATION (should be replaced by user application)
    # this just bounces the input line back to the server
    def application(self,line):

        # line in is bytes and stripped
        # return str or bytes

        print('  APP LINEIN:',line)

        # ----------------------------------------------
        # empty lines        

        if not line:
            return 'ERROR no data'

        # ----------------------------------------------
        # server lines        

        # PING
        elif line == b'PING':
            print('    RETURN:',b'PING Example APP')
            return b'PING Example APP'

        # EOD
        elif line == b'EOD':
            return line
            
        # server indicates new client
        elif line[:8] == b'_client:':
            return line

        # server gives ip
        elif line[:4] == b'_ip:':
            return line

        # ----------------------------------------------
        # client lines

        # anything
        else:
            print('    RETURN:',b'BOUNCE '+line)
            return b'BOUNCE '+line

    # serve forever
    def serve(self):

        # check server address outside of loop and catch
        self.server_address = socket.getaddrinfo(self.server_host,self.server_port)[0][-1]

        # client connection count
        cc = 0 

        # restart forever (except KeyboardInterrupt)
        while 1:

            # catch all
            try:

                # open server socket
                server_socket = socket.socket()
                server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                server_socket.bind(self.server_address)
                server_socket.listen(1)
                print('OpenSocket Server listening on addr {}.'.format(self.server_address))

                # accept request loop
                while 1:

                    # accept a request
                    client_socket,client_address = server_socket.accept()
                    client_socket.settimeout(0) # 0 = non-blocking

                    # start variables
                    t1 = time.ticks_ms()
                    cc += 1

                    # notify
                    print('Client {} - OPEN - IP:{}'.format(cc,client_address[0]))

                    # send init data to application (nothing sent to client)
                    for item,value in (('_client',cc),
                                       ('_ip',client_address[0]),
                                       ):
                        self.application(bytes('{}:{}'.format(item,value),'ascii','?'))

                    # input variables
                    timeout = time.ticks_add(self.client_timeout*1000,time.ticks_ms()) # updated after client transaction                    
                    bytes_in = 0
                    bytes_out = 0
                    buffer = b''
                    eod = False
                    lc = 0 # client line count

                    # catch client socket errors
                    try:

                        # loop
                        while 1:

                            # read data (non-blocking, so may be empty)
                            data = client_socket.read(256)

                            # no data
                            if not data:

                                # timeout period since last read passed
                                if time.ticks_diff(time.ticks_ms(),timeout) >= 0:
                                    print('TIMEOUT: {} seconds since last data.'.format(self.client_timeout))
                                    bytes_out += client_socket.write(b'TIMEOUT\r\n')
                                    break

                                # wait and try again
                                else:
                                    time.sleep_ms(10)

                            # new data
                            else:

                                # add to current buffer
                                bytes_in += len(data)
                                buffer += data

                                # parse buffer
                                if b'\r\n' in buffer:

                                    # split (last item won't be a full line)
                                    buffer = buffer.split(b'\r\n')

                                    # process lines in buffer
                                    for line in buffer[:-1]:
                                        lc += 1
                                        line = line.strip()

                                        # ping
                                        if line in (b'PING',b'ping'):
                                            response = self.application(b'PING')
                                            if type(response) != bytes:
                                                response = bytes(str(response),'utf-8')
                                            bytes_out += client_socket.write(response.strip()+b'\r\n')

                                        # end of data (don't notify client or app here)
                                        elif line in (b'EOD',b'eod'):
                                            eod = True
                                            break

                                        # process line (send result to client)
                                        elif line:
                                            response = self.application(line)
                                            if type(response) != bytes:
                                                response = bytes(str(response),'utf-8')
                                            lineid = bytes('L{} '.format(lc),'ascii')
                                            bytes_out += client_socket.write(lineid+response.strip()+b'\r\n')

                                    # reset line buffre
                                    buffer = buffer[-1]

                                # reset timeout after transaction
                                timeout = time.ticks_add(self.client_timeout*1000,time.ticks_ms())

                            # break on EOD
                            if eod:
                                break

                        # no EOD and buffer has input data
                        if (not eod) and buffer:
                            lc += 1
                            response = self.application(buffer)
                            if type(response) != bytes:
                                response = bytes(str(response),'utf-8')
                            lineid = bytes('L{} '.format(lc),'ascii')
                            bytes_out += client_socket.write(lineid+response.strip()+b'\r\n')

                        # send EOD to client
                        bytes_out += client_socket.write(b'EOD\r\n')

                    # catch client socket errors
                    except OSError as e:
                        sys.print_exception(e)
                        print('Client socket error.')

                    # send EOD to app (always)
                    self.application(b'EOD')

                    # clean up big stuff
                    buffer,data,block = None,None,None

                    # close client socket
                    client_socket.close()

                    # notify
                    print('Client {} - CLOSED - IN:{} OUT:{} SECS:{}'.format(cc,bytes_in,bytes_out,round(time.ticks_diff(time.ticks_ms(),t1)/1000.0,2)))

                    # clean up
                    gc.collect()

            # keyboard kill
            except KeyboardInterrupt:
                print('KeyboardInterrupt: End server loop.')
                break

            # any other exception
            except Exception as error:
                print('Exception: Go to socket reset.')
                sys.print_exception(error)

            # close main socket
            server_socket.close()
            print('OpenSocket Server closed.')

# ----------------------------------------------
# end
# ----------------------------------------------

