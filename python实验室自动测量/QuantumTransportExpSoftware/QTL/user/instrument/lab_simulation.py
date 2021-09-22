#注意：control_state & measure_state 为dict（mutable variable），作为变量传入各个thread，所有thread包括主进程都读取同一块内存，所以在一个进程中修改这两个变量，其他进程中该变量的值也会变化，通过这种方式来实现不同进程之间的交流。但一定不能使用赋值操作，该操作会指定新的内存空间来储存变量，导致同一个变量在各个进程之间的内存不再一样，交流中断！
#================================================================
import threading
import socket
#import time
from queue import Queue 
import numpy as np

#================================================================
def virtual_GS610R_func(control_state, q):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33560
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode(); 
        if not command_str: break
        command_vec = command_str.strip().split("\r\n")
        
        #deal with command
        for command in command_vec:
          if   ("*IDN?" in command): conn.send("Yokogawa\n".encode())
          elif ("RANG " in command): pass
          elif ("ERR?"  in command): conn.send("No error\n".encode())
          elif ("LEV?"  in command): 
              voltage = control_state["GS610R"]
              conn.send( (str(voltage)+"\n").encode())
          elif ("OUTP ON" in command):
              voltage = float(command.split(";")[0][15:])
              control_state["GS610R"] = voltage
              q.put("refresh control_state")
              print("GS610R: %.3f (V)"%voltage)
          elif not command: break
          
  s.shutdown(socket.SHUT_RDWR)
  conn.close()
  
#================================================================
def virtual_GS610L_func(control_state, q):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33561
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n") 
        #deal with command
        for command in command_vec:
            if   ("*IDN?" in command): conn.send("Yokogawa\n".encode())
            elif ("RANG " in command): pass
            elif ("ERR?"  in command): conn.send("No error\n".encode())
            elif ("LEV?"  in command): 
                voltage = control_state["GS610L"]
                conn.send( (str(voltage)+"\n").encode())
            elif ("OUTP ON" in command):
                voltage = float(command.split(";")[0][15:])
                control_state["GS610L"] = voltage
                q.put("refresh control_state")
                print("GS610L: %.3f (V)"%voltage)
          
  s.shutdown(socket.SHUT_RDWR)
  conn.close()
  
#================================================================
def virtual_GS210_func(control_state, q):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33562
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen(1)

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:      
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n")
        #deal with command
        for command in command_vec:
            if   ("*IDN?" in command): conn.send("GS210\n".encode())
            elif ("RANG " in command): pass
            elif ("ERR?"  in command): conn.send("No error\n".encode())
            elif ("LEV?"  in command): 
                voltage = control_state["GS210"]
                conn.send( (str(voltage)+"\n").encode())
            elif ("OUTP ON" in command):
                voltage = float(command.split(";")[1][4:])
                control_state["GS210"] = voltage
                q.put("refresh control_state")
                print("GS210: %.3f (V)"%voltage)
          
  s.shutdown(socket.SHUT_RDWR)
  conn.close()
  
#================================================================
def virtual_Magnet_func(control_state, q):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33563
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen()

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n")
        #deal with command
        for command in command_vec:
            #connect
            if ("POC" in command): conn.send("STAT:SYS:VRM\n".encode())
            elif ("MODE" in command): conn.send("\n".encode())
            #setMagnet
            elif (command=="READ:SYS:VRM:ACTN"): conn.send("STAT:SYS:VRM:ACTN:IDLE\n".encode())
            elif ("VSET:[" in command):
                Magnet = float(command.split(" ")[-1][:-1])
                control_state["Magnet"] = Magnet
                q.put("refresh control_state")
                print("Magnet: %.3f (T)"%Magnet)

  s.shutdown(socket.SHUT_RDWR)
  conn.close()


#================================================================
def virtual_LI5650_func(measure_state):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33564
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen()

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n")
        #deal with command
        for command in command_vec:
            if (command=="*IDN?"): conn.send("LI5650\n".encode())
            elif (command==":SYST:ERR?"):conn.send("No error\n".encode())
            elif (command==":DATA?"): conn.send("19\n".encode())
            elif (command==":FETC?"): 
                [LI5650_real, LI5650_imag] = measure_state["LI5650"]
                conn.send( ("0,"+str(LI5650_real)+","+str(LI5650_imag)+"\n").encode())

  s.shutdown(socket.SHUT_RDWR)
  conn.close()
  
#================================================================
def virtual_SR830_func(measure_state):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33565
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen()

  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n")
        #deal with command
        for command in command_vec:
            if   (command =="*IDN?"): conn.send("SR830\n".encode())
            elif (command =="SNAP?1,2"): 
                [SR830_real, SR830_imag] = measure_state["SR830"]
                conn.send( (str(SR830_real)+","+str(SR830_imag)+"\n").encode())

  s.shutdown(socket.SHUT_RDWR)
  conn.close()

  
#================================================================
def virtual_N5244A_func(measure_state):

  TCP_IP = '127.0.0.1'
  TCP_PORT = 33566
  BUFFER_SIZE = 1024
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind((TCP_IP, TCP_PORT))
  s.listen()
  #address = "TCPIP0::127.0.0.1::33566::SOCKET"
  sweepType  = "CW"
  X_axis     = [0]
  points     = 1    
  startFreq  = 1    #GHz
  stopFreq   = 2    #GHz
  startPower = -10  #dBm
  stopPower  = 0    #dBm

  def get_X_axis():
    if   (sweepType == "CW") : X_axis = [0]
    elif (sweepType == "POWer"): X_axis = np.linspace(startPower, stopPower, points)
    elif (sweepType == "LINear"): X_axis = np.linspace(startFreq , stopFreq , points)
    return X_axis
    
  while True:
      #receve data
      conn, addr  = s.accept()
      while True:
        command_str = conn.recv(BUFFER_SIZE).decode()
        if not command_str: break        
        command_vec = command_str.strip().split("\r\n")
        
        #deal with command
        for command in command_vec:
          #setting
          if   ("*IDN?" in command): conn.send("N5244A\n".encode())          
          elif ("*OPC?" in command): conn.send("\n".encode())
          elif ("POINts"in command): points= int(command[20:])
          elif ("TYPE " in command): sweepType= command[17:]
          #sweepPower
          elif ("POWer:STARt" in command): startPower= float(command[19:])
          elif ("POWer:STOP"  in command): stopPower = float(command[18:])
          #sweepFrequence
          elif ("FREQuency:STARt" in command): startFreq= float(command[23:])
          elif ("FREQuency:STOP"  in command): stopFreq = float(command[22:])
          
          #set_trace: No query!
          #refresh measure_state
          measure_state["N5244A"][0] = get_X_axis()
          q.put("measure_state")
          #initiate_and_read_data
          if ("SELect" in command)       : data_index = int(command[-2:-1])
          elif ("TYPE?"  in command_str ): conn.send((sweepType+"\n").encode());
          elif ("X?"  in command_str):
            X_axis_str = ",".join(map(str, measure_state["N5244A"][0]))
            conn.send( (X_axis_str+"\n").encode() )
          elif ("FDATA"  in command):
            Y_axis_str = ",".join(map(str, measure_state["N5244A"][data_index]))
            conn.send( (Y_axis_str+"\n").encode() )
  s.shutdown(socket.SHUT_RDWR)
  conn.close()
  
#================================================================
def measure_result(control_state, measure_state):
    GS610R = control_state["GS610R"]
    GS610L = control_state["GS610L"]
    GS210  = control_state["GS210" ]
    Magnet = control_state["Magnet"]

    #---- LI5650 ----
    LI5650 = np.exp(1j*np.cos(GS610R)*np.pi*2) + np.cos(GS610L)*np.exp(1j*GS610L) + \
             np.exp(1j*GS610L**3) + GS210**2 + Magnet * np.cos(GS610L) * np.sin(GS210) * np.cos(Magnet)**2
             
    #---- SR830 ----
    SR830  = LI5650
    
    #---- N5244A ----
    X_axis = np.array(measure_state["N5244A"][0])
    if ( np.max(np.abs(X_axis)) > 10**6): N5244A = LI5650 * np.exp(1j*X_axis/10**9) * np.cos(X_axis/10**9)  #convert Hz to GHz
    else: N5244A = LI5650 * np.exp(1j*X_axis) * np.cos(X_axis)
    
    #---- measure_state ----
    measure_state["LI5650"] = [np.real(LI5650), np.imag(LI5650)]
    measure_state["SR830" ] = [np.real(SR830) , np.imag(SR830 )]
    measure_state["N5244A"] = [X_axis, np.real(N5244A), np.imag(N5244A), np.abs(N5244A), np.angle(N5244A, deg=True)]

    
#================================================================
if __name__ == "__main__":

    #---- initiate experimental state ----
    #control_state
    control_state = {}
    control_state["GS610R"] = 0
    control_state["GS610L"] = 0
    control_state["GS210" ] = 0
    control_state["Magnet"] = 0
    #N5244A_state
   
    #measure_state
    #Note: 
    #N5244A:[[X_axis],[N5244A],[N5244Y],[N5244R],[N5244Theta]]
    measure_state = {"LI5650":[0,0], "SR830":[0,0], "N5244A":[[0],[0],[0],[0],[0]]}
    measure_result(control_state, measure_state)
       
    q = Queue() 
    
    GS610R = threading.Thread(target=virtual_GS610R_func, args=(control_state, q))
    GS610R.start()
    
    GS610L = threading.Thread(target=virtual_GS610L_func, args=(control_state, q))
    GS610L.start()
    
    GS210 = threading.Thread(target=virtual_GS210_func, args=(control_state, q))
    GS210.start()
    
    Magnet = threading.Thread(target=virtual_Magnet_func, args=(control_state, q))
    Magnet.start()
    
    LI5650 = threading.Thread(target=virtual_LI5650_func, args=(measure_state, ))
    LI5650.start()

    SR830 = threading.Thread(target=virtual_SR830_func, args=(measure_state, ))
    SR830.start()

    N5244A = threading.Thread(target=virtual_N5244A_func, args=(measure_state, ))
    N5244A.start()
    
    while True:
        q.get()
        measure_result(control_state, measure_state)
        
