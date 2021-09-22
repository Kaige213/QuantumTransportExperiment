import visa
import time

class LI5650_instrument:
    
    def __init__(self, address):
        self.address = address
        
    def connect(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n', open_timeout=1000)
            #check connection status
            return_str = self.inst.query("*IDN?")
            self.inst.close() #close visa
            if ("LI5650" in return_str):return "No error"
            else: return "Error:LI5650:Connection"
        except: return "Error:LI5650:connect"
        
    def set_referenceSignal(self, referenceSignal, voltage, frequence):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #set reference signal source
            if (referenceSignal == "REF IN"):
                command = ":ROUT2 RINP"
            elif (referenceSignal == "INT OSC"):
                command = ":ROUT2 IOSC"
            else:
                command = ":ROUT2 SINP"
            #set voltage
            command = command + ";" + ":SOUR:IOSC PRI;:SOUR:VOLT "+ str(voltage)
            #set frequece
            command = command + ";" + ":SOUR:FREQ " + str(frequence)
            #send command to instrument and query error_info
            self.inst.write(command);time.sleep(0.01)
            error_info = self.inst.query(":SYST:ERR?")
            self.inst.close() #close visa
            if("No error" in error_info): return "No error"
            else: return "Error:LI5650:set_referenceSignal"
        except: return "Error:LI5650:set_referenceSignal"
        
    def set_filter(self, slope, TC, auto):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            if (auto == True): command = ":FILT:AUTO:ONCE"
            else: command = ":FILT:SLOP " + str(slope) + ";" + ":FILT:TCON " + str(TC)
            #send command to instrument and query error_info
            self.inst.write(command);time.sleep(0.01)
            error_info = self.inst.query(":SYST:ERR?")
            self.inst.close() #close visa
            if("No error" in error_info): return "No error"
            else: return "Error:LI5650:set_filter"
        except: return "Error:LI5650:set_filter"
        
    def set_signalInput(self, signalInput):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            if (signalInput == "I"):
                command = ":ROUT I"
            elif (signalInput == "A-B"):
                command = ":ROUT AB"
            else:
                command = ":ROUT A"
            #send command to instrument and query error_info
            self.inst.write(command);time.sleep(0.01)
            error_info = self.inst.query(":SYST:ERR?")
            self.inst.close() #close visa
            if("No error" in error_info): return "No error"
            else: return "Error:LI5650:set_signalInput"
        except: return "Error:LI5650:set_signalInput"
        
    def read_XY(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #check data format
            if ( self.inst.query(":DATA?") != "19" ):self.inst.write(":DATA 19")
            time.sleep(0.01)
            
            #read data
            for n in range(20):
                data_str = self.inst.query(":FETC?")
                status   = int(data_str.split(",")[0])
                if ( status == 0 ):
                    [X, Y] = [float(data_str.split(",")[1]), float(data_str.split(",")[2])]
                    error_info = "No error"
                    break
                else: X=float("NAN");Y=float("NAN");error_info="Error:LI5650:read_XY"; time.sleep(1)
            #self.inst.close() #close visa
            return [X,Y, error_info]
        
        except: return [float("NAN"), float("NAN"), "Error:LI5650:read_XY"]
      
#=====================================================================
if __name__ == "__main__":
    #address = "GPIB0::4::INSTR"
    address = "TCPIP0::127.0.0.1::33564::SOCKET"
    inst    = LI5650_instrument(address)
    
    #----  check connection ----
    error_info = inst.connect()
    print("Connection:", error_info)
    
    #---- set reference signal ----
    #referenceSignal = "REF IN"
    referenceSignal = "INT OSC"
    #referenceSignal = "SIGNAL"
    frequence       = 1100
    voltage         = 0.67
    error_info = inst.set_referenceSignal(referenceSignal, voltage, frequence)
    print("Set reference signal: ", error_info)
    
    #set filter
    auto = True
    slope = 24  # slope= 6, 12, 18, 24
    TC    = 0.5   #time constant
    error_info = inst.set_filter(slope, TC, auto)
    print("Set filter: ", error_info)
    
    #set signal input
    signalInput = "A"
    error_info = inst.set_signalInput(signalInput)
    print("Set signal input: ", error_info)

    #read data
    [X,Y, error_info] = inst.read_XY()
    print("Data: ", "X=", X, "Y=", Y, "error_info: ", error_info)
