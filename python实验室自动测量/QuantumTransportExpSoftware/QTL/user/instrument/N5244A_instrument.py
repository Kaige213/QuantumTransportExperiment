"""
1. 对于N5244A的设置参数，有一些是半公共参数，如frequence。CW和sweepPower其实可以用一个frequence参数
   但是为了防止混淆，任然将它区分为CW_frequence和power_frequence。虽然有一点重复，但程序会更清晰，并
   且一目了然，非常方便地知道不同实验所需要的所有设置参数；
2. N5244A_instrument.py的返回数据始终为list，在setOrRead_instrument中会根据实验类型进行修正，但如果
   实验为CW，则将数据转化为float；如果实验为sweepPower/sweepFrequence，则数据类型不变，只设定单位

"""

import visa
#import traceback
#import numpy as np


class N5244A_instrument:
    
    def __init__(self, address):
        self.address = address
        
    def connect(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #check connection status
            command = "*IDN?"
            return_str = self.inst.query(command)
            if ("N5244A" in return_str):return "No error"
            else: return "Error:N5244A:Connection"
        except: return "Error:N5244A:connect"

                
    def configure_CW(self, frequence, ifPowerOn, power, ifAverage, averaging_factor, IF_BW):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #==== default setting ====
            self.inst.query("INITiate1:CONTinuous OFF;*OPC?")
            self.inst.write("SENSe1:SWEep:TRIGger:POINt OFF" )
            #set points
            points  = 1
            self.inst.write("SENSe1:SWEep:POINts " + str(points))
            #==== user setting ====
            #set averaging
            if (ifAverage == True):
                self.inst.write("SENS:AVER:STAT ON")  #set averaging_on
                self.inst.write("SENS:AVER:MODE POINT") #set point_averaging mode
                self.inst.write("SENS:AVER:COUN "+ str(averaging_factor))
            else: self.inst.write("SENS:AVER:STAT OFF")
            
            #set power
            if (ifPowerOn == True):            
                self.inst.write("OUTPUT ON")
                self.inst.write( "SOURce:POWer " + str(power))
            else: self.inst.write("OUTPUT OFF")

            #set IF BW (Hz)
            self.inst.write( "SENSe1:BANDwidth " + str(IF_BW))
            
            #set sweep mode
            self.inst.write("SENSe:SWEep:TYPE CW")
            #set CW frequence (GHz)
            self.inst.write( "SENSe:FREQuency:CW " + str(frequence*10**9))
            
            return "No error"
        except: return "Error:N5244A:configure_CW"
        
    #====================================================
    def configure_sweepPower(self, start_power, stop_power, points, frequence, ifAverage, averaging_factor, IF_BW):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')

            #---- default setting ----
            self.inst.query("INITiate1:CONTinuous OFF;*OPC?")
            self.inst.write("SENSe1:SWEep:TRIGger:POINt OFF" )
            #---- sweep type ----
            self.inst.write("SENSe:SWEep:TYPE POWer")
            
            #---- linear power ----
            self.inst.write("SOURce:POWer:STARt "+str(start_power))
            self.inst.write("SOURce:POWer:STOP " +str(stop_power))
            
            #---- sweep points ----
            self.inst.write("SENSe1:SWEep:POINts "+str(points))
            
            #set CW frequence (GHz)
            self.inst.write( "SENSe:FREQuency:CW " + str(frequence*10**9))
            
            #---- set averaging ----
            if (ifAverage == True):
                self.inst.write("SENS:AVER:STAT ON")  #set averaging_on
                self.inst.write("SENS:AVER:MODE POINT") #set point_averaging mode
                self.inst.write("SENS:AVER:COUN "+ str(averaging_factor))
            else: self.inst.write("SENS:AVER:STAT OFF")

            #---- band width ----
            self.inst.write("SENSe1:BANDwidth "+str(IF_BW))
            return "No error"
        except: traceback.print_exc();return "Error:N5244A:configure_weepPower"
        
    #====================================================
    def configure_sweepFrequence(self, start_freq, stop_freq, points, ifPowerOn, power, ifAverage, averaging_factor, IF_BW):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            
            #---- default setting ----
            self.inst.query("INITiate1:CONTinuous OFF;*OPC?")
            self.inst.write("SENSe1:SWEep:TRIGger:POINt OFF" )
            #---- sweep type ----
            self.inst.write("SENSe:SWEep:TYPE LINear")
            
            #---- set linear frequence ----
            self.inst.write("SENSe1:FREQuency:STARt "+str(start_freq*10**9))
            self.inst.write("SENSe1:FREQuency:STOP " +str(stop_freq*10**9))

            #---- set points ----
            self.inst.write("SENSe1:SWEep:POINts "+str(points))

            #---- set power ----
            if (ifPowerOn == True):            
                self.inst.write("OUTPUT ON")
                self.inst.write( "SOURce:POWer " + str(power) )
            else: self.inst.write("OUTPUT OFF")

            #---- set averaging ----
            if (ifAverage == True):
                self.inst.write("SENS:AVER:STAT ON")  #set averaging_on
                self.inst.write("SENS:AVER:MODE POINT") #set point_averaging mode
                self.inst.write("SENS:AVER:COUN "+ str(averaging_factor))
            else: self.inst.write("SENS:AVER:STAT OFF")

            #---- band width ----
            self.inst.write("SENSe1:BANDwidth "+str(IF_BW))
            
            return "No error"
        except: return "Error:N5244A:configure_weepFrequence"


    #====================================================
    def set_trace(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')

            #deleta all before setting trace
            self.inst.write("CALCulate:PARameter:DELete:ALL")
            
            #-------- set trace --------
            #---- set Real(S21) ----
            #Creates a measurement but does NOT display it.
            self.inst.write( "CALCulate1:PARameter:DEFine:EXT '1', S21" )
            #Creates a new trace <tnum> and associates (feeds) a measurement <name> to the
            #specified window<wnum>. 
            self.inst.write("DISPlay:WINDow1:TRACe1:FEED '1'")
            #Sets the selected measurement. 
            self.inst.write( "CALCulate1:PARameter:SELect '1'" )
            #set format
            self.inst.write( "CALCulate1:FORMat REAL" )
            self.inst.write("CALCulate1:MARKer:STATe ON") #set marker
            
            #---- set Imag(S21) ----
            self.inst.write( "CALCulate1:PARameter:DEFine:EXT '2', S21" )
            self.inst.write( "DISPlay:WINDow1:TRACe2:FEED '2'" )
            self.inst.write( "CALCulate1:PARameter:SELect '2'" )
            self.inst.write( "CALCulate1:FORMat IMAGinary" )
            self.inst.write("CALCulate1:MARKer:STATe ON") #set marker
            
            #---- set R(S21) ----
            self.inst.write("CALCulate1:PARameter:DEFine:EXT '3', S21")
            self.inst.write("DISPlay:WINDow1:TRACe3:FEED '3'")
            self.inst.write("CALCulate1:PARameter:SELect '3'")
            self.inst.write("CALCulate1:FORMat MLOGarithmic")
            self.inst.write("CALCulate1:MARKer:STATe ON") #set marker
            
            #---- set Phase(S21) ----
            self.inst.write( "CALCulate1:PARameter:DEFine:EXT '4', S21" )
            self.inst.write( "DISPlay:WINDow1:TRACe4:FEED '4'" )
            self.inst.write( "CALCulate1:PARameter:SELect '4'" )
            self.inst.write( "CALCulate1:FORMat PHASe" ) 
            self.inst.write("CALCulate1:MARKer:STATe ON") #set marker
            
            #marker properties
            self.inst.write("DISP:WIND:ANN:MARK:SIZE LARG") #marker size
            self.inst.write("CALCulate1:MARKer:COUP ON")    #marker coupled
            self.inst.write("CALCulate1:MARKer:DISC ON")    #marker discrete
        
            return "No error"
        except: return "Error:N5244A:set_trace"
        
    def initiate_and_read_data(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #initiate or trigger
            self.inst.write("INITiate1")
            #wait for completing operation
            self.inst.write("*OPC?")
            while True:
                try: self.inst.read();break
                except:pass
                
            #---- read data ----
            #x axis
            data_str = self.inst.query("CALCulate1:X?").split(",")
            X_axis   = list(map(float, data_str) )

            #select measurement            
            self.inst.write("CALCulate1:PARameter:SELect '1'")
            #set format
            self.inst.write("FORMat ASCII")
            #read data
            data_str = self.inst.query("CALCulate1:DATA? FDATA").split(",")
            S21_real = list(map(float, data_str) )

            #select measurement
            self.inst.write("CALCulate1:PARameter:SELect '2'")
            #set format
            self.inst.write("FORMat ASCII")
            #read data
            data_str = self.inst.query("CALCulate1:DATA? FDATA").split(",")
            S21_imag = list(map(float, data_str) )

            #select measurement
            self.inst.write( "CALCulate1:PARameter:SELect '3'" )
            #set format
            self.inst.write( "FORMat ASCII" )
            #read data
            data_str = self.inst.query("CALCulate1:DATA? FDATA").split(",")
            S21_R = list(map(float, data_str) )

            #select measurement
            self.inst.write("CALCulate1:PARameter:SELect '4'")
            #set format
            self.inst.write("FORMat ASCII")
            #read data
            data_str = self.inst.query("CALCulate1:DATA? FDATA").split(",")
            S21_phase = list(map(float, data_str) )
            
            #convert unit if sweepType = LINear frequence
            sweepType= self.inst.query("SENSe:SWEep:TYPE?")
            if (sweepType == "LIN"): X_axis = list(map(lambda freq: freq/10**9, X_axis))#convert Hz to GHz
            
            return [X_axis   , S21_real   , S21_imag   , S21_R   , S21_phase   , "No error"]
        except: return [[float("NAN")]]*5+[["Error:N5244A:initiate_and_read_data"]]
        
#=====================================================================
if __name__ == "__main__":
    #address = "GPIB0::5::INSTR"
    address = "TCPIP0::127.0.0.1::33566::SOCKET"
    inst    = N5244A_instrument(address)
       
    #----  check connection ----
    error_info = inst.connect()
    print("Connection:", error_info)
   
    #----------------------------------------------------------------------
    print();print();print("CW: ")
    
    #---- configure CW ----
    ifAverage = True
    averaging_factor = 11
    ifPowerOn = True
    power     = -10.0  #dBm
    IF_BW     = 10.0   #Hz
    frequence = 1.0  #Ghz
    error_info = inst.configure_CW(frequence, ifPowerOn, power, ifAverage, averaging_factor, IF_BW)
    print("Configure:", error_info)


    #---- set trace ----
    error_info = inst.set_trace()
    print("Set_trace:", error_info)
    
    for n in range(2):
        #---- initiate measurement and read data ----
        [X_axis, S21_real, S21_imag, S21_R, S21_phase, error_info] = inst.initiate_and_read_data()
        print("Data: ", [X_axis, S21_real, S21_imag, S21_R, S21_phase])

    #----------------------------------------------------------------------
    print();print();print("Sweep Power")
    
    #--------------------------------
    #---- configure sweepPower ----
    start_power      = -10   #unit: dBm
    stop_power       = 0     #unit: dBm
    points           = 5
    frequence        = 1     #unit: GHz
    ifAverage        = False
    averaging_factor = 11
    IF_BW            = 10    #unit: Hz
    error_info = inst.configure_sweepPower(start_power, stop_power, points, frequence, ifAverage, averaging_factor, IF_BW)
    print("Configure:", error_info)


    #---- set trace ----
    error_info = inst.set_trace()
    print("Set_trace:", error_info)
    
    #---- initiate measurement and read data ----
    [X_axis, S21_real, S21_imag, S21_R, S21_phase, error_info] = inst.initiate_and_read_data()
    print(X_axis)
    print( S21_real, S21_imag, S21_R, S21_phase )
    
#    #---- check data ----
#    inst_forMarker = visa.ResourceManager().open_resource(address, read_termination='\n')
#    for m in range(len(X_axis)):
#        X = X_axis[m]
#        inst_forMarker.write("CALCulate1:MARKer:X "+str(X))
#        print("Data: ", S21_real[m], S21_imag[m])
#        if ( abs(S21_real[m]+1j*S21_imag[m] - 10**(S21_R[m]/20) * np.exp(1j*S21_phase[m]/180*np.pi)) > 10**-6 ):
#              print("Error: ", X_axis[m], S21_real[m], S21_imag[m], S21_R[m], S21_phase[m])
#        

 
    #----------------------------------------------------------------------
    print();print();print("Sweep Frequence")
    
    #--------------------------------
    #---- configure sweepFreuence ----
    start_freq       = 1     #unit: GHz
    stop_freq        = 2     #unit: GHz
    points           = 5       
    ifPowerOn        = True
    power            = -10   #unit: dBm
    ifAverage        = True
    averaging_factor = 11
    IF_BW            = 10    #unit: Hz
    error_info = inst.configure_sweepFrequence(start_freq, stop_freq, points, ifPowerOn, power, ifAverage, averaging_factor, IF_BW)
    print("Configure:", error_info)


    #---- set trace ----
    error_info = inst.set_trace()
    print("Set_trace:", error_info)
    
    #---- initiate measurement and read data ----
    [X_axis, S21_real, S21_imag, S21_R, S21_phase, error_info] = inst.initiate_and_read_data()
    print(X_axis)
    print( S21_real, S21_imag, S21_R, S21_phase )
    
    #---- check data ----
#    inst_forMarker = visa.ResourceManager().open_resource(address, read_termination='\n')
#    for m in range(len(X_axis)):
#        X = X_axis[m]
#        inst_forMarker.write("CALCulate1:MARKer:X "+str(X*10**9))
#        print("Data: ", S21_real[m], S21_imag[m])
#        if ( abs(S21_real[m]+1j*S21_imag[m] - 10**(S21_R[m]/20) * np.exp(1j*S21_phase[m]/180*np.pi)) > 10**-6 ):
#              print("Error: ", X_axis[m], S21_real[m], S21_imag[m], S21_R[m], S21_phase[m])
#        
