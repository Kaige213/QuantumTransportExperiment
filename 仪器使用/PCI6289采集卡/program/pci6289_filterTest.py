import nidaqmx

with nidaqmx.Task() as task:
    channel = task.ai_channels.add_ai_voltage_chan("PCI6289/ai0", min_val=-10, max_val=10)
    #---- 修改量程 ----
    print("Range_high: ", channel.ai_rng_high)
    print("Range_low:  ", channel.ai_rng_low)
    channel.ai_rng_high = 0.01
    channel.ai_rng_low = -0.01
    print("Range_high: ", channel.ai_rng_high)
    print("Range_low:  ", channel.ai_rng_low)
    #---- 设定滤波器 ----
    print("Filter: ", channel.ai_lowpass_enable)
    channel.ai_lowpass_enable = True
    print("Filter: ", channel.ai_lowpass_enable)