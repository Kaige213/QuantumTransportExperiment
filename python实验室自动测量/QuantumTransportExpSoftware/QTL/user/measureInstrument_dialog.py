from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox

import user.instrument as instrument_class
import traceback
import time

class measureInstrument_dialog(QtWidgets.QDialog):
  def __init__(self):
    super(measureInstrument_dialog, self).__init__()
    uic.loadUi('./UI/measure_dialog.ui', self)

  def setUp(self, configureParameters):
    self.configureParameters = configureParameters

    #--------------------------------------------------------------------------------------
    #set default value according the last used value
    try:
        #---- set LI5650 parameters ----
        self.LI5650IfRun_checkBox.setChecked(self.configureParameters["LI5650"]["ifRun"])
        self.LI5650Address_lineEdit.setText(self.configureParameters["LI5650"]["address"])
        self.LI5650Auto_checkBox.setChecked(self.configureParameters["LI5650"]["auto"])
        self.LI5650Voltage_lineEdit.setText(str(self.configureParameters["LI5650"]["voltage"]))
        self.LI5650Frequency_lineEdit.setText(str(self.configureParameters["LI5650"]["frequency"]))
        self.LI5650TimeConstant_lineEdit.setText(str(self.configureParameters["LI5650"]["timeConstant"]))

        index = self.LI5650ReferenceSignal_comboBox.findText(self.configureParameters["LI5650"]["referenceSignal"])
        self.LI5650ReferenceSignal_comboBox.setCurrentIndex(index)
        index = self.LI5650SignalInput_comboBox.findText(self.configureParameters["LI5650"]["signalInput"])
        self.LI5650SignalInput_comboBox.setCurrentIndex(index)
        index = self.LI5650FilterSlope_comboBox.findText(self.configureParameters["LI5650"]["filterSlope"])
        self.LI5650FilterSlope_comboBox.setCurrentIndex(index)
        #---- check connection status ----    
        self.connection_check("LI5650")

        #---- set SR830 parameters ----
        self.SR830IfRun_checkBox.setChecked(self.configureParameters["SR830"]["ifRun"])
        self.SR830Address_lineEdit.setText(self.configureParameters["SR830"]["address"])
        self.SR830Voltage_lineEdit.setText(str(self.configureParameters["SR830"]["voltage"]))
        self.SR830Frequency_lineEdit.setText(str(self.configureParameters["SR830"]["frequency"]))
        self.SR830Phase_lineEdit.setText(str(self.configureParameters["SR830"]["phase"]))
        #---- check connection status ---        
        self.connection_check("SR830")
        
        #---- set N5244A parameters ----
        self.N5244AIfRun_checkBox.setChecked(self.configureParameters["N5244A"]["ifRun"])
        self.N5244AAddress_lineEdit.setText(self.configureParameters["N5244A"]["address"])
        self.N5244AIF_BW_lineEdit.setText( str(self.configureParameters["N5244A"]["IF_BW"]))
        self.N5244AAveragingFactor_lineEdit.setText( str(self.configureParameters["N5244A"]["averagingFactor"]))
        self.N5244AAverage_checkBox.setChecked(self.configureParameters["N5244A"]["ifAverage"])

        index = self.N5244ASweepType_comboBox.findText(self.configureParameters["N5244A"]["sweepType"])
        self.N5244ASweepType_comboBox.setCurrentIndex(index)
        #able only current tab
        for n in range(3):
          self.N5244ASweepType_tab.setTabEnabled(n,False)
        self.N5244ASweepType_tab.setTabEnabled(index,True)
        self.N5244ASweepType_tab.setCurrentIndex(index)

        #CW input
        self.N5244ACW_frequence_lineEdit.setText( str(self.configureParameters["N5244A"]["CW_frequence"]))
        self.N5244ACW_power_lineEdit.setText( str(self.configureParameters["N5244A"]["CW_power"]))
        self.N5244ACW_powerOn_checkBox.setChecked(self.configureParameters["N5244A"]["CW_ifPowerOn"])
        #sweepPower input
        self.N5244APower_points_lineEdit.setText( str(self.configureParameters["N5244A"]["power_points"]))
        self.N5244APower_frequence_lineEdit.setText( str(self.configureParameters["N5244A"]["power_frequence"]))
        self.N5244APower_startPower_lineEdit.setText( str(self.configureParameters["N5244A"]["power_start"]))
        self.N5244APower_stopPower_lineEdit.setText( str(self.configureParameters["N5244A"]["power_stop"]))
        #sweepFrequence input
        self.N5244AFrequence_points_lineEdit.setText( str(self.configureParameters["N5244A"]["frequence_points"]))
        self.N5244AFrequence_power_lineEdit.setText( str(self.configureParameters["N5244A"]["frequence_power"]))
        self.N5244AFrequence_powerOn_checkBox.setChecked(self.configureParameters["N5244A"]["frequence_ifPowerOn"])
        self.N5244AFrequence_startFrequence_lineEdit.setText( str(self.configureParameters["N5244A"]["frequence_start"]))
        self.N5244AFrequence_stopFrequence_lineEdit.setText( str(self.configureParameters["N5244A"]["frequence_stop"]))
        #---- check connection status ---        
        self.connection_check("N5244A")
        
        #---- set waiting time ----
        self.otherWaitingTime_lineEdit.setText(str(self.configureParameters["other"]["waitingTime"]))
    except:  pass
    
    #--------------------------------------------------------------------------------------
    #---- action part (user) ----
    self.LI5650Connect_pushButton.clicked.connect(lambda:self.connection_check("LI5650"))
    self.SR830Connect_pushButton.clicked.connect(lambda:self.connection_check("SR830"))
    
    self.N5244AConnect_pushButton.clicked.connect(lambda:self.connection_check("N5244A"))
    self.N5244ASweepType_comboBox.currentTextChanged.connect(self.N5244ASweepType_comboBoxChanged)
    
    self.apply_pushButton.clicked.connect(self.apply_clicked)
    self.exit_pushButton.clicked.connect(self.reject)
    
  #===========================================================================
  def connection_check(self, instrument):
    if (instrument == "LI5650"):
        address = self.LI5650Address_lineEdit.text()
        LI5650_instrument = instrument_class.LI5650_instrument(address)
        error_info = LI5650_instrument.connect()
        if (error_info == "No error"):
          self.LI5650Connect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.LI5650Connect_pushButton.setText("ON")
        else:
          self.LI5650Connect_pushButton.setStyleSheet('background-color: None')
          self.LI5650Connect_pushButton.setText("OFF")
    elif (instrument == "SR830"):
        address = self.SR830Address_lineEdit.text()
        SR830_instrument = instrument_class.SR830_instrument(address)
        error_info = SR830_instrument.connect()
        if (error_info == "No error"):
          self.SR830Connect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.SR830Connect_pushButton.setText("ON")
        else:
          self.SR830Connect_pushButton.setStyleSheet('background-color: None')
          self.SR830Connect_pushButton.setText("OFF")
    elif (instrument == "N5244A"):
        address = self.N5244AAddress_lineEdit.text()
        N5244A_instrument = instrument_class.N5244A_instrument(address)
        error_info = N5244A_instrument.connect()
        if (error_info == "No error"):
          self.N5244AConnect_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
          self.N5244AConnect_pushButton.setText("ON")
        else:
          self.N5244AConnect_pushButton.setStyleSheet('background-color: None')
          self.N5244AConnect_pushButton.setText("OFF")
          
  #=============================================================================
  def N5244ASweepType_comboBoxChanged(self):
      index = self.N5244ASweepType_comboBox.currentIndex()
      #able only current tab
      for n in range(3):
          self.N5244ASweepType_tab.setTabEnabled(n,False)
      self.N5244ASweepType_tab.setTabEnabled(index,True)
      self.N5244ASweepType_tab.setCurrentIndex(index)
      
  #=============================================================================
  def apply_clicked(self):
    #---- save inputs to self.configureParameters ----
    try:
        #---- LI5650 settings ----
        self.configureParameters["LI5650"]["ifRun"]           = self.LI5650IfRun_checkBox.isChecked()
        self.configureParameters["LI5650"]["auto"]            = self.LI5650Auto_checkBox.isChecked()
        self.configureParameters["LI5650"]["address"]         = self.LI5650Address_lineEdit.text()
        self.configureParameters["LI5650"]["voltage"]         = float(self.LI5650Voltage_lineEdit.text())
        self.configureParameters["LI5650"]["frequency"]       = float(self.LI5650Frequency_lineEdit.text())
        self.configureParameters["LI5650"]["timeConstant"]    = float(self.LI5650TimeConstant_lineEdit.text())
        self.configureParameters["LI5650"]["referenceSignal"] = self.LI5650ReferenceSignal_comboBox.currentText()
        self.configureParameters["LI5650"]["filterSlope"]     = self.LI5650FilterSlope_comboBox.currentText()
        self.configureParameters["LI5650"]["signalInput"]     = self.LI5650SignalInput_comboBox.currentText()

        #---- SR830 state ----
        self.configureParameters["SR830"]["ifRun"]     = self.SR830IfRun_checkBox.isChecked()
        self.configureParameters["SR830"]["address"]   = self.SR830Address_lineEdit.text()
        self.configureParameters["SR830"]["voltage"]   = float(self.SR830Voltage_lineEdit.text())
        self.configureParameters["SR830"]["frequency"] = float(self.SR830Frequency_lineEdit.text())
        self.configureParameters["SR830"]["phase"]     = float(self.SR830Phase_lineEdit.text())

        #---- N5244A state ----
        self.configureParameters["N5244A"]["ifRun"] = self.N5244AIfRun_checkBox.isChecked()
        self.configureParameters["N5244A"]["address"] = self.N5244AAddress_lineEdit.text()
        self.configureParameters["N5244A"]["IF_BW"] = float(self.N5244AIF_BW_lineEdit.text())
        self.configureParameters["N5244A"]["averagingFactor"] = int(self.N5244AAveragingFactor_lineEdit.text())
        self.configureParameters["N5244A"]["ifAverage"] = self.N5244AAverage_checkBox.isChecked()
        self.configureParameters["N5244A"]["sweepType"] = self.N5244ASweepType_comboBox.currentText()
        #CW input
        self.configureParameters["N5244A"]["CW_frequence"] = float(self.N5244ACW_frequence_lineEdit.text())
        self.configureParameters["N5244A"]["CW_power"] = float(self.N5244ACW_power_lineEdit.text())
        self.configureParameters["N5244A"]["CW_ifPowerOn"] = self.N5244ACW_powerOn_checkBox.isChecked()
        #sweepPower input
        self.configureParameters["N5244A"]["power_points"] = int(self.N5244APower_points_lineEdit.text())
        self.configureParameters["N5244A"]["power_frequence"] = float(self.N5244APower_frequence_lineEdit.text())
        self.configureParameters["N5244A"]["power_start"] = float(self.N5244APower_startPower_lineEdit.text())
        self.configureParameters["N5244A"]["power_stop"] = float(self.N5244APower_stopPower_lineEdit.text())
        #sweepFrequence input
        self.configureParameters["N5244A"]["frequence_points"] = int(self.N5244AFrequence_points_lineEdit.text())
        self.configureParameters["N5244A"]["frequence_power"] = float(self.N5244AFrequence_power_lineEdit.text())
        self.configureParameters["N5244A"]["frequence_ifPowerOn"] = self.N5244AFrequence_powerOn_checkBox.isChecked()
        self.configureParameters["N5244A"]["frequence_start"] = float(self.N5244AFrequence_startFrequence_lineEdit.text())
        self.configureParameters["N5244A"]["frequence_stop"] = float(self.N5244AFrequence_stopFrequence_lineEdit.text())

        #---- other ----
        self.configureParameters["other"]["waitingTime"] = float(self.otherWaitingTime_lineEdit.text())

        #check power_points and frequence_points
        power_points     = self.configureParameters["N5244A"]["power_points"]
        frequence_points = self.configureParameters["N5244A"]["frequence_points"]
        if (power_points<2 or frequence_points<2): float("Error!")
        
    except ValueError:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText("Wrong Input!")
      msg.setWindowTitle("Warning!")
      msg.exec_()
      return
    
    #---- apply settings ----
    try:
        #---- LI5650 ----
        if (self.LI5650IfRun_checkBox.isChecked() == True):
            address = self.LI5650Address_lineEdit.text()
            LI5650_instrument = instrument_class.LI5650_instrument(address)
            #set reference signal
            referenceSignal = self.LI5650ReferenceSignal_comboBox.currentText()
            voltage         = float(self.LI5650Voltage_lineEdit.text())
            frequency       = float(self.LI5650Frequency_lineEdit.text())
            error_info      = LI5650_instrument.set_referenceSignal(referenceSignal, voltage, frequency)
            if (error_info != "No error"): raise Exception('Error Occur')
            #set filter
            auto            = self.LI5650Auto_checkBox.isChecked()
            timeConstant    = float(self.LI5650TimeConstant_lineEdit.text())
            filterSlope     = int(self.LI5650FilterSlope_comboBox.currentText().split()[0])
            error_info      = LI5650_instrument.set_filter(filterSlope, timeConstant,auto)
            if (error_info != "No error"): raise Exception('Error Occur')
            #set signal input
            signalInput     = self.LI5650SignalInput_comboBox.currentText()
            error_info      = LI5650_instrument.set_signalInput(signalInput)
            if (error_info != "No error"): raise Exception('Error Occur')
        #---- SR830 ----
        if (self.SR830IfRun_checkBox.isChecked() == True):
            address = self.SR830Address_lineEdit.text()
            SR830_instrument = instrument_class.SR830_instrument(address)
            #set reference signal
            voltage         = float(self.SR830Voltage_lineEdit.text())
            frequency       = float(self.SR830Frequency_lineEdit.text())
            phase           = float(self.SR830Phase_lineEdit.text())
            error_info      = SR830_instrument.set_referenceSignal(voltage, frequency, phase)
            if (error_info != "No error"): raise Exception('Error Occur')
        #---- N5244A ----
        if (self.N5244AIfRun_checkBox.isChecked() == True):
            address = self.N5244AAddress_lineEdit.text()
            N5244A_instrument = instrument_class.N5244A_instrument(address)
            ifAverage       = self.N5244AAverage_checkBox.isChecked()
            averagingFactor = int(self.N5244AAveragingFactor_lineEdit.text())
            IF_BW           = float(self.N5244AIF_BW_lineEdit.text())

            sweepType = self.N5244ASweepType_comboBox.currentText()
            if (sweepType == "CW"):
                #configure
                frequence       = float(self.N5244ACW_frequence_lineEdit.text())
                ifPowerOn       = self.N5244ACW_powerOn_checkBox.isChecked()
                power           = float(self.N5244ACW_power_lineEdit.text())
                error_info      = N5244A_instrument.configure_CW(frequence, ifPowerOn, power, ifAverage, averagingFactor, IF_BW)
                if (error_info != "No error"): raise Exception('Error Occur')
            elif (sweepType == "Power"):
                #configure
                frequence       = float(self.N5244APower_frequence_lineEdit.text())
                points          = int(self.N5244APower_points_lineEdit.text())
                startPower      = float(self.N5244APower_startPower_lineEdit.text())
                stopPower       = float(self.N5244APower_stopPower_lineEdit.text())
                error_info      = N5244A_instrument.configure_sweepPower(startPower, stopPower, points, frequence, ifAverage, averagingFactor, IF_BW)
                if (error_info != "No error"): raise Exception('Error Occur')
            elif (sweepType == "Frequence"):
                #configure
                points          = int(self.N5244AFrequence_points_lineEdit.text())
                ifPowerOn       = self.N5244AFrequence_powerOn_checkBox.isChecked()
                power           = float(self.N5244AFrequence_power_lineEdit.text())
                startFreq       = float(self.N5244AFrequence_startFrequence_lineEdit.text())
                stopFreq        = float(self.N5244AFrequence_stopFrequence_lineEdit.text())
                error_info      = N5244A_instrument.configure_sweepFrequence(startFreq, stopFreq, points, ifPowerOn, power, ifAverage, averagingFactor, IF_BW)
                if (error_info != "No error"): raise Exception('Error Occur')
            time.sleep(0.3)
            #set trace
            error_info = N5244A_instrument.set_trace()
            if (error_info != "No error"): raise Exception('Error Occur')
    except Exception:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      try: msg.setText(error_info)
      except: msg.setText("Error Occur")
      msg.setWindowTitle("Warning!")
      msg.exec_()   