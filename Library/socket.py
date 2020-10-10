import usocket as socket


def sendudp(host, port):
    address = ("127.0.0.1", 8000)
    data = b'hello udp'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("data is type {}".format(type(data)))

    sock.sendto(data, address)


def sendtcp(host, port):
    data = b'hello tcp'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("data is type {}".format(type(data)))

    sock.connect((host, port))
    sock.send(data)
    sock.close()
