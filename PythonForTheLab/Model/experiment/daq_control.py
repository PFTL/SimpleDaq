import numpy as np
import yaml
from time import time, sleep


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

    def load_daq(self, daq_model):
        """ Loads a DAQ Model already initialized"""
        self.daq = daq_model

    def read_analog(self, port):
        value = self.daq.get_analog_value(port)
        return value

    def read_digital(self, port):
        return self.daq.get_digital_value(port)

    def do_scan(self):
        self.running_scan = True
        start = self.properties['scan_start']
        stop = self.properties['scan_stop']
        step = self.properties['scan_step']
        port_in = self.properties['scan_port_in']
        port_out = self.properties['scan_port_out']
        delay = self.properties['scan_delay']
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
        delay = self.properties['time_resolution']
        total_time = self.properties['total_time'].m_as('s')
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
