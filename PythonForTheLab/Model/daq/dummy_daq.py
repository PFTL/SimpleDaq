"""
Dummy DAQ
=========
Class that implements the base methods but that doesn't interact with a real device.
This helps developing the GUI without the need of a real device or a specific computer.
It is useful for debugging and timing applications.

"""
import numpy as np
from PythonForTheLab import Q_
from PythonForTheLab.Model.daq import DAQBase


class DummyDaq(DAQBase):
    serial_number = '1234ABC'
    """Fake serial number of the dummy device."""
    def __init__(self, port):
        super().__init__(port=port)
        self.port = port
        self.i = 0

    def idn(self):
        """Returns the serial number of the fake device."""
        return self.serial_number

    def get_analog_value(self, port):
        """Gets an analog value. They are going to represent a sine with frequency 250 points.

        :return Quantity: Voltage of the analog output
        """
        self.i += 1
        return np.sin(self.i/10)*Q_('V')

    def get_digital_value(self, port):
        """Gets a digital input value. It returns either 1 or 0 with a random probability.
        period

        :param int port: Port from which to read the digital input.
        :return bool: Value of the fake digital input port.
        """
        return np.random.random(1) > 0.5

    def __str__(self):
        return "DummyDaq"
