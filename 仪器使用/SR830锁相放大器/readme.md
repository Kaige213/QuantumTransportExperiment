## SR830

**Note**: 

- 输入信号选择中（A, A-B, I），I(10^8) 该模式在部分情况下才能使用。实验室暂时不会使用到该功能，所以此次没有查看该模式的使用方式（2019.11.25）

- query函数实际上是先执行write()，然后执行read()。对SR830使用该函数时，返回的数据不一定对应我的命令，如下例所示：

  ```python
  import visa
  
  address = "GPIB0::8::INSTR"
  inst = visa.ResourceManager().open_resource(address, read_termination='\n')
  
  inst.write("*IDN?")
  print(inst.query("SNAP?1,2")) #读取XY值
  ```

  **Output: **

  ```python
  >>> %Run test.py
  Stanford_Research_Systems,SR830,s/n55581,ver1.07 
  ```

  程序中，print(inst.query("SNAP?1,2")) 是为了读取测量到的XY值，但实际返回的是设备信息，对应的是"*IDN?"命令。因为上一个有命令的返回值没有被输出，等到下一个read()执行时，被输出，导致错误的发生

- 由于暂时没有找到好的方法清除仪器内存，解决办法很拙劣：如下面代码，每次需要使用query()函数时，先用read()重复读取，直到没有返回值而导致timeout，退出循环。注意一定要提前设置timeout，否则等待时间会很长，默认时间大约5s左右。

  ```python
  address = "GPIB0::8::INSTR"
    inst = visa.ResourceManager().open_resource(address, read_termination='\n')
    
    inst.write("*IDN?")
    inst.write("*IDN?")
    
    inst.timeout = 100
    while True:
        try: inst.read()
        except: break
    
    data_str = inst.query("SNAP?1,2")
    print("data: ", data_str)
        
    inst.close() #close visa
  ```

  




#### VISA 示例

```python
import visa
import time

address = "GPIB0::8::INSTR"
inst = visa.ResourceManager().open_resource(address, read_termination='\n')

#check connection status
command = "*IDN?"
return_str = inst.query(command)
print("Return(*IDN?): ", return_str)

if ("SR830" in return_str):print("No error")
else: print( "Error:SR830:Connection")



#set Frequency
freq    = 12.7
command = "FREQ " + str(freq)
inst.write(command)
inst.write("PHAS 0")  #set phase

#set reference signal source
#command = "FMOD 0"
command = "FMOD 1"
inst.write(command)
 
#set signal input connector
command = "ISRC 0"
#command = "ISRC 1"
#command = "ISRC 2"
#command = "ISRC 3"
inst.write(command)
 
#set voltage
voltage = 0.11
command = "SLVL "+ str(voltage)
inst.write(command)

#read data
data_str = inst.query("SNAP?1,2")
print(data_str)
 
inst.close() #close visa
```

