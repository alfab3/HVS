# Python script for user to set voltage.
# Author: Andrew Schick and Daniel Lis
# License: MIT License

import time

#Import the module
import Adafruit_MCP4725

#import the ADC module class
import mcp3428
import smbus

#create bus object 
bus = smbus.SMBus(1)
#create a dictionary of addresses and information needed for the ADC instance
kwargs = {'address': 0x68, 'mode': 0x10, 'sample_rate': 0x08, 'gain':0x00}

#crate a ADC instance directing towards the bus with the addresses located in kwargs
mcp3428 = mcp3428.MCP3428(bus, kwargs)

# Create a DAC instance...whatever that means
dac = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)

#Initialization of variables

conversion_factor = .002 #How the readings change when they get read into and out of the ADC
voltage = 0
dac.set_voltage(0) #set the voltage to zero through the dac instance
set_voltage = True


#steps to follow
#1. While loop that keeps on going through
print ('Press ctrl-C to exit...')

while True:
    voltage += 1
    bit = voltage / conversion_factor
    time.sleep(0.01)
    dac.set_voltage(bit)
    print ('increasing voltage to' + voltage)
    print ('\r\n')
    print ('------------')
    print('\r\n')
    print ('Voltage: ' + mcp3428.take_single_recording(0))
    print('\r\n')
    print('------------')
    print('\r\n')
    previous_reading = mcp3428.take_single_recording(0)
    start = time.time() #start time of loop
    time.sleep(0.1)
    current_reading = mcp3428.take_single_reading(0)
    end = time.time() #end time
    rate = (current_reading - previous_reading)/(end - start)

    if rate > 1: #if the rate exceeds 1 volt per second, as in it jumps past the increase in voltage, it will be done.
        voltage -= 1
        bit = voltage / conversion_factor
        dac.set_voltage(bit)
        print('Decreasing Voltage by 1')
        print('\r\n')
        print('------------')
        print('\r\n')
        print('Voltage: ' + mcp3428.take_single_reading(0))
        print('\r\n')
        print('------------')
        print('\r\n')
        time.sleep(60)
    else:
        time.sleep(.9)

    while current_reading > 1799:
        while True:
            current_reading = mcp3428.take_single_reading(0)
            if current_reading < 1800:
                breakDirection = False
                break
            elif current_reading > 1800:
                breakDirection = True
                break
        if ~breakDirection:
            break
        elif breakDirection:
            the_read = current_reading
            while the_read > 1801:
                voltage -= 1
                bit = voltage / conversion_factor
                time.sleep(0.01)
                dac.set_voltage(bit)
                time.sleep(1)
                the_read = mcp3428.take_single_reading(0)
                print('Decreasing Voltage by 1:')
                print('\r\n')
                print('------------')
                print('\r\n')
                print('Voltage: ' + the_read)



                                
                 # now if the voltage is at about 1800, we need to keep it constant
                # the purpose of this look is to stop the loop from going on forever and for it to stop in the voltage range we need it to
                #so that's why I'm having it print the voltage it has so we know to make adjustments or no
        





