from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from controlInstrument_dialog import controlInstrument_dialog

class Ui(QtWidgets.QMainWindow):

  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('main.ui', self)
    self.control_action.triggered.connect(self.popUp_controlInstrument_dialog)

  #=============================================================================
  def popUp_controlInstrument_dialog(self):
    self.controlDialog = controlInstrument_dialog()
    #forbidden main window
    self.controlDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    self.controlDialog.show()

#===============================================================================
if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()
