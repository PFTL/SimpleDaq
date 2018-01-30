import importlib
import numpy as np
import yaml
from time import time, sleep

from PythonForTheLab import Q_


class Experiment():
    def __init__(self):
        self.daq = None
        self.properties = {}
        self.stop_monitor = False
        self.xdata = np.zeros((0))
        self.ydata = np.zeros((0))
        self.xdata_scan = np.zeros((0))
        self.ydata_scan = np.zeros((0))
        self.running_scan = False

    def read_analog(self, port):
        value = self.daq.get_analog_value(port)
        return value

    def read_digital(self, port):
        return self.daq.get_digital_value(port)

    def do_scan(self):
        self.running_scan = True
        start = self.properties['Scan']['start']
        stop = self.properties['Scan']['stop']
        step = self.properties['Scan']['step']
        port_in = self.properties['Scan']['port_in']
        port_out = self.properties['Scan']['port_out']
        delay = self.properties['Scan']['delay']
        self.stop_scan = False

        units = start.u
        stop = stop.to(units)
        data = []
        num_points = (stop-start)/step
        num_points = int(num_points.m_as(''))
        scan = np.linspace(start, stop, num_points+1)
        self.xdata_scan = scan
        self.ydata_scan = np.zeros((num_points+1))
        i = 0
        for value in scan:
            if self.stop_scan:
                break
            value = value*units
            self.daq.set_analog_value(port_out, value)
            sleep(delay.m_as('s'))
            data = self.read_analog(port_in).m_as('V')
            self.ydata_scan[i] = data
            i += 1
        self.running_scan = False

    def monitor_signal(self):
        delay = self.properties['Monitor']['time_resolution']
        total_time = self.properties['Monitor']['total_time'].m_as('s')
        self.xdata = np.zeros((int(total_time/delay.m_as('s'))))
        self.delta_x = delay.m_as('s')
        self.ydata = np.zeros(int(total_time/delay.m_as('s')))
        self.t0 = time()
        while not self.stop_monitor:
            self.ydata = np.roll(self.ydata, -1)
            self.ydata[-1] = self.read_analog(1).m_as('V')
            self.xdata = np.roll(self.xdata, -1)
            self.xdata[-1] = time()-self.t0 #self.xdata[-2] + self.delta_x
            sleep(delay.m_as('s'))

    def load_config(self, filename=None):
        if filename is None:
            filename = 'Config/experiment.yml'

        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.properties = d
        self.properties['config_file'] = filename
        self.properties['Scan']['start'] = Q_(self.properties['Scan']['start'])
        self.properties['Scan']['stop'] = Q_(self.properties['Scan']['stop'])
        self.properties['Scan']['step'] = Q_(self.properties['Scan']['step'])
        self.properties['Scan']['delay'] = Q_(self.properties['Scan']['delay'])
        self.properties['Scan']['refresh_time'] = Q_(self.properties['Scan']['refresh_time'])

        self.properties['Monitor']['time_resolution'] = Q_(self.properties['Monitor']['time_resolution'])
        self.properties['Monitor']['refresh_time'] = Q_(self.properties['Monitor']['refresh_time'])
        self.properties['Monitor']['total_time'] = Q_(self.properties['Monitor']['total_time'])

    def load_devices(self, filename=None):
        if filename is None:
            if 'devices' in self.properties['init']:
                filename = self.properties['init']['devices']
            else:
                raise Exception("Devices file not defined")
        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.devices = d

    def load_sensors(self, filename=None):
        if filename is None:
            if 'sensors' in self.properties['init']:
                filename = self.properties['init']['sensors']
            else:
                raise Exception("Sensors file not defined")

        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.sensors = d

    def load_actuators(self, filename=None):
        if filename is None:
            if 'actuators' in self.properties['init']:
                filename = self.properties['init']['actuators']
            else:
                raise Exception("Actuators file not defined")

        with open(filename, 'r') as f:
            d = yaml.load(f)

        self.actuators = d

    def load_daq(self, daq_model=None):
        """ Loads a DAQ Model already initialized or loads from yaml specifications"""
        if daq_model is None:
            if 'DAQ' in self.devices:
                if 'driver' in self.devices['DAQ']:
                    d = self.devices['DAQ']['driver'].split('/')
                    driver_class = getattr(importlib.import_module(d[0]), d[1])
                    self.daq = driver_class(self.devices['DAQ']['connection']['port'])
                else:
                    raise Exception("Driver for DAQ not defined in config file")
            else:
                raise Exception("DAQ device not defined in devices")
        else:
            self.daq = daq_model