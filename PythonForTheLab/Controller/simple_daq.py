import serial
from time import sleep

class SimpleDaq():
    DEFAULTS = {'write_termination': '\n',
                'read_termination': '\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'write_timeout': 1,
                'read_timeout': 1,
                }
    rsc = None

    def __init__(self, port):
        self.initialize(port)

    def initialize(self, port):
        self.rsc = serial.Serial(port=port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        sleep(0.5)


    def finalize(self):
        if self.rsc is not None:
            self.rsc.close()

    def query(self, message):
        self.write(message)
        return self.read()

    def write(self, message):
        msg = (message + self.DEFAULTS['write_termination']).encode(self.DEFAULTS['encoding'])
        self.rsc.write(msg)

    def read(self):
        line = "".encode(self.DEFAULTS['encoding'])
        read_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])

        while True:
            new_char = self.rsc.read(size=1)
            line += new_char
            if new_char == read_termination:
                break
        return line.decode(self.DEFAULTS['encoding'])


if __name__ == "__main__":
    from time import sleep
    d = SimpleDaq('/dev/ttyACM0')
    # input('Waiting to ready')
    print(d.query('IDN'))
    d.write('OUT:CH0:4000')
    input('Press to read value')
    print(d.query('IN:CH0'))
    d.finalize()