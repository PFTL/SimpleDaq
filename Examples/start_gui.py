import sys
from PyQt4.Qt import QApplication

from PythonForTheLab.Model import Experiment
from PythonForTheLab.View.main_window import MainWindow

e = Experiment()
e.load_config('Config/experiment.yml')
e.load_devices()
e.load_actuators()
e.load_sensors()
e.load_daq()

ap = QApplication(sys.argv)
m = MainWindow(e)
m.show()
ap.exit(ap.exec_())