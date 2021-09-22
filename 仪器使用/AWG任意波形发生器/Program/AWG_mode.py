import visa
import numpy as np
import matplotlib.pyplot as plt

# Set up VISA instrument object
rm = visa.ResourceManager()
awg = rm.open_resource('TCPIP0::169.254.102.2::inst0::INSTR')

#==== 初始化仪器 ====
awg.timeout = 25000
awg.encoding = 'latin_1'
awg.write_termination = None
awg.read_termination = '\n'
print('Connected to ', awg.query('*idn?'))
awg.write('*rst')
awg.write('*cls')


#==== 生成波形数据 ====
# Change these based on your signal requirements
name         = 'test_wfm'
sampleRate   = 10e9
recordLength = 500000
freq         = 100e6

# Create Waveform
t = np.linspace(0, recordLength/sampleRate, recordLength, dtype=np.float32)
wfmData = 0.1*np.sin(2*np.pi*freq*t)

#==== 将波形数据发送给仪器，并设定响应参数 ====
#set sample rate
awg.write("FREQ "+str(sampleRate))

# Send Waveform Data
awg.write('wlist:waveform:new "{}", {}'.format(name, recordLength))
stringArg = 'wlist:waveform:data "{}", 0, {}, '.format(name, recordLength)
awg.write_binary_values(stringArg, wfmData*4)
#暂时不知道为什么波形数据需要乘以4，AWG才能输出正常的幅值
awg.query('*opc?')


# Load waveform, being playback, and turn on output
awg.write('source1:waveform "{}"'.format(name))
awg.write('awgcontrol:run:immediate')
awg.query('*opc?')
awg.write('output1 on')

# Check for errors
error = awg.query('system:error:all?')
print('Status: {}'.format(error))