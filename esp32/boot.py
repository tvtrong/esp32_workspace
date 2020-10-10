import webrepl
import esp
import gc
import network
import connectWifi

esp.osdebug(0)
if connectWifi.is_connect() is False:
    connectWifi.connect()
webrepl.start()
gc.collect()
