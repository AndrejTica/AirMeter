from time import sleep
import time
import board
import busio
import adafruit_ccs811
import adafruit_sgp30
import RPi.GPIO as GPIO
import math
import pigpio
from DHT22 import *

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)
dht22 = sensor(pi, 10)

def readDHT22():
    
    _,_,status,temperature,humidity = dht22.read()
    return (humidity, temperature, status)


dhtConnected = True
_,_,status = readDHT22()
print(status)
if(status == 3):
    dhtConnected = False
    
time.sleep(5)

for y in range(0, 4):
    if(dhtConnected):
        humidity, temperature, status = readDHT22()
        print("status is: {}".format(status))
        print("Humidity rel. is: {} %".format(humidity))
        print("Temperature is: {} °C".format(temperature))
        humidityAbs = (6.112 * math.exp( ( 17.67 * temperature ) / ( temperature + 243.5 )) * humidity * 2.16774 ) / (273.15 + temperature)
        print("Humidity abs. is: {:.2f} g/m³\n".format(humidityAbs))
        #f.write("Temp: {} °C; Humidity rel.: {} %; Humidity abs.: {:.2f} g/m³; ".format(
                #temperature, humidity, humidityAbs
        #))
    else:
        print("geht nicht amk")
    
    time.sleep(5.0)