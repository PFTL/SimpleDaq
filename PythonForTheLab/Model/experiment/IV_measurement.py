# coding=utf-8
"""
Experiment Model
================
Building a model for the experiment allows developers to have a clear picture of the logic of their
experiments. It allows to build simple GUIs around them and to easily share the code with other users.

"""
import os
import numpy as np
import yaml
from time import time, sleep

from PythonForTheLab import Q_


class Experiment:
    """Class for performing a measurement of an I-V curve of a light emitting photodiode (LED).
    """

    def __init__(self):
        self.daq = None
        self.properties = {}
        self.stop_monitor = False
        self.xdata = np.zeros(0)
        self.ydata = np.zeros(0)
        self.xdata_scan = np.zeros(0)
        self.ydata_scan = np.zeros(0)
        self.running_scan = False
        self.stop_scan = False
        self.delta_x = 0
        self.t0 = time()

    def read_analog(self, port: int):
        """Re-implements the function as provided by the model.

        :param int port: Port to read
        :return Quantity: The value read by the device model.
        """
        value = self.daq.get_analog_value(port)
        return value

    def do_scan(self):
        """Does a scan of an analog output while recording an analog input. It doesn't take any arguments,
        it relies on having the proper properties set in the dictionary properties['Scan']
        """
        if self.running_scan:
            raise Warning('Trying to start a second scan')

        start = Q_(self.properties['Scan']['start'])
        stop = Q_(self.properties['Scan']['stop'])
        step = Q_(self.properties['Scan']['step'])
        channel_in = self.properties['Scan']['channel_in']
        channel_out = self.properties['Scan']['channel_out']
        delay = Q_(self.properties['Scan']['delay'])
        units = start.u
        stop = stop.to(units)
        num_points = (stop - start) / step
        num_points = round(num_points.m_as('')) + 1
        scan = np.linspace(start, stop, num_points) * units
        self.xdata_scan = scan
        self.ydata_scan = np.zeros(num_points) * units
        i = 0
        self.running_scan = True
        self.stop_scan = False
        for value in scan:
            if self.stop_scan:
                break
            self.daq.set_analog_value(int(channel_out), value)
            sleep(delay.m_as('s'))
            self.ydata_scan[i] = self.daq.get_analog_value(int(channel_in))
            i += 1
        self.running_scan = False

    def monitor_signal(self):
        """Monitors a signal in a specific port. Doesn't take any parameters, it assumes there is
        well-configured dictionary called self.properties['Monitor']
        """
        delay = Q_(self.properties['Monitor']['time_resolution'])
        total_time = Q_(self.properties['Monitor']['total_time']).m_as('s')
        self.xdata = np.zeros((round(total_time / delay.m_as('s'))))
        self.delta_x = delay.m_as('s')
        self.ydata = np.zeros(int(total_time / delay.m_as('s')))
        self.t0 = time()
        while not self.stop_monitor:
            self.ydata = np.roll(self.ydata, -1)
            self.ydata[-1] = self.read_analog(1).m_as('V')
            self.xdata = np.roll(self.xdata, -1)
            self.xdata[-1] = time() - self.t0  # self.xdata[-2] + self.delta_x
            sleep(delay.m_as('s'))

    def load_config(self, filename=None):
        """Loads the configuration file to generate the properties of the Scan and Monitor.

        :param str filename: Path to the filename. Defaults to Config/experiment.yml if not specified.
        """
        if filename is None:
            filename = 'Config/experiment.yml'

        with open(filename, 'r') as f:
            params = yaml.load(f)

        self.properties = params
        self.properties['config_file'] = filename
        self.properties['User'] = self.properties['User']['name']

    def load_daq(self, daq_model=None):
        """ Loads a DAQ Model already initialized or loads from yaml specifications. The DAQ that can
        be provided through the YAML are 'DummyDaq' and 'RealDaq'. There are no limitations regarding
        an already initialized DAQ provided that follows the Daq Model.

        :param daq_model: it can be a model already initailized. If not provided, loads the default.
        """
        if daq_model is None:
            if 'DAQ' in self.properties:
                name = self.properties['DAQ']['name']
                port = self.properties['DAQ']['port']
                if name == 'DummyDaq':
                    from PythonForTheLab.Model.daq import DummyDaq
                    self.daq = DummyDaq(port)

                elif name == 'RealDaq':
                    from PythonForTheLab.Model.daq.analog_daq import AnalogDaq
                    self.daq = AnalogDaq(port)

                else:
                    filename = self.properties['config_file']
                    raise Exception('The daq specified in {} does not exist in this program'.format(filename))
            else:
                filename = self.properties['config_file']
                raise Exception("No DAQ specified in {}".format(filename))
        else:
            self.daq = daq_model

    def save_scan_data(self, file_path=None):
        """Saves the data from the scan into the specified file. If the file already exists, it will
        automatically append a number before the extension.

        :param str file_path: Full path to the file. It should end with an extension (a dot and 3
        letters).
        """
        if file_path is None:
            file_path = self.properties['Save_File']['filename']
        i = 0
        ext = file_path[-4:]  # Get the file extension (it assumes is a dot and three letters)
        filename = file_path[:-4]
        while os.path.exists(file_path):
            file_path = filename + '_' + str(i) + ext
            i += 1

        header = "# Data saved by Python For the Lab\n"
        header += "# First Column X-Axis channel: {}, units: {}\n".format(
                self.properties['Scan']['channel_out'], self.xdata_scan[0].u)
        header += "# Second Column Y-Axis channel: {}, units: {}\n".format(
                self.properties['Scan']['channel_in'], self.ydata_scan[0].u)

        with open(file_path, 'wb') as f:
            f.write(header.encode('ascii'))
            scan_data = np.vstack((self.xdata_scan, self.ydata_scan))
            np.savetxt(f, scan_data.T, fmt='%7.5f')

        print('Data saved to {}'.format(file_path))


if __name__ == "__main__":
    e = Experiment()
    data = e.read_analog(1)
