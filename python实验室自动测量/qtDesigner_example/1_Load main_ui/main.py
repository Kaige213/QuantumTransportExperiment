from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore

class Ui(QtWidgets.QMainWindow):
  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('main.ui', self)


#===============================================================================
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
