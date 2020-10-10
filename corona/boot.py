#boot.py
import network
import gc
gc.collect()
ssid = "Makerfabs"
password = "20160704"
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
  pass
