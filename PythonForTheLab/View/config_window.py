import os
import numpy as np
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui, uic

from PythonForTheLab import Q_


class ConfigWindow(QtGui.QDialog):
    propertiesChanged = QtCore.pyqtSignal([dict])

    def __init__(self, experiment, parent=None):
        super().__init__(parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/config_window.ui'), self)
        self.buttonBox.accepted.connect(self.apply_new_values)

        self.portLine.setText('{}'.format(experiment.properties['Monitor']['port']))
        self.timeResolutionLine.setText('{:~}'.format(experiment.properties['Monitor']['time_resolution']))
        self.refreshTimeLine.setText('{:~}'.format(experiment.properties['Monitor']['refresh_time']))
        self.totalTimeLine.setText('{:~}'.format(experiment.properties['Monitor']['total_time']))

    def apply_new_values(self):
        new_values = {'port_monitor': int(self.portLine.text()),
                      'time_resolution': Q_(self.timeResolutionLine.text()),
                      'refresh_time': Q_(self.refreshTimeLine.text()),
                      'total_time': Q_(self.totalTimeLine.text()),}
        self.propertiesChanged.emit(new_values)

if __name__ == "__main__":
    import sys
    from PyQt4.Qt import QApplication
    ap = QApplication(sys.argv)
    from Model.experiment.daq_control import Experiment
    e = Experiment()
    session = {'port_monitor': 1,
               'time_resolution': Q_('1ms'),
               'refresh_time': Q_('20ms'),
               'total_time': Q_('15s')}
    e.properties = session

    m = ConfigWindow(e)
    m.show()
    ap.exit(ap.exec_())