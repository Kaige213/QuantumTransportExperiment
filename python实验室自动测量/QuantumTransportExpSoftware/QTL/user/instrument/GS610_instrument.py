import visa
import time
import numpy as np

#import traceback


class GS610_instrument:
    
    def __init__(self, address):
        self.address = address
        
    def connect(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #check connection status
            command = "*IDN?"
            return_str = self.inst.query(command)
            self.inst.close() #close visa
            if ("Yokogawa" in return_str):return "No error"
            else: return "Error:GS610:Connection"
        except: return "Error:GS610:connect"

    def setRange(self, rng):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            command = ":SOUR:VOLT:RANG " + str(rng)
            self.inst.write(command)
            error_info = self.inst.query(":SYST:ERR?")
            self.inst.close() #close visa
            if("No error" not in error_info): return "Error:GS610:setRange"
            else: return "No error"
        except: return "Error:GS610:setRange"
        
        
    def setVoltage(self, voltage, step):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            voltage_now = float(self.inst.query( ":SOUR:VOLT:LEV?"))
            #check step and produce voltage_vec
            if ( abs(step) < 10**-6): voltage_vec = np.linspace(voltage_now, voltage, 11)[1:]
            else:
                #check step
                if (voltage>voltage_now) : step =  abs(step)
                else                     : step = -abs(step)
                #produce voltage_vec
                voltage_vec = []
                while True:
                    voltage_next = voltage_now + step
                    if ( step>0 and voltage_next>(voltage-10**-6) ): break
                    elif(step<= 0 and voltage_next<(voltage+10**-6)): break
                    else: voltage_vec.append(voltage_next); voltage_now = voltage_next
                voltage_vec.append(voltage)
            #change voltage
            for n in range(len(voltage_vec)):
                if (n > 0): time.sleep(0.2)      #if (len(voltage_vec)=1): do not wait
                voltage_next = voltage_vec[n]
                command = ":SOUR:VOLT:LEV "+ str(voltage_next) + ";:OUTP ON"
                self.inst.write(command)
                
            #check error info
            error_info = self.inst.query(":SYST:ERR?")
            #self.inst.close() #close visa
            if("No error" not in error_info): return "Error:GS610:setVoltage:value="+ str(voltage)
            else: return "No error"
        except:  return "Error:GS610:setVoltage:value="+ str(voltage)
#=====================================================================
if __name__ == "__main__":
    #address = "GPIB0::2::INSTR"
    address = "TCPIP0::127.0.0.1::33560::SOCKET"
    inst    = GS610_instrument(address)
    
    #----  check connection ----
    error_info = inst.connect()
    print("Connection:", error_info)
    
    #----  set range ----
    rng = 20
    error_info = inst.setRange(rng)
    print("Set Range:", error_info)

    #----  set voltage ----
    voltage = 1
    step    = 0
    error_info = inst.setVoltage(voltage, step)
    print("Set voltage:", error_info)
