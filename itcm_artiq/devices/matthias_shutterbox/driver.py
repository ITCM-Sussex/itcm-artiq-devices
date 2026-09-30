import numpy as np
import logging

from itcm_artiq.devices.pic_comms import PICComm

logger = logging.getLogger(__name__)

class MatthiasShutterBox:
    '''Driver for Matthias black box RC servo shutter controller'''

    def __init__(self, device, baud_rate=9600, timeout=10):
        logger.info("Opening Matthias shutter box on %s", device)
        self._pic = PICComm(device, baud_rate = baud_rate, timeout=timeout)
        logger.info("Shutter box opened")

    def ping(self):
        return True
    
    def close(self):
        self._pic.close()

    def read_shutter_setup(self):
        logger.info("Reading shutter setup")
        response = self._pic.send_command('r', recv_bytes = 20)
        if response[0] != 82:
            logger.warning("Response command mismatch")
        logger.debug("read response: %s", response)

        rep_rate = int(response[1])
        delay = int(response[2])
        usb_or_ttl_ctrl = [bool(response[3] & (1 << i)) for i in range(8)]
        on_angles = self._bytes_to_angles(response[4:12])
        off_angles = self._bytes_to_angles(response[12:])

        return rep_rate, delay, usb_or_ttl_ctrl, on_angles, off_angles

    def write_shutter_setup(self, rep_rate, delay, ext_ttl_control, on_angles, off_angles):
        usb_ttl_byte = sum(int(bit) << i for i, bit in enumerate(ext_ttl_control))
        on_angle_bytes = self._angles_to_bytes(on_angles)
        off_angle_bytes = self._angles_to_bytes(off_angles)

        data_array = list(bytes(rep_rate)) + list(bytes(delay)) + list(usb_ttl_byte) + list(on_angle_bytes) + list(off_angle_bytes)

        logger.debug(f"sent cmd w + {data_array}")
        response = self._pic.send_command('w', data_array)
        if response[0] != 87:
            logger.warning("Response command mismatch")
        return response

    def read_shutter_positions(self):
        response = self._pic.send_command('p', recv_bytes=2)
        positions = [bool(response[1] & (1 << i)) for i in range(8)]
        return positions

    def write_shutter_position(self, positions):
        position_byte = sum(int(bit) << i for i, bit in enumerate(positions))
        response = self._pic.send_command('s',data_bytes=list(position_byte))
        return position_byte

    def _angles_to_bytes(self, angles):
        byte_array = []
        for i, angle in enumerate(angles):
            if angle > 180:
                logger.warning("Angle at position %s out of range", i)
            byte = int(256 * np.round(angle) / 180) 
            byte_array.append(byte)
        return byte_array

    def _bytes_to_angles(self, byte_array):
        angles = []
        for byte in byte_array:
            angle = 180 * byte / 256
            angles.append(angle)
        return angles