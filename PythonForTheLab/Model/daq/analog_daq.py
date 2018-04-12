"""
Analog DAQ
==========
Class for communicating with a real device. It implements the base for communicating with the device
through a Controller. The experiment in mind is measuring the I-V curve of a diode, adding the logic
into a separate Model for the experiment may seem redundant, but incredibly useful in bigger projects.

"""
from PythonForTheLab.Controller.simple_daq import SimpleDaq

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
        self.driver = SimpleDaq(port)

    def idn(self):
        """Identify the device.

        :return str: Serial number of the device.
        """
        return self.driver.query('IDN')

    def switch_off_LED(self):
        pass

    def switch_on_LED(self):
        pass

    def get_analog_value(self, channel):
        """ Reads the analog value from a specified port.

        :param int channel: Port number from which to read the value
        """
        query_string = 'IN:CH{}'.format(channel)
        value_bits = int(self.driver.query(query_string))
        value_volts = value_bits/1024*Q_('3.3V')
        return value_volts

    def set_analog_value(self, channel, value):
        """ Sets the analog value of a given port.

        :param int channel: Port on which to generate the output.
        :param Quantity value: Voltage to output.
        """
        value = int(value.m_as('V')/3.3*4096)
        query_string = 'OUT:CH{}:{}'.format(channel, value)
        self.driver.write(query_string)


if __name__ == "__main__":
    from time import sleep
    d = AnalogDaq('/dev/ttyACM0')
    print(d.idn())
    off_voltage = Q_('0V')
    on_voltage = Q_('3.3V')
    for i in range(10):
        d.set_analog_value(0, on_voltage)
        print(d.get_analog_value(0))
        sleep(0.5)
        d.set_analog_value(0, off_voltage)
        print(d.get_analog_value(0))
        sleep(0.5)