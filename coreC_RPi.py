#
# coreC_RPi
#
# Rainer Brehm
# May, 23 2020
#
# Version 1.0 

import struct, array, time, io, fcntl

# I2C Address
COREC_ADDRESS =  (0x5A)

# The status (`stat` output parameter of `read`) uses the following flags0x00: OK (data valid)
IAQ_CORE_OK                =  (0x00) # Data ok
IAQ_CORE_BUSY              =  (0x01) # Data might be inconsistent; re-read()
IAQ_CORE_RUNIN             =  (0x10) # iAQcore chip in warm up phase
IAQ_CORE_ERROR             =  (0x80) # Sensor might be broken
IAQ_CORE_I2C_ERR           =  (0x10) # Software added error: I2C transaction error
IAQ_CORE_STATUS_UNDEFINED  =  (0xFF) # 
IAQ_CORE_NOT_PRESENT       =  (0xA8) # arbitrary library status code

# Chip constants
IAQCORE_I2C_ADDR           =  (0x5A)  # 7-bit I2C slave address of the iAQcore
IAQCORE_I2C_CLOCK_STRETCH  =  (3000)
IAQCORE_I2C_FREQ           =  (100000)

IAQCORE_DATA_SIZE          =  (9)  # Size (in bytes) of the measurement data block 
IAQCORE_REG                =  (0)


# Definition of error codes
IAQ_CORE_I2C_OK            =  (0)
IAQ_CORE_I2C_NOK           =  (-1)

# Error codes for the I2C interface
IAQ_CORE_I2C_READ_FAILED   =  (1)
IAQ_CORE_SENSOR_ERROR      =  (2)
IAQ_CORE_I2C_BUSY          =  (3)
IAQ_CORE_HEATING_UP        =  (4)

IAQ_CORE_CO2_MSB_OFFSET           =  (0)
IAQ_CORE_CO2_LSB_OFFSET           =  (1)
IAQ_CORE_STATUS_OFFSET            =  (2)
IAQ_CORE_RESISTANCE_MSB_OFFSET    =  (4)
IAQ_CORE_RESISTANCE_MID_OFFSET    =  (5)
IAQ_CORE_RESISTANCE_LSB_OFFSET    =  (6)
IAQ_CORE_TVOC_MSB_OFFSET          =  (7)
IAQ_CORE_TVOC_LSB_OFFSET          =  (8)

I2C_SLAVE=0x0703

COREC_fw= 0
COREC_fr= 0

class coreC_RPi:
        def __init__(self, twi=1, addr=COREC_ADDRESS ):
                global CCOREC_fr, CCOREC_fw
                
                CCOREC_fr= io.open("/dev/i2c-"+str(twi), "rb", buffering=0)
                CCOREC_fw= io.open("/dev/i2c-"+str(twi), "wb", buffering=0)

                # set device address
                fcntl.ioctl(CCOREC_fr, I2C_SLAVE, COREC_ADDRESS)
                fcntl.ioctl(CCOREC_fw, I2C_SLAVE, COREC_ADDRESS)
                time.sleep(0.015)


        # public functions
        def getResults(self):
                data = CCOREC_fr.read(10)
                
                buf = array.array('B', data)
                result = {}
                if (buf[2] == IAQ_CORE_I2C_ERR):
                        return False; # dev->error_code = IAQ_CORE_I2C_READ_FAILED

                if (buf[2] == IAQ_CORE_ERROR):
                        return False; # dev->error_code = IAQ_CORE_SENSOR_ERROR

                result = {}
                # Read eCO2 value and check if it is valid
                result['etvoc'] = buf[IAQ_CORE_TVOC_MSB_OFFSET]*256 + buf[IAQ_CORE_TVOC_LSB_OFFSET]
                result['eco2'] = buf[IAQ_CORE_CO2_MSB_OFFSET]*256  + buf[IAQ_CORE_CO2_LSB_OFFSET]

                result['stat'] = buf[IAQ_CORE_STATUS_OFFSET]
                return result
        def isMeasuring(self):
                data = CCOREC_fr.read(10)
                
                buf = array.array('B', data)
                result = {}
                if (buf[2] == IAQ_CORE_BUSY):
                        return True; # dev->error_code = IAQ_CORE_I2C_BUSY;
                return False;

        def isHeating(self):
                data = CCOREC_fr.read(10)
                
                buf = array.array('B', data)
                result = {}
                if (buf[2] == IAQ_CORE_RUNIN):
                        return True; # dev->error_code = IAQ_CORE_HEATING_UP
                return False;
