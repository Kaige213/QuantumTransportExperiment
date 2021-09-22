from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import traceback
import time

import user.instrument as instrument_class

class controlInstrument_dialog(QtWidgets.QDialog):
  def __init__(self):
      super(controlInstrument_dialog, self).__init__()
      uic.loadUi('./UI/control_dialog.ui', self)

  def setUp(self, configureParameters):
    self.configureParameters = configureParameters
    
    #=======================================================================
    #set default value according the last used value
    try:        
        #---- GS610R ----
        address = self.configureParameters["GS610R"]["address"]
        self.GS610RAddress_lineEdit.setText(address) #set address
        index = self.GS610RRange_comboBox.findText(self.configureParameters["GS610R"]["range"])
        self.GS610RRange_comboBox.setCurrentIndex(index)  #set range
        self.connection_check("GS610R")  #check connection status
        
        #---- GS610L ----
        address = self.configureParameters["GS610L"]["address"]
        self.GS610LAddress_lineEdit.setText(address) #set address
        index = self.GS610LRange_comboBox.findText(self.configureParameters["GS610L"]["range"])
        self.GS610LRange_comboBox.setCurrentIndex(index)  #set range
        self.connection_check("GS610L")  #check connection status
        
        #---- GS210 ----
        address = self.configureParameters["GS210"]["address"]
        self.GS210Address_lineEdit.setText(address) #set address
        index = self.GS210Range_comboBox.findText(self.configureParameters["GS210"]["range"])
        self.GS210Range_comboBox.setCurrentIndex(index)  #set range
        self.connection_check("GS210")  #check connection status
        
        #---- Magnet ----
        #set address
        address = self.configureParameters["Magnet"]["address"]
        self.MagnetAddress_lineEdit.setText(address)
        #set rate
        self.MagnetRate_lineEdit.setText(str(self.configureParameters["Magnet"]["rate"]))
        #set seepMode
        index = self.MagnetSweepMode_comboBox.findText(self.configureParameters["Magnet"]["sweepMode"])
        self.MagnetSweepMode_comboBox.setCurrentIndex(index)
        # if persistent on completion
        self.MagnetPOC_checkBox.setChecked( self.configureParameters["Magnet"]["ifPOC"] )
        if (self.configureParameters["Magnet"]["sweepMode"] == "As Fast As Possible"):
          self.MagnetRate_lineEdit.setDisabled(True)
        self.connection_check("Magnet")  #check connection status

    except: pass
    #=======================================================================
    #=======================================================================
    #---- action part (user) ----
    self.GS610RConnect_pushButton.clicked.connect(lambda:self.connection_check("GS610R"))
    self.GS610LConnect_pushButton.clicked.connect(lambda:self.connection_check("GS610L"))
    self.GS210Connect_pushButton.clicked.connect(lambda:self.connection_check("GS210"))
    self.MagnetConnect_pushButton.clicked.connect(lambda:self.connection_check("Magnet"))
    self.MagnetSweepMode_comboBox.currentTextChanged.connect(self.MagnetSweepMode_comboBoxChanged)

    self.apply_pushButton.clicked.connect(self.apply_clicked)
    self.exit_pushButton.clicked.connect(self.reject)

  #=============================================================================
  #-----------------------------------------------------------------------------
  def connection_check(self, instrument):
    if (instrument == "GS610R"):
        address = self.GS610RAddress_lineEdit.text()
        GS610R_instrument = instrument_class.GS610_instrument(address)
        error_info = GS610R_instrument.connect()
        if (error_info == "No error"):
          self.GS610RConnect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.GS610RConnect_pushButton.setText("ON")
        else:
          self.GS610RConnect_pushButton.setStyleSheet('background-color: None')
          self.GS610RConnect_pushButton.setText("OFF")
    elif (instrument == "GS610L"):
        address = self.GS610LAddress_lineEdit.text()
        GS610L_instrument = instrument_class.GS610_instrument(address)
        error_info = GS610L_instrument.connect()
        if (error_info == "No error"):
          self.GS610LConnect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.GS610LConnect_pushButton.setText("ON")
        else:
          self.GS610LConnect_pushButton.setStyleSheet('background-color: None')
          self.GS610LConnect_pushButton.setText("OFF")
    elif (instrument == "GS210"):
        address = self.GS210Address_lineEdit.text()
        GS210_instrument = instrument_class.GS210_instrument(address)
        error_info = GS210_instrument.connect()
        if (error_info == "No error"):
          self.GS210Connect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.GS210Connect_pushButton.setText("ON")
        else:
          self.GS210Connect_pushButton.setStyleSheet('background-color: None')
          self.GS210Connect_pushButton.setText("OFF")
    elif (instrument == "Magnet"):
        address = self.MagnetAddress_lineEdit.text()
        Magnet_instrument = instrument_class.Magnet_instrument(address)
        error_info = Magnet_instrument.connect()
        if (error_info == "No error"):
          self.MagnetConnect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.MagnetConnect_pushButton.setText("ON")
        else:
          self.MagnetConnect_pushButton.setStyleSheet('background-color: None')
          self.MagnetConnect_pushButton.setText("OFF")
  #-----------------------------------------------------------------------------      
  def MagnetSweepMode_comboBoxChanged(self):
    if (self.MagnetSweepMode_comboBox.currentText() == "As Fast As Possible"):
      self.MagnetRate_lineEdit.setDisabled(True)
    else:
      self.MagnetRate_lineEdit.setDisabled(False)
      
  #-----------------------------------------------------------------------------
  def apply_clicked(self):
    #---- save inputs to self.configureParameters ----
    try:
      #---- read parameters from input ----
      #---- GS610R state ----
      self.configureParameters["GS610R"]["range"]   = self.GS610RRange_comboBox.currentText()
      self.configureParameters["GS610R"]["address"] = self.GS610RAddress_lineEdit.text()
      
      #---- GS610L state ----
      self.configureParameters["GS610L"]["range"]   = self.GS610LRange_comboBox.currentText()
      self.configureParameters["GS610L"]["address"] = self.GS610LAddress_lineEdit.text()

      #---- GS210 state ----
      self.configureParameters["GS210"]["range"]   = self.GS210Range_comboBox.currentText()
      self.configureParameters["GS210"]["address"] = self.GS210Address_lineEdit.text()

      #---- Magnet state ----
      self.configureParameters["Magnet"]["rate"]      = float(self.MagnetRate_lineEdit.text())
      self.configureParameters["Magnet"]["sweepMode"] = self.MagnetSweepMode_comboBox.currentText()
      self.configureParameters["Magnet"]["address"]   = self.MagnetAddress_lineEdit.text()
      self.configureParameters["Magnet"]["ifPOC"]     = self.MagnetPOC_checkBox.isChecked()
      
    except ValueError:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText("Wrong Input!")
      msg.setWindowTitle("Warning!")
      msg.exec_()
      return
    #---- apply settings ----
    try:
        #---- GS610R ----
        if (self.GS610RConnect_pushButton.text() == 'ON'):
            address = self.GS610RAddress_lineEdit.text()
            GS610R_instrument = instrument_class.GS610_instrument(address)
            rng_string = self.GS610RRange_comboBox.currentText()
            rng        = float(rng_string.split()[0])
            error_info = GS610R_instrument.setRange(rng)
            if (error_info != "No error"): raise Exception('Error Occur')
        #---- GS610L ----
        if (self.GS610LConnect_pushButton.text() == 'ON'):
            address = self.GS610LAddress_lineEdit.text()
            GS610L_instrument = instrument_class.GS610_instrument(address)
            rng_string = self.GS610LRange_comboBox.currentText()
            rng        = float(rng_string.split()[0])
            error_info = GS610L_instrument.setRange(rng)
            if (error_info != "No error"): raise Exception('Error Occur')
        #---- GS210 ----
        if (self.GS210Connect_pushButton.text() == 'ON'):
            address = self.GS210Address_lineEdit.text()
            GS210_instrument = instrument_class.GS210_instrument(address)
            rng_string = self.GS210Range_comboBox.currentText()
            rng        = float(rng_string.split()[0])
            error_info = GS210_instrument.setRange(rng)
            if (error_info != "No error"): raise Exception('Error Occur')
        #---- Magnet ----
        if (self.MagnetConnect_pushButton.text() == 'ON'):
            address = self.MagnetAddress_lineEdit.text()
            Magnet_instrument = instrument_class.Magnet_instrument(address)
            #check connection status
            error_info = Magnet_instrument.connect()
            if (error_info != "No error"): raise Exception('Error Occur')
            #set sweepMode and rate
            sweepMode  = self.MagnetSweepMode_comboBox.currentText()
            rate       = float(self.MagnetRate_lineEdit.text())
            error_info = Magnet_instrument.setRvstMode(sweepMode, rate)
            if (error_info != "No error"): raise Exception('Error Occur')
            #set POC
            ifPOC      = self.MagnetPOC_checkBox.isChecked()
            error_info = Magnet_instrument.setPOC(ifPOC)
            if (error_info != "No error"): raise Exception('Error Occur')
  
    except Exception:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText(error_info)
      msg.setWindowTitle("Warning!")
      msg.exec_()
