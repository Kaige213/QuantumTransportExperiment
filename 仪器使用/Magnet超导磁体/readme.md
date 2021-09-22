## Magnet (VRM)

实验中使用VRM软件控制超导磁体，需要下载安装Labview2009_runtime_engine来运行VRM（下载网址： http://www.ni.com/en-us/support/downloads/software-products/download.labview.html#306223）版本：2009 SP1， 32-bit，注意超导磁体的控制软件VRM不能在64-bit的runtime engine上运行，所以只能下载32-bit的runtime engine。VRM是用labview语言写的，而且应该是编译好了的，所以需要安装runtime_engine。有了它，就可以直接运行被编译的VI程序了，如果是源码，可能就只能用Labview来打开了。（上面是我自己粗浅的理解，可能有误，但有一点是明确的，那就是：不慌！反正runtime_engine也是公开免费软件，放心使用！）

<img src=".\VRM.PNG" style="zoom:50%;" />

#### 如何使用

在Simulation模式下，用户可以随意操作软件，不会影响到超导磁体。也可以将该软件拷贝到其他电脑上，熟悉其功能。在我们实验中，只用到如下几个功能：

- 确定目标磁场：
  - 坐标系：只使用Cartesian坐标系，不用另外两个
  - 坐标值：只在Z方向施加磁场，XY方向始终为0

- 改变磁场的方式（Sweep Mode）：
  - As fast as possible 
  - Specify rate overall （同时设定扫描速度：sweep rate (T/min) ）
  - Specify time to setpoint（没有使用）

- 是否 Persistent on completion。如果是扫描磁场，需要不停地改变磁场（即两次设定磁场值之间的间隔时间较短），则选否；如果在很长一段时间内，都不需要改变磁场，则选是



#### VISA

VRM采用TCP/IP与其他程序通讯

- 地址：TCPIP0::127.0.0.1::33575::SOCKET

- Note：

  - 有些命令的执行需要一定时间，如果两条命令的时间间隔太短，第二条命令可能会被忽略。在编程时尽量避免这种情况的出现。

  -  All commands are terminated by <CR><LF> 

    #似乎pyvisa默认命令结尾为\r\n，所以不用自行添加

  -  All responses are terminated by <LF>

    #需要在使用pyvisa时，设定：read_termination='\n'

  - COO、RVST、MODE、VSET这几个不能单独设置，需要在同一个命令里，一起设置

- VISA命令：

  ```python
  "READ:SYS:VRM:POC" #询问是否POC
  #在程序中，该命令用来检查VRM与测量程序通讯状态是否正常
  "SET:SYS:VRM:POC:ON"   #设置POC：是
  "SET:SYS:VRM:POC:OFF"  #设置POC：否
  "SET:SYS:VRM:COO:CART:RVST:MODE:ASAP:VSET:[0 0 0]" 
  #设置坐标系为CART，扫描方式为ASAP，目标值为0T
  "SET:SYS:VRM:COO:CART:RVST:MODE:RATE:RATE:0.2:VSET:[0 0 0]"
  #设置坐标系为CART，扫描方式为RATE，扫描速度为0.2T/min，目标值为0T
  "READ:SYS:VRM:RVST:MODE:RATE" #查询坐标系，扫描方式，扫描速度
  #程序中，不能单独设定磁场目标值，所以设定目标值前，查询坐标系，扫描方式，扫描速度然后同时设置
  "SET:SYS:VRM:ACTN:RTOS" #开始扫描磁场
  "READ:SYS:VRM:ACTN"  #查询现在状态
  #程序中，每次设定完目标磁场并执行后，当VRM状态回到IDLE时，说明命令执行完毕，磁场已经到达目标值
  ```

- 示例：

  ```python
  import visa
  import time
  
  address = "TCPIP0::127.0.0.1::33575::SOCKET"
  inst = visa.ResourceManager().open_resource(address, read_termination='\n')
  
  print( inst.query("READ:SYS:VRM:POC") )
  print( inst.query("READ:SYS:VRM:RVST:MODE:RATE") )
  print( inst.query("READ:SYS:VRM:ACTN") )
  
  inst.write("SET:SYS:VRM:POC:OFF")
  time.sleep(1)
  inst.write("SET:SYS:VRM:COO:CART:RVST:MODE:ASAP:VSET:[0 0 0.1]")
  time.sleep(1)
  inst.write("SET:SYS:VRM:COO:CART:RVST:MODE:RATE:RATE:0.2:VSET:[0 0 0.2]")
  time.sleep(1)
  inst.write("SET:SYS:VRM:ACTN:RTOS")
  inst.close()
  ```




#### LOG

- [2019.11.19] pyvisa使用socket通讯时，建立连接时的timeout大约为5s，一直没找到修改该值的方法。导致每次点击磁场对应的connect按钮时，如果不能正常连接，则会有5s的时间，程序都没有反应。所以，在Magnet_instrument类的connect 函数里，使用func_timeout函数来设定执行的时长。暂时学到func_timeout的两种使用方式：装饰器和func_timeout函数。

  参考网址：https://pypi.org/project/func-timeout/ 
  
  ```python
  import time
  from func_timeout import func_set_timeout
  from func_timeout import func_timeout
  
  @func_set_timeout(2)  #set timeout=2s
  def foo():
      print("LALALALA")
      time.sleep(4)
          
  def foo2(haha):
      print(haha)
      time.sleep(1)
      return 1
  
  start = time.time()
  try: foo()
  except: print("Time: ", time.time() - start)
  print()
  

  try: return_value = func_timeout(5, foo2, ("Hello!",)) #set timeout=5s
  except: print("Timeout!")
  print()
  
  try: return_value = func_timeout(0.5, foo2, ("Hello!",)) #set timeout=0.5s
  except: print("Timeout!")
  ```
  
- [2019.11.20] 使用func_timeout关闭pyvisa，可能会出现意想不到的错误（可能时通道或者设备被占用），导致不能正常使用。重新修改VRM的connect函数，使用socket来检查VRM是否打开，再用pyvisa来检查命令执行是否正常。示例如下

  ```python
  import visa
  import time
  import socket
  
  address = "TCPIP0::127.0.0.1::33575::SOCKET"
  start = time.time()
  try:
      #check scocket connection
      IP   = address.split("::")[1]
      PORT = int(address.split("::")[2])
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.settimeout(0.1)
      s.connect((IP, PORT))
      s.shutdown(socket.SHUT_RDWR)
      s.close()
      #check connection status    
      inst = visa.ResourceManager().open_resource(address, read_termination='\n')
      command = "READ:SYS:VRM:POC"
      return_str = inst.query(command)
      inst.close() #close visa
      if ("STAT:SYS:VRM" in return_str):print( "No error")
      else: print("Error:Magnet:connect")
  except :print( "Error:Magnet:connect")
  print("Time: ", time.time()-start)
  ```

  

