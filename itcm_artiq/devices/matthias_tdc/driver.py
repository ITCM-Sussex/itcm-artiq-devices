import numpy as np
import logging

from devices.pic_comms import PICComm

logger = logging.getLogger(__name__)

class MatthiasTDC:
    '''Driver for Matthias black box TDC'''

    def __init__(self, device, baud_rate=9600, timeout=10):
       
        self._pic = PICComm(device, baudrate = baud_rate, timeout=10, write_timeout=timeout)

        self.finished = False #finished flag
        
    def check_status(self):
        '''This function checks the status of the TDC.'''
        
        response = self._pic.send_command('a', recv_bytes =6)

        # Extract status from response
        status = response[0]
        stop_number = (response[1] << 8) | response[2]
        start_number = (response[3] << 8) | response[4]

        return status, start_number, stop_number 
    

    def start_measurement(self):
        '''This function starts the TDC measurement.'''

        self.finished = False

        response = self._pic.send_command('g')

        return response
    
    def set_up(self, tdc_mode_string, measurement_time, histogram_length, histogram_resolution):
        '''Sets up the parameters for the TDC measurement.
        
        Parameters
        tdc_mode: string, options are 'fast' or 'slow'
            which mode to run the TDC in
        measurement_time: float
            time to measure for, s
        histogram_length: int
            length of histogram recorded by TDC == max. delay after start trigger to record a stop, ns
        resolution: int
            bin width of histogram, ns
        '''

        if (histogram_length / histogram_resolution) > 29696:
            logger.error('The number of bins in the histogram exceeds the maximum value.')
        else:

            clock_frequency = 80000
            clock_divider = 256

            measurement_cycles = int((measurement_time * 1000) * (clock_frequency / clock_divider))

            # Split into two 16-bit words
            low_word = measurement_cycles & 0xFFFF
            high_word = (measurement_cycles >> 16) & 0xFFFF

            # Split each word into two bytes
            low_word_low_byte = low_word & 0xFF
            low_word_high_byte = (low_word >> 8) & 0xFF

            high_word_low_byte = high_word & 0xFF
            high_word_high_byte = (high_word >> 8) & 0xFF



            #Rearrange 
            measurement_time_bytes = [high_word_high_byte, high_word_low_byte, low_word_low_byte, low_word_high_byte]

            if tdc_mode_string == 'fast':
                tdc_mode = bytes([1])
            else:
                tdc_mode = bytes([0])

            #Count mode (unused mode)
            counts = 0
            counts_bytes = [(counts >> 24) & 0xFF, (counts >> 16) & 0xFF, (counts >> 8) & 0xFF, (counts) & 0xFF]
            measurement_mode = bytes([0]) # = measure for chosen length of time, 1 would be to record until total counts reach 'counts'

            # Convert histogram length to number of bins
            bin_number = np.int16(np.ceil(histogram_length / histogram_resolution))
            bin_number_bytes = [(bin_number >> 8) & 0xFF, bin_number & 0xFF]

            # Convert histogram resolution with scaling factor
            histogram_resolution_scaled = np.int16(np.ceil(histogram_resolution / 0.055))
            histogram_resolution_bytes = [(histogram_resolution_scaled >> 8) & 0xFF, histogram_resolution_scaled & 0xFF]

            # Make data array to parse to PIC comm
            data_array = list(measurement_time_bytes) + list(measurement_mode) + list(tdc_mode) + list(counts_bytes) + list(bin_number_bytes) + list(histogram_resolution_bytes)
        

            # Send to PIC
            response = self._pic.send_command('h', data_array, 13)

            #logger.info(f'set up response: {response}')

            return bin_number

    def read_histogram(self, bin_number):
        '''Reads the histogram from the PIC controller at the end of a measurement.'''
        
        n_loops = bin_number / 64

        histogram = []

        for index in range(int(np.ceil(n_loops))):

            # Make data array with index of next segment
            data_array = [(index >> 8) & 0xFF, (index) & 0xFF]

            # Read histogram segment from PIC
            read_string = self._pic.send_command('r', data_array, 64)

            # Extract new segment
            new_segment = list(read_string[1:])

            logger.debug(f'new segment: {new_segment}')

            # Append new histogram segment to existing histogram array
            histogram.extend(new_segment)

        return histogram[0:bin_number]
