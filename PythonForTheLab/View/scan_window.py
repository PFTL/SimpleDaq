"""
Scan Window
===========
This is the core window for the Experiment. It implements a form where the user can change the input port,
and delay between measurements. It has control also over the output port and range.

.. todo:: Add a menu for opening the monitor.

"""
import os
import numpy as np
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, uic, QtWidgets

from PythonForTheLab import Q_
from .general_worker import WorkThread


class ScanWindow(QtWidgets.QMainWindow):
    def __init__(self, experiment, parent=None):
        super().__init__(parent)


        self.experiment = experiment

        p = os.path.dirname(__file__)
        self.directory = p
        uic.loadUi(os.path.join(p, 'GUI/scan_window.ui'), self)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_scan)

        self.main_plot = pg.PlotWidget()
        layout = self.centralwidget.layout()
        layout.addWidget(self.main_plot)
        self.ydata = np.zeros((0))
        self.xdata = np.zeros((0))
        self.p = self.main_plot.plot(self.xdata, self.ydata)

        self.startButton.clicked.connect(self.start_scan)
        self.stopButton.clicked.connect(self.stop_scan)

        self.outChannelLine.setText('{}'.format(self.experiment.properties['Scan']['channel_out']))
        self.outStartLine.setText('{:~}'.format(Q_(self.experiment.properties['Scan']['start'])))
        self.outStopLine.setText('{:~}'.format(Q_(self.experiment.properties['Scan']['stop'])))
        self.outStepLine.setText('{:~}'.format(Q_(self.experiment.properties['Scan']['step'])))

        self.inChannelLine.setText('{}'.format(self.experiment.properties['Scan']['channel_in']))
        self.inDelayLine.setText('{:~}'.format(Q_(self.experiment.properties['Scan']['delay'])))

        self.running_scan = False

        self.action_Save.triggered.connect(self.save_data)

        menubar = self.menuBar()
        self.scanMenu = menubar.addMenu('&Scan')
        self.start_scan_action = QtWidgets.QAction("Start Scan", self)
        self.start_scan_action.setShortcut('Ctrl+Shift+S')
        self.start_scan_action.setStatusTip('Start the scan')
        self.start_scan_action.triggered.connect(self.start_scan)
        self.scanMenu.addAction(self.start_scan_action)


    def start_scan(self):
        """Starts the scan as defined in the Experiment model. Gets the parameters from the GUI, i.e.:
        it gets the input port and delay, the output port and range.
        It updates the plot with the proper units and ranges and creates a worker thread for running the
        scan.
        A timer will be responsible for updating the values into the plot.
        """
        if self.running_scan:
            print('Scan already running')
            return

        self.running_scan = True
        self.experiment.properties['Scan'].update({
            'channel_out': int(self.outChannelLine.text()),
            'start': Q_(self.outStartLine.text()),
            'stop': Q_(self.outStopLine.text()),
            'step': Q_(self.outStepLine.text()),
            'channel_in': int(self.inChannelLine.text()),
            'delay': Q_(self.inDelayLine.text()),
        })
        xlabel = self.experiment.properties['Scan']['channel_out']
        units = self.experiment.properties['Scan']['start'].u
        ylabel = self.experiment.properties['Scan']['channel_in']

        self.main_plot.setLabel('bottom', 'Port: {}'.format(xlabel),
                                units=units)
        self.main_plot.setLabel('left', 'Port: {}'.format(ylabel), units='V')

        self.worker_thread = WorkThread(self.experiment.do_scan)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker_thread.finished.connect(self.stop_scan)
        self.worker_thread.start()
        refresh_time = Q_(self.experiment.properties['GUI']['refresh_time'])
        self.update_timer.start(refresh_time.m_as('ms'))

    def update_scan(self):
        """Updates the plot with the available data in the experiment model. This method is triggered
        through a timer that starts with the start_scan method.
        The method also monitors whether the scan is still running or not. If it has stopped it will update
        the GUI in order to know it.
        """
        self.xdata = self.experiment.xdata_scan
        self.ydata = self.experiment.ydata_scan

        self.p.setData(self.xdata, self.ydata)

        if not self.experiment.running_scan:
            self.stop_scan()

    def stop_scan(self):
        """Stops the scan if it is running. It sets the proper variable to the experiment model in order
        to finish it in an elegant way. It stops the update timer and calls the update plot one last time
        in order to display the very last available data.
        """
        if not self.running_scan:
            return

        print('Stopping Scan')
        self.running_scan = False
        self.experiment.stop_scan = True
        self.update_timer.stop()
        self.xdata = self.experiment.xdata_scan
        self.ydata = self.experiment.ydata_scan

        self.p.setData(self.xdata, self.ydata)

    def save_data(self):
        """Saves the data to disk. It opens a Dialog for selecting the directory. The default filename for
        the data is 'scan_data.dat'. The experiment model takes care of handling the saving itself.
        """
        self.directory = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        filename = 'scan_data.dat'
        file = os.path.join(self.directory, filename)

        self.experiment.save_scan_data(file)

    def closeEvent(self, evnt):
        print('Closing')
        super().closeEvent(evnt)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    from PythonForTheLab.Model.experiment.IV_measurement import Experiment

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

    app = QApplication(sys.argv)
    s = ScanWindow(e)
    s.show()
    app.exit(app.exec_())