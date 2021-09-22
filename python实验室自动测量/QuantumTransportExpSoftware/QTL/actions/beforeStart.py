from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import os
import numpy as np

def checkBoxChanged_inSweepParamters(mainWin, instrument):
    ifRun = mainWin.sweepParameters_widgetsPorts[instrument]["ifRun"].isChecked()
    if (instrument == "sweepBack"):
        #---- check if setDiabled for sweepBack ----
        mainWin.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(not ifRun)
    else:
        #---- check if setDiabled for instrument ----
        mainWin.sweepParameters_widgetsPorts[instrument]["start"].setDisabled(not ifRun)
        mainWin.sweepParameters_widgetsPorts[instrument]["loop"].setDisabled(not ifRun)
        mainWin.sweepParameters_widgetsPorts[instrument]["stop"].setDisabled(not ifRun)
        mainWin.sweepParameters_widgetsPorts[instrument]["current"].setDisabled(not ifRun)
        mainWin.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(not ifRun)
        mainWin.sweepParameters_widgetsPorts[instrument]["step"].setDisabled(not ifRun)

        loop = mainWin.sweepParameters_widgetsPorts[instrument]["loop"].currentText()
        if (loop == "="):
            mainWin.sweepParameters_widgetsPorts[instrument]["stop"].setDisabled(True)
            mainWin.sweepParameters_widgetsPorts[instrument]["current"].setDisabled(True)
            mainWin.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(True)
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setDisabled(True)

    
#=============================================================================
def checkBoxChanged_inSaveFile(mainWin):
  mainWin.folderPath_textEdit.setDisabled(not mainWin.save_checkBox.isChecked())
  mainWin.selectFolder_pushButton.setDisabled(not mainWin.save_checkBox.isChecked())
  mainWin.log_textEdit.setDisabled(not mainWin.save_checkBox.isChecked())
  
#=============================================================================
def parameterInput_changed(mainWin, instrument, change="?"):
    try:
        if (change == "start"):
            loop = mainWin.sweepParameters_widgetsPorts[instrument]["loop"].currentText()
            if (loop != "="):
                start  = float( mainWin.sweepParameters_widgetsPorts[instrument]["start"].text() )
                stop   = float( mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text() )
                points = int( mainWin.sweepParameters_widgetsPorts[instrument]["points"].text() )            
                if (points < 1): raise FError("points<1")
                elif (points == 1): step = start
                else: step   = (stop - start) / (points-1)
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText(str(np.float32(step)))
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setCursorPosition(0)
        elif (change == "loop"):
            loop   = mainWin.sweepParameters_widgetsPorts[instrument]["loop"].currentText()
            if (loop == "="):
                mainWin.sweepParameters_widgetsPorts[instrument]["stop"].setText("0")
                mainWin.sweepParameters_widgetsPorts[instrument]["current"].setText("0")
                mainWin.sweepParameters_widgetsPorts[instrument]["points"].setText("1")
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText("0")
                #---- disable ----
                mainWin.sweepParameters_widgetsPorts[instrument]["stop"].setDisabled(True)
                mainWin.sweepParameters_widgetsPorts[instrument]["current"].setDisabled(True)
                mainWin.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(True)
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setDisabled(True)
            else:
                mainWin.sweepParameters_widgetsPorts[instrument]["stop"].setDisabled(False)
                mainWin.sweepParameters_widgetsPorts[instrument]["current"].setDisabled(False)
                mainWin.sweepParameters_widgetsPorts[instrument]["points"].setDisabled(False)
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setDisabled(False)
                #modify input
                start  = float( mainWin.sweepParameters_widgetsPorts[instrument]["start"].text() )
                stop   = float( mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text() )
                points = int( mainWin.sweepParameters_widgetsPorts[instrument]["points"].text() )
                if (points < 1): raise FError("points<1")
                elif (points == 1): step = start
                else: step   = (stop - start) / (points-1)
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText(str(np.float32(step)))
                mainWin.sweepParameters_widgetsPorts[instrument]["step"].setCursorPosition(0)

        elif (change == "stop"):
            start  = float( mainWin.sweepParameters_widgetsPorts[instrument]["start"].text() )
            stop   = float( mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text() )
            points = int( mainWin.sweepParameters_widgetsPorts[instrument]["points"].text() )
            if (points < 1): raise FError("points<1")
            elif (points == 1): step = start
            else: step   = (stop - start) / (points-1)
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText(str(np.float32(step)))
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setCursorPosition(0)
        elif (change == "points"):
            start  = float( mainWin.sweepParameters_widgetsPorts[instrument]["start"].text() )
            stop   = float( mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text() )
            points = int( mainWin.sweepParameters_widgetsPorts[instrument]["points"].text() )
            if (points < 1): raise FError("points<1")
            elif (points == 1): step = start
            else: step = (stop - start) / (points-1)
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText(str(np.float32(step)))
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setCursorPosition(0)
        elif (change == "step"):
            start  = float( mainWin.sweepParameters_widgetsPorts[instrument]["start"].text() )
            stop   = float( mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text() )
            step   = float( mainWin.sweepParameters_widgetsPorts[instrument]["step"].text() )
            points = round((stop-start)/step+1)
            if (points < 1): raise FError("points<1")
            elif (points == 1): step = start
            else: step = (stop - start) / (points-1)
            step   = (stop - start) / (points-1)
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText(str(np.float32(step)))
            mainWin.sweepParameters_widgetsPorts[instrument]["points"].setText(str(points))
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setCursorPosition(0)
    except:
        if (change=="step"):
            mainWin.sweepParameters_widgetsPorts[instrument]["points"].setText("Error!")
        else:
            mainWin.sweepParameters_widgetsPorts[instrument]["step"].setText("Error!")

#-----------------------------------------------------------------------------
def select_folder(mainWin):
  try:
      folderPath_old = mainWin.saveConfigure["folderPath"]
      folderPath = QFileDialog.getExistingDirectory(QtWidgets.QWidget(), "Select Folder",folderPath_old)
  except:  folderPath = QFileDialog.getExistingDirectory(QtWidgets.QWidget(), "Select Folder","./")
  mainWin.folderPath_textEdit.setText(folderPath)

#-----------------------------------------------------------------------------
def readInputParamters(mainWin):
    #------------------------------------------------------------------------
    #---- read sweepParameters and saveConfigure ----
    try:
        #---- sweep parameters ----
        for instrument in mainWin.runningParameters.keys():
            if (instrument == "sweepBack"):
                mainWin.runningParameters["sweepBack"]["ifRun"]  = mainWin.sweepParameters_widgetsPorts[instrument]["ifRun"].isChecked()
                mainWin.runningParameters["sweepBack"]["points"] = int(mainWin.sweepParameters_widgetsPorts[instrument]["points"].text())
                continue
            mainWin.runningParameters[instrument]["ifRun"]  = mainWin.sweepParameters_widgetsPorts[instrument]["ifRun"].isChecked()
            mainWin.runningParameters[instrument]["start"]  = float(mainWin.sweepParameters_widgetsPorts[instrument]["start"].text())
            mainWin.runningParameters[instrument]["loop"]   = mainWin.sweepParameters_widgetsPorts[instrument]["loop"].currentText()
            mainWin.runningParameters[instrument]["stop"]   = float(mainWin.sweepParameters_widgetsPorts[instrument]["stop"].text())
            mainWin.runningParameters[instrument]["points"] = int(mainWin.sweepParameters_widgetsPorts[instrument]["points"].text())
            mainWin.runningParameters[instrument]["step"]   = float(mainWin.sweepParameters_widgetsPorts[instrument]["step"].text())
        #---- folderPath ----
        mainWin.saveConfigure["ifSave"]     = mainWin.save_checkBox.isChecked()
        mainWin.saveConfigure["folderPath"] = mainWin.folderPath_textEdit.toPlainText()
        mainWin.saveConfigure["log"]        = mainWin.log_textEdit.toPlainText()
        #---- run ----
        mainWin.runConfigure["numberOfCurves"] = numberOfCurves = int(mainWin.numberOfCurves_lineEdit.text())

    #---- error occur ----
    except ValueError:
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText("Illegal Input!")
      msg.setWindowTitle("Warning!")
      msg.exec_()     
      return "Error!"
    #
    if (mainWin.runConfigure["numberOfCurves"] < 1):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText("Wrong: Number of curves!")
      msg.setWindowTitle("Warning!")
      msg.exec_()
      return "Error!"
    
    #------------------------------------------------------------------------
    #if saveData, then check if path exists
    if (mainWin.save_checkBox.isChecked() == True):            
        folderPath = mainWin.saveConfigure["folderPath"]
        try:
          if (os.path.exists(folderPath) == False): os.makedirs(folderPath)
        except:
          msg = QMessageBox()
          msg.setIcon(QMessageBox.Warning)
          msg.setText("Wrong: Data Path!")
          msg.setWindowTitle("Warning!")
          msg.exec_()     
          return "Error!"
    
    #------------------------------------------------------------------------
    #---- check if loops are legal ----
    #check instrument with loop="=", its 'points' must equal 1
    for instrument in mainWin.runningParameters:
      if (instrument == "sweepBack"):
          continue
      ifRun  = mainWin.runningParameters[instrument]["ifRun"]
      loop   = mainWin.runningParameters[instrument]["loop"]
      points = mainWin.runningParameters[instrument]["points"]
      if (loop == "="  and ifRun==True):
          if ( points != 1 ):
              msg = QMessageBox()
              msg.setIcon(QMessageBox.Warning)
              msg.setText("Wrong: Loop=\"=\"!")
              msg.setWindowTitle("Warning!")
              msg.exec_()
              return "Error!"
    
    #---- find loop= 1->, 2->, 3-> ... ----
    loop_list = []
    for instrument in mainWin.runningParameters:
      if (instrument == "sweepBack"):
          continue
      ifRun = mainWin.runningParameters[instrument]["ifRun"]
      loop  = mainWin.runningParameters[instrument]["loop"]
      if (instrument != "sweepBack" and loop!="=" and ifRun==True):
          loop_list.append(loop)

    for n in range(len(loop_list)):
        loop = str(n+1)+"->"         #must exist in the loop_dict
        if ( (loop in loop_list) == False ):
          msg = QMessageBox()
          msg.setIcon(QMessageBox.Warning)
          msg.setText("Wrong: Loop!")
          msg.setWindowTitle("Warning!")
          msg.exec_()
          return "Error!"

    #---- 检查如果sweepBack，则loop1必须存在 ----
    if_sweepBack = mainWin.runningParameters["sweepBack"]["ifRun"]
    if (if_sweepBack == True):
        loop1_exists = False
        for instrument in mainWin.runningParameters:
            if (instrument == "sweepBack"): continue
            ifRun = mainWin.runningParameters[instrument]["ifRun"]
            loop  = mainWin.runningParameters[instrument]["loop"]
            if (ifRun and loop=="1->"):loop1_exists = True
        if ( loop1_exists == False):
          msg = QMessageBox()
          msg.setIcon(QMessageBox.Warning)
          msg.setText("Wrong: sweepBack!")
          msg.setWindowTitle("Warning!")
          msg.exec_()
          return "Error!"


    #---- check if no control instrument is used ----
    ifRun_list = []
    for instrument in mainWin.runningParameters:
      if (instrument != "sweepBack"):
        ifRun = mainWin.runningParameters[instrument]["ifRun"]
        ifRun_list.append(ifRun)
    if ( (True in ifRun_list) == False):
      msg = QMessageBox()
      msg.setIcon(QMessageBox.Warning)
      msg.setText("Wrong: No Control Instrument!")
      msg.setWindowTitle("Warning!")
      msg.exec_()
      return "Error!"
