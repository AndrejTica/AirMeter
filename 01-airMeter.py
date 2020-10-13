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
# only2see!
#
#
def capture_black_image(brightness, iso, file_name):
    # https://picamera.readthedocs.io/en/release-1.13/recipes1.html
    # 3.7. Capturing in low light
    # The V1 camera module can manage 6 second maximum exposure time.
    # The V2 camera module can manage 10 second maximum exposure time.
    #
    from picamera import PiCamera
    from time import sleep
    from fractions import Fraction
    #
    # Force sensor mode 3 (the long exposure mode), set
    # the framerate to 1/10fps, the shutter speed to 6s,
    # and ISO to 800 (for maximum gain)
    #sleep(3)
    camera = PiCamera()
    camera.sensor_mode=3
    camera.resolution = (3280, 2464)
    # camera.resolution = camera.MAX_RESOLUTION
    #
    # shutter speed =  6s => frame rate = 1/6 s
    # shutter speed = 10s => frame rate = 1/10 s
    camera.framerate = Fraction(1, 10)
    camera.shutter_speed = 10000000 
    camera.iso = iso # Set ISO to force unity gains, then lock...
    sleep(30) # long time to set gains
    camera.exposure_mode = 'off' # ... locks gains
    #camera.brightness = brightness
    camera.capture(file_name, format='bmp')
    camera.close()	
    #
    return 'OK'
#
def analyse_black_image(temp_file_name, file_name, \
    log_date_time, log_brightness, log_iso, log_analyse):
    # vollständig schwarz => return none
    # wenige pixel nicht schwarz => anzahl x,y,wert x,y,wert
    # viele (ab 5) pixel nicht schwarz => anzahl
    import os
    import math
    from PIL import Image
    img = Image.open(temp_file_name)
    #
    analyse_str = ""
    anzahl_nicht_0 = 0
    summe_nicht_0 = 0
    max = 0.0 # direkt
    min = 1000 # direkt
    durchschnitt_nicht_0 = 0.0
    myon_faktor = 0.0
    myon_faktor_u = 0.0
    myon_faktor_o = 0.0
    #
    brightness_list = []
    for i in range(800):
        brightness_list.append(0)
    #
    hoehe_max = 2464
    breite_max = 3280
    #
    for y in range(0,hoehe_max): #2464
        for x in range(0,breite_max): #3280
            #
            imgload = img.load() #lädt bildparameter
            farbe = imgload[x,y] #holt die Farbwerte des aktuellen Pixel
            r,g,b = farbe #spaltet den rgbwert in einzelne werte
            brightness = r+g+b #berechnet die helligkeit des Pixels
            #
            if(brightness>0):
                anzahl_nicht_0 = anzahl_nicht_0+1
                summe_nicht_0 = summe_nicht_0+brightness
                brightness_list[brightness] = brightness_list[brightness] + 1
            if(brightness>max):
                max = brightness
            if(brightness<min):
                min = brightness
    #
    anteil_nicht_0 = 100 * anzahl_nicht_0 / (hoehe_max*breite_max) # in %
    if(anzahl_nicht_0>0):
        durchschnitt_nicht_0 = summe_nicht_0/anzahl_nicht_0
    #
    if((max-durchschnitt_nicht_0)!=0.0 and (durchschnitt_nicht_0-min)!=0.0):
        myon_faktor_o = (max-durchschnitt_nicht_0)/(durchschnitt_nicht_0-min)
        myon_faktor_u = (min-durchschnitt_nicht_0)/(max-durchschnitt_nicht_0)
        myon_faktor = myon_faktor_o
        if(abs(myon_faktor_u)>myon_faktor):
            myon_faktor=myon_faktor_u
    #
    brightness_str = ""
    length = len(brightness_list)
    brightness_print_count = 0
    for i in range(length):
        if(brightness_list[i]>0):
            brightness_print_count = brightness_print_count+1
            #if(brightness_print_count<6):
            brightness_str = brightness_str+str(i)+":"+str(brightness_list[i])+"/"
    #
    f = open(log_analyse, "a")
    f.write(log_date_time+";"+log_brightness+";"+log_iso+";"+ \
        "Tonpapier;"+ \
        str(anteil_nicht_0)+";"+ \
        str(min)+";"+ \
        str(durchschnitt_nicht_0)+";"+ \
        str(max)+";"+ \
        str(max-min+1)+";"+ \
        str(myon_faktor_u)+";"+ \
        str(myon_faktor_o)+";"+ \
        brightness_str + "\n")
    f.close()
    #
    if((myon_faktor>2.0)or((max-min)>5)):
        full_file_name = file_name+"-"+log_brightness+"-"+log_iso+ \
            "-"+str(myon_faktor)+".bmp"
        os.rename(temp_file_name, full_file_name)
    return 'OK'
#
# main:
from time import sleep
import time
import board
import busio
import adafruit_ccs811
#
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
    ccs811 = adafruit_ccs811.CCS811(i2c)
 
    # Wait for the sensor to be ready
    while not ccs811.data_ready:
        pass
    f.write("{}{}\n".format(time_string, ccs811.eco2))
    f.close()
    sleep(15)
#
