## 电脑设置

- 下载并安装：AgilentConnectionExpert （或者： Keysight_Instrument_Control_Bundle）

  网址：https://www.keysight.com/main/software.jspx?cc=US&lc=eng&id=2175637&pageMode=CV

  <img src=".\figures\agilentConnectionExpert.PNG" style="zoom:25%;" />

  **Log**：本次安装AiglentConnectionExpert时，始终报错，让我关闭AiglentConnectionExpert再尝试安装。然而电脑刚重置，并没有这个软件。所以选择安装Keysight_Instrument_Control_Bundle 。这个软件提供了三个模块(IO Libraries Suite、Command Expert、BenchVue)，只需要安装第一个模块（如下图）。安装过程中，一直点击下一步即可（即采用默认安装）。

  <img src=".\figures\keysightInstrumentControlBundle.PNG" style="zoom:50%;" />

  **Note**：至此，已经可以使用USB线来实现仪器与电脑之间的通讯（如果实验仪器支持USB通讯接口）。步骤如下：

  - 用USB线连接实验仪器与电脑。注意这里使用的USB线与常规数据线不一样，如下图。方头连接实验仪器，矩形一端连接电脑。

    <img src=".\figures\usb.png" style="zoom:100%;" />

  - 打开KeysightConnectionExpert软件，在软件左边应该可以看到所连接的仪器，仪器图标的右上角有一个绿色的勾，表示与仪器的通讯状态良好。点击该仪器，再点击右边的 Interactive IO按钮，进入VISA命令输入界面。在该界面里，可以测试仪器的VISA命令，比如下图中的 "*IDN?"（这是一个通用命令），点击Send & Read，如果没有报错并得到正确的返回值，说明通讯顺利。仪器说明书上会提供全部的VISA命令，但一般实验中只会用到一小部分功能，测试一下这部分命令，然后记下来，后面会在Python或Labview中使用这些命令（字符串）。

    <img src=".\figures\interactiveIO.PNG" style="zoom:31.7%;" />

    <img src=".\figures\commandTest_USB.PNG" style="zoom:52%;" />



- 下载安装ni-488.2 （本次安装的是18.5版本）

  这个驱动是为了使用GPIB-USB线（免费软件，直接在ni官网上下载）。实验室使用GPIB线来实现电脑与仪器之间的通讯，而电脑端没有GPIB的接口，所以需要GPIB转USB连接线（如下图）。这个转接线还挺贵的，建议直接使用USB或者网线来连接电脑与仪器，现在的仪器大多支持USB和网线，一些仪器甚至不再支持GPIB通讯。

  <img src=".\figures\gpib_usb.PNG" style="zoom:50%;" />

  **Note**：

  - 将转接线连接电脑和实验仪器（USB端连电脑，GPIB端连接仪器），打开AgilentConnectionExpert软件，点击刷新，即可看到被连接的实验仪器。点击刷新时，转接线上的指示灯会闪烁，刷新完毕后为常亮黄色。

  - 如果硬件连接，驱动安装都正确，则点击刷新就会自动出现被连接的仪器，不需要点Add按钮自行添加。初次连接可能不会马上出现，可以尝试重复刷新或重启电脑。

  - 下面图中，"GS210, YOKOGAWA"表示仪器名及制造商，"GPIB0::1::INSTR"表示VISA地址，在后面的pytohn或labview中会使用到该地址（字符串）。可以在仪器端修改该地址（即修改数字1）。以GS210为例，"UTILITY" -> "Remote I/F" -> "GPIB" -> "Adrs 1" ->（修改地址）。查看VISA地址："UTILITY" -> "Remote I/F" -> "VISA Info" -> (GPIB : ... , USB : ...)。一般仪器前面板上有"UTILITY"按钮，VISA地址相关选项都在这儿。

  - 与USB通讯一样，在ConnectionExpert中，点击Interactive IO，进入VISA命令输入面板。可以在这里测试需要使用到的VISA命令。在下面第二张图中，以GS210电压源为例，测试了三个命令

    1. ":SOUR:FUNC VOLT;RANG 1"  #设置仪器GS210为电压输出，输出最大值为1V
    2. ":SOUR:LEV 0.5"   #设置仪器GS210输出电压0.5V
    3. ":OUTP ON"          #输出电压，前面板的output按钮变红，表示有电压输出

    <img src=".\figures\gpib_connection.PNG" style="zoom:50%;" />

    <img src=".\figures\gs210_command_test.PNG" style="zoom:100%;" />

- 下载安装NI DAQmx（本次安装版本为18.5）（下载网址： https://www.ni.com/en-us/support/downloads/drivers/download.ni-daqmx.html#288283 ）

  实验室要使用NI采集卡（PCI6289/PCI6230）所以需要安装该软件，如果使用其他设备，可能不需要安装。

  **Log**：装上该软件后，插入采集卡PCI6289，发现在NIMAX软件中不能正常使用PCI6289设备。经过多次卸载安装的尝试，发现：应该先插入采集卡，再安装NI DAQmx软件，最后软件才能正确识别该设备（原因不明）。PCI6289的基本使用方法以及如何在NI DAQmx / Python 中使用该设备，见文件夹中的instrument/NI 6289。

- 下载安装Labview2009_runtime_engine（下载网址： http://www.ni.com/en-us/support/downloads/software-products/download.labview.html#306223）

  **Note**：版本：2009 SP1， 32-bit，注意超导磁体的控制软件VRM不能在64-bit的runtime engine上运行，所以只能下载32-bit的runtime engine。实验室使用的牛津仪器公司出的超导磁体，控制软件VRM是用labview语言写的，而且应该是编译好了的，所以需要安装runtime_engine。有了它，就可以直接运行被编译的VI程序了，如果是源码，可能就只能用Labview来打开了。（上面是我自己粗浅的理解，可能有误，但有一点是明确的，那就是：不慌！反正runtime_engine也是公开免费软件，放心使用！）

  <img src=".\figures\VRM.PNG" style="zoom:40%;" />

- 下载安装python（本次是：python3.7）

  win+R -> cmd 进入windows的终端，用pip安装必要的库：

  - ```bash
    pip install --upgrade pip #更新pip
    #设置为清华源，下载速度快
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    ```
  
  - pip install numpy
  - pip install pyqt5          #测试程序使用pyqt5搭建图形化界面
  - pip install PyVISA 
  -  pip install nidaqmx   # Contains a Python API for interacting with NI-DAQmx 
  -   pip install PyVISA-py
  

**Log**：

- 下图是我写的测试程序，构建过程见相应文档（过程挺好玩的，哈哈）。

<img src=".\figures\myMeasureProgram.PNG" style="zoom:50%;" />



- 下载安装python编辑器：thonny（一款轻量级编辑器，使用非常方便）

  thonny自带了python解释器，可以修改为自己安装python3.7：

  Run -> Interpreter -> Alternative Python ... -> ...

  ([2020.3.23] 更新: thonny自带的解释器以及库函数管理功能其实挺好用的，不用修改)

- 下载安装qt-designer

- 下载安装bandzip（一款好用的压缩/解压软件）



## Tips

- 有的台式机没有无线网卡，使用网线可能不方便，这里推荐一款随身无线网卡：水星USB无线网卡（免驱动版）。插上主机usb，点击安装自带的WiFi驱动。
- 禁止windows的shift键切换中英输入法（编程时需要用shift切换英文大小写），并修改默认输入为英文：
  1.在电脑屏幕右下角的【任务设置栏】中找到输入法【中/英】，点右键然后选【设置】
  2.在【设置】中点选【按键】
  3.在【按键】中将【中/英文模式切换】下面的【shift】改成【无】
  4.设置->常规，将默认输入语言改为英文
- 在sublime text3 中运行 python：
  1. 到sublime官网上下载sublime text3，并安装
      #安装时，注意勾选Add to explorer context menu，这样Sublime Text可以被添加到右键中，在右键单击文件时，可以直接使用Sublime Text打开
  2. 到python官网下载python，并安装
      #在安装的界面给Add Python 3.x To Path前面打上对号
      #安装完成时，Win+R → 输入cmd → Enter → 调出来命令行，输入python确认安装是否成功（即在windows的终端中查看python是否为可运行的程序）
  3. sublime运行python文件的设置:
      3.1 打开sublime  → Preferences → Browse Packages (即打开对应的文件夹)
      3.2 打开Python文件夹（如果没有，自行创建） → 创建文件：Python.sublime-build → 将下面的代码粘贴到该文件（如果该文件已经存在，则内容全部替换）：
  {
  "cmd":["python.exe", "-u", "$file"],
  "path":"C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python37",  //注意：路径根据自己的python安装路径而定
  "file_regex": "^[ ]File "(...?)", line ([0-9]*)",
  "selector": "source.python"
  }
      3.3 点击菜单栏中的工具 —> 编译系统，勾选Python即可
      3.4 创建hello.py文件，Ctrl+S保存文件，Ctrl+B执行文件，查看执行结果
- 如何查看python的安装地址：打开python的终端，依次输入：import sys；sys.path #即可显示python的安装位置
- 注意PCI-6289插入电脑后，需要重启电脑才能被识别
- 将记事本的字体改为Consolas，这样用记事本打开数据文件时，数据整齐排列（Note：因为在我自己写的软件中，保存数据时，每个数据占据的字符数是相同的）。
-  VISA close releases the resource, VISA clear clears the buffers but keeps the session going 

