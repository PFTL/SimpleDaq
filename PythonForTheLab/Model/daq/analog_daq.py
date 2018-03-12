"""
Analog DAQ
==========
Class for communicating with a real device. It implements the base for communicating with the device
through a Controller. The experiment in mind is measuring the I-V curve of a diode, adding the logic
into a separate Model for the experiment may seem redundant, but incredibly useful in bigger projects.

"""

from PythonForTheLab.Controller import SimpleDaq
from PythonForTheLab.Model.daq import DAQBase
from PythonForTheLab import Q_


class AnalogDaq(DAQBase):
    """ Simple Model that reflects the logic of the MVC pattern. This model relies on the real controller
    for communicating with an Arduino based DAQ.
    """
    def __init__(self, port):
        """Initializes the driver for communicating with the device.

        :param str port: Port where the device is hooked.
        """
        super().__init__()
        self.driver = SimpleDaq(port)

    def idn(self):
        """Identify the device.

        :return str: Serial number of the device.
        """
        return self.driver.query('IDN')

    def get_analog_value(self, port):
        """ Reads the analog value from a specified port.

        :param int port: Port number from which to read the value
        """
        query_string = 'IN:CH{}'.format(port)
        value_bits = int(self.driver.query(query_string))
        print("Got value: {}".format(value_bits))
        value_volts = value_bits/1024*Q_('3.3V')
        return value_volts

    def set_analog_value(self, port, value):
        """ Sets the analog value of a given port.

        :param int port: Port on which to generate the output.
        :param Quantity value: Voltage to output.
        """
        value = int(value.m_as('V')/3.3*4095)
        print("Setting value: {}".format(value))
        query_string = 'OUT:CH{}:{}'.format(port, value)
        self.driver.write(query_string)
        from time import sleep
        sleep(0.1)


if __name__ == "__main__":
    from time import sleep
    d = AnalogDaq('/dev/ttyACM0')
    sleep(0.5)
    print(d.idn())
    value = Q_('3.0V')
    d.set_analog_value(0, value)
    print('Got value: {:2.2f}'.format(d.get_analog_value(0)))