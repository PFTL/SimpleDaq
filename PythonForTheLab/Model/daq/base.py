"""
    Base class for the DAQ objects. It keeps tracks of the functions every new model should implement in order to be
    downstream compliant.

"""

class DAQBase(object):
    def __init__(self):
        pass

    def idn(self):
        pass

    def get_analog_value(self, port):
        pass

    def set_analog_value(self, port, value):
        pass

    def get_digital_value(self, port):
        pass

    def set_digital_value(self, port, value):
        pass