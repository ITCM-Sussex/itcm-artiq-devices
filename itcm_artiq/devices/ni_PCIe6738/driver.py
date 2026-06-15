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

    def __init__(self, device="DC_DAC"):
        self.device = device

    def set_voltage(self, channel, voltage):
        """Set a single AO channel voltage. Channel is an integer 0-31."""
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(f"{self.device}/ao{channel}")
            task.write(voltage)

    def ping(self):
        return True
    
    def close(self):
        self.task.close()