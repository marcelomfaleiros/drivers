# encoding: utf-8

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import pyvisa as visa
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

    snstvt = ["100 nVrms / -127 dBm", "300 nVrms / -117 dBm",
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

    smpl_rat = ["62.5 mHz", "125 mHz", "250 mHz", "500 mHz", "1 Hz",
                "2 Hz", "4 Hz", "8 Hz", "16 Hz", " 32 Hz", "64 Hz",
                "128 Hz", "256 Hz", "512 Hz", "Trigger"]

    def __init__(self):
        super().__init__()
        self.brand = 'Stanford Research Systems'
        self.model = 'sr830'

    def ref_phas():        
        '''REFERENCE and PHASE COMMANDS
           ============================
       
        FMOD (?) {i}    Set (Query) the Reference Source to External (0) or Internal (1)
        HARM (?) {i}    Set (Query) the Detection Harmonic to 1 ≤ i ≤ 19999 and i•f ≤ 102 kHz.
        FREQ (?) {f}    Set (Query) the Reference Frequency to f Hz. Set only in Internal reference mode.        
        FRAQ?           Query the reference frequency.                 
        FRIQ?           Query the IF frequency. 
        PHAS (?) {x}    Set (Query) the detection phase, in degrees, relative to the reference. 
        APHS            Perform the Auto Phase function. 
        REFZ(?){i}      Set (Query) the Reference Input impedance. i selects 50 Ω (i=0) or 10 kΩ (i=1).
        '''
        pass
    
    def input_filter():    
                    
        '''SIGNAL INPUT 
           ============
    
        WRSV(?){i}    Set (Query) the Wide Reserve Mode of the instrument. High Reserve (i=0),
                      Normal (i=1), or Low Noise (minimum wide reserve) (i=2).
        AWRS          Perform the Auto Wide Reserve function. 
        INPZ(?){i}    Set (Query) the Signal Input impedance. 50 Ω (i=0) or 1 MΩ (i=1).
        '''
        pass

    def gain_timeconstant():
                    
        '''GAIN and TIME CONSTANT COMMANDS
           ===============================
    
        SENS (?) {i}    Set (Query) the sensitivity. The parameter i
                        selects a sensitivity below.

                                i Sensitivity               i Sensitivity
                                0 100 nVrms / -127 dBm      8 1 mVrms / -47 dBm
                                1 300 nVrms / -117 dBm      9 3 mVrms / -37 dBm
                                2 1 µVrms / -107 dBm       10 10 mVrms / -27 dBm
                                3 3 µVrms / -97 dBm        11 30 mVrms / -17 dBm
                                4 10 µVrms / -87 dBm       12 100 mVrms / -7 dBm
                                5 30 µVrms / -77 dBm       13 300 mVrms / +3 dBm
                                6 100 µVrms / -67 dBm      14 1 Vrms / +13 dBm
                                7 300 µVrms / -57 dBm
                        
        AGAN            Perform the Auto Sensitivity function. Check the Interface Ready bit (bit
                        1) in the Serial Poll Status to determine when the command is finished.
        CRSV(?){i}      Set (Query) the Close Dynamic Reserve Mode. High Reserve (i=0), Normal (i=1),
                        or Low Noise (minimum close reserve) (i=2).
        ACRS            Perform the Auto Close Reserve function. 
        OFLT (?) {i}    The OFLT command sets or queries the time constant. The parameter i
                        selects a time constant below.
                                i    time constant    i    time constant
                                0       100 µs        9         3 s 
                                1       300 µs        10       10 s
                                2         1 ms        11       30 s
                                3         3 ms        12      100 s
                                4        10 ms        13      300 s
                                5        30 ms        14       1 ks
                                6       100 ms        15       3 ks 
                                7       300 ms        16      10 ks 
                                8         1 s         17      30 ks                                                  
        OFSL (?) {i}    Set (Query) the Low Pass Filter Slope to 6 (0), 12 (1), 18 (2) or 24 (3) dB/oct.
        SETL(?)         Reset the Elapsed Time counter to zero, while the SETL?
                        query returns the Elapsed Time as a real number, in units of the current Time
                        Constant, since either the last SETL command or since the Settle... key was
                        pressed. The SETL? query does not reset the Elapsed Time counter.
        '''
        pass

    def display_output():
                    
        '''DISPLAY and OUTPUT COMMANDS
           ===========================
    
        DDEF (?) ch {,q}        Set (Query) the CH1 or CH2 (i=1,2) display to XY, Rθ, XnYn, Aux 1,3 or Aux 2,4 (j=0..4)
                                and ratio the display to None, Aux1,3 or Aux 2,4 (k=0,1,2).
                                          Channel 1 (ch=1)        Channel2 (ch=2)
                                        q    display         q    display
                                        0    X               0       Y
                                        1    R [Volts rms]   1       θ
                                        2    R [dBm]         2       Y Noise [Volts]
                                        3    X noise         3       Y Noise [dBm]
                                        4    Aux In 1        4       Aux In 2
        DRAT(?){i}              Set (Query) the instrument ratio mode. 
                                The DRAT i command sets the ratio mode as listed below.
                                                    i Ratio
                                                    0 none
                                                    1 ÷ AUX IN 1
                                                    2 ÷ AUX IN 2                                
        FPOP (?) ch{,i}         The FPOP command sets or queries the front panel (CH1 and CH2)
                                output sources. The parameter i selects CH1 (i=1) or CH2 (i=2)
                                and is required. The FPOP i, j command sets output i to quantity j
                                where j is listed below.
                                            CH1 (i=1)               CH2 (i=2)
                                        j   output quantity      j  output quantity
                                        0   CH 1 Display         0  CH 2 Display
                                        1   X                    1  Y
                                        
        DOFF(?) ch,q{,x}        Set (Query) the Offset for the quantity specified by ch,q
                                in the table below. The offset x is specified in % of full scale. The allowed ranges
                                for x are specified in the table below.
                                    ch,q quantity x unit
                                    1,0 X –110 to +110 % of full scale
                                    1,1 R[V] –110 to +110 % of full scale
                                    1,2 R[dBm] –110 to +110 % of 200 dBm
                                    2,0 Y –110 to +110 % of full scale
                                    4-16 Display and Output

        AOFF ch,q               Automatically offsets the chosen quantity to zero. 
        DEXP(?) ch,q{,i}        Set (Query) the output Expand of the display quantity. i specifies No Expand (0),
                                ×10 (1) or ×100 (2).
        '''
        pass

    def aux_in_out():
                            
        '''AUX INPUT and OUTPUT COMMANDS
           =============================
    
        AUXI? i           Query the value of Aux Input i (1,2).
        AUXO (?) i{,x}    Set (Query) voltage of Aux Output i (1,2) to x Volts. -10.500 ≤ x ≤ 10.500. 
        ''' 
        pass

    def setup(self):
                        
        '''SETUP COMMANDS
           ==============    
        OUTX (?) {i}    Set (Query) the Output Interface to RS232 (0) or GPIB (1).
        OVRM i          Set (Query) the GPIB Overide Remote state to Off (0) or On (1).
        KCLK (?) {i}    Set (Query) the Key Click to Off (0) or On (1).
        ALRM (?) {i}    Set (Query) the Alarms to Off (0) or On (1).
        SSET i          Save current setup to setting buffer i (1≤i≤9).
        RSET i          Recall current setup from setting buffer i (1≤i≤9).
        '''
        srate = 'SRAT' + str(sample_rate[spl_rt])
        #self.sr830.timeout = 300000   #2x the largest time to wait
        stp = ['OUTX 1', '*CLS', srate, 'RMOD 1', 'SEND 0']
        for i in stp:
            self.sr830.write(i)
            time.sleep(0.2)

    def auto():
        '''AUTO FUNCTIONS
           ==============
    
        AWRS         Perform the Auto Wide Reserve function. 
        ACRS         The ACRS command performs the Auto Close Reserve function. 
        AGAN         Perform the Auto Sensitivity function. 
        APHS         Perform the Auto Phase function. 
        AOFF ch,q    Automatically offsets the chosen quantity to zero. 
                                    ch,q Quantity
                                        1,0 X
                                        1,1 R[V]
                                        1,2 R[dBm]
                                        2,0 Y        
        '''
        pass

    def scan_rel():
        '''SCAN AND REL FUNCTION
           =====================
    
        SSTR(?){f}      Set (Query) the Scan Start Frequency. The parameter f
                        is a real number of Hz. The Start Frequency may not be set while a scan is in
                        progress.
        SFIN(?){f}      Set (Query) the Scan Stop Frequency. The parameter f
                        is a real number of Hz. The Stop Frequency may not be set while a scan is in
                        progress.
        SSTP(?){i}      Set (Query) the Number of Scan Points. The parameter
                        i is 2 ≤ i ≤ 11. The Number of Points may not be set while a scan is in
                        progress.
        SMOD(?){i}      Set (Query) the current scan point.
                        SMOD i moves to point i (1 ≤ i ≤ N) in the scan where N=Number of Scan
                        Points. Use SMOD to move from scan frequency to scan frequency (in any order).
                        SMOD 0 exits Scan Mode.
        RSTO i          Store XY (i=1) or R[dBm]θ (i=2) Rel Values along with
                        the measurement configuration at the current frequency.
        RRDY? i         Queriy whether any Rel Values are stored for the current
                        frequency. XY (i=1) or R[dBm]θ (i=2). RRDY? i returns 0 (no Rel Values) or 1 (Rel Values stored).
        RCLR            The RCLR command clears all stored Rel Values and Configurations.
        RMOD(?){i}      The RMOD command sets and queries REL MODE Off (i=0) or On (i=1).'''
        pass

    def data_storage():
        '''DATA STORAGE COMMANDS
           =====================

        SRAT (?) {i}    The SRAT command sets or queries the data sample rate. The parameter i
                        selects the sample rate listed below.
                                    i  quantity        i  quantity
                                    0  62.5 mHz        7    8 Hz
                                    1  125 mHz         8   16 Hz
                                    2  250 mHz         9   32 Hz
                                    3  500 mHz        10   64 Hz
                                    4    1 Hz         11  128 Hz
                                    5    2 Hz         12  256 Hz
                                    6    4 Hz         13  512 Hz
                                                      14  Trigger
        SEND (?) {i}    Set (Query) the Data Scan Mode to 1 Shot (0) or Loop (1). 
        TRIG            Software trigger command. Same as trigger input.
        TSTR (?) {i}    Set (Query) the Trigger Starts Scan modeto No (0) or Yes (1).
        STRT            Start or continue a scan.
        PAUS            Pause a scan. Does not reset a paused or done scan.
        REST            Reset the scan. All stored data is lost.
        '''
        pass

    def data_transfer():
        '''DATA TRANSFER COMMANDS
           ======================
    
        OUTP ? i                Query the value of X (1), Y (2), R (3) or q (4). Returns ASCII floating point value.
        OUTR ? i                Query the value of Display i (1,2). Returns ASCII floating point value.
        SNAP ? i,j {,k,l,m,n}   The SNAP? command records the values of either 2, 3, 4, 5 or 6
                                parameters at a single instant. For example, SNAP? is a way to
                                query values of X and Y (or R and θ) which are taken at the same
                                time. This is important when the time constant is very short. Using
                                the OUTP? or OUTR? commands will result in time delays, which may
                                be greater than the time constant, between reading X and Y (or R
                                and θ). The SNAP? command requires at least two parameters and at
                                most six parameters. The parameters i, j, k, l, m, n select the
                                parameters below.
                                        i,j,k,l,m,n        parameter
                                        1                      X
                                        2                      Y
                                        3                      R
                                        4                      θ
                                        5                      Aux In 1
                                        6                      Aux In 2
                                        7                      Aux In 3
                                        8                      Aux In 4
                                        9                      Reference Frequency
                                        10                     CH1 display
                                        11                     CH2 display
                                The requested values are returned in a single string with the
                                values separated by commas and in the order in which they were
                                requested. For example, the SNAP?1,2,9,5 will return the values of
                                X, Y, Freq and Aux In 1. These values will be returned in a single
                                string such as "0.951359,0.0253297,1000.00,1.234". The first value
                                is X, the second is Y, the third is f, and the fourth is Aux In 1.

                                The values of X and Y are recorded at a single instant. The values
                                of R and θ are also recorded at a single instant. Thus reading X,Y
                                OR R,θ yields a coherent snapshot of the output signal. If X,Y,R
                                and θ are all read, then the values of X,Y are recorded
                                approximately 10µs apart from R,θ. Thus, the values of X and Y may
                                not yield the exact values of R and θ from a single SNAP? query.

                                The values of the Aux Inputs may have an uncertainty of up to 32µs.
                                The frequency is computed only every other period or 40 ms, whichever is
                                longer.
                                The SNAP? command is a query only command. The SNAP? command
                                is used to record various parameters simultaneously, not to
                                transfer data quickly.
       
        SPTS ?                  Query the number of points stored in Display buffer.
        TRCA ? i, j, k          Read k>=1 points starting at bin j>=0 from Display i (1,2) buffer in ASCII floating point.
        TRCB ? i, j, k          Read k>=1 points starting at bin j>=0 from Display i (1,2) buffer in IEEE binary floating point.
        TRCL ? i, j, k          Read k>=1 points starting at bin j>=0 from Display i (1,2) buffer in non-normalized binary floating
                                point.                           
        FAST (?) {i}            The FAST command sets the data transfer mode on and off. The parameter i selects:
    
                                i=0: Off
                                i=1: On (DOS programs or other dedicated data collection computers)
                                i=2: On (Windows Operating System Programs)
                            
                                When the fast transfer mode is on, whenever data is sampled (during a scan), the
                                values of X and Y are automatically transmitted over GPIB (not available over RS232).
                                The sample rate sets the frequency of the data transfers. It is important that the
                                receiving interface be able to keep up with the transfers.
                            
                                To use the FAST2 mode, a ROM version of 1.06 or higher is required. The FAST2
                                version uses the lock-in transmit queue to buffer the GPIB data being sent to
                                the host.
                                Since the transmit queue can buffer a maximum of 63 X and Y data pairs, the host
                                can only be diverted for short periods of time (e.g. 120mS at 512Hz sample rate)
                                without causing the lock-in to "time out" and abort the FAST mode data transfer.
                            
                                The values of X and Y are transferred as signed integers, 2 bytes long (16 bits).
                                X is sent first followed by Y for a total of 4 bytes per sample. The values range
                                from -32768 to 32767. The value ±30000 represents ±full scale (i.e. the sensitivity).
                            
                                Offsets and expands are included in the values of X and Y. The transferred values are
                                (raw data - offset) x expand. The resulting value must still be a 16 bit integer.
                                The value ±30000 now represents ±full scale divided by the expand factor.
                                At fast sample rates, it is important that the receiving interface be able to keep
                                up. If the SR830 finds that the interface is not ready to receive a point, then the
                                fast transfer mode is turned off. The fast transfer mode may be turned off with the
                                FAST0 command.
                            
                                The transfer mode should be turned on (using FAST1 or FAST 2) before a scan is
                                started. Then use the STRD command (see below) to start a scan. After sending the
                                STRD command, immediately make the SR830 a talker and the controlling interface a
                                listener. Remember, the first transfer will occur with the first point in the scan.
                                If the scan is started from the front panel or from a trigger, then make sure that
                                the SR830 is a talker and the controlling interface a listener BEFORE the scan
                                actually starts.
        STRD                    Start a scan after 0.5sec delay. Use with Fast Data Transfer Mode.
        '''
        pass

    def interface(self):
        '''INTERFACE COMMANDS
           ==================
    
        ❊RST           Reset the unit to its default configurations.
        PRST            Power-on reset. Configuration, the DSP and programmable logic are re-loaded.
                        The next command (after IFC ready becomes set again) should be OUTX i.
        ❊IDN?          Read the SR830 device identification string.
        LOCL (?) {i}    Set (Query) the Local/Remote state to LOCAL (0), REMOTE (1), or LOCAL LOCKOUT (2).             
        OVRM (?) {i}    Set (Query) the GPIB Overide Remote state to Off (0) or On (1).
        '''
        interf_com = ['RST', 'PRST', '*IDN?', 'LOCL?', 'LOCL 0', 'LOCL 1', 'OVRM?', 'OVRM 0', 'OVRM 1']
        self.rm = visa.ResourceManager()
        self.sr830 = self.rm.open_resource('GPIB0::12')
        self.sr830.read_termination = '\n'
        self.sr830.write_termination = '\n'
        self.sr830.write('❊RST')

    def status_rep():
        '''STATUS REPORTING COMMANDS
           =========================
    
        The Status Byte definitions follow this section.
    
        ❊CLS                   Clear all status bytes.
        ❊ESE (?) {i} {,j}      Set (Query) the Standard Event Status Byte Enable Register to the decimal value i (0-255).
                                ❋ESE i,j sets bit i (0-7) to j (0 or 1). ❋ESE? queries the byte. ❋ESE?i queries only bit i.
        ❊ESR? {i}              Query the Standard Event Status Byte. If i is included, only bit i is queried.
        ❊SRE (?) {i} {,j}      Set (Query) the Serial Poll Enable Register to the decimal value i (0-255). ❋SRE i,j sets bit i (0-
                                7) to j (0 or 1). ❋SRE? queries the byte, ❋SRE?i queries only bit i.
        ❊STB? {i}              Query the Serial Poll Status Byte. If i is included, only bit i is queried.
        ❊PSC (?) {i}           Set (Query) the Power On Status Clear bit to Set (1) or Clear (0).

        ERRE (?) {i} {,j}       Set (Query) the Error Status Enable Register to the decimal value i (0-255). ERRE i,j sets bit i
                                (0-7) to j (0 or 1). ERRE? queries the byte, ERRE?i queries only bit i.
        ERRS? {i}               Query the Error Status Byte. If i is included, only bit i is queried.
        LIAE (?) {i} {,j}       Set (Query) the LIA Status Enable Register to the decimal value i (0-255). LIAE i,j sets
                                bit i (0-7) to j (0 or 1). LIAE? queries the byte, LIAE?i queries only bit i.
        LIAS? {i}               Query the LIA Status Byte. If i is included, only bit i is queried.
        '''
        pass
                
    def time_constant(self, tc_index):
        tc_response = [0.05, 0.05, 0.05, 0.05, 0.05, 0.15, 0.5, 1.5,
                       5, 15, 50, 150, 500, 1500, 5000, 15000, 50000, 150000]
        time_wait = tc_response[tc_index]
        time.sleep(time_wait)
  
    def gpib_set_up(self):
        self.rm = visa.ResourceManager()
        self.lia_sr830 = self.rm.open_resource('GPIB0::08')
        #self.lia_sr830.write('*RST')        
        self.lia_sr830.write_termination = '\n'
        self.lia_sr830.read_termination = '\n'

    def sr830_initialize():
        sr830.timeout = 20000
        sr830.write('OUTX 1')       #Set the Output Interface to GPIB (1).
        sr830.write('*CLS')         #Clear all status bytes.
        sr830.write('REST')
        sr830.write('FREQ 80000')
        sr830.write('SEND 1')       #Set the End of Scan mode to Loop (1).
        sr830.write('SRAT 11')      #Set the Data Sample Rate 16 Hz.

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
    
    #sr830.write('REST')
        
