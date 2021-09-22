( 这玩意儿一点都不好写，现在写了一个粗糙的，以后有缘再更新。根据后期维护程序时，使用该文档的感受，来调整文档 2019.11.1)

#### 原则

- 尽量让代码局部合理/可读，避免为了让程序的一个地方代码简洁，而在另一个地方出现不易理解的代码的情况。

- 希望确定好准则，并定义好接口，然后后期维护时，需要阅读的代码、考虑的细节尽量少

  

#### 软件使用

##### 可能遇到的问题

- 测量开始后点击stop没有反应，可能是磁场或N5244A还没执行完。

  解决办法：等待其操作完成，或者直接关闭程序

- 如果打开软件，发现全部（或部分）的参数输入框都是空的，说明parameters_initiate.json文件缺失，或者被损坏，导致软件初始化出现问题。软件可以打开，但不能使用。
  解决方法：打开BackUp/defaullValueProduce.py，同时打开软件，根据软件界面内的输入框，将其对应的值写到defaullValueProduce.py中（即定义下面三个dict: configureParameters, runningParameters, saveConfigure），并执行defaullValueProduce.py，生成parameter_initiate.json文件，然后将该文件放到main.py相同目录下，关闭软件，再次打开。注意，所有输入参数都必须有定义。

##### Configure (menu bar):

- 每个仪器对应一个connect按钮。每次弹出设置对话框时，绿色表示该仪器与电脑连接成功，灰色表示连接失败，需要检查硬件连接，或者GIPB地址是否正确。排除所有错误后，再次点击connect按钮，如果按钮变成绿色，表示连接成功；



#### 测量数据的处理

（从measureThread中返回 control_record 和 measure_record后，主进程对这些数据的处理流程）

1. 得到一个测量数据点后，主进程将control_record 和 measure_record传入afterStart.getOnePoint();

2. afterStart.getOnePoint() 调用 dataConvert.dataConvert() 将control_record 和 measure_record转换为 dataToPlot （type：list），这样做是为了方便绘图，dataToPlot中的"varName"对应主进程中的绘图端口。

3. 得到dataToPlot后，需要判断该数据点是否属于新的曲线（or：新的数据文件）。判断条件有三个：

   a. `type(dataToPlot[0]["X"]) == list`（即实验中用到了N5244A的sweepPower or sweepFrequency）; 

   b. `control_record[0]["loopState"] == 0`;

   c. `control_record[0]["loopState"] == points_forward` （这里的points_forward指loop1的控制仪器正扫的点数，如果这里的条件成立，表示loop1的控制仪器正扫结束，已经开始回扫，数据点属于新的曲线）

4. 如果数据点属于回扫，我们需要将`control_record[0]["loopState"]`的值减去正扫的点数，才能得到正确回扫状态值

   ```python
   control_record[0]["loopState"] = control_record[0]["loopState"] - points_forward
   ```

5. 如果数据点属于新的曲线，afterStart.getOnePoint()将调用afterStart.newCurve()。afterStart.newCurve()的功能：

   a. curveInFigure和curveInStore中添加一条曲线（pyqtgraph curve）

   b. 生成新的数据文件名，并将该文件名当作attribute添加到curve中（因为每组曲线与数据文件一一对应，除了Nyquist图）；

   c. 在新文件中保存描述文字，包括时间，扫描参数，数据变量名

6. afterStart.getOnePoint()将数据保存到数据文件中

7. afterStart.getOnePoint()更新主界面中的曲线，即把数据添加到curve中

8. afterStart.getOnePoint()更新主界面的sweepParametersFrame中的current值，用来表示参数空间的扫面状态

9. Done！

**Note**：

1. N5244A的Nyquist图没有数据文件对应；

2. N5244A的sweepFrequence和sweepPower扫描模式非常特殊，因为一次测量就得到一条曲线以及一个数据文件，而且x值不是loop1的控制仪器对应的控制状态；

3. 如果有回扫，loop1仪器的扫描空间是将正扫回扫连接到一起，成为一个一维数组。所以如果数据点属于回扫，loop1的loopState需要减去正扫点数

   ```python
   #在measureThread.py中:
   ...
   self.controlInstrument_sortedByLoop[0]["vector"] = list(np.append(vector_forward,vector_backward))
   ...
   ```




#### Parameters Input

- loop="="的设备，points=1

- 需要向lineEdit控件输入数字用于显示时，将浮点数转化为单精度再放到控件中。因为由于二进制与十进制转换问题，有时会出现一些特别长的数字。如下例：

  ```python
  import numpy as np
  print( 0.3 / 3 )
  print( np.float32(0.3 / 3) )
  ```

  **Output: **

  ```python
  0.09999999999999999
  0.1
  ```




#### UI

- control_dialog.ui, measure_dialog.ui 在qt-designer中创建时，没有使用带ok&cancel按钮的对话框，因为ok&cancel按钮被默认连接到self.accept()和self.reject()，而我们需要在关闭对话框的同时读取用户的输入参数，如果重写self.accept()，又会影响到QMessageBox()的使用（用户输入错误时，弹出该提示框），因为QMessageBox()的关闭也会使用到self.accept()。所以，我们的两个对话框的ok&cancel按钮是重新用pushButton创建的，并选择ok按钮为default（Property Editor最后面的几个选项，autoDefault后面那个选项），作用是，按回车，ok按钮相应，并退出对话框。[不够后来没有使用ok&Cancel按钮了]
- 在ubuntu中使用qt-designer，如果想要在窗口内添加menubar，需要将native menubar选为false，否则，menubar 会出现在ubuntu默认的桌面左上角；

#### measureThread

- 设备loop="="与设备loop="1->"（以及其他）没有区别对待，仅仅在对instrument进行排序时，设置了它们扫描的先后循序（如果有多台设备满足loop="="，实际上没有一个明确的标准来对它们进行排序，因为这些设备只会在实验的初期被执行一次。只要在数据文件名中，它们的先后顺序保持一致即可）

- 参数空间中的每一个点对应一次实验，一次测量，一次数据记录，一次主界面的刷新，一次while循环



#### 数据保存

- 文件名中的ID是为了方便数据处理时，程序区分并读取数据文件，ID后面的内容是为了方便实验人员了解对应的实验内容；
- ID的顺序是为了在文件夹中显示数据文件时，它们的顺序与实验测量时的顺序保持一致；

- 生成数据文件名时，首先生成该文件的ID，并查看目标目录下该ID是否已经存在。如果存在，则ID中最后一个数字加一，直到目标目录下没有重复ID，由此得到新文件的ID。所以，程序中只查看ID是否存在，并非全部文件；
- 数据文件中，每列数据占用的字符数是一样的，所以将windows中，记事本的字体设置为Consolas，可以等宽度显示字符，可以让数据列对齐；
- 保存数据时，使用单精度



#### setOrRead_instrument & instrument.py

- N5244A_instrument.py的返回数据始终为list，在setOrRead_instrument中会根据实验类型进行修正，但如果实验为CW，则将数据转化为float；如果实验为sweepPower/sweepFrequence，则数据类型不变，只设定单位
- N5244A: 程序中频率的单位都是GHz（除了if_bandwidth），但与仪器通讯时，频率单位都是Hz
- 程序与仪器之间的通讯，只发生在3个地方
  1. controlInstrument_dialog.py (点击Apply按钮后，根据用户输入的参数设置仪器)
  2. measureInsturment-dialog.py (点击Apply按钮后，根据用户输入的参数设置仪器)
  3. measureThread.py 中调用setOrRead_instrument.py (扫描参数空间，设置一次"控制仪器"，读取一次"测量仪器"）



#### parameters_initiate:

- 用于初始化三个dict：configureParameters, runningParameters, saveConfigure。打开程序时会使用该文件来初始化这三个量。如果该文件缺失，或损坏，软件可以打开，但不能正常使用。解决方法见bug说明。用于记录上一次的实验设置，减少重复操作。



#### Error Info

- 如果文件保存目录中已经存在`_error_.log`文件,程序会在原文件后面继续添加内容，不会生成新文件。

  

## 程序中几个重要的变量

#### main.py

- configureParameters：类型为dict，记录所有仪器的使用参数，详情见parameters_initiate.json 或者 BackUp/defaultValueProduce.py

- runningParameters：类型为dict，记录本次实验中需要使用的控制仪器，以及待扫描的参数空间，详情见parameters_initiate.json 或者 BackUp/defaultValueProduce.py

- saveConfigure：类型为dict，记录本次实验使用保存数据，数据保存的路径，用户输入的Log，详情见parameters_initiate.json 或者 BackUp/defaultValueProduce.py

- runConfigure：类型为dict，记录本次实验，figure中显示的曲线条数

- curvesInStore：类型为list，保存已经绘制以及正在绘制的曲线数据，包括figure窗口中不再显示的曲线。当用户修改“Number of Curves”，增加显示的曲线条数时，程序从该list中调取旧的曲线，将其显示在figure窗口中。但，用户点击“Clear Memory”时，程序将清理，该list中除最新一组数据外，其他所有旧的曲线数据（del curvesInStore[:-1]）。Note：该list中最后一组数据（curvesInStore[:-1]）对应figure中正在绘制的一组曲线。

  Example：curvesInStore = [... , {"LI5650X":curve1, "LI5650Y":curve2, "SR830X":curve3,...} ,...]

- curvesInFigure：类型为list，保存figure中显示的曲线数据

  Example：curvesInFigure = [... , {"LI5650X":curve1, "LI5650Y":curve2, "SR830X":curve3,...} ,...]

#### measureThread.py

- control_record：类型为list，记录当前实验的控制状态
- measure_record：类型为list，记录当前实验的测量状态
- loopState_new：类型为list



#### 添加仪器时

##### 添加控制仪器（control_instrument）:

1. 用qt-designer打开 UI/main.ui文件，在sweepParameters 框中，添加该仪器的扫描参数输入控件（checkBox，start，loop，stop，current，points，step）。并在qt-designer/Property Editor中修改控件的objectName。注意命名规则，尽量与以前的命名规则保持一致。

2. 打开user/linker.py文件，将该仪器的输入控件放到sweepParameters_widgetsPorts中。

   (主程序直接从sweepParameters_widgetsPorts中调用这些控件，不需要用户再去修改主程序的代码)

3. 用qt-designer 打开 UI/control_dialog.ui文件，添加该使用该仪器需要的设置输入框；

4. 打开user/controlInstrument_dialog.py ，添加两部分代码：a. 将该仪器相关的输入框的内容设置为上一次使用值；b. action部分 (并非所有的仪器对应的输入框都有action)；c. apply部分，即点击apply，根据用户输入，设置仪器（需要使用到communicateWithInstrument.py）

5. 打开BackUp/defaultValueProduce.py，写入该仪器的使用参数。修改完毕，运行该文件，生成parameters_initiate.json文件。目的：初始化 configureParameters 和 runningParameters 两个dict。

6. 打开 user/communicateWithInstrument.py 添加程序与仪器通讯的代码（通过pyvisa）

7. 搞定！收工！

##### 添加测量仪器（measure_instrument）:

（以N5244A网络分析仪为例）

1. 手动操作该仪器，熟悉需要使用的功能

2. 在仪器说明书上查找这些功能对应的visa命令，并在python里测试这些命令

3. 编写N5244A_instrument.py，该仪器的python class，如下所示，包含需要使用到的全部功能。注意一定要使用`if __name__ == "__main__"`。这样，N5244A_instrument.py可以单独运行，方便调试，而调用该class时，测试代码不会被执行。

   ```python
   import visa
   import time
   
   class N5244A_instrument:   
       def __init__(self, address):
           self.address = address
       def connect(self):
           do_something                
       def configure(self):
           do_somethinig        
       def set_trace(self):
           do_something        
       def initiate_and_read_data(self):
           do_something
           
   #=====================================================================
   #test
   if __name__ == "__main__":
       address = "GPIB0::5::INSTR"
       inst    = N5244A_instrument(address)
          
       #----  check connection ----
       error_info = inst.connect()
       print("Connection:", error_info)
       
       other_code
   ```

4. 用qt-designer 打开 UI/measure_dialog.ui文件，添加该使用该仪器需要的设置输入框；

5. 打开user/measureInstrument_dialog.py ，添加代码：a. 将该仪器相关的输入框的内容设置为上一次使用值并检查连接状态；b. action部分 (并非所有的仪器对应的输入框都有action)；c. apply部分，即点击apply，程序将用户的输入参数储存在configureParameters dict中，并设置仪器（需要使用到communicateWithInstrument.py）

6. 用qt-designer打开UI/main.ui文件，添加仪器对应的figure窗口

   Note：1. 修改tab标签：点击选择总tabWidget，Property中出现currentTabText，修改后面的文字；2. 设置某个子tab的layout：点击选择该tab，放入widget，在右边的Object Inspector编辑框中，选择总tab widget（注意：tab页停留在需要编辑的那一页），再点击上方的"Lay Out in a Grid"按钮。Object Inspector框中，该子tab的图标也发生相应变化；3. 通过复制粘贴添加pyqtgraph控件

 7. 打开user/setOrRead_instrument.py，添加readMeasureInstrument()函数中对应的代码，将该仪器对应的测量数据，以及错误信息放到 measurement_record，error_info_record 两个list中，注意顺序；

 8. 打开action/dataConvert.py文件，a. 将测量数据转化为figure窗口对应的绘图数据, b. 将测量数据转化为data_toSave（用于方便数据保存）

 9. 打开user/linker.py，将该仪器的pyqtgraph窗口放到figurePort中，主程序自动将data_toPlot中的数据与figurePort对应；

 10. 打开BackUp/defaultValueProduce.py，写入该仪器的使用参数。修改完毕，运行该文件，生成parameters_initiate.json文件。目的：初始化 configureParameters 和 runningParameters 两个dict。

 11. 搞定！收工！

##### 检查：

  1. 运行N5244A_instrument.py，查看得到的数据与仪器端显示的数据是否一致；
  2. 运行虚拟仪器，保存所有的figure曲线，与数据，然后对比figure数据/文本数据，与生成函数是否一致；