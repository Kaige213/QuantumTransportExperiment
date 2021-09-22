import nidaqmx
from nidaqmx.constants import AcquisitionType 

sample_per_second  = 10
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("PCI6289/ai0", min_val=-0.1, max_val=0.1)
    task.timing.cfg_samp_clk_timing(rate=sample_per_second, sample_mode=AcquisitionType.CONTINUOUS)
    for n in range(10):
        data = task.read(10)
        print(type(data), len(data))

"""
nidaqmx.constants.AcquisitionType.CONTINUOUS
nidaqmx.constants.AcquisitionType.FINITE
"""