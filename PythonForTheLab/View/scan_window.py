import os
import numpy as np
import pyqtgraph as pg
from PyQt4 import QtCore, QtGui, uic

from PythonForTheLab import Q_
from .general_worker import WorkThread


class ScanWindow(QtGui.QMainWindow):
    def __init__(self, experiment, parent=None):
        super().__init__(parent)


        self.experiment = experiment

        p = os.path.dirname(__file__)
        self.directory = p
        uic.loadUi(os.path.join(p, 'GUI/scan_window.ui'), self)

        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.update_scan)

        self.main_plot = pg.PlotWidget()
        self.plot_layout =QtGui.QHBoxLayout()
        self.plot_layout.addWidget(self.main_plot)
        self.plotWidget.setLayout(self.plot_layout)
        # self.centralwidget.layout.addWidget(self.main_plot)
        self.ydata = np.zeros((0))
        self.xdata = np.zeros((0))
        self.p = self.main_plot.plot(self.xdata, self.ydata)

        self.startButton = QtGui.QPushButton('&Start')
        self.stopButton = QtGui.QPushButton('&Stop')
        self.buttonBox.addButton(self.startButton, QtGui.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.stopButton, QtGui.QDialogButtonBox.ActionRole)
        self.startButton.clicked.connect(self.start_scan)
        self.stopButton.clicked.connect(self.stop_scan)

        self.outPortLine.setText('{}'.format(self.experiment.properties['Scan']['port_out']))
        self.outStartLine.setText('{:~}'.format(self.experiment.properties['Scan']['start']))
        self.outStopLine.setText('{:~}'.format(self.experiment.properties['Scan']['stop']))
        self.outStepLine.setText('{:~}'.format(self.experiment.properties['Scan']['step']))

        self.inPortLine.setText('{}'.format(self.experiment.properties['Scan']['port_in']))
        self.inDelayLine.setText('{:~}'.format(self.experiment.properties['Scan']['delay']))

        self.running_scan = False

        self.action_Save.triggered.connect(self.save_data)


    def start_scan(self):
        if self.running_scan:
            print('Scan already running')
            return

        self.running_scan = True
        self.experiment.properties['Scan'].update({
            'port_out': int(self.outPortLine.text()),
            'start': Q_(self.outStartLine.text()),
            'stop': Q_(self.outStopLine.text()),
            'step': Q_(self.outStepLine.text()),
            'port_in': int(self.inPortLine.text()),
            'delay': Q_(self.inDelayLine.text()),
        })
        xlabel = self.experiment.properties['Scan']['port_out']
        units = self.experiment.properties['Scan']['start'].u
        ylabel = self.experiment.properties['Scan']['port_in']

        self.main_plot.setLabel('bottom', 'Port: {}'.format(xlabel),
                                units=units)
        self.main_plot.setLabel('left', 'Port: {}'.format(ylabel), units='V')

        self.worker_thread = WorkThread(self.experiment.do_scan)
        self.worker_thread.start()
        self.update_timer.start(self.experiment.properties['Scan']['refresh_time'].m_as('ms'))

    def update_scan(self):
        self.xdata = self.experiment.xdata_scan
        self.ydata = self.experiment.ydata_scan

        self.p.setData(self.xdata, self.ydata)

        if not self.experiment.running_scan:
            self.stop_scan()

    def stop_scan(self):
        print('Stopping Scan')
        self.running_scan = False
        self.experiment.stop_scan = True
        self.update_timer.stop()

    def save_data(self):
        self.directory = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", self.directory))
        i = 0
        filename = 'scan_data_'
        while os.path.isfile(os.path.join(self.directory, '%s%i.dat' % (filename, i))):
            i += 1
        file = os.path.join(self.directory, '%s%i.dat' % (filename, i))
        header = "# Data saved by Python For the Lab\n"
        header += "# First Column X-Axis device {}\n".format(self.experiment.properties['scan_port_out'])
        header += "# Second Column Y-Axis device {}\n".format(self.experiment.properties['scan_port_in'])

        with open(file, 'wb') as f:
            f.write(header.encode('ascii'))
            data = np.vstack((self.xdata, self.ydata))
            np.savetxt(f, data.T, fmt='%7.5f')



if __name__ == "__main__":
    import sys
    from PyQt4.Qt import QApplication
    from PythonForTheLab.Model.experiment.daq_control import Experiment

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