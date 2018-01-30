"""
    Example of a daq returning values but without any real device connected to it.

"""
import numpy as np
from PythonForTheLab import Q_
from PythonForTheLab.Model.daq import DAQBase


class DummyDaq(DAQBase):
    serial_number = '1234ABC'
    def __init__(self):
        super().__init__()
        self.i = 0

    def idn(self):
        return self.serial_number

    def get_analog_value(self, port):
        self.i += 1
        return np.sin(self.i/250)*Q_('V')

    def get_digital_value(self, port):
        return np.random.random(1) > 0.5
