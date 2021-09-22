import visa
#import traceback
import numpy as np
import matplotlib.pyplot as plt


address = "GPIB0::19::INSTR"
inst = visa.ResourceManager().open_resource(address, read_termination='\n')

#设备初始化
inst.write('*RST')
inst.write('*CLS')
inst.query("*OPC?")

#=======================================
#Parameters
freq = 50.556e6 #Hz
power = -21 #dBm

#sent commands to inst
inst.write("FREQ:CW %fHz"%freq)
inst.write("POW:AMPL %fDBM"%power)
inst.write(":OUTP:STAT ON")
inst.query("*OPC?")
#inst.query("FREQ:CW?")