# Tektronix AWG70002A

[2020.9.1]

Ref：

- *AWG70001A and AWG70002A Arbitrary  Waveform Generators Installation and Safety Instructions.pdf* 
- *AWG70000A Series Arbitrary Waveform Generators Programmer.pdf*
- https://github.com/tkzilla/visa_control_examples/blob/master/Python/AWG/awg_simple_waveform_sender.py



## 一、基本介绍

两个主要功能：

1. Function

   该模式下，仪器输出周期波形，包括正弦波、方波、高斯波等。操作简单，可以简单看一下说明文档：*AWG70001A and AWG70002A Arbitrary  Waveform Generators Installation and Safety Instructions.pdf* ，然后在仪器面板上手动操作，并用采集卡或者示波器测量输出信号，查看输出是否正确。

   了解手动操作后，python远程控制也就不难了，其示例程序放在后面。

2. AWG

   该模式下仪器输出波形由用户自定义。本次没有尝试手动操作部分，直接根据网上的示例程序，用python来实现该功能的远程控制。示例代码放在后面，示例程序的网址：https://github.com/tkzilla/visa_control_examples/blob/master/Python/AWG/awg_simple_waveform_sender.py。另外，仪器的maker功能，由于我们暂时不需要，所以没有尝试（但marker功能很有意思，作用也很大）。

   

   

## 二、示例程序

### 2.1 Function 模式

```python
'''
Note:
  1. 发送VISA命令时：注意命令字符串与参数字符串之间有空格隔开
  2. 在function模式下，似乎不需要用户来设定采样率
  3. 仪器设定需要一定时间，所以发送完一个设置命令后，不要立刻询问。应该间隔一段时间后再询问。
    例如:
    awg.write('FGEN:CHANnel1:AMPLitude '+str(amplitude))
    time.sleep(0.1)
    awg.query('FGEN:CHANnel1:AMPLitude?')
  4. 执行该程序前，建议先在AWG70002A上手动操作一边，了解各个功能的含义
   
这里使用网线连接仪器与电脑
步骤：
  1. 用网线连接电脑；
  2. 打开软件keysight IQ Liberaries Suite中的connection expert。
  3. 点击LAN选项，右边出现Detail for TCPIP0的界面。界面上方有三个选项：rescan, edit, instrument
  4. 点击instrument，自动识别出AWG仪器，然后添加；
  5. 执行下面代码，显示可用的visa地址，AWG的visa地址应该在此列
      import pyvisa
      rm = pyvisa.ResourceManager()
      print(rm.list_resources())
'''

import visa
import time
import numpy as np
import matplotlib.pyplot as plt


# Set up VISA instrument object
rm = visa.ResourceManager()
awg = rm.open_resource('TCPIP0::169.254.102.2::inst0::INSTR')

#==== 初始化仪器 ====
awg.timeout = 10000  #AWG内包含一些机械操作，所以会花费较长的时间，5s的timeout并不够用
awg.encoding = 'latin_1'
awg.write_termination = None
awg.read_termination = '\n'

print('Connected to ', awg.query('*idn?'))
awg.write('*rst')
awg.write('*cls')

#==== 打开仪器的1通道，选择工作模式为FGEN ====
awg.write('output1 on')
awg.write('INSTRUMENT:MODE FGEN')

#==== 设定波形参数 ====
#主要参考说明文档的page 36


#TYPE: {SINE|SQUare|TRIangle|NOISe|DC|GAUSsian|EXPRise|EXPDecay|NONE}
awg.write('FGEN:CHANNEL1:TYPE SQUare')
#time.sleep(0.1);awg.query('FGEN:CHANnel1:TYPE?')

#振幅
amplitude = 0.1 
awg.write('FGEN:CHANnel1:AMPLitude '+str(amplitude))
#time.sleep(0.1);awg.query('FGEN:CHANnel1:AMPLitude?')

#频率
frequency = 1e8
awg.write('FGEN:CHANnel1:FREQuency '+str(frequency))
#time.sleep(0.1);awg.query('FGEN:CHANnel1:FREQuency?')

#DC 分量
#offset是周期信号中的DC分量，
#DCLevel是选择直流输出时，需要设定的参数
offset = 0.125
awg.write('FGEN:CHANnel1:OFFSet '+str(offset))
#time.sleep(0.1);awg.query('FGEN:CHANnel1:OFFSet?')

#==== 开始输出 ====
awg.write('AWGControl:RUN')
awg.query('*opc?')
# Check for errors
error = awg.query('system:error:all?')
print('Status: {}'.format(error))
```



### 2.2. AWG 模式

```python
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

#==== 将波形数据发送给仪器，并设定参数 ====
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
```

### 2.3 其他命令

```python
awg.write('AWGCONTROL:STOP:IMMEDIATE')
#如果AWG正在执行sine_wfm波形，则需要先停止输出，再删除该波形
awg.write('WLIST:WAVEFORM:DELETE "Sine_wfm"')
time.sleep(0.1)
awg.query('WLIST:LIST?')  #输出AWG中有哪些波形数据


awg.write('OUTPut:OFF 0')  #all off
awg.write('OUTPut:OFF 1')  #all on

awg.write('OUTPUT1:STATE OFF') #disable channel 1
awg.write('OUTPUT1:STATE ON')  # enable channel 1

awg.write('AWGCONTROL:RUN:IMMEDIATE')
```






## 三、其他

### Maker

- From:https://spectrum-instrumentation.com/zh-hans/introduction-modular-arbitrary-function-generators

  Another useful feature is having a trigger input to initiate the output or to advance the waveform through multiple segments.

  AWG’s can also produce an output trigger or marker output synchronous  with the waveform output. These signals can then be used to trigger a  digitizer, oscilloscope, or other instrument at appropriate times during  the waveform.

- From:https://www.ni.com/zh-cn/support/documentation/supplemental/06/advanced-arbitrary-waveform-generator-features.html#section--556225413

  Data marker events allow for tighter synchronization between signal generators and other devices. For example, an AWG and a digitizer are often synchronized using the exported start trigger of the AWG. However, there exists a short delay between the time the start trigger is  exported to the time analog waveform generation occurs at the output connector. When using the data marker event as the trigger source, faster trigger response times are achieved because the marker event is synchronized directly with the analog output.