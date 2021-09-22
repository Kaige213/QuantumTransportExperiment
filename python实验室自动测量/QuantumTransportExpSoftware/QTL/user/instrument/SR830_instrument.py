import visa
import time

class SR830_instrument:
    
    def __init__(self, address):
        self.address = address
        
    def connect(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n', open_timeout=1000)
            #clear buffer
            self.inst.timeout = 100
            while True:
                try: self.inst.read()
                except: break
            #check connection status
            return_str = self.inst.query("*IDN?", )
            self.inst.close() #close visa
            if ("SR830" in return_str):return "No error"
            else: return "Error:SR830:Connection"
        except: return "Error:SR830:connect"
        
    def set_referenceSignal(self, voltage, frequence, phase):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #set Frequency
            command = "SLVL " + str(voltage)
            command = command + ";" + "FREQ " + str(frequence)
            command = command + ";" + "PHAS " + str(phase)
            self.inst.write(command)
            self.inst.close() #close visa
            return "No error"
        except: return "Error:SR830:set_referenceSignal"
        
    def read_XY(self):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #clear buffer
            self.inst.timeout = 100
            while True:
                try: self.inst.read()
                except: break
            #query data
            data_str  = self.inst.query("SNAP?1,2")
            [X,Y]     = [float(data_str.split(",")[0]), float(data_str.split(",")[1])]
            return [X, Y, "No error"]
        except: return [float("NAN"),float("NAN"),"Error:SR830:read_XY"]
      
#=====================================================================
if __name__ == "__main__":
    #address = "GPIB0::8::INSTR"
    address = "TCPIP0::127.0.0.1::33565::SOCKET"
    inst    = SR830_instrument(address)
    
    #----  check connection ----
    error_info = inst.connect()
    print("Connection:", error_info)
    
    #---- set reference signal ----
    voltage   = 0.05
    frequence = 11
    phase     = 1
    
    error_info = inst.set_referenceSignal(voltage, frequence, phase)
    print("Set reference signal: ", error_info)
    
    #---- read data ----
    [X, Y, error_info] = inst.read_XY()
    print("X: ", X, " Y: ", Y, " Error: ", error_info)
    
