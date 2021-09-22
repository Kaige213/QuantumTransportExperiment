import visa
import time
import socket

class Magnet_instrument:
    
    def __init__(self, address):
        self.address = address
        
    def connect(self):
        start = time.time()
        try:
            #check socket connection
            IP   = self.address.split("::")[1]
            PORT = int(self.address.split("::")[2])
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect((IP, PORT))
            s.shutdown(socket.SHUT_RDWR)
            s.close()

            #check connection status           
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            command = "READ:SYS:VRM:POC"
            return_str = self.inst.query(command)
            self.inst.close() #close visa

            if ("STAT:SYS:VRM" in return_str):return "No error"
            else: return "Error:Magnet:connect"
        except :return "Error:Magnet:connect"
        
    def setPOC(self, ifPOC):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            if (ifPOC): command = "SET:SYS:VRM:POC:ON"
            else      : command = "SET:SYS:VRM:POC:OFF"
            self.inst.write(command)
            return_str = self.inst.read()
            self.inst.close() #close visa
            if("INVALID" in return_str): return "Error:Magnet:setPOC"
            else: return "No error"
        except: return "Error:Magnet:setPOC"
        
    def setRvstMode(self, mode, rate=0):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            if (mode == "As Fast As Possible"):
                command = "SET:SYS:VRM:COO:CART:RVST:MODE:ASAP:VSET:[0 0 0]"
                self.inst.write(command)
                return_str = self.inst.read()
                self.inst.close() #close visa
                if("INVALID" in return_str): return "Error:Magnet:setRvsMode"
                else: return "No error"
            if (mode == "Specify Rate"):
                command = "SET:SYS:VRM:COO:CART:RVST:MODE:RATE:RATE:"+str(rate)+":VSET:[0 0 0]"
                self.inst.write(command)
                return_str = self.inst.read()
                self.inst.close() #close visa
                if("INVALID" in return_str): return "Error:Magnet:setRvsMode"
                else: return "No error"
        except: return "Error:Magnet:setRvsMode"
        
    def setMagnet(self, value):
        try:
            self.inst = visa.ResourceManager().open_resource(self.address, read_termination='\n')
            #---- get MODE and RATE to construct command string ----
            command    = "READ:SYS:VRM:RVST:MODE:RATE"
            return_str = self.inst.query(command)
            command    = "SET" + return_str.strip("STAT").strip("T/m") + ":VSET:[0 0 "+str(value)+"]"
            self.inst.write(command)   #set magnet
            time.sleep(1)
            #---- action ----
            command = "SET:SYS:VRM:ACTN:RTOS"
            self.inst.write(command)
            #---- wait for completion ---
            while True:
                time.sleep(1)
                command = "READ:SYS:VRM:ACTN"
                return_str = self.inst.query(command)
                if (return_str == "STAT:SYS:VRM:ACTN:IDLE"): self.inst.close(); return "No error"
        except: return "Error:Magnet:setMagnet:Value="+str(value)+"T"
      
#=====================================================================
if __name__ == "__main__":
    import time
    address = "TCPIP0::127.0.0.1::33563::SOCKET"
    inst    = Magnet_instrument(address)
    
    #----  check connection ----
    start = time.time()
    error_info = inst.connect()
    print("Connection:", error_info)
    print("Time: ", time.time()-start)
    
    #----  set POC ----
    error_info = inst.setPOC(False)
    print("Set POC:", error_info)

    #---- set AFAP ----
    error_info = inst.setRvstMode("As Fast As Possible")
    print("Set AFAP: ", error_info)

    #---- set RATE ----
    rate = 0.1
    error_info = inst.setRvstMode("Specify Rate", rate=rate)
    print("Set RATE: ", error_info)
    
    #---- set magnet ----
    magnet = 0.1234
    error_info = inst.setMagnet(magnet)
    print("Set Magnet: ", error_info)
