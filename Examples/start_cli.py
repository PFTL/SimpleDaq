import os
import pyqtgraph as pg
from datetime import datetime

from PythonForTheLab.Model import Experiment

e = Experiment()
e.load_config('Config/experiment.yml')
e.load_devices()
e.load_actuators()
e.load_sensors()
e.load_daq()


print("Starting new Experiment with device: \n {}".format(e.daq.idn()))

# Do a scan

print("Doing a scan...")
e.do_scan()
print("Scan finished!")
print("Data: ")
print(e.ydata_scan)

# PlotWidget = pg.plot(title="Plotting I vs V")
# PlotWidget.setLabel('bottom', 'Port: {}'.format(e.properties['Scan']['port_out']), units="V")
# PlotWidget.setLabel('left', 'Port: {}'.format(e.properties['Scan']['port_in']), units="V")
# PlotWidget.plot(e.xdata_scan, e.ydata_scan)

filename = "Data_scan_{:03}.dat"

header = "# Data saved by Python For The Lab\n"
header += "# Creation date: {:%Y-%m-%d %H:%M:%S}\n".format(datetime.now())
header += "# Number of lines: {}\n".format(len(e.xdata_scan))
header += "##################################\n"
i = 0
while os.path.exists(filename.format(i)):
    i += 1

with open(filename.format(i), 'w') as f:
    f.write(header)
    for i in range(len(e.xdata_scan)):
        line = "{:4.4f}, {:4.4f}\n".format(e.xdata_scan[i], e.ydata_scan[i])
        f.write(line)