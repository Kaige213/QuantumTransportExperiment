import nidaqmx

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("PCI6289/ao0",min_val=-1, max_val=1)
    task.write(0.5)

