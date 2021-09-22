## GS210

#### 手动操作

（根据前面板的文字提示就能知道的操作就不在这儿累述，比如：量程选择，电压选择，OUPUT等）

- 设置GPIB地址：

  UTILITY ->  Remote I/F ->  GPIB -> Adrs 1 -> （设置）

- 查看GPIB地址：

  UTILITY ->  Remote I/F ->  GPIB -> VISA Info

- 查看错误信息：

  UTILITY ->  Error  Log 

- 清除错误信息：

  UTILITY ->  Error Log -> Clear



#### VISA

示例：

```python
import visa
import time

address = "GPIB0::1::INSTR"
inst = visa.ResourceManager().open_resource(address, read_termination='\n')

print("Instrument Info: ", inst.query("*IDN?") )
inst.write(":SOUR:FUNC VOLT;RANG 1")   #设置仪器为电压源，最大值为1V
inst.write(":SOUR:FUNC VOLT;LEV 0.1;:OUTP ON") #设置仪器为电压源，值为0.1，并执行
print("Output Voltage: ", float(inst.query(":SOUR:LEV?"))) #查询输出电压
print(inst.query(":SYST:ERR?")) #查询错误信息，并清空仪器的错误信息

inst.close()  #关闭VISA
```



#### Log

- [2019.11.17] 在本次测试中，右边两个输出端口（上红下黑）输出正确的电压。下面两个黑色的输出端口电势并不相等（存在电压）