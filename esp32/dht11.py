import dht
import machine
d = dht.DHT11(machine.Pin(27))


def get():
    d.measure()
    t = float(d.temperature())
    h = float(d.humidity())
    data = {
        "temperature": t,
        "humidity": h
    }
    return data
