import numpy as np
import pyqtgraph as pg

y_vec = np.random.normal(size=10)
plt = pg.plot(y_vec)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()