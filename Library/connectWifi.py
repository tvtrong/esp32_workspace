def connect():
    import network

    ip = '192.168.1.200'
    subnet = '255.255.255.0'
    gateway = '192.168.1.1'
    dns = '203.113.131.2'
    ssid = "PhongLy"
    password = "0905653008"

    station = network.WLAN(network.STA_IF)

    if station.isconnected() == True:
        print("Already connected")
        return

    station.active(True)
    station.ifconfig((ip, subnet, gateway, dns))
    station.connect()

    while station.isconnected() == False:
        pass

    print("Connection successful")
    print(station.ifconfig())


def disconnect():
    import network
    station = network.WLAN(network.STA_IF)
    station.disconnect()
    station.active(False)
