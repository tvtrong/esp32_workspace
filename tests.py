import machine
import network
import socket
import utime
import time
import sys
from machine import Pin
from ntptime import settime
prg_n = 'ESP_SocketDemo.py'
#
# NOTE - Server socket must be up and running first
# This prog uploads the first file found in '/DATA' dir on the ESP8266
# Must first create '/DATA' and save a text file there
#
host = '192.168.1.10'
port = 8000
my_ssid = 'PhongLy'
my_wifi_pw = '0905653008'
#
#
uos.chdir('/DATA')  # must be pre set up on ESP8266, add a text file demo here
#
# main code loop below, afer defs...
#


def set_WIFI(cntrl):
  i = 0
  sta_if = network.WLAN(network.STA_IF)
  if cntrl == 'ON':
    if not sta_if.isconnected():
      print('conn WiFi')
      sta_if.active(True)
      sta_if.connect(my_ssid, my_wifi_pw)
      while not sta_if.isconnected():
        print(".", end="")
        time.sleep(1)
        i += 1
        if i > 9:
          return  # >>
  else:
    sta_if.active(False)
  print('NW CFG:', sta_if.ifconfig())
#
#


def upld_data():
  sd = .3  # delay between sends - experiment with this
  df = ''  # data file name
  p16.high()
  red_LED = False
  fl = uos.listdir()
  df = fl[0]
  print('fl: ', fl, '   dl:  ', dl)
  #
  set_WIFI('ON')
  s = socket.socket()
  time.sleep(sd)
  try:
    s.connect((host, port))
  except Exception as err:
    print('SockConn-ERR#: ', err)
    return('NOP')  # >>
  #
  cmd = s.recv(1024)
  if cmd.startswith('ACK'):  # I have Server send 'ACK' on connect
    print('SRV-ACK')
  else:  # catch???
    print(cmd+' SRV-NO-ACK')
    s.close()
    return('NOP')  # >>
  #
  print(df)
  s.send(df)
  time.sleep(sd)
  with open(df, 'r') as fobj:
    for line in fobj:  # will loop here until end-of-file
      print(line, end='')
      if red_LED == False:  # toggle LED during sends
        p16.low()
        red_LED = True
      else:
        p16.high()
        red_LED = False
      s.send(line)
      time.sleep(sd)
  p16.low()
  red_LED = True
  #
  # following is extra info I send after the file has been read
  s.send('\nprg_n: '+prg_n+', Free MEM:,'+str(gc.mem_free())+'\n')
  time.sleep(sd)
  s.send('fl is: '+str(fl)+'\n')
  time.sleep(sd)
  fl = uos.statvfs('/')
  fl = 'Tot/Used/Free %d blocks: %d/%d/%d\n' % (
      fl[0], fl[2], fl[2]-fl[3], fl[3])
  print(fl)
  s.send(fl)
  time.sleep(sd)
  s.send('EOF\n')  # Server will look for EOF message from ESP, finish,
  # close/open its socket, loop back, wait for next upload
  p16.high()
  return('DONE')  # >>


#
#END DEF
#
while True:  # upload every 60 seconds
  if utime.time() % 60 == 0:
    df_status = upld_data()
    print(df_status)
    time.sleep(1)
    gc.collect()
  #
#
