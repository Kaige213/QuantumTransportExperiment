import json

configureParameters={
    "other": {
        "waitingTime": 0.05,
        "unit": "s"
    },
    "LI5650": {
        "ifRun": False,
        "address": "GPIB0::5::INSTR",
        "voltage": 1.0,
        "frequency": 17.7,
        "referenceSignal": "REF IN",
        "signalInput": "I",
        "filterSlope": "24 dB",
        "timeConstant": 1.0,
        "auto": True,
        "unit": "V"
    },
    "SR830": {
        "ifRun": True,
        "address": "GPIB0::5::INSTR",
        "voltage": 1.0,
        "frequency": 17.7,
        "phase": 0,
        "unit": "V"
    },
    "N5244A": {
        "ifRun"     : True,
        "address"   : "GPIB0::5::INSTR",
        "sweepType" : "CW", #or: frequence, or, power
        #CW
        "CW_frequence" : 1.0,
        "CW_ifPowerOn" : True,
        "CW_power"     : -10, #dBm
        #sweep power
        "power_points"   : 101,
        "power_frequence": 1,     #GHz
        "power_start"    : -10,   #dBm
        "power_stop"     : 0,     #dBm
        #sweep frequence
        "frequence_points": 101,
        "frequence_power" : -10,  #dBm
        "frequence_ifPowerOn": True,
        "frequence_start" : 1, #GHz
        "frequence_stop"  : 2, #GHz
        #public
        "ifAverage" :True,
        "averagingFactor":11,
        "IF_BW":10, #Hz
    },
    "GS610R": {
        "range": "2 V",
        "address": "GPIB0::5::INSTR",
        "unit": "V"
    },
    "GS610L": {
        "range": "110 V",
        "address": "GPIB0::5::INSTR",
        "unit": "V"
    },
    "GS210": {
        "range": "10 V",
        "address": "GPIB0::5::INSTR",
        "unit": "V"
    },
    "Magnet": {
        "sweepMode": "As Fast As Possible",
        "rate": 0.1,
        "address": "TCPIP0::127.0.0.1::5005::SOCKET",
        "ifPOC": False,
        "unit": "T"
    },
    "Time": {
        "address": "GPIB0::5::INSTR",
        "unit": "s"
    }
}

runningParameters={
    "GS610R": {
        "ifRun": True,
        "start": 1.0,
        "loop": "2->",
        "stop": 0.0,
        "current": 0,
        "points": 21,
        "step": -0.05
    },
    "GS610L": {
        "ifRun": False,
        "start": 10.0,
        "loop": "2->",
        "stop": 0.0,
        "current": 0,
        "points": 11,
        "step": -1.0
    },
    "GS210": {
        "ifRun": True,
        "start": 1.0,
        "loop": "3->",
        "stop": 0.0,
        "current": 0,
        "points": 11,
        "step": -0.1
    },
    "Magnet": {
        "ifRun": True,
        "start": 12.0,
        "loop": "1->",
        "stop": 0.0,
        "current": 0,
        "points": 101,
        "step": -0.12
    },
    "Time": {
        "ifRun": False,
        "start": 12.0,
        "loop": "5->",
        "stop": 0.0,
        "current": 0,
        "points": 5,
        "step": -3.0
    },
    "sweepBack": {
        "ifRun": True,
        "points": 101
    }
}

saveConfigure={
    "folderPath": "E:/PyTest/data6",
    "ifSave": True,
    "log": "Error info"
}

runConfigure={
    "numberOfCurves":11
}

parameters_initiate = {
  "configureParameters" : configureParameters,
  "runningParameters"   : runningParameters,
  "saveConfigure"       : saveConfigure,
  "runConfigure"        : runConfigure
}

with open("parameters_initiate.json", "w") as write_file:
    json.dump(parameters_initiate, write_file, indent=2)


#---- test part ----
#with open("parameters_initiate.json", "r") as read_file:
#    parameters_initiate_readout = json.load(read_file)
#index_str1 = "runningParameters"
#index_str2 = "Magnet"
#index_str3 = "step"
#print(parameters_initiate_readout[index_str1][index_str2][index_str3])
#print(type(parameters_initiate_readout[index_str1][index_str2][index_str3]))
