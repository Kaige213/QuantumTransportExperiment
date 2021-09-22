from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

class measureInstrument_dialog(QtWidgets.QDialog):
    def __init__(self):
        super(measureInstrument_dialog, self).__init__()
        uic.loadUi('measure_dialog.ui', self)

