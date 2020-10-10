import gc
import esp
import webrepl
import machine
import network

esp.osdebug(0)


wlan = network.WLAN()  # get current object, without changing the mode
print(wlan.ifconfig())
if machine.reset_cause() != machine.SOFT_RESET:
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # configuration below MUST match your home router settings!!
    wlan.ifconfig(['192.168.1.199', '255.255.255.0',
                   '192.168.1.1', '203.113.131.2'])

if not wlan.isconnected():
    # change the line below to match your network ssid, security and password
    wlan.connect('PhongLy', '0905653008')
    while not wlan.isconnected():
        machine.idle()  # save power while waiting
print(wlan.ifconfig())


webrepl.start()
gc.collect()
