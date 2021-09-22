'''
Note:
  1. 如果实验中使用N5244A sweepPower/sweepFrequence，则使用listCheck.py检查数据，如果没有，使用nonListCheck.py检查数据
  2. 检查数据时，不要重复实验，导致数据文件夹中有多余文件，可能产生不必要的混淆
  3. 检查数据时，每次都要重新启动lab_simulation.py，否则控制参数可能有问题
#------------------------------------------------------------------------------
程序部分：
  第一步：得到待扫描的所有参数点(loopState)，顺序与实验中的扫面顺序一致
  第二步：检查数据文件
         扫描参数空间时，不区分正扫or回扫，但记录数据或者画图时需要区分
  第三步：检查由figure保存的数据（即检查绘图是否正确）
  第四步：如果有Nyquist，单独检查
         Nyquist图根据XY来检查
'''

#=================================================================================================================
#=================================================================================================================
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import json

folderPath = ".."
with open(folderPath+"/curves/experiment_info.json", "r") as read_file:
  experimentInfo_dict = json.load(read_file)
  
controlInstrument_sortedByLoop = experimentInfo_dict["controlInstruments"]
ifSweepBack     = experimentInfo_dict["ifSweepBack"]
variable_toSave = experimentInfo_dict["variable_toSave"]
variable_toPlot = experimentInfo_dict["variable_toPlot"]
N5244A_info     = experimentInfo_dict["N5244A"]
points_forward  = experimentInfo_dict["points_forward"]

sweepVarible = N5244A_info["sweepType"]
if ( sweepVarible == "Power"):
    start  = N5244A_info["power_start"]
    stop   = N5244A_info["power_stop"]
    points = N5244A_info["power_points"]
    X_axis = np.linspace(start, stop, points)
if ( sweepVarible == "Frequence"):
    start  = N5244A_info["frequence_start"]
    stop   = N5244A_info["frequence_stop"]
    points = N5244A_info["frequence_points"]
    X_axis = np.linspace(start, stop, points)

#-----------------------------------------------------
def measure_result(variable_toSave, control_state, X_value=0):
    try:GS610R = control_state["GS610R"]
    except:GS610R=0
    try:GS610L = control_state["GS610L"]
    except:GS610L=0
    try:GS210  = control_state["GS210" ]
    except:GS210=0
    try:Magnet = control_state["Magnet"]
    except:Magnet=0

    #---- LI5650 ----
    LI5650 = np.exp(1j*np.cos(GS610R)*np.pi*2) + np.cos(GS610L)*np.exp(1j*GS610L) + \
             np.exp(1j*GS610L**3) + GS210**2 + Magnet * np.cos(GS610L) * np.sin(GS210) * np.cos(Magnet)**2
    #---- SR830 ----
    SR830  = LI5650
    #---- N5244A ----
    N5244A = LI5650 * np.exp(1j*X_value) * np.cos(X_value)
    
    #---- measure_state ----
    measure_state = []
    #check if LI5650 is used
    for varName in variable_toSave:
      if ("LI5650" in varName):
        measure_state = measure_state + [np.real(LI5650), np.imag(LI5650), np.abs(LI5650), np.angle(LI5650, deg=True)]
        break
    #check if SR830 is used
    for varName in variable_toSave:
      if ("SR830" in varName):
        measure_state = measure_state + [np.real(SR830) , np.imag(SR830 ), np.abs(SR830 ), np.angle(SR830 , deg=True)]
        break
    #check if N5244A is used
    for varName in variable_toSave:
      if ("N5244A" in varName):
        measure_state = measure_state + [np.real(N5244A), np.imag(N5244A), np.abs(N5244A), np.angle(N5244A, deg=True)]
        break    
    
    return measure_state
    
#=================================================================================================================
#=================================================================================================================
#第一步：得到待扫描的所有参数点(loopState)，顺序与实验中的扫面顺序一致
loopState_mat    = []
loopState_now    = [0] * len(controlInstrument_sortedByLoop)

#---------------------------------------------------------
#loopState_mat记录待扫描参数空间中的所有点
while True:
  loopState_mat.append(loopState_now.copy())
  
  #next loopState
  loopState_now[0] = loopState_now[0] + 1
  
  #检查loopID是否超了
  for n in range(len(loopState_now)-1):
    if (loopState_now[n] == len(controlInstrument_sortedByLoop[n]["vector"])):
      loopState_now[n+1] = loopState_now[n+1] + 1
      loopState_now[n]   = 0
  #检查是否扫描完毕
  if (loopState_now[-1] == len(controlInstrument_sortedByLoop[-1]["vector"])): break

#----------------------------------------
#---- check controlState in fileName ----
#参数空间的每个点对应一个文件（一对一）
print("文件名检查：")

allFileNamesAreCorrect = True
for n in range(len(loopState_mat)):
  loopState_now = loopState_mat[n].copy()  
    
  #initiate
  fileName = "ID"
  #loopID
  for m in range(len(loopState_now)-1,0,-1):    #descending order
    ID       = loopState_now[m]
    fileName = fileName +  "." + str(ID)
  
  #对于回扫的instrument，ID=loopState_now[0] - points_forward
  #sweep对应的ID为0
  if (loopState_now[0] >= points_forward):
    fileName = fileName+".%s.0"%(str(loopState_now[0] - points_forward))
  else:
    fileName = fileName+".%s.0"%(str(loopState_now[0]))

  #controlState
  for m in range(len(loopState_now)-1,-1,-1):
    ID       = loopState_now[m]
    name     = controlInstrument_sortedByLoop[m]["instrument"]
    unit     = controlInstrument_sortedByLoop[m]["unit"]
    value    = controlInstrument_sortedByLoop[m]["vector"][ID]
    fileName = fileName + "_%s=%s(%s)"%(name, str(np.float32(value)), unit)
  #sweepVariable
  fileName = fileName + "_%s=sweep.dat"%(sweepVarible)
  
  #扫描参数空间时，不区分正扫or回扫，但记录数据或者画图时需要区分
  if (loopState_now[0] >= points_forward):
    pathAndFile = "%s/SweepBack/%s"%(folderPath,fileName)
  else: pathAndFile = "%s/%s"%(folderPath,fileName)
  
  #check if file exists
  if os.path.isfile(pathAndFile):   pass
  else:  print("    文件缺失: ", pathAndFile); allFileNamesAreCorrect=False

#---- result ----  
if (allFileNamesAreCorrect == True): print("    文件名正确！")
else: sys.exit(0)

#=================================================================================================================
#=================================================================================================================
#第二步：检查数据文件
##----------------------------------------------------------
print("数据检查：")

error_mat   = []
measure_mat = []

#---- step 1 ----
#extrace data in dataFile
for n in range(len(loopState_mat)):
  loopState_now  = loopState_mat[n].copy()

  #对于回扫的instrument，ID=loopState_now[0] - points_forward
  if (loopState_now[0] >= points_forward):
    loopState_now[0] = loopState_now[0] - points_forward
    folderPath_temp  = folderPath + "/SweepBack"
  else: folderPath_temp  = folderPath
    
  #find fileName
  fileID_str = "ID."+".".join( list(map(str, loopState_now[::-1]))) + ".0"
  for fileName in os.listdir(folderPath_temp): 
    if (fileID_str in fileName): break

  #提取数据
  with open(folderPath_temp+'/'+fileName) as f:
    for line_str in f.readlines():
      if (line_str[0] == "#"): continue
      data_vec = []
      for string in line_str.split(" "):
        try: num = float(string); data_vec.append(num);
        except:pass
      #store data in matrix
      measure_mat.append(data_vec[1:])

#---- step 2 ----
#compare data
for n in range(len(loopState_mat)):
  loopState_now  = loopState_mat[n]
  #controlState
  controlState = {}
  for m in range(len(loopState_now)):
    ID       = loopState_now[m]
    name     = controlInstrument_sortedByLoop[m]["instrument"]
    value    = controlInstrument_sortedByLoop[m]["vector"][ID]
    controlState[name] = value
  
  for k in range(len(X_axis)):
    X_value = X_axis[k]
    #计算理论值
    measureState = measure_result(variable_toSave, controlState,  X_value)
    
    #if (n == 0 and k == 0): print(measureState);sys.exit(0)
    
    pos = n*len(X_axis) + k
    #计算相对误差
    error_vec    = []
    for m in range(len(measureState)):
      if (abs(measureState[m]) > 10**-10): 
        error_vec.append((measure_mat[pos][m] - measureState[m]) / abs(measureState[m]))
      else:
        error_vec.append((measure_mat[pos][m] - measureState[m]))
    error_mat.append(error_vec)
    
#---- plot error ----
error_mat = np.array(error_mat)
plt.figure(figsize=(16, len(measureState)))
for n in range(len(measureState)):
  plt.subplot(len(measureState)//4, 4, n+1)
  plt.plot(error_mat[:,n])
  plt.title(variable_toSave[n])
plt.show()  


#=================================================================================================================
#=================================================================================================================
#第三步：检查由figure保存的csv数据（即检查绘图是否正确）
print("检查curve数据文件：")
measure_mat = []
error_mat   = []

#---- step 1 ----
#extrace data in dataFile
for variable in variable_toSave:
  Y_vec = np.load(folderPath+"/curves/"+variable+".npz")["Y_vec"]
  measure_mat.append(list(Y_vec))
measure_mat = np.array(measure_mat).T

#---- step 2 ----
#compare data
for n in range(len(loopState_mat)):
  loopState_now  = loopState_mat[n]
  #controlState
  controlState = {}
  for m in range(len(loopState_now)):
    ID       = loopState_now[m]
    name     = controlInstrument_sortedByLoop[m]["instrument"]
    value    = controlInstrument_sortedByLoop[m]["vector"][ID]
    controlState[name] = value
  
  for k in range(len(X_axis)):
    X_value = X_axis[k]
    #计算理论值
    measureState = measure_result(variable_toSave, controlState,  X_value)   
    pos = n*len(X_axis) + k
    #计算相对误差
    error_vec    = []
    for m in range(len(measureState)):
      if (abs(measureState[m]) > 10**-10): 
        error_vec.append((measure_mat[pos][m] - measureState[m]) / abs(measureState[m]))
      else:
        error_vec.append((measure_mat[pos][m] - measureState[m]))
    error_mat.append(error_vec)

#---- plot error ----
error_mat = np.array(error_mat)
plt.figure(figsize=(16, len(measureState)))
for n in range(len(measureState)):
  plt.subplot(len(measureState)//4, 4, n+1)
  plt.plot(error_mat[:,n])
  plt.title(variable_toSave[n])
plt.show()

#=================================================================================================================
#=================================================================================================================
#第四步：如果有Nyquist，单独检查
for varName in variable_toPlot:
  if ("Nyquist" in varName):
    #---- step 1 ----
    #extrace Nyquist data
    N5244ANyquist_mat = np.load(folderPath+"/curves/N5244ANyquist.npz")
    #extrace N5244AX data
    N5244AX_vec = np.load(folderPath+"/curves/N5244AX.npz")["Y_vec"]
    N5244AY_vec = np.load(folderPath+"/curves/N5244AY.npz")["Y_vec"]

    #---- step 2 ----
    #---- compare and plot ----
    plt.figure(figsize=(8, 4))
    #error: X
    plt.subplot(1, 2, 1)
    plt.plot(np.array(N5244ANyquist_mat["X_vec"]) - np.array(N5244AX_vec))
    plt.title("N5244ANyquist X")
    #error: Y
    plt.subplot(1, 2, 2)
    plt.plot(np.array(N5244ANyquist_mat["Y_vec"]) - np.array(N5244AY_vec))
    plt.title("N5244ANyquist Y")
    plt.show()

