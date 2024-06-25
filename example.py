from DT2100.DT2100 import DT2100
import matplotlib.pyplot as plt
import time
import csv


def current_milli_time():
    return round(time.time() * 1000)

# Setting Parameters
port = "COM4"
baud = 38400

tach = DT2100(port, baud)
datax = []
datay = []
try:
    print("Starting Capture...")
    now = current_milli_time()
    while True:
        t = current_milli_time()
        speed = tach.getSpeed()
        datax.append(t-now)
        datay.append(int(speed))
        
except KeyboardInterrupt as e:
    pass

print("Dumping to CSV...")
with open('testdata.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(datax, datay))

print("Plotting Capture...")
plt.plot(datax, datay)
plt.show()