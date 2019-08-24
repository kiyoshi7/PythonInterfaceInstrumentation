# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 12:15:04 2019

@author: Daniel
"""

import serial
from serial.tools import list_ports
import time

class SerialConnection:
    Error = True
    EMsg = ""
    Device = ""
    Port=""
    Baud=0
    ID=""
    baudrates = [9600, 14400, 19200, 28800, 38400, 57600, 115200]
    def __init__(self):
        #Com. Data and registers
        self.CommTest = "sKIAjfrcfvmo2CbzOsogvkR9dm7ZOaSN"
        self.Connect()
        
        
    def Connect(self):
        self.MCU  = self.FindMCU()
        print(self.MCU)
        self.Port = self.MCU[0]
        self.Baud = self.MCU[1]
        if len(self.MCU)>= 0:
            self.Error = False
            self.SendData("0001")
            time.sleep(1)
            self.ID = self.ReadData()[0]
            self.Device.close()
            self.Device = serial.Serial(self.Port, baudrate=self.Baud, timeout=1);
        print('end ',self.MCU)
        #print("MCU found on port {}, baudrate {}.".format(MCU[0], MCU[1]))
    
    def Disconnect(self):
        self.Device.close()
        
    def HandleError(self,error):
        self.Error=True
        self.EMsg = "{}. line:{}".format(error, error.__traceback__.tb_lineno)
        return #self.EMsg
    
    def SendData(self, cmd):
        setTemp1 = str(cmd)+'\r\n'
        self.Device.write(setTemp1.encode())
        self.Device.flushInput()
        
    def ReadData(self):
        time.sleep(1)
        data=[]
        while self.Device.in_waiting:
            try:
                data.append(self.Device.readline().decode('utf-8').rstrip("\n\r"))
                data.append("123456789")
            except:
                pass
        return data
    
    def FindMCU(self):
        device = [p.device for p in serial.tools.list_ports.comports()]
        devicesAvailable = []
        # if no device is connected
        if len(device) == 0:
            import time
            print('please connect device')
            loop = True
            while loop:
                time.sleep(1)
                if len([p.device for p in serial.tools.list_ports.comports()]) != 0:
                    loop = False
                print('...', end ="")
            self.FindMCU()
        try:
            select = None
            # if one device is connected try to connect to it
            if len(device) == 1:
                select = device[0]
                #print ( serial.tools.list_ports.comports()[len(device)-1].description, 'connected' )
                return(self.FindBaud(serial.tools.list_ports.comports()[len(device)-1].device))
                
            #if more than one device is connected
            if len(device) > 1:
                print('Available devices: ')
                for i in range(len(device)):
                    devicesAvailable.append( device[i] )
                    print(i, serial.tools.list_ports.comports()[i].description )
                select = int(input('Select a device: '))
                print(serial.tools.list_ports.comports()[select].description, 'selected')
                return serial.tools.list_ports.comports()[select].device
                
        except Exception as a:
            self.HandleError(a)
            print('unable to connect to device')
            #FindMCU()
            
    def FindBaud(self, COMPORT):
        for i in self.baudrates:
            self.Device = serial.Serial(COMPORT, baudrate=i, timeout=1);
            self.Device.flushInput()
            din=0
            for j in range(3):
                self.SendData("0000")
                din=self.ReadData()
                print(din)
                if len(din) != 0:
                    din=din[0]
            if len(din) >> 0:         
                if din == self.CommTest :
                    return (COMPORT, i)
            self.Device.close()
