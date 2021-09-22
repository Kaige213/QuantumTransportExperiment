import time
import user.instrument as instrument_class
   
#===============================================================================
def readMeasureInstrument(configureParameters):
    #clear/initiate the measurment result in self.experimentState_record
    measurement_record = []
    error_info_record  = []
    
    #---- read data from measurementInstrument ----
    #---- read data from LI5650 ----
    if (configureParameters["LI5650"]["ifRun"]):
      address = configureParameters["LI5650"]["address"]
      LI5650_instrument = instrument_class.LI5650_instrument(address)
      unit   = configureParameters["LI5650"]["unit"]
      [LI5650X, LI5650Y, error_info] = LI5650_instrument.read_XY()
      #----------------------------------------------------------------
      # record measurement
      measurement_record.append({"name":"LI5650X", "value":LI5650X, "unit":unit})
      measurement_record.append({"name":"LI5650Y", "value":LI5650Y, "unit":unit})
      if (error_info == "No error"):  pass
      else: error_info_record.append(error_info)
      
    #---- read data from SR830 ----
    if (configureParameters["SR830"]["ifRun"]):
      address          = configureParameters["SR830"]["address"]
      SR830_instrument = instrument_class.SR830_instrument(address)
      unit             = configureParameters["SR830"]["unit"]
      [SR830X, SR830Y, error_info] = SR830_instrument.read_XY()
      #----------------------------------------------------------------
      # record measurement
      measurement_record.append({"name":"SR830X", "value":SR830X, "unit":unit})
      measurement_record.append({"name":"SR830Y", "value":SR830Y, "unit":unit})
      if (error_info == "No error"): pass
      else: error_info_record.append(error_info)
      
    #---- read data from N5244A ----
    if (configureParameters["N5244A"]["ifRun"]):
      address           = configureParameters["N5244A"]["address"]
      N5244A_instrument = instrument_class.N5244A_instrument(address)
      [X_axis, N5244AX, N5244AY, N5244AR, N5244ATheta, error_info] = N5244A_instrument.initiate_and_read_data()
      
      #unit of X_axis accroding to sweepType
      sweepType = configureParameters["N5244A"]["sweepType"]
      if  (sweepType == "CW") :
        X_unit=""     #unit = the unit of instrument with loop=1->
        [X_axis,N5244AX,N5244AY,N5244AR,N5244ATheta]=[X_axis[0],N5244AX[0],N5244AY[0],N5244AR[0],N5244ATheta[0]]
      elif (sweepType == "Power"):     X_unit="dBm"
      elif (sweepType == "Frequence"): X_unit="GHz"

      #----------------------------------------------------------------
      # record measurement
      measurement_record.append({"name":"N5244AX"    , "value":N5244AX    , "unit":"U"})
      measurement_record.append({"name":"N5244AY"    , "value":N5244AY    , "unit":"U"})
      measurement_record.append({"name":"N5244AR"    , "value":N5244AR    , "unit":"dB"})
      measurement_record.append({"name":"N5244ATheta", "value":N5244ATheta, "unit":"Deg"})
      measurement_record.append({"name":"X_axis"     , "value":X_axis     , "unit":X_unit})
      
      if (error_info == "No error"): pass
      else: error_info_record.append(error_info)
            
    #chech if error occur
    if (len(error_info_record) == 0): error_info = "No error"
    else:  error_info = "; ".join(error_info_record)
    return [measurement_record, error_info]
        
#===============================================================================
def setControlInstrument(name, address, value, step):
  #---------------------
  if (name == "GS610R"):
    GS610R_instrument = instrument_class.GS610_instrument(address)
    error_info = GS610R_instrument.setVoltage(value, step)
    
  #---------------------
  if (name == "GS610L"):
    GS610L_instrument = instrument_class.GS610_instrument(address)
    error_info = GS610L_instrument.setVoltage(value, step)
    
  #---------------------
  if (name == "GS210"):
    GS210_instrument = instrument_class.GS210_instrument(address)
    error_info = GS210_instrument.setVoltage(value, step)
    
  #---------------------
  if (name == "Magnet"):
    Magnet_instrument = instrument_class.Magnet_instrument(address)
    error_info = Magnet_instrument.setMagnet(value)

  #---------------------
  if (name == "Time"):
    time.sleep(abs(step))
    error_info = "No error"

  return error_info
