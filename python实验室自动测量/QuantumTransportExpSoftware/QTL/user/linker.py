def sweepParameters_widgetsPorts_producer(mainWin):
    #---- sweepParameters_widgetsPorts ----
    sweepParameters_widgetsPorts = {"GS610R":{},"GS610L":{},"GS210":{},"Magnet":{},"Time":{},"sweepBack":{}}
    sweepParameters_widgetsPorts["GS610R"] = {"ifRun":mainWin.GS610R_checkBox,
                                     "start":mainWin.GS610RStart_lineEdit,
                                     "loop":mainWin.GS610RLoop_comboBox,
                                     "stop":mainWin.GS610RStop_lineEdit,
                                     "current":mainWin.GS610RCurrent_lineEdit,
                                     "points":mainWin.GS610RPoints_lineEdit,
                                     "step":mainWin.GS610RStep_lineEdit}
    sweepParameters_widgetsPorts["GS610L"] = {"ifRun":mainWin.GS610L_checkBox,
                                     "start":mainWin.GS610LStart_lineEdit,
                                     "loop":mainWin.GS610LLoop_comboBox,
                                     "stop":mainWin.GS610LStop_lineEdit,
                                     "current":mainWin.GS610LCurrent_lineEdit,
                                     "points":mainWin.GS610LPoints_lineEdit,
                                     "step":mainWin.GS610LStep_lineEdit}
    sweepParameters_widgetsPorts["GS210"] = {"ifRun":mainWin.GS210_checkBox,
                                    "start":mainWin.GS210Start_lineEdit,
                                    "loop":mainWin.GS210Loop_comboBox,
                                    "stop":mainWin.GS210Stop_lineEdit,
                                    "current":mainWin.GS210Current_lineEdit,
                                    "points":mainWin.GS210Points_lineEdit,
                                    "step":mainWin.GS210Step_lineEdit}
    sweepParameters_widgetsPorts["Magnet"] = {"ifRun":mainWin.Magnet_checkBox,
                                     "start":mainWin.MagnetStart_lineEdit,
                                     "loop":mainWin.MagnetLoop_comboBox,
                                     "stop":mainWin.MagnetStop_lineEdit,
                                     "current":mainWin.MagnetCurrent_lineEdit,
                                     "points":mainWin.MagnetPoints_lineEdit,
                                     "step":mainWin.MagnetStep_lineEdit}
    sweepParameters_widgetsPorts["Time"] = {"ifRun":mainWin.Time_checkBox,
                                   "start":mainWin.TimeStart_lineEdit,
                                   "loop":mainWin.TimeLoop_comboBox,
                                   "stop":mainWin.TimeStop_lineEdit,
                                   "current":mainWin.TimeCurrent_lineEdit,
                                   "points":mainWin.TimePoints_lineEdit,
                                   "step":mainWin.TimeStep_lineEdit}
    sweepParameters_widgetsPorts["sweepBack"] = {"ifRun":mainWin.sweepBack_checkBox,
                                        "points":mainWin.backPoints_lineEdit}
    
    return sweepParameters_widgetsPorts

#----------------------------------------------------------------------------- 
def figurePorts_producer(mainWin):
    #---- figurePort ----
    figurePort = {"LI5650X":mainWin.LI5650X_figure,
                "LI5650Y":mainWin.LI5650Y_figure,
                "LI5650R":mainWin.LI5650R_figure,
                "LI5650Theta":mainWin.LI5650Theta_figure,
                "SR830X":mainWin.SR830X_figure,
                "SR830Y":mainWin.SR830Y_figure,
                "SR830R":mainWin.SR830R_figure,
                "SR830Theta":mainWin.SR830Theta_figure,
                "N5244AX":mainWin.N5244AX_figure,
                "N5244AY":mainWin.N5244AY_figure,
                "N5244AR":mainWin.N5244AR_figure,
                "N5244ATheta":mainWin.N5244ATheta_figure,
                "N5244ANyquist":mainWin.N5244ANyquist_figure,
                  }
    
    return figurePort