"""
如果dataToPlot中有Nyquist数据，程序会跳过，不保存Nyquist数据
"""
import os
import numpy as np
import time

#---------------------------------------------------
def fileName_func(control_record, data_toSave, folderPath, ifSweepBack):
    
  if (ifSweepBack == True):   folderPath = folderPath + "/SweepBack"
  if (os.path.exists(folderPath) == False):  os.makedirs(folderPath)
  
  #--------------------------------------------------
  #---- get fileID ----
  fileID   = []
  #get the loopState of "=", "=", "5->","4->","3->","2->", "1->"
  for n in range(len(control_record)): 
    fileID.insert(0, control_record[n]["loopState"])

  #check sweep varible
  sweepVariable = control_record[0]["instrument"]
  if (type(data_toSave[0]["X"]) == list):
      sweepVariable = data_toSave[0]["xlabel"].split(" ")[0] #去掉单位：Power (dBm) -> Power
      fileID.append(0)

  #if the fileID already exists, add one to the last ID
  #使用while循环，一直加1，直到得到一个不重复的fileID
  file_exist = True
  files      = os.listdir(folderPath)
  while file_exist:
    file_exist = False
    fileID_str = "ID."+".".join(map(str, fileID))
    for f in files:
      if ( (fileID_str in f) and f.endswith('.dat')):
        fileID[-1] = fileID[-1] + 1
        file_exist = True
        break

  #--------------------------------------------------      
  #get the controlInstrument state of "=", "=", "5->","4->","3->","2->"
  controlState = ""
  for n in range(len(control_record)-1,0,-1):
    instrument   = control_record[n]["instrument"]
    value        = control_record[n]["value"]
    unit         = control_record[n]["unit"]
    controlState = controlState + "_" + instrument+"="+str(np.float32(value))+"("+unit+")"
  #检查sweepVairable
  if (type(data_toSave[0]["X"]) == list):
    #如果数据文件不以loop1为x变量
    #controlState中加入loop1的设备状态
    instrument   = control_record[0]["instrument"]
    value        = control_record[0]["value"]
    unit         = control_record[0]["unit"]
    controlState = controlState + "_" + instrument+"="+str(np.float32(value))+"("+unit+")"
    #最后加上扫描变量
    controlState = controlState + "_" + sweepVariable + "=sweep"
  else:
    #如果数据文件中以loop1为x变量
    controlState = controlState + "_" + sweepVariable + "=sweep"

  #fileName
  fileName = "ID.%s%s.dat" % (".".join(map(str, fileID)), controlState)
          
  #---- add path ----
  path_and_file = folderPath + "/" + fileName

  return path_and_file

#=========================================================================
def addDescriptiveWords_func(data_toSave, log_info, runningParameters, path_and_file):
  dataLength = 16
  f= open(path_and_file,"w")
  
  #save time and log
  f.write("#Time: %s\n"%time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
  f.write("#Log:  %s\n"%log_info.replace("\n", "\n#      "))
  #save runningParameters_dict
  f.write("#RunningParameters:\n")
  for ele in runningParameters.items():
    if (ele[1]["ifRun"] == False): continue
    f.write("#    %s: %s\n"%(str(ele[0]),str(ele[1])))
  f.write("#------------------------------------------------------------------------\n")

  #save x_variable
  str_toSave = data_toSave[0]["xlabel"].replace(" ","")   #去掉空格
  str_toSave = str_toSave + " "*(dataLength-1 - len(str_toSave))
  f.write("#")
  f.write(str_toSave)
  f.write(" ")    #add one space to seperate
  
  #save variable name in the measurement
  for variable in data_toSave:
    if ("Nyquist" in variable["varName"]): continue
    str_toSave = variable["ylabel"].replace(" ","")   #去掉空格
    str_toSave = str_toSave + " "*(dataLength - len(str_toSave))
    f.write(str_toSave)
    f.write(" ")
  f.write("\n")
  #close f
  f.close()

#=========================================================================
def store_data_func(data_toSave, path_and_file):
  dataLength = 16
  #------------ store data --------------
  f= open(path_and_file, "a")
  
  #data_num
  try: data_num = len(data_toSave[0]["X"]) #表示有多行数据
  except: data_num = 1                     #表示只有单行数据
  
  for n in range(data_num):
      #save x_variable
      try:    value = data_toSave[0]["X"][n]
      except: value = data_toSave[0]["X"]
      str_toSave = str(np.float32(value))
      str_toSave = str_toSave + " "*(dataLength - len(str_toSave))
      f.write(str_toSave)
      f.write(" ")
     
      #save y_variable
      for variable in data_toSave:
        try:    value = variable["Y"][n]
        except: value = variable["Y"]
        str_toSave = str(np.float32(value))
        str_toSave = str_toSave + " "*(dataLength - len(str_toSave))
        f.write(str_toSave)
        f.write(" ")
      #add '\n' and close f
      f.write("\n")
  f.close()

#=========================================================================
if __name__ == "__main__":
  #control_record #, 说明: 1. instrument按loop，由小到大排列
  control_record = [{'instrument': 'GS610R', 'loopState': 1, 'value': 0.5, 'unit': 'V'},
                    {'instrument': 'GS610L', 'loopState': 2, 'value': 0.0, 'unit': 'V'}, 
                    {'instrument': 'GS210', 'loopState': 3, 'value': 1.0, 'unit': 'V'}, 
                    {'instrument': 'Magnet', 'loopState': 4, 'value': 0.3, 'unit': 'T'},
                    {'instrument': 'Time', 'loopState': 0, 'value': 0.0, 'unit': 's'}]
  

  #runningParameters              
  runningParameters = {'GS610R': {'ifRun': True, 'start': 0.0, 'loop': '1->', 'stop': 1.0, 'current': 0, 'points': 11, 'step': 0.1}, 
                       'GS610L': {'ifRun': True, 'start': 0.0, 'loop': '2->', 'stop': 1.0, 'current': 0, 'points': 11, 'step': 0.1}, 
                       'GS210': {'ifRun': True, 'start': 1.0, 'loop': '3->', 'stop': 0.0, 'current': 0, 'points': 11, 'step': -0.1}, 
                       'Magnet': {'ifRun': True, 'start': 0.3, 'loop': '4->', 'stop': 0.0, 'current': 0, 'points': 4, 'step': -0.1}, 
                       'Time': {'ifRun': True, 'start': 0.0, 'loop': '5->', 'stop': 1.0, 'current': 0, 'points': 2, 'step': 1.0}, 
                       'sweepBack': {'ifRun': False, 'points': 11}}
  folderPath = "."
  log_info   = "Test\nasdfa\nasdf"
  ifSweepBack= True
  
  #---------------------------------------------------------------------------------------------------------------
  #part one: N5244A CW
  data_toSave = [{'varName': 'N5244AX', 'X': 0, 'Y': -0.8539806, 'xlabel': 'Time(s)', 'ylabel': 'N5244AX (U)'},
                 {'varName': 'N5244AY', 'X': 0, 'Y': -0.166395, 'xlabel': 'Time(s)', 'ylabel': 'N5244AY (U)'},
                 {'varName': 'N5244AR', 'X': 0, 'Y': -1.209212, 'xlabel': 'Time(s)', 'ylabel': 'N5244AR (dB)'},
                 {'varName': 'N5244ATheta', 'X': 0, 'Y': -168.9743, 'xlabel': 'Time(s)', 'ylabel': 'N5244ATheta (Deg)'},
                 {'varName': 'N5244ANyquist', 'X': -0.8539806, 'Y': -0.166395, 'xlabel': 'N5244AX (U)', 'ylabel': 'N5244AY (U)'}]

  #---- save data ----
  path_and_file = fileName_func(control_record, data_toSave, folderPath,ifSweepBack)
  addDescriptiveWords_func(data_toSave, log_info, runningParameters, path_and_file)
  store_data_func(data_toSave, path_and_file)

  #---------------------------------------------------------------------------------------------------------------
  #part two: N5244A sweepPower
  data_toSave = [{'varName': 'N5244AX',       'X': [-10.0, 0.0], 'Y': [-0.8553937, -0.8553911], 'xlabel': 'Power (dBm)', 'ylabel': 'N5244AX (U)'},
                 {'varName': 'N5244AY',       'X': [-10.0, 0.0], 'Y': [-0.167176, -0.1669568], 'xlabel': 'Power (dBm)', 'ylabel': 'N5244AY (U)'},
                 {'varName': 'N5244AR',       'X': [-10.0, 0.0], 'Y': [-1.193886, -1.19433], 'xlabel': 'Power (dBm)', 'ylabel': 'N5244AR (dB)'},
                 {'varName': 'N5244ATheta',   'X': [-10.0, 0.0], 'Y': [-168.9416, -168.9557], 'xlabel': 'Power (dBm)', 'ylabel': 'N5244ATheta (Deg)'},
                 {'varName': 'N5244ANyquist', 'X': [-0.8553937, -0.8553911], 'Y': [-0.167176, -0.1669568], 'xlabel': 'N5244AX (U)', 'ylabel': 'N5244AY (U)'}]
  
  #---- save data ----
  path_and_file = fileName_func(control_record, data_toSave, folderPath,ifSweepBack)
  addDescriptiveWords_func(data_toSave, log_info, runningParameters, path_and_file)
  store_data_func(data_toSave, path_and_file)
