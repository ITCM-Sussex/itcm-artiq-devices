import serial

class MulticompMP710086:
    '''Driver for Multicomp MP710086 power supply'''

    def __init__(self, device, timeout= 10):
        self.stream = serial.serial_for_url(device, baudrate=115200, timeout=timeout, write_timeout=timeout)

    def identify(self):
        self.stream.write("*IDN?")
        return self.stream.readline().decode()

    def close(self):
        self.stream.close()