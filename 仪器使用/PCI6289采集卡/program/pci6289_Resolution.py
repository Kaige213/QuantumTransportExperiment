import nidaqmx
import matplotlib.pyplot as plt

sample_per_second  = 100000
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("PCI6289/ai0", min_val=-0.1, max_val=0.1)
    task.timing.cfg_samp_clk_timing(rate=sample_per_second)
    data = task.read(sample_per_second)
    
plt.plot(data, '+')
plt.grid()
plt.pause(0.1)