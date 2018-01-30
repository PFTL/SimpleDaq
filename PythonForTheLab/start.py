import sys
from PyQt4.Qt import QApplication
from View.main_window import MainWindow
from Model.daq.analog_daq import AnalogDaq
from Model.experiment.daq_control import Experiment

a = AnalogDaq('/dev/ttyACM1')

from pint import UnitRegistry
ureg = UnitRegistry()
Q_ = ureg.Quantity

print(a.idn())
print(a.get_analog_value(0))


e = Experiment()
session = {'port_monitor': 1,
           'time_resolution': Q_('1ms'),
           'refresh_time': Q_('100ms'),
           'total_time': Q_('15s'),
           'scan_port_out': 1,
           'scan_start': Q_('0.1V'),
           'scan_stop': Q_('0.7V'),
           'scan_step': Q_('0.1V'),
           'scan_port_in': 2,
           'scan_delay': Q_('10ms'),
           }

e.properties = session
e.load_daq(a)
ap = QApplication(sys.argv)
m = MainWindow(e)
m.show()
ap.exit(ap.exec_())