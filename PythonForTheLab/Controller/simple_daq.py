import serial
from time import sleep, time


class SimpleDaq():
    """ Controller for the serial devices that ships with Python for the Lab.
    """
    DEFAULTS = {'write_termination': '\n',
                'read_termination': '\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'write_timeout': 1,
                'read_timeout': 1,
                }
    rsc = None

    def __init__(self, port):
        """ Automatically initializes the communication with the device.
        """
        self.initialize(port)

    def initialize(self, port):
        """ Opens the serial port with the DEFAULTS.
        """
        self.rsc = serial.Serial(port=port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        sleep(0.5)

    def idn(self):
        """Identify the device.
        """
        return self.query("IDN")

    def set_analog_value(self, port, value):
        """ Sets a voltage to an output port.
        :param port (int): Port number. Range depends on device
        :param value (Quantity): The output value in Volts.
        """

        value = int(value.m_as('V')/3.3*4095)
        write_string = 'OUT:CH{}:{}'.format(port, value)
        self.write(write_string)

    def finalize(self):
        """ Closes the communication with the device.
        """
        if self.rsc is not None:
            self.rsc.close()

    def query(self, message):
        """Sends a message to the devices an reads the output.
        """
        self.write(message)
        return self.read()

    def write(self, message):
        """ Writes a message to the device using the DEFAULT end of line and encoding.
        :param message (str): The message to send to the device
        """
        if self.rsc is None:
            raise Warning("Trying to write to device before initializing")

        msg = (message + self.DEFAULTS['write_termination']).encode(self.DEFAULTS['encoding'])
        self.rsc.write(msg)

    def read(self):
        """ Reads from the device using the DEFAUTLS end of line and encoding.
        :return (str): The message received from the device.
        """
        line = "".encode(self.DEFAULTS['encoding'])
        read_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])

        t0 = time()
        new_char = "".encode(self.DEFAULTS['encoding'])
        while new_char != read_termination:
            new_char = self.rsc.read(size=1)
            line += new_char
            if time()-t0 > self.DEFAULTS['read_timeout']:
                raise Exception("Readout time reached when reading from the device")

        return line.decode(self.DEFAULTS['encoding'])


if __name__ == "__main__":
    d = SimpleDaq('/dev/ttyACM0')
    # input('Waiting to ready')
    print(d.query('IDN'))
    d.write('OUT:CH0:4000')
    input('Press to read value')
    print(d.query('IN:CH0'))
    d.finalize()