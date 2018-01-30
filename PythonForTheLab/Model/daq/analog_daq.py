from PythonForTheLab.Controller import SimpleDaq
from PythonForTheLab.Model.daq import DAQBase
from PythonForTheLab import Q_

class AnalogDaq(DAQBase):
    def __init__(self, port):
        self.driver = SimpleDaq(port)

    def idn(self):
        return self.driver.query('IDN')

    def get_analog_value(self, port):
        query_string = 'IN:CH{}'.format(port)
        value_bits = int(self.driver.query(query_string))
        print("Got value: {}".format(value_bits))
        value_volts = value_bits/4095*Q_('3.3V')
        return value_volts

    def set_analog_value(self, port, value):
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