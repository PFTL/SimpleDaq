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
        self.delta_x = 0

    def read_analog(self, port):
        """Re-implements the function as provided by the model.

        :param int port: Port to read
        :return Quantity: The value read by the device model.
        """
        value = self.daq.get_analog_value(port)
        return value

    def read_digital(self, port):
        """Reads the value of a digital port.
        """
        return self.daq.get_digital_value(port)

    def do_scan(self):
        """Does a scan of an analog output while recording an analog input. It doesn't take any arguments,
        it relies on having the proper properties set in the dictionary properties['Scan']
        """
        self.running_scan = True
        start = Q_(self.properties['Scan']['start'])
        stop = Q_(self.properties['Scan']['stop'])
        step = Q_(self.properties['Scan']['step'])
        port_in = self.properties['Scan']['port_in']
        port_out = self.properties['Scan']['port_out']
        delay = Q_(self.properties['Scan']['delay'])
        self.stop_scan = False

        units = start.u
        stop = stop.to(units)
        num_points = (stop - start) / step
        num_points = int(num_points.m_as(''))
        scan = np.linspace(start, stop, num_points + 1)
        self.xdata_scan = scan
        self.ydata_scan = np.zeros((num_points + 1))
        i = 0
        for value in scan:
            if self.stop_scan:
                break
            value = value * units
            self.daq.set_analog_value(port_out, value)
            sleep(delay.m_as('s'))
            data = self.read_analog(port_in).m_as('V')
            self.ydata_scan[i] = data
            i += 1
        self.running_scan = False

    def monitor_signal(self):
        """Monitors a signal in a specific port. Doesn't take any parameters, it assumes there is
        well-configured dictionary called self.properties['Monitor']
        """
        delay = self.properties['Monitor']['time_resolution']
        total_time = self.properties['Monitor']['total_time'].m_as('s')
        self.xdata = np.zeros((int(total_time / delay.m_as('s'))))
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
            d = yaml.load(f)

        self.properties = d
        self.properties['config_file'] = filename
        self.properties['User'] = self.properties['User']['name']
        # self.properties = self.properties['Experiment']
        # self.properties['Scan']['start'] = Q_(self.properties['Scan']['start'])
        # self.properties['Scan']['stop'] = Q_(self.properties['Scan']['stop'])
        # self.properties['Scan']['step'] = Q_(self.properties['Scan']['step'])
        # self.properties['Scan']['delay'] = Q_(self.properties['Scan']['delay'])
        # self.properties['Scan']['refresh_time'] = Q_(self.properties['Scan']['refresh_time'])
        #
        # self.properties['Monitor']['time_resolution'] = Q_(self.properties['Monitor']['time_resolution'])
        # self.properties['Monitor']['refresh_time'] = Q_(self.properties['Monitor']['refresh_time'])
        # self.properties['Monitor']['total_time'] = Q_(self.properties['Monitor']['total_time'])

    def load_devices(self, filename=None):
        """Load devices is not used in the Python for the Lab book, but is a handy procedure to work with
        a more sophisticated logic of devices, sensors and actuators.
        """
        if filename is None:
            if 'devices' in self.properties['init']:
                filename = self.properties['init']['devices']
            else:
                raise Exception("Devices file not defined")
        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.devices = d

    def load_sensors(self, filename=None):
        """Load sensors is not used in the Python for the Lab book, but is a handy procedure to work with
            a more sophisticated logic of devices, sensors and actuators.
        """
        if filename is None:
            if 'sensors' in self.properties['init']:
                filename = self.properties['init']['sensors']
            else:
                raise Exception("Sensors file not defined")

        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.sensors = d

    def load_actuators(self, filename=None):
        """Load devices is not used in the Python for the Lab book, but is a handy procedure to work with
            a more sophisticated logic of devices, sensors and actuators.
        """
        if filename is None:
            if 'actuators' in self.properties['init']:
                filename = self.properties['init']['actuators']
            else:
                raise Exception("Actuators file not defined")

        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.actuators = d

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
                    from PythonForTheLab.Model.daq import AnalogDaq
                    self.daq = AnalogDaq(port)

                else:
                    filename = self.properties['config_file']
                    raise Exception('The daq specified in {} does not exist in this program'.format(filename))
            else:
                filename = self.properties['config_file']
                raise Exception("No DAQ specified in {}".format(filename))
        else:
            self.daq = daq_model

    def save_scan_data(self, file_path):
        """Saves the data from the scan into the specified file. If the file already exists, it will
        automatically append a number before the extension.

        :param str file_path: Full path to the file. It should end with an extension (a dot and 3
        letters).
        """
        i = 0
        ext = file_path[-4:]  # Get the file extension (it assumes is a dot and three letters)
        filename = file_path[:-4]
        while os.path.exists(file_path):
            file_path = filename + '_' + str(i) + ext
            i += 1

        header = "# Data saved by Python For the Lab\n"
        header += "# First Column X-Axis port: {}\n".format(self.properties['Scan']['port_out'])
        header += "# Second Column Y-Axis port: {}\n".format(self.properties['Scan']['port_in'])

        with open(file_path, 'wb') as f:
            f.write(header.encode('ascii'))
            data = np.vstack((self.xdata_scan, self.ydata_scan))
            np.savetxt(f, data.T, fmt='%7.5f')

        print('Data saved to {}'.format(file_path))
