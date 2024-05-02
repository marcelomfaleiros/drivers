# encoding: utf-8

"""
     Author: Marcelo Meira Faleiros
     State University of Campinas, Brazil

     """

import serial
import time

class Spex500():
    '''
    Controla o monocromador Spex 500 via porta GPIB ou RS232.

    -------------------------------------------------------------------------------------------------------
    Command                  | Host sends                  | Spex Controller sends              
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
                                                    Utility commands
    -------------------------------------------------------------------------------------------------------
    -------------------------------------------------------------------------------------------------------
    where am I: "<space>"    | 1. Command                  | 1. Program status      
    ---------------------------------------------------------------------------------------------------
                             | Send "<Space>"              | Receive Nothing if system is hung or;
                             |                             | "*" if autobauding is successful 1st time;
         Example:            |                             | "<escape>"+string if in Terminal mode;
                             |                             | "B" if in BOOT program;
                             |                             | "F" if in Main program 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    set intelligent mode:    | 1. Command                  | 1. No response at all
           "<248>"           |                             |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<248>"                | Receive nothing
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    set terminal mode: "<Y>" | 1. Command                  | 1. Confirmation             
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<Y>"                  | Receive "o"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    start main program:      | 1. Command                  | 1. Confirmation        
         "O2000<Null>"       |                             |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "O2000<Null>"          | Receive "<*>"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    reboot if hung: "<222>"  | 1. Command                  | 1. Nothing             
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<222>"                | Receive nothing
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    read main version:       | 1. Command                  | 1. Confirmation         
         "<z>"               |                             | 2. MAIN version number                                    
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<z>"                  | "o"
                             |                             | "V3.3<CR>" or similar response
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    read boot version:       | 1. Command                  | 1. Confirmation         
         "<y>"               |                             | 2. BOOT version number                                    
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<y>"                  | "o"
                             |                             | "V2.3<CR>" or similar response
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    change IEEE488 address:  | 1. Command                  | 1. Acknowledgement    
         "<E>"               | 2. New address in ASCII HEX |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "E3<Null>"             | Receive "<2>"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
                                                Grating Motor Commands
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor init:  "A"         | 1. Command                            | 1. Confirmation
         timeout = 100 s     |                                       |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "<A>"                            | Receive "o"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor set speed:  "B"    | 1. Command                            | 1. Confirmation
         timeout = 300 ms    | 2. Mono System #              [0]     |
                             | 3. Min Frequency Steps/Sec    [1000]  |
                             | 4. Max Frequency Steps/Sec    [36000] |
                             | 5. Ramp TimeMilliseconds (ms) [3000]  |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "B0,400,800,2000<CR>"            | Receive "o"                                 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor read speed: "C"    | 1. Command                            | 1. Confirmation 
         timeout = 300 ms    | 2. Mono System #[0..1]                | 2. Min Frequency Steps/Sec
                             |                                       | 3. Max Frequency Steps/Sec
                             |                                       | 4. Ramp TimeMilliseconds (ms)
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "C0<CR>"                         | Receive "o"
                             |                                       | Receive "400,800,2000<CR>" 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor busy check: "E"    | 1. Command                            | 1. Confirmation  
         timeout = 300 ms    |                                       |                                 
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "E"                              | Receive "o"
                             |                                       | Receive "q" 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor move relative: "F" | 1. Command                            | 1. Confirmation
         timeout = 300 ms    | 2. Mono System #[0..1]                | 
                             | 3. Steps to Move                      |
    ---------------------------------------------------------------------------------------------------
             Example:            | Send "F0,1000<CR>"                    | Receive "o"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor set position: "G"  | 1. Command                            | 1. Confirmation
         timeout = 300 ms    | 2. Mono System #[0..1]                | 
                             | 3. Mono step position                 |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "G0,1000000<CR>"                 | Receive "o"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor read position: "H" | 1. Command                            | 1. Confirmation  
         timeout = 300 ms    | 2. Mono System #[0..1]                | 2. Motor Step Position
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "H0<CR>"                         | Receive "o"
                             |                                       | Receive "1000000<CR>" 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor limit status: "K"  | 1. Command                            | 1. Confirmation 
         timeout = 300 ms    |                                       | 2. Motor Limit Status
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "K"                              | Receive "o"
                             |                                       | Receive "0<CR>" 
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------
    motor stop:   "L"        | 1. Command                            | 1. Confirmation
         timeout = 300 ms    |                                       |
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "L"                              | Receive "o"
    ---------------------------------------------------------------------------------------------------
    mirror exit side: "e"    | 1. Command                            | 1. Confirmation
    ---------------------------------------------------------------------------------------------------
         Example:            | Send "e0"                              | Receive "o"
    ---------------------------------------------------------------------------------------------------
    ---------------------------------------------------------------------------------------------------

    Usage
    -----

    import spex500 as spex
    spx = spex.Spex500()
    spx.set_up()
    spx.start_up()
    spx.calibration(400)
    spx.run(500)

    '''   
    
    def __init__(self):
        self.data = ['Spex', 'model 232', 's/n 0289']        
        
    def set_up(self):
        self.spex = serial.Serial(timeout = 25000)
        self.spex.port = 'COM3'
        self.spex.baudrate = 4800
        self.spex.bytesize = 8
        self.spex.parity = 'N'
        self.spex.stopbits = 1
        self.spex.rts = False
        self.spex.dtr = True
        
    def identity(self):   
        self.spex.write(b"z\r")     
        self.data.append(self.spex.read())                #read MAIN version number
        self.spex.write(b"y\r")
        self.data.append(self.spex.read())                #read BOOT version number
        return self.data    
 
    def start_up(self):    
        self.spex.write(b" \r")             #send WHERE AM I command
        self.spex.read()
        self.spex.write(b"247\r")           #set inteligent mode for rs232
        respWAI = self.spex.read()       #response will be "B" for BOOT or "F" for MAIN
        if respWAI == "B":
            self.spex.write(b"O2000" + ""+'\r')     #send "O2000<null>" - transfer control from BOOT to MAIN program
            self.spex.read()
        time.sleep(0.5)        
        self.spex.write(b"A\r")                    #initialize mono
        self.spex.read()
        self.spex.timeout = 30000
       
    def busy_status(self):
        self.spex.write(b"E\r")
        status = self.spex.read()
        while status != "oz":
            self.spex.write(b"E\r")                            #while motor busy
            status = self.spex.read()                #check motor status                                        
    
    def calibration(self, dsp_wavelength_A):    
        self.spex.write(b"B0,1000,36000,3000\r")   #set motor speed
        self.spex.read()
        Gwl = dsp_wavelength_A                  #wavelength (wl) A display
        Ground = round(Gwl * 4000)              #wl to steps conversion
        self.spex.write(b"G0," + str(Ground)+'\r')    #setting motor position
        self.spex.read()
  
    def run(self, F):                           #F = target wl
        self.spex.write(b"H0\r")                   #motor read position
        time.sleep(0.1)
        Houti = self.spex.read()
        Houticond = Houti[1:len(Houti)]         #motor position without termination character
        Hinti = int(Houticond)                  #convert to integer
        Froundi = round(F * 4000)               #convert target wl to steps
        Fin = Froundi - Hinti                   #compute steps to run
        if Fin < 0:                             #if target wl < current wl
            Fin = Fin - 20000                   #5nm backlash
            self.spex.write(b"F0," + str(Fin)+'\r')   #motor move relative
            time.sleep(0.1)
            self.spex.read()
            self.busy_status()                  #motor busy check  
            self.spex.write(b"F0," + str(20000)+'\r') #backlash
            self.spex.read()
            self.busy_status()
        else:
            self.spex.write(b"F0," + str(Fin)+'\r')   #if target wl > current wl
            time.sleep(0.1)
            self.spex.read()
            self.busy_status()

    def stop(self):
        self.spex.write(b"L")
        self.spex.read()