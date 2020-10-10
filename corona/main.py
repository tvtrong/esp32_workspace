from machine import Pin,I2C
import ssd1306
import urequests
import network
import json
import math
import time

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)     
olcd=ssd1306.SSD1306_I2C(128,64,i2c)


#Add country name
CountryName = ['意大利','伊朗','韩国','法国','西班牙','德国','日本','美国','挪威','瑞士','丹麦',
'荷兰','瑞典','英国','比利时','卡塔尔','奥地利','巴林','新加坡','马来西亚','澳大利亚','加拿大','希腊',
'冰岛','以色列','芬兰','捷克','斯洛文尼亚','阿联酋','伊拉克','科威特','埃及','巴西','印度','爱尔兰',
'泰国','葡萄牙','俄罗斯']

def Display_Country():
  for i in range(38):
    get_url = 'https://lab.isaaclin.cn/nCoV/api/area?&province='+CountryName[i]
    _response = urequests.get(get_url, headers={"Content-Type":"application/json"},)
    resp_json = _response.json()
    _response.close()
    total = resp_json['results'][0] 
    date = resp_json['results'][0]['updateTime']
    time.sleep_ms(200)
    
    Time_Epoch = 946656000000
    now_timestamp = (date - Time_Epoch) // 1000
    x = time.localtime(now_timestamp)
    update_time = '{}-{:0>2d}-{:0>2d} '.format(x[0], x[1], x[2])

    olcd.fill(0) 
    #Make form
    olcd.hline(0,0,127,1)
    olcd.hline(0,10,127,1)
    olcd.hline(0,21,127,1)
    olcd.hline(0,32,127,1)
    olcd.hline(0,43,127,1)
    olcd.hline(0,53,127,1)
    olcd.hline(0,63,127,1)
    olcd.vline(0,0,63,1)
    olcd.vline(127,0,63,1)
    olcd.vline(78,22,63,1)
    #data display
    olcd.text(update_time,25,2)
    olcd.text(str(total['provinceEnglishName']),2,12) 
    olcd.text(str('confirmed %d' % (total['confirmedCount'])),2,23) 
    olcd.text(str('current   %d' % (total['currentConfirmedCount'])),2,34) 
    olcd.text(str('cured     %d' % (total['curedCount'])),2,45) 
    olcd.text(str('dead      %d' % (total['deadCount'])),2,55) 
    olcd.show() 
    
try:
  while True:
      Display_Country() 
      time.sleep_ms(2000)
except KeyboardInterrupt:
          pass

