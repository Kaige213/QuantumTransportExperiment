from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from measureInstrument_dialog import measureInstrument_dialog

class Ui(QtWidgets.QMainWindow):

  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('main.ui', self)
    self.measure_action.triggered.connect(self.popUp_measureInstrument_dialog)

  #=============================================================================
  def popUp_measureInstrument_dialog(self):
    self.measureDialog = measureInstrument_dialog()
    #forbidden main window
    self.measureDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    self.measureDialog.show()
    
#===============================================================================
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
