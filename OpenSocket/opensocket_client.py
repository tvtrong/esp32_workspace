# Posty Project: opensocket_client.py
# Copyright (c) 2019 Clayton Darwin claytondarwin@gmail.com

# notify
import select
import socket
import traceback
import time
import sys
print('LOAD: opensocket_client.py')

# ----------------------------------------------
# imports
# ----------------------------------------------

# standard library imports

# ----------------------------------------------
# simple non-threaded socket client
# ----------------------------------------------


class OpenSocket_Client:

    # ----------------------------------------------

    # this is an example of how you might interact with the OpenSocket_Server
    # this has minimal socket management (i.e. no reconnect and such)

    # connect and sendline errors (or closed socket) will raise exceptions
    # getline and waitforline will not raise exceptions (will return None)

    # set the ip and port variables, then connect()

    # use sendline(line) to send a line of str or bytes data
    # sent data will be converted bytes(str(line),'utf-8','?').strip() + b'\r\n'

    # use getline() to get a line of data from server
    # it will read io buffer and parse lines
    # it will return None if there are no lines
    # it will return bytes.strip() data if there is a line
    # it does not wait for a line if none are available

    # use waitforline(timeout_seconds) to get a line if you want to wait
    # it will keep trying until timeout is up
    # it will return same data as getline()

    # ----------------------------------------------

    # user defined variables
    server_ip = '192.168.1.10'
    server_port = 8000
    server_connect_timeout = 10  # how long to try and connect

    # process variables
    socket = None
    socket_lines = []
    socket_buffer = b''

    def connect(self):

        # try connect
        try:

            # clear data
            socket_lines = []

            # close open socket
            self.disconnect()

            # create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(0.0)  # non-blocking

            # when to stop trying
            stop_at = time.time() + self.server_connect_timeout

            # try to connect
            while 1:

                if self.socket.connect_ex((self.server_ip, self.server_port)) == 0:
                    print('SOCKET CONNECTED')
                    break

                elif time.time() >= stop_at:
                    raise OSError('No route to host.')

                else:
                    #print('CONNECT WAIT')
                    time.sleep(0.1)

            # done
            return True

        # connect failed
        except Exception as e:
            print(traceback.format_exc())
            self.disconnect()  # may raise errors
            raise e

    def disconnect(self):

        # socket did exist
        if self.socket:

            # attempt to inform server
            try:
                self.socket.sendall(b'EOD\r\n')
                time.sleep(0.5)  # wait a bit for send to happen
            except:
                pass

            # attempt to formally close socket
            try:
                self.socket.close()
            except:
                pass

            # notify
            print('SOCKET CLOSED')

        # set socket to None
        self.socket = None

    def sendline(self, line):

        # socket must be open
        if not self.socket:
            raise OSError('Socket is not open.')

        # data must be bytes
        if type(line) != bytes:
            line = bytes(str(line), 'utf-8', '?')

        # format
        line = line.strip() + b'\r\n'

        # catch broken pipe
        try:
            self.socket.sendall(line)

        # broken pipe
        except BrokenPipeError as e:
            self.disconnect()
            raise e

        # done
        return len(line)

    def getline(self):

        # line exists in buffer
        if self.socket_lines:
            return self.socket_lines.pop(0)

        # socket closed
        if not self.socket:
            return None

        # read io buffer data
        while 1:
            rlist, wlist, xlist = select.select([self.socket], [], [], 0.01)
            if rlist:
                self.socket_buffer += self.socket.recv(1024)
            else:
                break

        # parse bytes buffer
        if b'\r\n' in self.socket_buffer:
            self.socket_buffer = self.socket_buffer.split(b'\r\n')
            for line in self.socket_buffer[:-1]:
                line = line.strip()
                if line:
                    self.socket_lines.append(line)
                    if line == b'EOD':
                        self.disconnect()
            self.socket_buffer = self.socket_buffer[-1]

        # return line
        if self.socket_lines:
            return self.socket_lines.pop(0)
        else:
            return None

    def waitforline(self, timeout=10):

        # line exists in buffer
        if self.socket_lines:
            return self.socket_lines.pop(0)

        # socket closed
        if not self.socket:
            return None

        # when to stop trying
        stop_at = time.time() + timeout

        # loop until timeout
        while 1:

            line = self.getline()

            if line:
                return line

            elif time.time() >= stop_at:
                return None

            else:
                time.sleep(0.01)

# ----------------------------------------------
# end
# ----------------------------------------------
