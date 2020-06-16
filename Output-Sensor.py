import time
import smbus
import mcp3428
import csv                         
import Adafruit_MCP4725
import matplotlib.pyplot as plt
import numpy as np

bus = smbus.SMBus(1)
kwargs = {'address': 0x68, 'mode': 0x10, 'sample_rate': 0x08, 'gain': 0x00}     
mcp3428 = mcp3428.MCP3428(bus, kwargs)

# Create a DAC instance...whatever that means                                                                                
dac = Adafruit_MCP4725.MCP4725(address=0x60, busnum=1)

print('Press Ctrl-C to quit...')
x = np.array([])
y = np.array([])
for i in range(0,4095):
    dac.set_voltage(i)
    time.sleep(.01)
    reading = mcp3428.take_single_reading(0)
    np.append(x, i)
    np.append(y, reading)
    
m, b = np.polyfit(x, y, 1)
plt.plot(x, y, '.b')
plt.title('Conversion Factor')
plt.show()


