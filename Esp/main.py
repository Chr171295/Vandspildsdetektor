import machine
import ds18x20
import time
import onewire
import network
import urequests
import json
import network


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
 
    if not sta_if.isconnected():
        sta_if.active(True)
        try:
            sta_if.config(dhcp_hostname="My ProS3")
            sta_if.connect("Fat Cat Cave", "Jofyeetpoum9")
        except Exception as err:
            sta_if.active(False)
            print("Error:", err)
            do_connect()
        print("Connecting", end="")
        n = 0
        while not sta_if.isconnected():
            print(".", end="")
            time.sleep(1)
            n += 1
            if n == 60:
                break
        if n == 60:
            sta_if.active(False)
            print("\nGiving up! Not connected!")
        else:
            print("\nNow connected with IP: ", sta_if.ifconfig()[0])
    print((sta_if.ifconfig()[0]))
    
    
def sendData(sensor1, sensor2):
    try:
        data_to_send = {"templuft": sensor1,
                        "temproer": sensor2
                        }
        jsonp=json.dumps(data_to_send)
        print(jsonp)
        response = urequests.post("http://79.171.148.158:5000/postdata", json=jsonp)
        print(response.text)
    finally:
        pass
do_connect()

ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()

print('Found DS devices: ', roms)
  #sensor1 = bytearray(b'(\x92\xd0\xd7u"\x01\xcc') (Dallas)
  #sensor2 = bytearray(b'(\xf4k\x9c\x0b\x00\x00\xe3')


while True:
   ds_sensor.convert_temp()
   time.sleep_ms(750)
   for rom in roms:
    time.sleep(5)
    sendData(ds_sensor.read_temp(roms[1]),ds_sensor.read_temp(roms[0]))