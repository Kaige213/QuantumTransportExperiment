from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui

import json
import sys
import numpy as np
import copy

import measureThread
import actions.beforeStart as beforeStart
import actions.afterStart  as afterStart
import user.linker         as linker
from   user.controlInstrument_dialog import controlInstrument_dialog
from   user.measureInstrument_dialog import measureInstrument_dialog

class Ui(QtWidgets.QMainWindow):

  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('./UI/main.ui', self)
    #configure parameters
    self.configureParameters = {}
    self.runningParameters   = {}
    self.saveConfigure       = {}
    self.runConfigure        = {}
    #data when running
    self.curvesInStore       = []
    self.curvesInFigure      = []
    

  #=====================================================================================================
  def setUp_defaultValue(self):
    #set style to be fusion
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("fusion"))
   
    #==== make ports for figure and sweepParameter input_widgets ====  
    self.sweepParameters_widgetsPorts = linker.sweepParameters_widgetsPorts_producer(self)
    self.figurePorts                  = linker.figurePorts_producer(self)
    self.figures_tabWidget.setCurrentIndex(0)
    
    #===========================================================================
    try:
        #read configure parameters from json file
        with open("parameters_initiate.json", "r") as read_file:
          parameters_initiate = json.load(read_file)          
          self.configureParameters = parameters_initiate["configureParameters"]
          self.runningParameters   = parameters_initiate["runningParameters"]
          self.saveConfigure       = parameters_initiate["saveConfigure"]
          self.runConfigure        = parameters_initiate["runConfigure"]
        
        #set by the previous user's settings
        #==== sweepParameters input ====
        for instrument in self.runningParameters.keys():
            for port_key in self.sweepParameters_widgetsPorts[instrument].keys():
                if (port_key == "loop"):
                    loop = self.runningParameters[instrument]['loop']
                    combBoxIndex = self.sweepParameters_widgetsPorts[instrument][port_key].findText(loop)
                    self.sweepParameters_widgetsPorts[instrument][port_key].setCurrentIndex(combBoxIndex)
                elif(port_key == "ifRun"):
                    ifRun = self.runningParameters[instrument]["ifRun"]
                    self.sweepParameters_widgetsPorts[instrument][port_key].setChecked( ifRun )
                else:
                    inputData = self.runningParameters[instrument][port_key]
                    if (type(inputData) == float): inputData = np.float32(inputData)
                    str_inTheInputWidget = str(inputData)
                    
                    self.sweepParameters_widgetsPorts[instrument][port_key].setText(str_inTheInputWidget)

        #---- check if disable some input_widgets according to ifRun----
        for instrument in self.runningParameters.keys():
            ifRun = self.runningParameters[instrument]["ifRun"]
            for port_key in self.sweepParameters_widgetsPorts[instrument].keys():
                if (port_key == "ifRun"):
                    continue
                self.sweepParameters_widgetsPorts[instrument][port_key].setDisabled(not ifRun)
                
        #---- check if disable some input_widgets according to loop == "=" ----
        for instrument in self.runningParameters.keys():
            if (instrument == "sweepBack"):
                continue
            loop = self.runningParameters[instrument]["loop"]
            if (loop == "="):
                self.sweepParameters_widgetsPorts[instrument]["stop"].setDisabled(True)
                self.sweepParameters_widgetsPorts[instrument]["current"].setDisabled(True)
                self.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(True)
                self.sweepParameters_widgetsPorts[instrument]["step"].setDisabled(True)
            
        #==== saveFrame ====
        #---- if save ----
        ifSave = self.saveConfigure["ifSave"] #true or false
        self.save_checkBox.setChecked(ifSave)
        #---- folder path input ----
        self.folderPath_textEdit.setText(self.saveConfigure["folderPath"])
        self.log_textEdit.setText(self.saveConfigure["log"])
        #---- check if disable some input_widgets according to ifSave ----
        self.folderPath_textEdit.setDisabled(not ifSave)
        self.selectFolder_pushButton.setDisabled(not ifSave)
        self.log_textEdit.setDisabled(not ifSave)

        #==== runFrame ====
        #---- widgets in run-frame ----
        self.numberOfCurves_lineEdit.setText(str(self.runConfigure["numberOfCurves"]))
        self.start_pushButton.setStyleSheet("background-color: rgb(255,0,0)")
    except:
        pass
    
  #=====================================================================================================
  def action_definition(self):
    #==== menu ====
    #---- action for dialog ----
    self.controlDialog_action.triggered.connect(self.popUp_controlInstrument_dialog)
    self.measureDialog_action.triggered.connect(self.popUp_measureInstrument_dialog)

    #---- action for style-choice ----
    self.windows_action.triggered.connect(lambda:self.style_choice("windows"))
    self.fusion_action.triggered.connect(lambda:self.style_choice("fusion"))
    self.windowsvistaa_action.triggered.connect(lambda:self.style_choice("windowsvista"))
   
    #==== main window ====
    #---- action for inputing parameters ----
    for instrument in self.sweepParameters_widgetsPorts.keys():
        if (instrument == "sweepBack"):
            continue
        self.sweepParameters_widgetsPorts[instrument]["ifRun"].stateChanged.connect(\
            lambda state, instrument=instrument:beforeStart.checkBoxChanged_inSweepParamters(self,instrument))
        self.sweepParameters_widgetsPorts[instrument]["start"].textEdited.connect(\
            lambda state, instrument=instrument:beforeStart.parameterInput_changed(self, instrument, change="start"))
        self.sweepParameters_widgetsPorts[instrument]["loop"].currentTextChanged.connect(\
            lambda state, instrument=instrument:beforeStart.parameterInput_changed(self, instrument, change="loop"))
        self.sweepParameters_widgetsPorts[instrument]["stop"].textEdited.connect(\
            lambda state, instrument=instrument:beforeStart.parameterInput_changed(self, instrument, change="stop"))
        self.sweepParameters_widgetsPorts[instrument]["points"].textEdited.connect(\
            lambda state, instrument=instrument:beforeStart.parameterInput_changed(self, instrument, change="points"))
        self.sweepParameters_widgetsPorts[instrument]["step"].editingFinished.connect(\
            lambda instrument=instrument:beforeStart.parameterInput_changed(self, instrument, change="step"))
        
    #---- action for checkBoxChanged for sweepBack ----    
    self.sweepParameters_widgetsPorts["sweepBack"]["ifRun"].stateChanged.connect(\
        lambda:beforeStart.checkBoxChanged_inSweepParamters(self,"sweepBack"))
            
    #---------------------------------------------------------------------------
    #---- action for saveFiles ----
    self.save_checkBox.stateChanged.connect(lambda:beforeStart.checkBoxChanged_inSaveFile(self))
    self.selectFolder_pushButton.clicked.connect(lambda:beforeStart.select_folder(self))

    #---------------------------------------------------------------------------
    #---- action for run ----
    self.clearMemory_pushButton.clicked.connect(lambda:afterStart.clearMemoryClicked(self))
    self.numberOfCurves_lineEdit.editingFinished.connect(lambda:afterStart.numberOfCurvesChanged(self))
    self.exit_pushButton.clicked.connect(self.close_application)
    self.start_pushButton.clicked.connect(self.start_pushed)

  #=====================================================================================================
  #functions called by ".connect()"
  #-----------------------------------------------------------------------------
  def start_pushed(self):
    if (self.start_pushButton.text() == 'Start'):
      #check if inputs are legal
      if_error = beforeStart.readInputParamters(self)
      if (if_error == "Error!"):
        return
      
      #save parameters_initiate
      parameters_initiate = {
        "configureParameters" : self.configureParameters,
        "runningParameters"   : self.runningParameters,
        "saveConfigure"       : self.saveConfigure,
        "runConfigure"        : self.runConfigure
      }
      with open("parameters_initiate.json", "w") as write_file:
        json.dump(parameters_initiate, write_file, indent=4)

      #-----------------------------------------------------------
      #---- initate curvesInStore, curvesInFigure and figures ----
      #---- clear figures ---- 
      for figure in self.figurePorts:
        self.figurePorts[figure].clear()
      
      #---- list to store figure ---- 
      self.curvesInStore  = []
      self.curvesInFigure = []
      
      #---- set input unit disabled ----
      afterStart.setUi_startOrStop(self, "start")
      #afterStart.logFile_create(self)

      #---- start ----
      #---- add new thread to execute measurment ----
      self.measureThread = measureThread.measureThread_cls(self.configureParameters,
                                self.runningParameters)
      self.measureThread.start()

      #---- get signal from measureThread ----
      self.measureThread.getOnePoint.connect(lambda control_record, measurement_record:afterStart.getOnePoint(self, control_record, measurement_record))
      self.measureThread.errorOccur.connect(lambda error_info:afterStart.errorOccur(self, error_info))
      self.measureThread.finished.connect(lambda:afterStart.setUi_startOrStop(self, "stop"))
      
    else:
      #set stopFlag=1, to exit measureThread
      self.measureThread.stopFlag = 1
      
  #-----------------------------------------------------------------------------
  def popUp_controlInstrument_dialog(self):
    self.controlDialog = controlInstrument_dialog()
    #forbidden main window
    self.controlDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    self.controlDialog.setUp(self.configureParameters)
    self.controlDialog.show()

  #-----------------------------------------------------------------------------
  def popUp_measureInstrument_dialog(self):
    self.measureDialog = measureInstrument_dialog()
    #forbidden main window
    self.measureDialog.setWindowModality(QtCore.Qt.ApplicationModal)
    self.measureDialog.setUp(self.configureParameters)
    self.measureDialog.show()
    
  #-----------------------------------------------------------------------------
  def style_choice(self, style_str):
    QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(style_str))
    
  #-----------------------------------------------------------------------------
  def resizeEvent(self, event):
    #---- initial geometry ----
    try:
      delta_w = self.frameGeometry().width()  - self.fG_geometry_init.width()
      delta_h = self.frameGeometry().height() - self.fG_geometry_init.height() - 20
    except:
      #---- get initial value ----
      self.fG_geometry_init = copy.deepcopy(self.frameGeometry())
      self.ta_geometry_init = copy.deepcopy(self.figures_tabWidget.geometry())
      self.sp_geometry_init = copy.deepcopy(self.sweepParameters_frame.geometry())
      self.fs_geometry_init = copy.deepcopy(self.fileSave_frame.geometry())
      self.ru_geometry_init = copy.deepcopy(self.run_frame.geometry())
      delta_w = 0
      delta_h = 0

    #new size or position   
    new_ta = copy.deepcopy(self.ta_geometry_init)
    new_sp = copy.deepcopy(self.sp_geometry_init)
    new_fs = copy.deepcopy(self.fs_geometry_init)
    new_ru = copy.deepcopy(self.ru_geometry_init)
     
    #---- new x  ----
    if ( delta_w  > 0):
      new_ta.setWidth(new_ta.width() + delta_w)
      new_ru.moveRight(new_ru.x() + new_ru.width() + delta_w)
    #---- new y  ----
    if ( delta_h  > 0):
      new_ta.setHeight(new_ta.height() + delta_h)
      new_sp.moveTop( new_sp.y() + delta_h )
      new_fs.moveTop( new_fs.y() + delta_h )
      new_ru.moveTop( new_ru.y() + delta_h )
    #set geometry
    self.figures_tabWidget.setGeometry(new_ta)
    self.sweepParameters_frame.setGeometry(new_sp)
    self.fileSave_frame.setGeometry(new_fs)
    self.run_frame.setGeometry(new_ru)
  
  #-----------------------------------------------------------------------------
  def close_application(self):
    sys.exit()


#===============================================================================
if __name__ == "__main__":   
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.setUp_defaultValue()
    window.action_definition()
    window.show()
    app.exec_()
