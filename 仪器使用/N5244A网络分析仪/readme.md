## N5244A （未完）

**网上的资料：**

http://na.support.keysight.com/pna/help/latest/Programming/XComFinderSet.htm
http://na.support.keysight.com/pna/help/latest/Programming/Programming_Guide.htm



#### 一些可能有用的命令

- 询问扫描类型

  ```python
  sweepType = inst.query("SENSe:SWEep:TYPE?")
  #部分可能的返回值: "CW", "POW", "LIN"
  ```

  

- 设置仪器的marker

  ```python
  inst.write("DISP:WIND:ANN:MARK:SIZE LARG") #marker size
  inst.write("CALCulate1:MARKer:COUP ON")    #marker coupled
  inst.write("CALCulate1:MARKer:DISC ON")    #marker discrete
  ```

  

#### Note

- IF_BW的值不是连续的：10、15、20、30、...  （单位：Hz）
- sweepType 为扫描时间时，sweepPoints表示在某个时间段内，测量点数为 sweepPoints
- sweep averaging 和 point averaging 的区别（page：263）
- 



#### Point Averaging

下面实验中，average mode 为point average 时，测量所花时间与 averaging point (or: averaging factor)几乎成正比。猜想，averaging factor=10 时，得到一个测量数据，跟averaging factor=1并重复测量10次而得到的平均值，这两种方式是等效的。

Operation Time:

<img src=".\time_for_point_averaging.png" style="zoom:72%;" />

```python
#关于设置网络分析仪的代码，这里只放了set averaging的代码
import visa
import time
import matplotlib.pyplot as plt
import numpy as np

address = "GPIB0::5::INSTR"
inst = visa.ResourceManager().open_resource(address, read_termination='\n')


#set average
command = "SENS:AVER:STAT ON\n"
inst.write(command)
#command = "SENS:AVER:MODE SWEEP"
command = "SENS:AVER:MODE POINT"
inst.write(command)

N_avg = 10
time_vec = []
for n in range(1, N_avg+1):
    avg     = n
    command = "SENS:AVER:COUN "+ str(avg) + "\n"
    inst.write(command)

    #==================================================
    #start sweep
    command = "INITiate1\n"
    inst.write(command)
    #check time
    start_time = time.time()
    while True:
        try:
            command = "*OPC?"
            inst.query(command)
            break
        except:pass    
    time_vec.append(time.time() - start_time)

plt.figure(figsize=(5,4))
plt.plot(np.arange(1,N_avg+1), time_vec)
plt.xlabel("Averaging Point")
plt.ylabel("Time For Operation(s)")
plt.title("Time For Point Averaging")
plt.xlim([1,10])
plt.show()
```



#### Note:

- "INITiate1" 和 "INITiate1\n" 都可以，



#### 问题

- 实验室每次使用网络分析仪时，调用某个态，似乎这个态是包括校准，测量设置（频率，功率等等），然后直接测量
- 在Labview2008的startSweep.vi中，timeout似乎是无穷大，query("*OPC?")，会一直等待仪器，直到仪器扫描完毕，返回查询结果。
- IF Bandwidth 看起来有点像锁相放大器的低通滤波器
- To read error terms, use SENS:CORR:CSET:DATA



#### Log

- [2019.11.29] 暂时来看，我们实验中需要用到的averaging功能应该是 point averaging，而不是 sweep averaging。以前老程序中，每次读取数据前都要执行restart_average的程序（command = "SENSe1:AVERage:CLEar\n"），是因为使用了默认的sweep averaging的模式，而且老程序中没有找到设置averaging mode 的代码。现在没有完全理解sweep averaging的工作原理，先放一放，直接使用point averaging，以后有时间了再看看sweep averaging的原理和用途。
- [2019.11.29] 在N5244A_instrument 类里，先执行configur，再执行set_trace，而且中间最好time.sleep( 0.2 )，否则CW的显示可能错误，依然显示旧的频率，新设置的CW频率没来得及显示在window中（set_trace函数会删除并添加window）