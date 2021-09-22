from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore

import numpy as np
import pyqtgraph as pg
import random

class Ui(QtWidgets.QMainWindow):
  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('example3.ui', self)
    
    #set pyqtgraph
    self.pyqt_graph.setLabel('bottom', 'xLabel', units='B')
    self.pyqt_graph.setLabel('left', 'yLabel', units='V')
    self.pyqt_graph.showGrid(x=True, y=True, alpha=0.4)
    
    #to store curves
    self.curvesInFigure = []

    
  def action_definition(self):
    self.addCurve_pushButton.clicked.connect(self.add_curve)
    self.addPoint_pushButton.clicked.connect(self.add_point)
    self.deleteCurve_pushButton.clicked.connect(self.delete_curve)
    
  def add_curve(self):
    color = [random.randint(0,255) for n in range(3)] #rgb color code
    pen   = pg.mkPen(color=color)
    curve = pg.PlotCurveItem(pen=pen)
    self.pyqt_graph.addItem(curve)
    self.curvesInFigure.append(curve)
    #set data
    x_vec = np.linspace(1,10,10)
    y_vec = np.random.normal(size=(10))
    curve.setData(x=x_vec, y=y_vec)
  
  def add_point(self):
    curve = self.curvesInFigure[-1]
    [x_vec, y_vec] = curve.getData() #get old data
    #or: [x_vec, y_vec] = self.curvesInFigure[-1].getData() #get old data
    x_vec = np.append(x_vec, x_vec[-1]+1)
    y_vec = np.append(y_vec, np.random.random())
    self.curvesInFigure[-1].setData(x=x_vec,y=y_vec)

  def delete_curve(self): 
    curve = self.curvesInFigure[0]
    self.pyqt_graph.removeItem(curve)
    #or: self.pyqt_graph.removeItem(self.curvesInFigure[0])
    del self.curvesInFigure[0]

#===============================================================================
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.action_definition()
    window.show()
    app.exec_()
