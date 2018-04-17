from lantz import Feat

from PythonForTheLab.Controller.lantz_daq import LantzDaq
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
        self.driver = LantzDaq.via_serial(port)

    @Feat()
    def idn(self):
        """Identify the device.

        :return str: Serial number of the device.
        """
        return self.driver.idn

    def switch_off_LED(self):
        pass

    def switch_on_LED(self):
        pass

    def get_analog_value(self, channel):
        """ Reads the analog value from a specified port.

        :param int channel: Port number from which to read the value
        """
        return self.driver.get_input[channel]

    def set_analog_value(self, channel, value):
        """ Sets the analog value of a given port.

        :param int channel: Port on which to generate the output.
        :param Quantity value: Voltage to output.
        """
        self.driver.set_output[channel] = value


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