"""
Base DAQ
========
Base class for the DAQ objects. It keeps track of the functions that every new model should implement.
This helps keeping the code organized and to maintain downstream compliancy.

"""

class DAQBase(object):
    _type = 'DAQModel'
    def __init__(self, port):
        pass

    def idn(self):
        pass

    def get_analog_value(self, port):
        pass

    def set_analog_value(self, channel, value):
        if not isinstance(channel, int):
            raise Exception('Output channel must be integer')
        try:
            value.to('V')
        except:
            raise Exception('Output value must be a quantity')
        pass

    def get_digital_value(self, port):
        pass

    def set_digital_value(self, port, value):
        pass

    def __str__(self):
        return "DAQBase"