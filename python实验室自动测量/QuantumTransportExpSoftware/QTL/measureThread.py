"""
self.runningParameters = {
  'GS610R': {'ifRun': True, 'start': 1.0, 'loop': '1->', 'stop': 5.0, 'current': 0, 'points': 3, 'step': 2.0},
  'GS610L': {'ifRun': True, 'start': 3.0, 'loop': '2->', 'stop': 4.0, 'current': 0, 'points': 3, 'step': 0.5},
  'GS210': {'ifRun': True, 'start': 2.0, 'loop': '3->', 'stop': 5.0, 'current': 0, 'points': 3, 'step': 1.5},
  'Magnet': {'ifRun': True, 'start': 12.0, 'loop': '=', 'stop': 0.0, 'current': 0, 'points': 1, 'step': 0.0},
  'Time': {'ifRun': True, 'start': 2.0, 'loop': '=', 'stop': 0.0, 'current': 0, 'points': 1, 'step': 0.0},
  'sweepBack': {'ifRun': True, 'points': 3}
  }
  
self.configureParameters = {
  'other' : {'waitingTime': 0.01, 'unit': 's'}, 
  'LI5650': {'ifRun': True, 'address': "'GPIB0::6::INSTR'", 'voltage': 1.0, 'frequency': 17.7,
             'referenceSignal': 'REF IN', 'signalInput': 'I', 'filterSlope': '24 dB', 'timeConstant': 1.0, 'auto': True, 'unit': 'V'}, 
  'SR830' : {'ifRun': True, 'address': "'GPIB0::7::INSTR'", 'voltage': 1.0, 'frequency': 17.7, 'phase': 0.0, 'unit': 'V'}, 
  'N5244A': {'ifRun': True, 'address': "'GPIB0::8::INSTR'", 'sweepType': 'CW', 'CW_frequence': 1.0, 'CW_ifPowerOn': True,
             'CW_power': -10.0, 'power_points': 11, 'power_frequence': 1.0, 'power_start': -10.0, 'power_stop': 0.0, 'frequence_points': 101,
             'frequence_power': -10.0, 'frequence_ifPowerOn': True, 'frequence_start': 1.0, 'frequence_stop': 2.0, 'ifAverage': False,
             'averagingFactor': 1, 'IF_BW': 10.0},
  'GS610R': {'range': '2 V', 'address': 'GPIB0::1::INSTR', 'unit': 'V'}, 
  'GS610L': {'range': '110 V', 'address': 'GPIB0::2::INSTR', 'unit': 'V'}, 
  'GS210' : {'range': '10 V', 'address': 'GPIB0::3::INSTR', 'unit': 'V'}, 
  'Magnet': {'sweepMode': 'As Fast As Possible', 'rate': 0.1, 'address': 'GPIB0::4::INSTR', 'ifPOC': False, 'unit': 'T'}, 
  'Time'  : {'address': 'GPIB0::5::INSTR', 'unit': 's'}
  }
  
self.controlInstrument_sortedByLoop = [
  {'instrument': 'GS610R', 'address': 'GPIB0::1::INSTR', 'unit': 'V', 'vector': [1.0, 3.0, 5.0, 5.0, 3.0, 1.0]},
  {'instrument': 'GS610L', 'address': 'GPIB0::2::INSTR', 'unit': 'V', 'vector': [3.0, 3.5, 4.0]},
  {'instrument': 'GS210',  'address': 'GPIB0::3::INSTR', 'unit': 'V', 'vector': [2.0, 3.5, 5.0]},
  {'instrument': 'Magnet', 'address': 'GPIB0::4::INSTR', 'unit': 'T', 'vector': [12.0]},
  {'instrument': 'Time',   'address': 'GPIB0::5::INSTR', 'unit': 's', 'vector': [2.0]}
  ]
  
#Note: time的地址是没有意义的，只是为了工整！
"""


import numpy as np
import time
import PyQt5.QtCore
import traceback

import user.setOrRead_instrument  as setOrRead_instrument

class measureThread_cls(PyQt5.QtCore.QThread):
  #---- signal definition ----
  getOnePoint = PyQt5.QtCore.pyqtSignal(list, list)
  errorOccur  = PyQt5.QtCore.pyqtSignal(str)
  finished    = PyQt5.QtCore.pyqtSignal()
  
  #=============================================================================
  def __init__(self, configureParameters, runningParameters):
    super(measureThread_cls, self).__init__()
    #---- measuring parameters ----
    self.configureParameters = configureParameters.copy()
    self.runningParameters   = runningParameters.copy()
    self.stopFlag            = 0    #to stop and exit this thread
  
    #---- dict to record experiment state ----
    #usage:
    #1. save data
    #2. return it to mainWindow to update the figures and controlParameters
    #initiate
    self.control_record = []
    self.measure_record = []
    self.controlInstrument_sortedByLoop = []

    #-----------------------
    #sort instrument by loop
    self.controlInstrument_sortedByLoop = []
    #sort instrument with loop= "1->", "2->", "3->", "4->", "5->" ...
    for n in range(len(self.runningParameters)):
      loop_str = str(n+1) + "->"
      for instrument in self.runningParameters:
        if (instrument == "sweepBack"): continue
        if (self.runningParameters[instrument]["ifRun"] == True):
          if (self.runningParameters[instrument]["loop"] == loop_str):
            instrument_dict = {}
            instrument_dict["instrument"] = instrument
            instrument_dict["address"] = self.configureParameters[instrument]["address"]
            instrument_dict["unit"] = self.configureParameters[instrument]["unit"]
            start  = self.runningParameters[instrument]["start"]
            stop   = self.runningParameters[instrument]["stop"]
            points = self.runningParameters[instrument]["points"]
            instrument_dict["vector"] = list(np.linspace(start, stop, points))
            self.controlInstrument_sortedByLoop.append(instrument_dict)
            
    #if sweepBack
    if (self.runningParameters["sweepBack"]["ifRun"] == True):
      instrument = self.controlInstrument_sortedByLoop[0]["instrument"]
      start  = self.runningParameters[instrument]["start"]
      stop   = self.runningParameters[instrument]["stop"]
      points_forward  = self.runningParameters[instrument]["points"]
      points_backward = self.runningParameters["sweepBack"]["points"]
      vector_forward  = np.linspace(start,stop,points_forward)
      vector_backward = np.linspace(stop,start,points_backward)
      self.controlInstrument_sortedByLoop[0]["vector"] = list(np.append(vector_forward,vector_backward))

    #add instrument with loop = "="
    for instrument in self.runningParameters:
      if (instrument == "sweepBack"): continue
      if (self.runningParameters[instrument]["ifRun"] == True):
        if (self.runningParameters[instrument]["loop"] == "="):
          instrument_dict = {}
          instrument_dict["instrument"] = instrument
          instrument_dict["address"]    = self.configureParameters[instrument]["address"]
          instrument_dict["unit"]       = self.configureParameters[instrument]["unit"]
          instrument_dict["vector"]     = [self.runningParameters[instrument]["start"]]
          self.controlInstrument_sortedByLoop.append(instrument_dict)
  #=============================================================================
  def my_timeSleep(self, seconds):
    if (self.stopFlag == 0):
      time.sleep(seconds)
    else:
      float("Wahahah!")
          
  #=============================================================================
  def run(self):
    try:
      #----------------------------------------------------------------------------
      #------------------------------- execute -------------------------------
      while (True):
        #initiate
        if (not ("loopState_new" in vars()) ):
          loopState_new = [0] * len(self.controlInstrument_sortedByLoop)
          for instrument in self.controlInstrument_sortedByLoop:
            self.control_record.append({"instrument":instrument, "loopState":-1, "value":0, "unit":"?"})

        #-----------------------------------------------------------------        
        #set instrument with loop="1->", "2->", "3->", "4->", "5->", "=", "="
        #loopState_new对应待扫描参数空间中的一，每个instrument对应一个维度
        #下面使用for循环对每个instrument进行设置
        #loopID != self.control_record[n]["loopState"]，表示该instrument的值需要更新
        for n in range(len(loopState_new)):
          loopID          = loopState_new[n] 
          instrument_dict = self.controlInstrument_sortedByLoop[n]
          if( loopID != self.control_record[n]["loopState"]):
              instrument = instrument_dict["instrument"]
              address    = instrument_dict["address"]
              unit       = instrument_dict["unit"]
              value      = instrument_dict["vector"][loopID]
              #get step
              if (len(instrument_dict["vector"]) == 1) : step = 0
              else: step = instrument_dict["vector"][1] - instrument_dict["vector"][0]
              #send command to the instrument
              error_info = setOrRead_instrument.setControlInstrument(instrument, address, value, step)
              if (error_info != "No error"): self.errorOccur.emit(error_info)
              #update self.control_record
              self.control_record[n] = {"instrument":instrument, "loopState":loopID, "value":value, "unit":unit}
              
          
        #---- waiting after control ----
        self.my_timeSleep(self.configureParameters["other"]["waitingTime"])
        
        #每设置好参数空间的一个点后，等待一定时间，再读取测量仪器的值（也就是该参数点对应的函数值）
        #read data
        [self.measure_record,error_info] = setOrRead_instrument.readMeasureInstrument(self.configureParameters.copy())
        if (error_info != "No error"):  self.errorOccur.emit(error_info)
        self.getOnePoint.emit(self.control_record.copy(), self.measure_record.copy())
          
        #-----------------------------------------------------------------  
        #next point
        loopState_new[0] = loopState_new[0] + 1
        #检查loopID是否超过了最大值，如果是，则归零，并向下一位进一
        for n in range(len(loopState_new)-1):
          instrument_dict = self.controlInstrument_sortedByLoop[n]
          if (loopState_new[n] == len(instrument_dict["vector"])):
              loopState_new[n]   = 0
              loopState_new[n+1] = loopState_new[n+1] + 1
              
        #after weeping completed
        instrument_dict = self.controlInstrument_sortedByLoop[-1]
        if (loopState_new[-1] == len(instrument_dict["vector"])):
          self.finished.emit();return

    except:self.finished.emit() # finished
