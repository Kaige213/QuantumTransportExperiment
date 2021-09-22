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