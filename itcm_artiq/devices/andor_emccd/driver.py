import logging

logger = logging.getLogger(__name__)

from pylablib.devices import Andor

class AndorEMCCD:
    def __init__(self):
        logger.info("Initialising Andor EMCCD camera")
        self.cam = Andor.AndorSDK2Camera()
        info = self.cam.get_device_info()
        logger.info("Connected to %s (serial %s)", info.head_model, info.serial_number)

    def ping(self):
        return True

    # Exposure settings
    def set_exposure(self, t):
        logger.info("Setting exposure to %s s", t)
        self.cam.set_exposure(t)

    def get_exposure(self):
        t = self.cam.get_exposure()
        logger.info("Exposure: %s s", t)
        return t

    # EM gain settings
    def set_em_gain(self, gain):
        gain = int(gain)
        logger.info("Setting EM gain to %s", gain)
        self.cam.set_EMCCD_gain(gain)

    def get_em_gain(self):
        gain = self.cam.get_EMCCD_gain()
        logger.info("EM gain: %s", gain)
        return gain

    def set_em_advanced(self, enabled):
        # Andor recommends gain below 300 to prevent sensor aging/degredation
        logger.warning("EM advanced mode %s - gains above 300 risk sensor degredation",
                       "enabled" if enabled else "disabled")
        self.cam.enable_EMCCD_gain_advanced(enabled)

    # ROI settings
    def set_roi(self, hstart, hend, vstart, vend, hbin=1, vbin=1):
        hstart, hend, vstart, vend, hbin, vbin = int(hstart), int(hend), int(vstart), int(vend), int(hbin), int(vbin)
        logger.info("Setting ROI: h=%s-%s v=%s-%s bin=%sx%s",
                    hstart, hend, vstart, vend, hbin, vbin)
        self.cam.set_roi(hstart, hend, vstart, vend, hbin, vbin)

    def get_roi(self):
        roi = self.cam.get_roi()
        logger.info("ROI: %s", roi)
        return roi

    def reset_roi(self):
        logger.info("Resetting ROI to full sensor")
        self.cam.set_roi()

    def get_detector_size(self):
        size = self.cam.get_detector_size()
        logger.info("Detector size: %s", size)
        return size

    # Acquisition settings
    def set_acquisition_mode(self, mode):
        logger.info("Setting acquisition mode to %s", mode)
        self.cam.set_acquisition_mode(mode)

    def get_acquisition_mode(self):
        mode = self.cam.get_acquisition_mode()
        logger.info("Acquisition mode: %s", mode)
        return mode

    def set_trigger_mode(self, mode):
        """
        Options: 'int' (internal), 'ext' (external), 'ext_start',
                 'ext_exp' (external exposure), 'cont' (continuous)
        """
        logger.info("Setting trigger mode to %s", mode)
        self.cam.set_trigger_mode(mode)

    def get_trigger_mode(self):
        mode = self.cam.get_trigger_mode()
        logger.info("Trigger mode: %s", mode)
        return mode

    def set_accumulation_params(self, n_frames, cycle_time):
        logger.info("Setting accumulation: %s frames, cycle time %s s",
                    n_frames, cycle_time)
        self.cam.set_accumulation_cycle_time(cycle_time)
        self.cam.set_accumulation_number(n_frames)

    def get_accumulation_params(self):
        params = {
            "n_frames": self.cam.get_accumulation_number(),
            "cycle_time": self.cam.get_accumulation_cycle_time(),
        }
        logger.info("Accumulation params: %s", params)
        return params

    # Temperature 
    def get_temperature(self):
        temp = self.cam.get_temperature()
        logger.debug("Temperature: %s", temp)
        return temp

    def get_status(self):
        status = self.cam.get_status()
        logger.debug("Camera status: %s", status)
        return status

    # Acquire signal
    def get_frame(self):
        logger.debug("Acquiring single frame")
        frame = self.cam.snap().tolist()
        logger.debug("Frame acquired")
        return frame

    def get_kinetic_series(self):
        logger.info("Starting kinetic series acquisition")
        self.cam.start_acquisition()
        self.cam.wait_for_frame()
        frames = self.cam.read_multiple_images()
        logger.info("Kinetic series complete: %s frames", len(frames))
        return frames.tolist()

    def close(self):
        logger.info("Closing camera connection")
        self.cam.close()
        