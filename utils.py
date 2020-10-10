import usocket as socket
import os
import socket

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
            # Python 2.7: remove the second argument for the bytes call
        )[20:24])


def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0", "eth1", "eth2", "wlan0",
                      "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip


def sendudp(host, port):
    address = ("127.0.0.1", 8000)
    data = b'1'

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("data is type {}".format(type(data)))

    sock.sendto(data, address)


def sendtcp(host, port):
    data = b'1'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("data is type {}".format(type(data)))

    sock.connect((host, port))
    sock.send(data)
    o = sock.recv(500)
    print(o)
    sock.close()
