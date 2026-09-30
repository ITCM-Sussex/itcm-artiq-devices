import nidaqmx
import time
import logging

logger = logging.getLogger(__name__)

class NI_PCIe6738Counter:
    """Driver for National Instruments PCIe-6738 edge counter"""

    def __init__(self, device="DC_DAC", channel="ctr0"):
        self.task = nidaqmx.Task()
        self.task.ci_channels.add_ci_count_edges_chan(f"{device}/{channel}")

    def count(self, bin_time=0.1):
        self.task.start()
        time.sleep(bin_time)
        counts = self.task.read()
        self.task.stop()
        return counts

    def ping(self):
        return True
    
    def close(self):
        self.task.close()

class NI_PCIe6738AO:
    """Driver for National Instruments PCIe-6738 analogue outputs"""

    def __init__(self, device="DC_DAC", channels=None):
        self.device = device
        self.tasks = {}
        for ch in (channels or []):
            try:
                t = nidaqmx.Task()
                t.ao_channels.add_ao_voltage_chan(f"{device}/ao{ch}")
                self.tasks[ch] = t
                logger.info("NI_PCIe6738AO reserved channels: %s", list(self.tasks))
            except nidaqmx.errors.DaqError as e:
                logger.error("Failed to reserve AO channel %s: %s", ch, e)
                raise

    def set_voltage(self, channel, voltage):
        """Set a single AO channel voltage. Channel is an integer 0-31."""
        if channel not in self.tasks:
            logger.error(
                "Attempted to set voltage on unreserved channel %s (reserved: %s)",
                channel, list(self.tasks)
            )
            raise ValueError(
                f"Channel {channel} is not reserved by this driver. "
                f"Reserved channels: {list(self.tasks)}"
            )
        self.tasks[channel].write(voltage)

    def ping(self):
        return True
    
    def close(self):
        for t in self.tasks.values():
            t.close()