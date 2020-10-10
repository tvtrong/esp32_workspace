import network


def connect():
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print("Already connected to Wifi")
        return
    else:
        ip = '192.168.1.199'
        subnet = '255.255.255.0'
        gateway = '192.168.1.1'
        dns = '203.113.131.2'
        ssid = "PhongLy"
        password = "0905653008"
        print("Connecting.....")
        station.active(True)
        station.ifconfig((ip, subnet, gateway, dns))
        station.connect(ssid, password)
        print("Connection successful")
        print(station.ifconfig())
        while not station.isconnected():
            pass


def is_connect():
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        return False
    else:
        return True


def disconnect():
    import network
    station = network.WLAN(network.STA_IF)
    station.disconnect()
    station.active(False)
