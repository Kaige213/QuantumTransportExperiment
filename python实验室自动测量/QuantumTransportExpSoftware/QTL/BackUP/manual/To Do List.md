#### ToDoList

- 问题：
  似乎原来的Labview程序，在sweepPower时，没有根据用户输入的start，stop改变N5244A的设置参数，frequence也没有改变  sweepFrequence都是对的 #因为默认是weepFrequence
    CW实验时，如果points不等于1，则CW 频率也没有根据用户改变
- 添加data_toSave用来保存数据

- SR830 的量程应该根据输入信号来作相应的更改；
- 需要测试N5244A_isntrument.py
- 根据是否随机，来判断是否读取锁相放大器的值