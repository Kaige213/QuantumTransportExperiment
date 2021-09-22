import random
import sys
import os
import time
import json
import numpy as np


#sys.path.append("../pyqtgraph")
import pyqtgraph   as pg
import actions.dataConvert as dataConvert
import actions.dataSave as dataSave

def setUi_startOrStop(mainWin, command):
  if (command == "start"):
    #---- disable input ----
    mainWin.sweepParameters_frame.setDisabled(True)
    mainWin.fileSave_frame.setDisabled(True)
    mainWin.menubar.setDisabled(True)
    mainWin.start_pushButton.setText("Stop")
    mainWin.start_pushButton.setStyleSheet("background-color: rgb(0,255,0)")
  elif (command == "stop"):   
    #---- measure finished ----[x_vec, y_vec] = mainWin.curvesInFigure[-1][varName].getData()
    mainWin.sweepParameters_frame.setDisabled(False)
    mainWin.fileSave_frame.setDisabled(False)
    mainWin.menubar.setDisabled(False)
    mainWin.start_pushButton.setText("Start")
    mainWin.start_pushButton.setStyleSheet("background-color: rgb(255,0,0)")
    
    #---------- save curves ----------
    if (mainWin.saveConfigure["ifSave"]):
        #创建文件夹
        folderPath = mainWin.saveConfigure["folderPath"] + "/curves"
        if (os.path.exists(folderPath) == False):
          os.makedirs(folderPath)
        #提取数据
        for varName in mainWin.curvesInFigure[0].keys():
          Xdata_vec = np.array([])
          Ydata_vec = np.array([])
          for n in range(len(mainWin.curvesInFigure)):
            [x_vec, y_vec] = mainWin.curvesInFigure[n][varName].getData()
            Xdata_vec = np.append(Xdata_vec, x_vec)
            Ydata_vec = np.append(Ydata_vec, y_vec)
          #保存数据
          path_and_file = folderPath + "/"+varName+".npz"
          np.savez(path_and_file, X_vec=np.float32(Xdata_vec),Y_vec=np.float32(Ydata_vec))
        #print(mainWin.measureThread.controlInstrument_sortedByLoop)     
        variable_toPlot = list(mainWin.curvesInFigure[0].keys())
        variable_toSave = variable_toPlot.copy()
        #find points_forward
        if (mainWin.runningParameters["sweepBack"]["ifRun"]):
          points_total    = len(mainWin.measureThread.controlInstrument_sortedByLoop[0]["vector"])
          points_backward = mainWin.runningParameters["sweepBack"]["points"]
          points_forward  = points_total - points_backward
        else: points_forward = len(mainWin.measureThread.controlInstrument_sortedByLoop[0]["vector"])
        #检查variable_toSave中是否有Nyquist，如果有，删除
        for n in range(len(variable_toSave)):
          if ("Nyquist" in variable_toSave[n]): del variable_toSave[n]
        #储存experiment_info，用于数据检查
        experiment_info = {"controlInstruments":mainWin.measureThread.controlInstrument_sortedByLoop,
                           "ifSweepBack":mainWin.runningParameters["sweepBack"]["ifRun"],
                           "variable_toSave":variable_toSave,
                           "variable_toPlot":variable_toPlot,
                           "N5244A":mainWin.configureParameters["N5244A"],
                           "points_forward":points_forward}
        with open(folderPath+"/experiment_info.json", "w") as write_file:
            json.dump(experiment_info, write_file, indent=2)

#-----------------------------------------------------------------------------        
def clearMemoryClicked(mainWin):
  #---- delete old data ----
  del mainWin.curvesInStore[:-1]

#-----------------------------------------------------------------------------  
def numberOfCurvesChanged(mainWin): 
  #if have no curvesInStore, skip!
  try: len(mainWin.curvesInStore)
  except: return
    
  #---- check if input legal ----
  try:
    numberOfCurves = int(mainWin.numberOfCurves_lineEdit.text())
  except:
    #if illegal, set the numOfCurves to be numOfCurvesNow in the mainWindow
    numberOfCurvesNow = len(mainWin.curvesInFigure)
    mainWin.numberOfCurves_lineEdit.setText(str(numberOfCurvesNow))
    return
  
  #if numberOfCurves < 1, set the numOfCurves to be numOfCurvesNow in the mainWindow
  if (numberOfCurves < 1):
    numberOfCurvesNow = len(mainWin.curvesInFigure)
    mainWin.numberOfCurves_lineEdit.setText(str(numberOfCurvesNow))
    return

  #if legal, check if numberOfCurvesNow > numberOfCurves
  #---- check if curvesInFigure > numberOfCurves ----
  if ( len(mainWin.curvesInFigure) > numberOfCurves ):
    numberOfCurves_toBeRemoved = len(mainWin.curvesInFigure) - numberOfCurves
    for m in range(numberOfCurves_toBeRemoved):
        #execute numberOfCurves_toBeRemoved times
        for name in mainWin.curvesInFigure[0].keys():
          mainWin.figurePorts[name].removeItem(mainWin.curvesInFigure[0][name])
        del mainWin.curvesInFigure[0]
     
  #---- check if curvesInFigure < numberOfCurves----
  while ( len(mainWin.curvesInFigure) < numberOfCurves ):
    if (len(mainWin.curvesInFigure) >= len(mainWin.curvesInStore) ):
      return
    #else add one more curve in figure
    mainWin.curvesInFigure.insert(0, mainWin.curvesInStore[-len(mainWin.curvesInFigure)-1])
    #if (positionOfData < 0): 
    for name in mainWin.curvesInFigure[0].keys():
        mainWin.figurePorts[name].addItem(mainWin.curvesInFigure[0][name])

#----------------------------------------------------------------------------- 
def getOnePoint(mainWin, control_record, measure_record):

  #---- convert control_record and measure_record to data_toPlot & data_toSave----
  [data_toPlot, data_toSave] = dataConvert.dataConvert(control_record.copy(), measure_record.copy())

  #---- figure and dataSave ----
  #len(data_toPlot) > 0 表示有测量数据，执行相关操作
  if (len(data_toPlot) > 0):
      #检查数据是否属于新的一条曲线，以及是正扫还是回扫
      #如果测量的数据类型为list，则每次测量都属于新曲线
      ifNewCurve       = False
      ifSweepBack      = False
      instrument_loop1 = control_record[0]["instrument"]
      points_forward   = mainWin.runningParameters[instrument_loop1]["points"]
      #if newCurve
      if (type(data_toPlot[0]["X"])      == list):           ifNewCurve = True
      if (control_record[0]["loopState"] == 0   ):           ifNewCurve = True
      if (control_record[0]["loopState"] == points_forward): ifNewCurve = True
      #if sweepBack
      if (control_record[0]["loopState"] >= points_forward):
        ifSweepBack=True
        #starts with 0
        control_record[0]["loopState"] = control_record[0]["loopState"] - points_forward
        
      #create new Curve and new dataFile
      if (ifNewCurve == True):  newCurve(mainWin, control_record, data_toPlot, ifSweepBack)
        
      #---- store data ----
      #每个曲线对应的数据文件名被作为属性保存到curve对象中
      #同组curve的path_and_file是一样的
      if (mainWin.saveConfigure["ifSave"]):
        path_and_file = list(mainWin.curvesInFigure[-1].values())[0].path_and_file
        dataSave.store_data_func(data_toSave, path_and_file)
          
      #---- update figures ----
      #使用data_toPlot更新figure
      for element in data_toPlot:
          varName = element["varName"]
          [x_vec, y_vec] = mainWin.curvesInFigure[-1][varName].getData()
          x_vec = np.append(x_vec, element["X"])    #没有声明axis时，np.append()始终返回一维数组
          y_vec = np.append(y_vec, element["Y"])
          mainWin.curvesInFigure[-1][varName].setData(x=x_vec,y=y_vec)
    
  #---- update current state in sweepParametersFrame ----
  #使用 control_recod 更新 current 值
  for n in range(len(control_record)):
    instrument = control_record[n]["instrument"]
    value      = control_record[n]["value"]
    mainWin.sweepParameters_widgetsPorts[instrument]["current"].setText(str(np.float32(value)))
    mainWin.sweepParameters_widgetsPorts[instrument]["current"].setCursorPosition(0)
  
#-----------------------------------------------------------------------------
def newCurve(mainWin, control_record, data_toPlot, ifSweepBack):

    if (mainWin.saveConfigure["ifSave"]):
      #produce dataFile_name
      path_and_file = dataSave.fileName_func(control_record, data_toPlot, mainWin.saveConfigure["folderPath"],ifSweepBack)
      #add descriptive words
      dataSave.addDescriptiveWords_func(data_toPlot, mainWin.saveConfigure["log"], mainWin.runningParameters, path_and_file)
    else: path_and_file = []
    
    #set label according to data_toPlot
    #---- set label ----
    #set xlable and ylable
    labelStyle = {'color': '#FFF', 'font-size': '14pt'}
    for element in data_toPlot:
        xlabel = element["xlabel"]
        ylabel = element["ylabel"]
        varName= element["varName"]
        mainWin.figurePorts[varName].setLabel("bottom", xlabel, **labelStyle)
        mainWin.figurePorts[varName].setLabel("left",   ylabel, **labelStyle)
        mainWin.figurePorts[varName].showGrid(x=True, y=True, alpha=0.4)
      
    #---- add new curve in curvesInFigure and initiate it----
    mainWin.curvesInFigure.append({})
    #select color
    color = [random.randint(0,255) for n in range(3)]
    pen   = pg.mkPen(color=color)
    for element in data_toPlot:
        curve  = pg.PlotCurveItem(pen=pen)
        curve.path_and_file = path_and_file         #add attributes to curve
        varName= element["varName"]
        mainWin.curvesInFigure[-1][varName] = curve
        mainWin.figurePorts[varName].addItem(curve)
        
    #---- backup curves ----
    mainWin.curvesInStore.append(mainWin.curvesInFigure[-1])
      
    #---- check if numberOfCurves exceed ----
    #---- check if input legal  ----
    try:
      numberOfCurves = int(mainWin.numberOfCurves_lineEdit.text())
    except:
      #if illegal, set the numOfCurves to be numOfCurvesNow in the mainWindow
      numberOfCurvesNow = len(mainWin.curvesInFigure)
      mainWin.numberOfCurves_lineEdit.setText(str(numberOfCurvesNow))
      return
    
    #if len(mainWin.curvesInFigure)>numberOfCurves, clear oldest curve
    if ( len(mainWin.curvesInFigure) > numberOfCurves ):
      numberOfCurves_toBeRemoved = len(mainWin.curvesInFigure) - numberOfCurves
      for m in range(numberOfCurves_toBeRemoved):
        #execute numberOfCurves_toBeRemoved times
        for name in mainWin.curvesInFigure[0].keys():
          mainWin.figurePorts[name].removeItem(mainWin.curvesInFigure[0][name])
        del mainWin.curvesInFigure[0]
        
    #---- check the number of curves In Store ----
    if (len(mainWin.curvesInStore) > 100):
        del mainWin.curvesInStore[0]
        #print(len(mainWin.curvesInStore))
        
#-----------------------------------------------------------------------------
def errorOccur(mainWin, error_info):
    #print error info in errorOut_textEdit
    mainWin.errorOut_textEdit.append(error_info)

    #check if save error info
    if (not mainWin.saveConfigure["ifSave"]):
        return
    folderPath    = mainWin.saveConfigure["folderPath"]
    path_and_file = folderPath + "/_error_.log"
    if (os.path.exists(folderPath) == False):
      os.makedirs(folderPath)
    f = open(path_and_file, "a")
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    f.write("%s    %s\n"%(time_str,error_info))
    f.close()
