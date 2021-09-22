## LI5650

#### 读取数据

":FETC?" 命令是读取测量的最新数据，默认读取缓存区的data1，data2数据。可以通过前面板DARA按钮查看或修改data1，data2保存的数据类型。查看DataOut：按一下DATA按钮，屏幕下方的Data Out区域显示数据输出格式。修改DataOut：DATA -> BASIC -> R-$\rm\theta$  ，这样设置后，data1，和data2将保存R和theta的值。（参考LI5650说明书，3.6.2小节，3-34页）。

<img src=".\dataOut.PNG" style="zoom:60%;" />

**Note** : 

- 我们的测量程序里，默认读取X，Y值，但有时可能设备被设置成data1和data2存放R-theta值，通过":FETC?"获取的数据就会出错。但是设备的data3，data4始终储存X，Y值，不会被改变。所以，我们使用命令":DATA 19"，设置":FETC?"读取data3，data4数据，以及STATUS

- status=0，表示没有异常，但并不一定说明测量成功，或者测量结果已经稳定。如果待测量的信号突然变化，锁相放大器需要一定时间才能趋于稳定，在这段时间内，status值可能也是0，即没有其他仪器问题出现。

- 现版本的程序里，每次读取数据时，检查status是否为0，如果否，表示测量有误，放弃该数据并等待1秒，然后重新读取，如此循环直到status=0，返回数据，和error_info="No error"。如果循环次数达到20次，则放弃测量，返回值：X=0, Y=0, error_info="Error:LI5650:read_XY"；

- 暂时没有找到这样的功能：标志锁相成功，或者测量结果已经稳定。所以现在的解决方法是，在测量程序里，手动设置等待时间，每次设置完控制仪器后，等待一段时间，让样品和测量仪器都稳定，再读取数据。

  （一个可能的方案：每次读取多个数据，比如10个X值，然后查看是否为随机，如果X值往一个方向变化，说明信号没稳定，如果有一定的随机性，说明测量可以结束，并返回测量值。该方案的缺点：1. 如果确定随机性； 2. 测量速度会极大地降低）

```
#:DATA命令后的参数含义，例如，":DATA 1"表示":FETC?"命令只读取status数据
#下面的: ->表示发送命令, <-表示返回数据 (keysight connection expert的表示格式)
-> :DATA 1  
-> :FETC?  
<- STATUS

-> :DATA 2
-> :FETC?
<- data1

-> :DATA 3
-> :FETC?
<- STATUS, data1

-> :DATA 4
-> :FETC?
<- data2

-> :DATA 5
-> :FETC?
<- STATUS, data2

-> :DATA 6
-> :FETC?
<- data1, data2

-> :DATA 7
-> :FETC?
<- STATUS, data1, data2

-> :DATA 19
-> :FETC?
<- STATUS, data3, data4
```



#### VISA 示例

```python
import visa
import time

address = "GPIB0::4::INSTR"
inst = visa.ResourceManager().open_resource(address, read_termination='\n')

#check connection status
command = "*IDN?"
return_str = inst.query(command)
print("Return(*IDN?): ", return_str)

#if ("LI5650" in return_str):print("No error")
#else: print( "Error:LI5650:Connection")

#set Frequency
freq    = 11
command = ":SOUR:FREQ " + str(freq)
inst.write(command)
error_info = inst.query(":SYST:ERR?")
print(error_info)
#time.sleep(0.1)

#set reference signal source
#command = ":ROUT2 RINP"
#command = ":ROUT2 IOSC"
command = ":ROUT2 SINP"
inst.write(command)
error_info = inst.query(":SYST:ERR?")
print(error_info)

#set signal input connector
command = ":ROUT A"
#command = ":ROUT AB"
#command = ":ROUT I"
inst.write(command)
error_info = inst.query(":SYST:ERR?")
print(error_info)

#set voltage
voltage = 0.23
command = ":SOUR:IOSC PRI;:SOUR:VOLT "+ str(voltage)
inst.write(command)
error_info = inst.query(":SYST:ERR?")
print(error_info)

#set filter
auto = False
slope = 24  # slope= 6, 12, 18, 24
TC    = 0.5   #time constant

if (auto == True):
    command = ":FILT:AUTO:ONCE"
else:
    command = ":FILT:SLOP " + str(slope)
    command = command + ";" + ":FILT:TCON " + str(TC)
inst.write(command)
error_info = inst.query(":SYST:ERR?")
print(error_info)

#read data
if ( self.inst.query(":DATA?") != "19" ): self.inst.write(":DATA 19")
data = inst.query(":FETC?")  #Queries latest measurement data
print(data)
 
inst.close() #close visa

```

