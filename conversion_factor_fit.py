import numpy as np
import csv
import matplotlib.pyplot as plt


with open('dac_conversion.txt',mode = 'r') as dac_file:
    dac_reader = csv.reader(dac_file)
    next(dac_reader)
    next(dac_reader)
    x = []
    y = []
    for row in dac_reader:
        x.append(int(row[0]))
        y.append(float(row[1]))

m, b = np.polyfit(x, y, 1)
print(m)

plt.plot(x,y, marker = '.')
plt.show()



