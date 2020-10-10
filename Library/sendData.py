import machine

try:
    import usocket as socket
except:
    import socket
import ussl as ssl

# a template of HTTP request to Server to post temperature and humidity
SERVER_POST_TEMPLATE = """
POST /update HTTP/1.1
Host: http://127.0.0.1:8000/api/
Connection: close
X-THINGSPEAKAPIKEY: %s
Content-Type: application/x-www-form-urlencoded
Content-Length: %d
%s
"""

DHT22_PIN = 14
API_THINGSPEAK_HOST = 'http://127.0.0.1:8000/api/'
API_THINGSPEAK_PORT = 8000
THINGSPEAK_WRITE_KEY = '...'  # put your key here

# timings in seconds
MESUREMENT_INTERVAL = 300  # TODO: read this from a config file

# mesures temperature and humidity with DHT22 sensor, and sends the data to ThingSpeak


def mesure_temperature_and_humidity():
    d = dht.DHT22(machine.Pin(DHT22_PIN))
    d.measure()
    t = d.temperature()
    h = d.humidity()
    print('temperature = %.2f' % t)
    print('humidity    = %.2f' % h)

    global THINGSPEAK_WRITE_KEY
    if not THINGSPEAK_WRITE_KEY:
        print('not ThingSpeak key specified, skip sending data')
        return

    print('send data to ThingSpeak')
    s = socket.socket()
    ai = socket.getaddrinfo(API_THINGSPEAK_HOST, API_THINGSPEAK_PORT)
    addr = ai[0][-1]
    s.connect(addr)
    s = ssl.wrap_socket(s)
    data = 'field1=%.2f&field2=%.2f' % (t, h)
    http_data = THINGSPEAK_POST_TEMPLATE % (
        THINGSPEAK_WRITE_KEY, len(data), data)
    s.write(http_data.encode())
    s.close()


while True:
    current_time = time.time()
    if current_time - last_mesurement_time > MESUREMENT_INTERVAL:
        mesure_temperature_and_humidity()
        last_mesurement_time = current_time
    time.sleep(DELAY)
