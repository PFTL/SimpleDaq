"""
    start_gui

"""

import sys
from PyQt4.Qt import QApplication

from PythonForTheLab.Model import Experiment
from PythonForTheLab.View.scan_window import ScanWindow

e = Experiment()
e.load_config('Config/experiment.yml')
e.load_devices()
e.load_daq()

ap = QApplication(sys.argv)
m = ScanWindow(e)
m.show()
ap.exit(ap.exec_())