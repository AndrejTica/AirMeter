def Measure(Pressure):
    import pigpio
    import time
    
    pi = pigpio.pi()
    deviceAddress = 0x28
    handlePasCO2 = pi.i2c_open(1, deviceAddress, 0)
    
    def readByte(regAddress):
        read = pi.i2c_read_byte_data(handlePasCO2, regAddress)
        if(read > 0):
            return read
        else:
            return 0x0

    def writeByte(regAddress, data):
        pi.i2c_write_byte_data(handlePasCO2, regAddress, data)

    
    status = pi.i2c_read_byte_data(handlePasCO2, 0x01)
    #status = 0x80: Sensor is initialised correctly
    #status = 0x90: Check 5V power supply
    
    PressureUnten = Pressure >>8
    PressureOben = Pressure&0xFF
    #set presure
    writeByte(0x0B, PressureUnten)
    writeByte(0x0C, PressureOben)
        
    #trigger measurement
    writeByte(0x04, 0x01)
    time.sleep(1)
        
    #measurement sequence complete if meas_status = 10hex
    meas_status = readByte(0x07)
    time.sleep(0.05)
        
    #Get PPM value
    value_MSB = readByte(0x05)
    time.sleep(0.05)
    value_LSB = readByte(0x06)
    time.sleep(0.05)
        
    #Calculate PPM value
    result = value_MSB << 8 | value_LSB
    
    
    time.sleep(2)
        
    pi.i2c_close(handlePasCO2)
    
    return (hex(PressureUnten), hex(PressureOben), hex(status), hex(meas_status), result)

