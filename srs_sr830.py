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
        self.sr830 = self.rm.open_resource('GPIB0::12')
        self.sr830.read_termination = '\n'
        self.sr830.write_termination = '\n'
        
    def initialize(self):
        srate = 'SRAT' + str(self.sample_rate[13])
        self.sr830.timeout = 20000
        self.sr830.write('OUTX 1')       #Set the Output Interface to GPIB (1).
        self.sr830.write('*CLS')         #Clear all status bytes.
        self.sr830.write('REST')
        self.sr830.write('FREQ 1500')
        self.sr830.write('SEND 1')       #Set the End of Scan mode to Loop (1).
        self.sr830.write(srate)          #Set the Data Sample Rate 16 Hz.

    def reset():
        self.sr830.write('*RST')
                
    def time_constant(self, tc_index):
        tc_response = [0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.5, 1.5,
                       5, 15, 50, 150, 500, 1500, 5000, 15000, 50000, 150000]
        time_wait = tc_response[tc_index]
        time.sleep(time_wait) 

    def measure(self, acqt):
        self.sr830.write('STRT')
        time.sleep(acqt)
        self.sr830.write('PAUS')
        self.sr830.write('SPTS?')
        time.sleep(0.1)
        length = self.sr830.read()
        readbuff_ch1 = 'TRCA? 1,0,'+ length
        self.sr830.write(readbuff_ch1)
        time.sleep(0.1)
        y_result = self.sr830.read()
        time.sleep(0.1)
        y_list = y_result.split(',')
        del y_list[-1]        
        for i in range(len(y_list)):
            y_list[i] = float(y_list[i])
        self.sr830.write('REST')
        mean = statistics.mean(y_list)

        return mean
        
