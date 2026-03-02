import numpy as np
import logging

from devices.pic_comms import PICComm

logger = logging.getLogger(__name__)

class MatthiasTDC:
    '''Driver for Matthias black box TDC'''

    def __init__(self, device, timeout=10):
        self.pic = PICComm(device, baudrate=9600, logger = logger, timeout=10, write_timeout=timeout)
        
    def check_status(self):
        '''This function checks the status of the TDC.'''
        response = self.pic.pic_comm('a', [], int(6))

        # Extract status from response
        status = response[0]
        stop_number = (response[1] << 8) | response[2]
        start_number = (response[3] << 8) | response[4]

        return status, start_number, stop_number 
    

