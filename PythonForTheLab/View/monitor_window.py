"""
Monitor Window
==============
Window to display a plot that updates over time at a given rate. The only parameter that can be changed
within the window is the delay between two consecutive reads. To change other parameters the user needs to
open the configuration window. It may not be the most intuitive behavior, but helps teaching how to open a
dialog and connect custom signals.
"""

import os
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, uic, QtWidgets

from PythonForTheLab import Q_

from .config_window import ConfigWindow
from .general_worker import WorkThread
from .scan_window import ScanWindow




class MonitorWindow(QtWidgets.QMainWindow):
    def __init__(self, experiment, parent=None):
        super().__init__(parent)

        self.experiment = experiment

        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'GUI/main_window.ui'), self)

        self.main_plot = pg.PlotWidget()
        self.main_plot.setLabel('bottom', 'Time', units='s')

        layout = QVBoxLayout()

        self.verticalLayout.addWidget(self.main_plot)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_monitor)
        self.running_monitor = False

        self.startButton.clicked.connect(self.start_monitor)
        self.stopButton.clicked.connect(self.stop_monitor)
        self.ydata = np.zeros((0))
        self.xdata = np.zeros((0))
        self.p = self.main_plot.plot(self.xdata, self.ydata)

        self.config_window = ConfigWindow(experiment, parent=self)
        self.config_window.propertiesChanged.connect(self.update_properties)
        self.actionConfig.triggered.connect(self.config_window.show)

        self.scan_window = ScanWindow(experiment)
        self.actionScan.triggered.connect(self.scan_window.show)

    def update_properties(self, props):
        """Method triggered when the signal for updating parameters is triggered.
        """
        self.experiment.properties['Monitor'] = props
        self.delayLine.setText(self.experiment.properties['Monitor']['time_resolution'])

    def start_monitor(self):
        """Starts a  monitor in a separated Worker Thread. There will be a delay for the update of the plot.
        """

        if self.running_monitor:
            print('Monitor already running')
            return
        self.running_monitor = True
        delay = Q_(self.delayLine.text())
        self.experiment.properties['time_resolution'] = delay
        self.worker_thread = WorkThread(self.experiment.monitor_signal)
        self.worker_thread.start()
        refresh_time = Q_(self.experiment.properties['Monitor']['refresh_time'])
        self.update_timer.start(refresh_time.m_as('ms'))

    def stop_monitor(self):
        """Stops the monitor and terminates the working thread.
        """
        if not self.running_monitor:
            print('Monitor not running')
            return

        self.update_timer.stop()
        self.worker_thread.terminate()
        self.running_monitor = False

    def update_monitor(self):
        """This method is called through a timer. It updates the data displayed in the main plot.
        """
        self.xdata = self.experiment.xdata
        self.ydata = self.experiment.ydata

        self.p.setData(self.xdata, self.ydata)

    def update_value(self):
        pass

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                           quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        event.accept()

