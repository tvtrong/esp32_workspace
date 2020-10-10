# Copyright (c) 2019 Clayton Darwin
# symple.design/clayton claytondarwin@gmail.com

# notify
print('LOAD: nettools.py')

# imports
import time,network,gc
gc.collect()

# setup on import
network.WLAN(network.STA_IF).active(False)
network.WLAN(network.AP_IF).active(False)

# scan for WiFi LANs (access points)
def wlan_scan():
    from ubinascii import hexlify as temphex
    wlan = network.WLAN(network.STA_IF)
    state = wlan.active() # save current state
    wlan.active(True) # set state active
    for ssid,bssid,channel,RSSI,authmode,hidden in wlan.scan():
        ssid = ssid.decode('ascii')
        bssid = temphex(bssid).decode('ascii')
        if len(bssid) == 12:
            bssid = ':'.join([bssid[x:x+2] for x in range(0,12,2)])
        authmode = ('OPEN','WEP','WPA-PSK','WPA2-PSK','WPA/WPA2-PSK')[min(4,max(0,authmode))]
        if hidden:
            hidden = True
        else:
            False
        #hidden = (False,True)[min(1,max(0,hidden))]
        print('Network AP:',[ssid,bssid,channel,RSSI,authmode,hidden])
    wlan.active(state) # return to pervious state
    del temphex

# connect to WiFi AP
def wlan_connect(essid,password,timeout=15):
    print('Network Connect:',essid)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid,password)
        time.sleep(0.1)
        for x in range(timeout):
            if wlan.isconnected():
                break
            time.sleep(1)
    return_value = wlan.isconnected()
    print('Network Connect:',essid,return_value)
    return return_value

# disconnect from WiFi AP
def wlan_disconnect(timeout=15):
    print('Network Disconnect')
    wlan = network.WLAN(network.STA_IF)
    return_value = True
    if wlan.active():
        if wlan.isconnected():
            wlan.disconnect()
            time.sleep(0.1)
            for x in range(timeout):
                if not wlan.isconnected():
                    break
                time.sleep(1)
            return_value = not wlan.isconnected()
    wlan.active(False)
    print('Network Disonnect:',return_value)
    return return_value
