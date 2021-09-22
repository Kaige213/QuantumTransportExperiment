#### MainWindow

```python
sweepParameters_widgetsPorts = {
    'GS610R': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x0859B440>, 
        'start': <PyQt5.QtWidgets.QLineEdit object at 0x0859B6C0>, 
        'loop': <PyQt5.QtWidgets.QComboBox object at 0x0859B710>, 
        'stop': <PyQt5.QtWidgets.QLineEdit object at 0x0859B760>, 
        'current': <PyQt5.QtWidgets.QLineEdit object at 0x0859B7B0>, 
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x0859B800>, 
        'step': <PyQt5.QtWidgets.QLineEdit object at 0x0859B850>}, 
    'GS610L': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x0859B490>, 
        'start': <PyQt5.QtWidgets.QLineEdit object at 0x0859BD50>, 
        'loop': <PyQt5.QtWidgets.QComboBox object at 0x0859BDA0>, 
        'stop': <PyQt5.QtWidgets.QLineEdit object at 0x0859BDF0>, 
        'current': <PyQt5.QtWidgets.QLineEdit object at 0x0859BE40>, 
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x0859BE90>, 
        'step': <PyQt5.QtWidgets.QLineEdit object at 0x0859BEE0>}, 
    'GS210': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x0859B4E0>, 
        'start': <PyQt5.QtWidgets.QLineEdit object at 0x0859BB20>, 
        'loop': <PyQt5.QtWidgets.QComboBox object at 0x0859BB70>, 
        'stop': <PyQt5.QtWidgets.QLineEdit object at 0x0859BBC0>, 
        'current': <PyQt5.QtWidgets.QLineEdit object at 0x0859BC10>, 
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x0859BC60>, 
        'step': <PyQt5.QtWidgets.QLineEdit object at 0x0859BCB0>}, 
    'Magnet': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x0859B530>,
        'start': <PyQt5.QtWidgets.QLineEdit object at 0x0859B8F0>,
        'loop': <PyQt5.QtWidgets.QComboBox object at 0x0859B940>,
        'stop': <PyQt5.QtWidgets.QLineEdit object at 0x0859B990>,
        'current': <PyQt5.QtWidgets.QLineEdit object at 0x0859B9E0>,
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x0859BA30>,
        'step': <PyQt5.QtWidgets.QLineEdit object at 0x0859BA80>},
    'Time': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x0859B580>,
        'start': <PyQt5.QtWidgets.QLineEdit object at 0x0859BF80>,
        'loop': <PyQt5.QtWidgets.QComboBox object at 0x085E9030>,
        'stop': <PyQt5.QtWidgets.QLineEdit object at 0x085E9080>,
        'current': <PyQt5.QtWidgets.QLineEdit object at 0x085E90D0>,
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x085E9120>,
        'step': <PyQt5.QtWidgets.QLineEdit object at 0x085E9170>},
    'sweepBack': {
        'ifRun': <PyQt5.QtWidgets.QCheckBox object at 0x085E9260>, 
        'points': <PyQt5.QtWidgets.QLineEdit object at 0x085E91C0>}
}

figurePorts = {
    'LI5650X': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x08528AD0>,
    'LI5650Y': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x08528C10>,
    'LI5650R': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0ACAB3F0>, 
    'LI5650Theta': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0ACAB3A0>,
    'SR830X': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4C3B70>,
    'SR830Y': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4C3B20>,
    'SR830R': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4DA350>,
    'SR830Theta': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4DA300>,
    'N5244AX': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4F1AD0>,
    'N5244AY': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C4F1A80>,
    'N5244AR': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C5062B0>,
    'N5244ATheta': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C506260>,
    'N5244ANyquist': <pyqtgraph.widgets.PlotWidget.PlotWidget object at 0x0C51EA30>
}
```

#### MainWindow Parameters

```python
configureParameters = {
    'other': {
        'waitingTime': 0.01,
        'unit': 's'}, 
    'LI5650': {
        'ifRun': True, 
        'address': 'TCPIP0::127.0.0.1::33564::SOCKET', 
        'voltage': 1.0, 
        'frequency': 17.7, 
        'referenceSignal': 'REF IN', 
        'signalInput': 'I', 
        'filterSlope': '24 dB', 
        'timeConstant': 1.0, 
        'auto': True, 
        'unit': 'V'}, 
    'SR830': {
        'ifRun': True, 
        'address': 'TCPIP0::127.0.0.1::33565::SOCKET', 
        'voltage': 1.0, 
        'frequency': 17.7, 
        'phase': 0.0, 
        'unit': 'V'}, 
    'N5244A': {
        'ifRun': True, 
        'address': 'TCPIP0::127.0.0.1::33566::SOCKET',
        'sweepType': 'CW', 
        'CW_frequence': 1.0,
        'CW_ifPowerOn': True,
        'CW_power': -10.0,
        'power_points': 10000,
        'power_frequence': 1.0,
        'power_start': -10.0,
        'power_stop': 0.0,
        'frequence_points': 1001,
        'frequence_power': -10.0,
        'frequence_ifPowerOn': True,
        'frequence_start': 1.0,
        'frequence_stop': 2.0,
        'ifAverage': False,
        'averagingFactor': 1,
        'IF_BW': 10.0}, 
    'GS610R': {
        'range': '2 V',
        'address': 'TCPIP0::127.0.0.1::33560::SOCKET',
        'unit': 'V'}, 
    'GS610L': {
        'range': '110 V',
        'address': 'TCPIP0::127.0.0.1::33561::SOCKET',
        'unit': 'V'}, 
    'GS210': {
        'range': '10 V',
        'address': 'TCPIP0::127.0.0.1::33562::SOCKET',
        'unit': 'V'}, 
    'Magnet': {
        'sweepMode': 'As Fast As Possible',
        'rate': 0.1,
        'address': 'TCPIP0::127.0.0.1::33563::SOCKET',
        'ifPOC': False,
        'unit': 'T'}, 
    'Time': {
        'address': 'GPIB0::5::INSTR',
        'unit': 's'}
}

runningParameters = {
    'GS610R': {
        'ifRun': True,
        'start': 0.0,
        'loop': '1->',
        'stop': 1.0,
        'current': 0,
        'points': 3,
        'step': 0.1}, 
    'GS610L': {
        'ifRun': True,
        'start': 0.0,
        'loop': '2->',
        'stop': 2.0,
        'current': 0,
        'points': 3,
        'step': 0.2}, 
    'GS210': {
        'ifRun': True,
        'start': 0.0,
        'loop': '3->',
        'stop': 3.0,
        'current': 0,
        'points': 11,
        'step': 0.3}, 
    'Magnet': {
        'ifRun': True,
        'start': 0.0,
        'loop': '4->',
        'stop': 4.0,
        'current': 0,
        'points': 3,
        'step': 0.4}, 
    'Time': {
        'ifRun': True,
        'start': 0.0,
        'loop': '=',
        'stop': 0.0,
        'current': 0,
        'points': 1,
        'step': 0.0}, 
    'sweepBack': {
        'ifRun': True,
        'points': 3}
}

saveConfigure = {
    'folderPath': 'F:/Data/13',
    'ifSave': True, 
    'log': 'Test Log'
}
```



#### Curves

```python
[
    {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919350>, 
     'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9193A0>, 
     'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919440>, 
     'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9193F0>, 
     'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919490>, 
     'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919530>, 
     'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9194E0>, 
     'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9195D0>, 
     'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919580>, 
     'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919620>, 
     'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919670>, 
     'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919710>, 
     'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919260>}, {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9197B0>, 'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9192B0>, 'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919EE0>, 'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919120>, 'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919B70>, 'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919990>, 'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919D00>, 'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9198F0>, 'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919DF0>, 'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919BC0>, 'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919850>, 'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E9190D0>, 'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E919A80>}, {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC311C0>, 'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31210>, 'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC312B0>, 'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31260>, 'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31300>, 'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31350>, 'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC313A0>, 'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC313F0>, 'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31440>, 'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31490>, 'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC314E0>, 'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31530>, 'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31580>}, {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC319E0>, 'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC317B0>, 'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31760>, 'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31620>, 'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC315D0>, 'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31A80>, 'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31D00>, 'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31170>, 'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31A30>, 'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31D50>, 'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31030>, 'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31940>, 'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31670>}, {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740300>, 'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x017403A0>, 'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740350>, 'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740440>, 'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x017403F0>, 'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x017404E0>, 'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740490>, 'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740530>, 'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x017405D0>, 'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740580>, 'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740620>, 'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740670>, 'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x01740710>}, {'LI5650X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC318F0>, 'LI5650Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31BC0>, 'LI5650R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31C10>, 'LI5650Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0D3DEC10>, 'SR830X': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31EE0>, 'SR830Y': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0D3DE670>, 'SR830R': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0D3DEBC0>, 'SR830Theta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E8C9D50>, 'N5244AX': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E8C90D0>, 'N5244AY': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E8C9800>, 'N5244AR': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0E8C9BC0>, 'N5244ATheta': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC31DA0>, 'N5244ANyquist': <pyqtgraph.graphicsItems.PlotCurveItem.PlotCurveItem object at 0x0EC310D0>}]
```





#### measureThread.py

```python
controlInstrument_sortedByLoop = [
    {'instrument': 'GS610R',
     'address': 'TCPIP0::127.0.0.1::33560::SOCKET',
     'unit': 'V',
     'vector': [0.0, 0.5, 1.0, 1.0, 0.5, 0.0]},
    {'instrument': 'GS610L',
     'address': 'TCPIP0::127.0.0.1::33561::SOCKET',
     'unit': 'V',
     'vector': [0.0, 1.0, 2.0]},
    {'instrument': 'GS210',
     'address': 'TCPIP0::127.0.0.1::33562::SOCKET',
     'unit': 'V',
     'vector': [0.0, 1.5, 3.0]},
    {'instrument': 'Magnet',
     'address': 'TCPIP0::127.0.0.1::33563::SOCKET',
     'unit': 'T',
     'vector': [0.0, 2.0, 4.0]},
    {'instrument': 'Time',
     'address': 'GPIB0::5::INSTR',
     'unit': 's',
     'vector': [0.0]}
]

control_record = [
    {'instrument': 'GS610R', 'loopState': 0, 'unit': 'V', 'value': 0.0},
    {'instrument': 'GS610L', 'loopState': 0, 'unit': 'V', 'value': 0.0},
    {'instrument': 'GS210', 'loopState': 0, 'unit': 'V', 'value': 0.0},
    {'instrument': 'Magnet', 'loopState': 0, 'unit': 'T', 'value': 0.0},
    {'instrument': 'Time', 'loopState': 0, 'unit': 's', 'value': 0.0}] 

measure_record = [
    {'name': 'LI5650X', 'unit': 'V', 'value': 3.0},
    {'name': 'LI5650Y', 'unit': 'V', 'value': -2.4492935982947064e-16},
    {'name': 'SR830X', 'unit': 'V', 'value': 3.0},
    {'name': 'SR830Y', 'unit': 'V', 'value': -2.4492935982947064e-16},
    {'name': 'N5244AX', 'unit': 'U', 'value': 3.0},
    {'name': 'N5244AY', 'unit': 'U', 'value': -2.4492935982947064e-16},
    {'name': 'N5244AR', 'unit': 'dB', 'value': 3.0},
    {'name': 'N5244ATheta', 'unit': 'Deg', 'value': -4.677806199023251e-15},
    {'name': 'X_axis', 'unit': '', 'value': 0.0}]
```



#### dataConvert.py

```python
data_toPlot = [
    {'varName': 'LI5650X', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650X (V)'}, 
    {'varName': 'LI5650Y', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650Y (V)'}, 
    {'varName': 'LI5650R', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650R (V)'}, 
    {'varName': 'LI5650Theta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650Theta (Deg)'}, 
    {'varName': 'SR830X', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830X (V)'}, 
    {'varName': 'SR830Y', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830Y (V)'}, 
    {'varName': 'SR830R', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830R (V)'}, 
    {'varName': 'SR830Theta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830Theta (Deg)'}, 
    {'varName': 'N5244AX', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AX (U)'}, 
    {'varName': 'N5244AY', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AY (U)'}, 
    {'varName': 'N5244AR', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AR (dB)'}, 
    {'varName': 'N5244ATheta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244ATheta (Deg)'}, 
    {'varName': 'N5244ANyquist', 'X': 3.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'N5244AX (U)', 'ylabel': 'N5244AY (U)'}]

data_toSave = [
    {'varName': 'LI5650X', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650X (V)'},
    {'varName': 'LI5650Y', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650Y (V)'},
    {'varName': 'LI5650R', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650R (V)'},
    {'varName': 'LI5650Theta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'LI5650Theta (Deg)'},
    {'varName': 'SR830X', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830X (V)'},
    {'varName': 'SR830Y', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830Y (V)'},
    {'varName': 'SR830R', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830R (V)'},
    {'varName': 'SR830Theta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'SR830Theta (Deg)'}, 
    {'varName': 'N5244AX', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AX (U)'},
    {'varName': 'N5244AY', 'X': 0.0, 'Y': -2.4492935982947064e-16, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AY (U)'},
    {'varName': 'N5244AR', 'X': 0.0, 'Y': 3.0, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244AR (dB)'},
    {'varName': 'N5244ATheta', 'X': 0.0, 'Y': -4.677806199023251e-15, 'xlabel': 'GS610R(V)', 'ylabel': 'N5244ATheta (Deg)'}
]
```

