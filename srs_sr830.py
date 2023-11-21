# encoding: utf-8

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import pyvisa as visa
import statistics
import time

class LIA_SR830():

    '''
        A command to the sr830 consists of a four character command mnemonic
        with optional ?, arguments if necessary, and a command terminator.
        The command, arguments and terminator may be separated by spaces. The
        terminator must be a linefeed <LF> or carriage return <CR> on RS232,
        or a linefeed <LF> or EOI on GPIB. No command processing occurs until
        a terminator is received

        Examples of Commands
        --------------------
        FMOD 1 <LF>      Set Reference Mode to Internal
        FREQ 27E5 <LF>   Set the internal reference frequency to 27E5 Hz (2.7 MHz)
        *IDN? <LF>       Query the device identification
        
        
       Variables:  ch              output channel (1=CH1, 2=CH2)
                    i,j,k,l,m,n,q   integers
                    x,y,z           real numbers
                    f               real number frequency in Hz                    
                    s               text string

        Commands:
        - Reference and phase.
        - Signal Input.
        - Gain and time constant.
        - Display and output.
        - Aux input and output.
        - Setup.
        - Auto.
        - Scan and Rel.
        - Data storage.
        - Data transfer.
        - Interface.
        - Status reporting.
    '''

    sensitivity = ["100 nVrms / -127 dBm", "300 nVrms / -117 dBm",
               "1 µVrms / -107 dBm", "3 µVrms / -97 dBm",
               "10 µVrms / -87 dBm", " 30 µVrms / -77 dBm",
               "100 µVrms / -67 dBm", "300 µVrms / -57 dBm",
               " 1 mVrms / -47 dBm", " 3 mVrms / -37 dBm",
               " 10 mVrms / -27 dBm", "30 mVrms / -17 dBm",
               "100 mVrms / -7 dBm", "300 mVrms / +3 dBm",
               "1 Vrms / +13 dBm"]
    
    time_ct = ["100 us", "300 us", "1 ms", "3 ms", "10 ms",
               "30 ms", "100 ms", "300 ms", "1 s", "3 s",
               "10 s", "30 s", "100 s", "300 s", "1 ks",
               "3 ks", "10 ks", "30 ks"]

    sample_rate = ["62.5 mHz", "125 mHz", "250 mHz", "500 mHz", "1 Hz",
                "2 Hz", "4 Hz", "8 Hz", "16 Hz", " 32 Hz", "64 Hz",
                "128 Hz", "256 Hz", "512 Hz", "Trigger"]

    def __init__(self):
        super().__init__()
        self.brand = 'Stanford Research Systems'
        self.model = 'sr830'

    def gpib_set_up(self):
        self.rm = visa.ResourceManager()
        self.sr830 = self.rm.open_resource('GPIB0::8') #Set gpib address
        self.sr830.read_termination = '\n'
        self.sr830.write_termination = '\n'
        
    def initialize(self):
        self.sr830.timeout = 20000
        self.sr830.write('OUTX 1')       #Set the Output Interface to GPIB (1).
        self.sr830.write('*CLS')         #Clear all status bytes.
        self.sr830.write('REST')         #Reset the scan. All stored data is lost.
        self.sr830.write('SEND 1')       #Set the End of Scan mode to Loop (1).
        self.sr830.write('SRAT 13')      #Set the Data Sample Rate to 512 Hz

    def reset(self):
        self.sr830.write('*RST')         #Reset to default configuration
                
    def time_constant(self, tc_index):
        tc_response = [0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.5, 1.5,
                       5, 15, 50, 150, 500, 1500, 5000, 15000, 50000, 150000]
        time_wait = tc_response[tc_index]
        time.sleep(time_wait) 

    def measure(self, channel, acqstn_time):
        self.sr830.write('STRT')         #Start or continue a scan
        time.sleep(acqstn_time)          #wait measuring
        self.sr830.write('PAUS')         #Pause during a scan.
        self.sr830.write('SPTS?')        #Query the number of points stored in the Display buffer
        time.sleep(0.1)
        length = self.sr830.read()       #read the number of points stored in the Display buffer
        if channel == 'ch1':
            read_buffer = 'TRCA? 1,0,'+ length
        elif channel == 'ch2':
            read_buffer = 'TRCA? 2,0,'+ length
        self.sr830.write(read_buffer)   #Query points from Display ch 1 buffer in ASCII floating point.
        time.sleep(0.1)
        y_result = self.sr830.read()     #Read points from Display ch 1 buffer in ASCII floating point.
        time.sleep(0.1)
        y_list = y_result.split(',')     #format data into a string list        
        del y_list[-1]
        for i in range(len(y_list)):
            y_list[i] = float(y_list[i]) #format data into a float list
        self.sr830.write('REST')         #Reset the scan. All stored data is lost.
        mean = statistics.mean(y_list)   #compute the mean of the data

        return mean
        
