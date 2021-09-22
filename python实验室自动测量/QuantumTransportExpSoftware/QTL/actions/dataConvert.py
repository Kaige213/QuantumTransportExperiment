import numpy as np

#----------------------------------------------------------------------------- 
def dataConvert(control_record, measure_record):
    data_toPlot = []
    for n in range(len(measure_record)):
        #--------------------------------------------------------------------------------------------
        #LI5650
        if (measure_record[n]["name"] == "LI5650X"):
            #get X_value
            X_value = control_record[0]["value"]
            xlabel  = control_record[0]["instrument"]+"("+control_record[0]["unit"]+")"
            
            #get LI5650X and LI5650Y
            LI5650X = measure_record[n]["value"]
            LI5650Y = measure_record[n+1]["value"]
            #calculate: LI5650R, LI5650Theta
            [LI5650R, LI5650Theta] = [abs(LI5650X+1j*LI5650Y), np.angle(LI5650X+1j*LI5650Y, deg=True)]
            
            #store data in dataToPlot according to figurePort in mainWindow
            data_toPlot.append({"varName":"LI5650X",    "X":X_value, "Y":LI5650X,     "xlabel":xlabel, "ylabel":"LI5650X (V)"})
            data_toPlot.append({"varName":"LI5650Y",    "X":X_value, "Y":LI5650Y,     "xlabel":xlabel, "ylabel":"LI5650Y (V)"})
            data_toPlot.append({"varName":"LI5650R",    "X":X_value, "Y":LI5650R,     "xlabel":xlabel, "ylabel":"LI5650R (V)"})
            data_toPlot.append({"varName":"LI5650Theta","X":X_value, "Y":LI5650Theta, "xlabel":xlabel, "ylabel":"LI5650Theta (Deg)"})
            
        #--------------------------------------------------------------------------------------------
        #SR830
        elif (measure_record[n]["name"] == "SR830X"):
            #get X_value
            X_value = control_record[0]["value"]
            xlabel = control_record[0]["instrument"]+"("+control_record[0]["unit"]+")"
            
            #get SR830X and SR830Y
            SR830X = measure_record[n]["value"]
            SR830Y = measure_record[n+1]["value"]
            #calculate: SR830R, SR830Theta
            [SR830R, SR830Theta] = [abs(SR830X+1j*SR830Y), np.angle(SR830X+1j*SR830Y, deg=True)]
            
            #store data in dataToPlot according to figurePort in mainWindow
            data_toPlot.append({"varName":"SR830X",    "X":X_value, "Y":SR830X,     "xlabel":xlabel, "ylabel":"SR830X (V)"})
            data_toPlot.append({"varName":"SR830Y",    "X":X_value, "Y":SR830Y,     "xlabel":xlabel, "ylabel":"SR830Y (V)"})
            data_toPlot.append({"varName":"SR830R",    "X":X_value, "Y":SR830R,     "xlabel":xlabel, "ylabel":"SR830R (V)"})
            data_toPlot.append({"varName":"SR830Theta","X":X_value, "Y":SR830Theta, "xlabel":xlabel, "ylabel":"SR830Theta (Deg)"})
            #X, Y are used to plot figures
            #xlabel and ylabel are used to set figures
        #--------------------------------------------------------------------------------------------
        #N5244A
        elif (measure_record[n]["name"] == "N5244AX"):
            #X_value and xlabel
            X_unit = measure_record[n+4]["unit"]
            
            if (X_unit == ""):
                #x_value
                X_value = control_record[0]["value"]
                xlabel = control_record[0]["instrument"]+"("+control_record[0]["unit"]+")"
            elif (X_unit == "dBm"):
                X_value = measure_record[n+4]["value"]
                xlabel  = "Power (dBm)"
            elif (X_unit == "GHz"):
                X_value = measure_record[n+4]["value"]
                X_value = list(np.array(X_value) / 10**9)
                xlabel  = "Frequence (GHz)"

            #y_value
            N5244AX = measure_record[n]["value"]
            N5244AY = measure_record[n+1]["value"]
            N5244AR = measure_record[n+2]["value"]
            N5244ATheta = measure_record[n+3]["value"]
            
            #store data in dataToPlot according to figurePort in mainWindow
            data_toPlot.append({"varName":"N5244AX","X":X_value, "Y":N5244AX,     "xlabel":xlabel, "ylabel":"N5244AX (U)"})
            data_toPlot.append({"varName":"N5244AY","X":X_value, "Y":N5244AY,     "xlabel":xlabel, "ylabel":"N5244AY (U)"})
            data_toPlot.append({"varName":"N5244AR","X":X_value, "Y":N5244AR,     "xlabel":xlabel, "ylabel":"N5244AR (dB)"})
            data_toPlot.append({"varName":"N5244ATheta","X":X_value, "Y":N5244ATheta, "xlabel":xlabel, "ylabel":"N5244ATheta (Deg)"})
            data_toPlot.append({"varName":"N5244ANyquist","X":N5244AX, "Y":N5244AY,   "xlabel":"N5244AX (U)", "ylabel":"N5244AY (U)"})

            #X, Y are used to plot figures
            #xlabel and ylabel are used to set figures
        
        #为了简化程序，data_toSave与data_toPlot基本一样，只是检查是否有Nyquist数据
        #data_toPlot中其余数据都要保存到数据文件中
        data_toSave = data_toPlot.copy()
        for n in range(len(data_toSave)):
            varName = data_toSave[n]["varName"]
            if ("Nyquist" in varName): del data_toSave[n]
                
        
    return [data_toPlot,data_toSave]