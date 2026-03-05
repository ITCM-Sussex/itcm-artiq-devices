import serial
import logging

logger = logging.getLogger(__name__)

class MulticompMP710086:
    '''Driver for Multicomp MP710086 power supply'''

class MulticompMP710086:
    '''Driver for Multicomp MP710086 single channel DC power supply.'''

    def __init__(self, device, timeout=10):
        logger.debug("Opening Multicomp MP710086 on %s", device)
        self.stream = serial.serial_for_url(device, baudrate=115200, timeout=timeout, write_timeout=timeout)
        logger.debug("Multicomp MP710086 opened")

    def _send(self, command):
        '''Send a SCPI command string.'''
        self.stream.write((command + "\n").encode())

    def _query(self, command):
        '''Send a SCPI query and return the response as a stripped string.'''
        self._send(command)
        return self.stream.readline().decode().strip()

    def ping(self):
        return True

    def close(self):
        self.stream.close()

    # IEEE488.2 common commands

    def identify(self):
        '''Query the ID string of the instrument.'''
        return self._query("*IDN?")

    def reset(self):
        '''Reset the instrument to factory default settings.'''
        self._send("*RST")

    # Output control

    def set_output(self, enabled: bool):
        '''Enable or disable the output.'''
        logger.debug("Setting output to %s", enabled)
        self._send("OUTP " + ("ON" if enabled else "OFF"))

    def get_output(self) -> bool:
        '''Query whether the output is enabled.'''
        return bool(int(self._query("OUTP?")))

    # Voltage

    def set_voltage(self, voltage: float):
        '''Set the output voltage in volts.'''
        logger.debug("Setting voltage to %.4f V", voltage)
        self._send("VOLT %.4f" % voltage)

    def get_voltage_setpoint(self) -> float:
        '''Query the voltage setting value in volts.'''
        return float(self._query("VOLT?"))

    def get_voltage(self) -> float:
        '''Measure the voltage on the output terminal in volts.'''
        return float(self._query("MEAS:VOLT?"))

    def set_voltage_limit(self, voltage: float):
        '''Set the overvoltage protection (OVP) value in volts.'''
        logger.debug("Setting voltage limit to %.4f V", voltage)
        self._send("VOLT:LIM %.4f" % voltage)

    def get_voltage_limit(self) -> float:
        '''Query the overvoltage protection (OVP) value in volts.'''
        return float(self._query("VOLT:LIM?"))

    # Current

    def set_current(self, current: float):
        '''Set the output current in amps.'''
        logger.debug("Setting current to %.4f A", current)
        self._send("CURR %.4f" % current)

    def get_current_setpoint(self) -> float:
        '''Query the current setting value in amps.'''
        return float(self._query("CURR?"))

    def get_current(self) -> float:
        '''Measure the current on the output terminal in amps.'''
        return float(self._query("MEAS:CURR?"))

    def set_current_limit(self, current: float):
        '''Set the overcurrent protection (OCP) value in amps.'''
        logger.debug("Setting current limit to %.4f A", current)
        self._send("CURR:LIM %.4f" % current)

    def get_current_limit(self) -> float:
        '''Query the overcurrent protection (OCP) value in amps.'''
        return float(self._query("CURR:LIM?"))

    # Power

    def get_power(self) -> float:
        '''Measure the power on the output terminal in watts.'''
        return float(self._query("MEAS:POW?"))