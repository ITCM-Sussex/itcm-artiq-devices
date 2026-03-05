import serial
import logging
logger = logging.getLogger(__name__)


class PICComm():
    '''Define a class to dictate the protocol for PIC comms.'''

    def __init__(self, port, baud_rate=9600, timeout=10):
        '''Defines the PIC protocol class'''

        #Open serial port 
        logger.debug("Opening PIC device...")
        self.ser = serial.serial_for_url(port, baud_rate, timeout=timeout)
        logger.debug("PIC device opened")

    def send_command(self, cmd_char, data_bytes=b'', recv_bytes=None):
        '''Sends command and optional data bytes to PIC
        
        Parameters
        cmd_char : str
            A single-character PIC command.
        data_bytes : bytes 
            data to be sent to the PIC in bytes. For simple commands (eg. start) there is no data sent. 
        recv_bytes : int
            number of bytes expected back. Unless specified, this equals the number of bytes sent.
        '''
        
        payload = cmd_char.encode('latin-1') + bytes(data_bytes)
        if recv_bytes is None:
            recv_bytes = len(payload)
        padding = bytes([0x01] * (recv_bytes - len(payload)))
        
        logger.debug("Sending %s", (payload + padding).hex() )
        self.ser.write(payload + padding)
        response = self.ser.read(recv_bytes)

        return response
        
        #some stuff I haven't written yet

    def close(self):
        '''Closes PIC serial when the program is stopped or closed.'''
        self.ser.close()


