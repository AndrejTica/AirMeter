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
import os
import time
from PAS_CO2_LIB import *


#TODO Kommentare


"""
function: Komma(VarFloat)
parameter: VarFloat
"""
def Komma(VarFloat):
    strVarFloat = str(VarFloat)
    KommaVarFloat = strVarFloat.replace(".", ",")
    return KommaVarFloat


def main():
    # Kommentar...
    LedPinGruen = 15
    LedPinRot = 8
    LedPinBlau = 7
    LedPinGelb = 24
    
    Luftdruck = 997

    CO2isZero = False
    
    GPIO.setup(LedPinGruen, GPIO.OUT)  # LedGrün !!Variablen!!!
    GPIO.setup(LedPinRot, GPIO.OUT)  # LedRot
    GPIO.setup(LedPinBlau, GPIO.OUT)  # LedBlau
    GPIO.setup(LedPinGelb, GPIO.OUT)  # LedGelb

    LedGruen = 200  # variable green
    LedGelb = 600  # variable yellow
    LedRot = 1500  # variable red


    # TODO ohne split programmieren
    time_string = time.strftime("%Y.%m.%d;%H:%M:%S")

    Date = time_string.split(".")
    Day = Date[2].split(";")

    # Leaf directory
    directory = Date[1]
    air_dir = '/home/pi/AirMeter/'

    with open(air_dir + "airMeter.ini", 'r') as u:
        Ini = u.read()
        Ini_split = Ini.split()

    # Parent Directories
    parent_dir = air_dir + "/Daten/" + Ini_split[17] + "/" + Date[0] + "/"

    # Path
    path = os.path.join(parent_dir, directory)

    # Create the directory
    # 'ihritik'
    try:
        os.makedirs(path, exist_ok=True)
        # print("Directory '%s' created successfully" %directory)
    except OSError as error:
        print("Directory '%s' can not be created")

    CSV = "airMeter_" + Date[0] + Date[1] + Day[0] + ".csv"
    air_file_name = air_dir + "Daten/" + Ini_split[17] + "/" + Date[0] + "/" + Date[1] + "/" + CSV

    pi = pigpio.pi()

    def readDHT22():

        _,_,status,temperature,humidity = dht22.read()
        return (humidity, temperature, status)
    
    def readPAS():
        _,_,status,meas_status, result = Measure(Luftdruck)
        return(status,meas_status, result)

    PasConnected = True
    status,meas_status,_ = readPAS()
    if(status != "0x80" or meas_status != "0x10"):
        PasConnected = False
        
    GPIO.setmode(GPIO.BCM)

   
   

    GPIODHT = int(Ini_split[3])
    dht22 = sensor(pi, GPIODHT)

    dhtConnected = True
    _,_,status = readDHT22()
    if(status == 3):
        dhtConnected = False

    # sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
    testDummy = open(air_file_name, "a")
    testDummy.close()

    with open(air_file_name, "r") as Header:
        Head = Header.read()
    Header.close()

    if Head == "":
        with open(air_file_name, "w") as Header:
            Header.write("Datum;Uhrzeit")
            if Ini_split[0] == "J":
                if Ini_split[1] == "DHT22":
                    Header.write(";T-DHT22;FR-DHT22;FA-DHT22")
            if Ini_split[4] == "J":
                if Ini_split[5] == "CCS811":
                    Header.write(";CO2-CCS811")
            if Ini_split[8] == "J":
                if Ini_split[9] == "SGP30":
                    Header.write(";CO2-SGP30")
            if Ini_split[12] == "J":
                if Ini_split[13] == "PASCO2":
                    Header.write(";CO2-PASCO2")
            Header.write("\n")
        Header.close()

    i2c = busio.I2C(3, 2, frequency=100000)
    time.sleep(5)
    for y in range(0, 4):
        f = open(air_file_name, "a")
        time_string = time.strftime("%Y.%m.%d;%H:%M:%S")
        f.write("{}".format(time_string))
        print(time_string)
        for x in range(0, 4):
        
            if Ini_split[0+4*x] == "J":
                        
                if Ini_split[1+4*x] == "DHT22":
                    if(dhtConnected):
                        humidity, temperature, status = readDHT22()
                        print("status is: {}".format(status))
                        temperatureKomm = Komma(temperature)
                        humidityRelKomm = Komma(humidity)
                        print("Humidity rel. is: {} %".format(humidityRelKomm))
                        print("Temperature is: {} C".format(temperatureKomm))
                        humidityAbs = (6.112 * math.exp( ( 17.67 * temperature ) / ( temperature + 243.5 )) * humidity * 2.16774 ) / (273.15 + temperature)
                        humidityAbsKomm = Komma("{:.1f}".format(humidityAbs))
                        print("Humidity abs. is: {} g/m3\n".format(humidityAbsKomm))
                        print(humidityAbs)
                        f.write(";{};{};{}".format(
                                temperatureKomm, humidityRelKomm, humidityAbsKomm
                        ))
                        
                    else:
                        print(";err;err;err")
                        f.write(";err;err;err")
                        for y in range (2):
                            GPIO.output(LedPinBlau, GPIO.HIGH)
                            sleep(0.1)
                            GPIO.output(LedPinBlau, GPIO.LOW)
                            sleep(0.1)
                            

                if Ini_split[1+4*x] == "CCS811":
                    cssConnected = True                            
                    try:
                        ccs811 = adafruit_ccs811.CCS811(i2c)     #try to reach ccs811 Sensor
                    except:
                        cssConnected = False
                                       
                    if(cssConnected != True):
                        f.write(";err")
                        for y in range (2):
                            GPIO.output(LedPinBlau, GPIO.HIGH)
                            sleep(0.1)
                            GPIO.output(LedPinBlau, GPIO.LOW)
                            sleep(0.1)
                                            
                    if(cssConnected):                                 #if CCS811 & Data ready -> write to CSV File           
                        while(ccs811.data_ready == False):
                            time.sleep(1)
                        if(ccs811.data_ready == True):
                            f.write(";{}".format(ccs811.eco2))
                            print(ccs811.eco2)
                            
                    
                if Ini_split[1+4*x] == "SGP30":
                    spgConnected = True
                    try:   
                        sgp30.iaq_init()               #try to reach spg30 Sensor
                        sgp30.set_iaq_baseline(0x8973, 0x8AAE)
                    except:
                        spgConnected = False
                        
                    if (spgConnected != True): #if SPG30 not found -> Signals to blue Led
                        f.write(";err")
                        for y in range (2):
                            GPIO.output(LedPinBlau, GPIO.HIGH)
                            sleep(0.1)
                            GPIO.output(LedPinBlau, GPIO.LOW)
                            sleep(0.1)        
                        
                    if(spgConnected):                                 #write to CSV File if SPG is Connected
                        f.write(";%d" % (sgp30.eCO2))
                        print(sgp30.eCO2)
                
                if Ini_split[1+4*x] == "PASCO2":
                    if (PasConnected):
                        _,_,result = readPAS()
                        print(result)
                        f.write(";{}".format(result))
                        if(result >= LedRot):                #output the value to LEDs
                            print("rot")
                            GPIO.output(LedPinGelb, GPIO.LOW)
                            GPIO.output(LedPinRot, GPIO.HIGH)
                            GPIO.output(LedPinGruen, GPIO.LOW)
                                
                        elif(result >= LedGelb):
                            print("gelb")
                            GPIO.output(LedPinGelb, GPIO.HIGH)
                            GPIO.output(LedPinRot, GPIO.LOW)
                            GPIO.output(LedPinGruen, GPIO.LOW)
                                
                        elif(result >= LedGruen):
                            print("grün")
                            GPIO.output(LedPinGruen, GPIO.HIGH)
                            GPIO.output(LedPinRot, GPIO.LOW)
                            GPIO.output(LedPinGelb, GPIO.LOW)
                    else:
                        f.write(";err")
                        for y in range (2):
                            GPIO.output(LedPinBlau, GPIO.HIGH)
                            sleep(0.1)
                            GPIO.output(LedPinBlau, GPIO.LOW)
                            sleep(0.1)       
                
                    
            sleep(3.75)
        f.write("\n")
        f.close()

if __name__=="__main__":
    main()



