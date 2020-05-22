#
# coreC_RPi class usage example
#
# Rainer Brehm
# May, 23 2020
#
# Version 1.0

import time

from coreC_RPi import coreC_RPi

coreC = coreC_RPi() # Hier wird die Klasse coreC_RPi initialisiert!

# Set read interval for retriveving last measurement data from the sensor
pause = 60

# check heating - loop
statusbyte = coreC.isHeating()
print 'Heating STATUS: ', statusbyte
while statusbyte:
        time.sleep(10)
        statusbyte = coreC.isHeating()
        print 'STATUS: ', statusbyte

while(1):

        statusbyte = coreC.isMeasuring()
        print 'Measuring STATUS: ', statusbyte
        while statusbyte:
                time.sleep(10)
                statusbyte = coreC.isMeasuring()
                print 'STATUS: ', statusbyte

        result = coreC.getResults();
        if(not result):
                print 'Invalid result received'
                time.sleep(10)
                #continue;
        print 'eco2: ',result['eco2'],' ppm'
        print 'etvoc: ',result['etvoc'], 'ppb'
        print 'Status register: ',bin(result['stat'])
        print '---------------------------------';
        time.sleep(pause)
