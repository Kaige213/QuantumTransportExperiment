from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

class controlInstrument_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(controlInstrument_dialog, self).__init__()
        uic.loadUi('control_dialog.ui', self)

