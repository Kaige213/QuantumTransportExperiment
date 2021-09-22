import numpy as np
import pyqtgraph as pg
import random

#example 2
plt = pg.plot()
for n in range(2):
  color = [random.randint(0,255) for n in range(3)] #rgb color code
  pen   = pg.mkPen(color=color)

  y_vec = np.random.normal(size=10)
  x_vec = np.linspace(0,1,10)
  curve = pg.PlotCurveItem(pen=pen)
  curve.setData(x=x_vec, y=y_vec)
  plt.addItem(curve)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()