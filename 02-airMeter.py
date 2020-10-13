#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# 01-airMeter.py: Da muss alles neu gemacht werden!!!
# ***************************************************
#
def get_time_string():
    import time
    time_string = time.strftime("%Y.%m.%d;%H:%M:%S;")
    return time_string

#
# main:
from time import sleep
import time
import board
import busio
import adafruit_ccs811
import adafruit_sgp30
import RPi.GPIO as GPIO
import numpy as np
import adafruit_dht
import math
#



GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)    #LedGrün
GPIO.setup(17, GPIO.OUT)   #LedRot
GPIO.setup(27, GPIO.OUT)   #LedBlau
GPIO.setup(22, GPIO.OUT)   #LedGelb

LedGruen = 400
LedGelb = 450
LedRot = 500

air_dir = '/home/pi/AirMeter/'
air_file_name = air_dir + 'airMeter.csv'
#
# 0 to 3!


for x in range(4): 
    f = open(air_file_name, "a")
    time_string = get_time_string()
    #
    # messen: Aufruf hier einbauen.
    # Messergebnis nun drucken.
    #
    i2c = busio.I2C(board.SCL, board.SDA)
    
    cssConnected = True
    try:
        ccs811 = adafruit_ccs811.CCS811(i2c)
    except:
        cssConnected = False
    
    if (cssConnected != True):
        for y in range (2):
            GPIO.output(27, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(27, GPIO.LOW)
            sleep(0.1)
    
    
    spgConnected = True
    try:
        sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
        sgp30.iaq_init()
        sgp30.set_iaq_baseline(0x8973, 0x8AAE)
    except:
        spgConnected = False
        
    if (spgConnected != True):
        for y in range (2):
            GPIO.output(27, GPIO.HIGH)
            sleep(0.1)
            GPIO.output(27, GPIO.LOW)
            sleep(0.1)
    
   
    
    
    
    f.write("{} ".format(time_string))
    # Wait for the sensor to be ready
    """
    dhtDevice = adafruit_dht.DHT22(board.D21, use_pulseio=False)
    hallo = True
    while (hallo):
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            humidityAbs = (6.112 * math.exp( ( 17.67 * temperature_c ) / ( temperature_c + 243.5 )) * humidity * 2.16774 ) / (273.15 + temperature_c)
            print(
                "Temp: {:.1f} C    Humidity: {:.1f}%  Humidity: {:.2f} g/m³".format(
                    temperature_c, humidity, humidityAbs
            )
        )
            f.write("Temp: {:.1f} C  ;  Humidity rel. : {:.1f}% ; Humidity abs. : {:.2f} g/m³".format(
                temperature_c, humidity, humidityAbs
                    ))
            hallo = False

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(3.5)
            hallo = True
            continue
        except Exception as error:
            dhtDevice.exit()
"""
    if(cssConnected):
        while(ccs811.data_ready == False):
            time.sleep(1)
        if(ccs811.data_ready):
            f.write("css811: {} ppm ;".format(ccs811.eco2))
            print(ccs811.eco2)
            
            if(ccs811.eco2 >= LedRot):
                print("rot")
                GPIO.output(22, GPIO.LOW)
                GPIO.output(17, GPIO.HIGH)
                GPIO.output(4, GPIO.LOW)
                
            elif(ccs811.eco2 >= LedGelb):
                print("gelb")
                GPIO.output(22, GPIO.HIGH)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(4, GPIO.LOW)
                
            elif(ccs811.eco2 >= LedGruen):
                print("grün")
                GPIO.output(4, GPIO.HIGH)
                GPIO.output(17, GPIO.LOW)
                GPIO.output(22, GPIO.LOW)
             
    
    if(spgConnected):
         f.write("sgp30: %d ppm ;" % (sgp30.eCO2))
    
    dhtDevice = adafruit_dht.DHT22(board.D21, use_pulseio=False)
    
    hallo = True
    while (hallo):
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            humidity = dhtDevice.humidity
            humidityAbs = (6.112 * math.exp( ( 17.67 * temperature_c ) / ( temperature_c + 243.5 )) * humidity * 2.16774 ) / (273.15 + temperature_c)
            print(
                "Temp: {:.1f} C    Humidity: {:.1f}%  Humidity: {:.2f} g/m³".format(
                    temperature_c, humidity, humidityAbs
            )
        )
            f.write("Temp: {:.1f} C  ;  Humidity rel. : {:.1f}% ; Humidity abs. : {:.2f} g/m³".format(
                temperature_c, humidity, humidityAbs
                    ))
            hallo = False

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            hallo = True
            continue
        except Exception as error:
            dhtDevice.exit()
    
    
    f.write("\n")

    f.close()
    sleep(15.0)
#
