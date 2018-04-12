"""
Configuration Window
====================
Simple QDialog that provides a form to update some values for the monitor.

"""
import os
from PyQt5 import QtCore, QtWidgets, QtGui, uic

from PythonForTheLab import Q_


class ConfigWindow(QtWidgets.QDialog):
    propertiesChanged = QtCore.pyqtSignal([dict])
    """Custom signal for informing the main window that there are new parameters available.
    """
    def __init__(self, experiment, parent=None):
        super().__init__(parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/config_window.ui'), self)
        self.buttonBox.accepted.connect(self.apply_new_values)

        self.portLine.setText('{}'.format(experiment.properties['Monitor']['channel']))
        self.timeResolutionLine.setText(experiment.properties['Monitor']['time_resolution'])
        self.refreshTimeLine.setText(experiment.properties['Monitor']['refresh_time'])
        self.totalTimeLine.setText(experiment.properties['Monitor']['total_time'])

    def apply_new_values(self):
        """Formats the values in the form and emits a custom signal *propertiesChanged* including a
        dictionary of the values that are provided (changed or not).
        """
        new_values = {'port_monitor': int(self.portLine.text()),
                      'time_resolution': Q_(self.timeResolutionLine.text()),
                      'refresh_time': Q_(self.refreshTimeLine.text()),
                      'total_time': Q_(self.totalTimeLine.text()),}
        self.propertiesChanged.emit(new_values)

if __name__ == "__main__":
    import sys
    from PyQt5.Qt import QApplication
    ap = QApplication(sys.argv)
    from PythonForTheLab.Model.experiment.IV_measurement import Experiment
    e = Experiment()
    session = {'port_monitor': 1,
               'time_resolution': Q_('1ms'),
               'refresh_time': Q_('20ms'),
               'total_time': Q_('15s')}
    e.properties = session

    m = ConfigWindow(e)
    m.show()
    ap.exit(ap.exec_())