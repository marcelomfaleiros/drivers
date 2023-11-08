# encoding: utf-8

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import pyvisa as visa
import time

class SMC100CC():
    '''
    Command format:
    
    nnAAxx
    
    nn — Optional or required controller address.
    AA — Command name.
    xx — Optional or required value or “?” to query current value

    For example, a 1VA10 sets the velocity of the controller #1 to
    10 units/second. A 1VA? sends the response 1VA10

    AC  Set/Get acceleration 
    BA  Set/Get backlash compensation 
    BH  Set/Get hysteresis compensation
    DV  Set/Get driver voltage 
    FD  Set/Get low pass filter 
    FE  Set/Get following error limit 
    FF  Set/Get friction compensation     
    HT  Set/Get HOME search type 
    ID  Set/Get stage identifier 
    JD  Leave JOGGING state 
    JM  Enable/disable keypad 
    JR  Set/Get jerk time 
    KD  Set/Get derivative gain 
    KI  Set/Get integral gain 
    KP  Set/Get proportional gain 
    KV  Set/Get velocity feed forward 
    MM  Enter/Leave DISABLE state 
    OH  Set/Get HOME search velocity 
    OR  Execute HOME search 
    OT  Set/Get HOME search time-out 
    PA  Move absolute 
    PR  Move relative 
    PT  Get motion time for a relative move 
    PW  Enter/Leave CONFIGURATION state 
    QI  Set/Get motor’s current limits 
    RA  Get analog input value 
    RB  Get TTL input value 
    RS  Reset controller 
    SA  Set/Get controller’s RS-485 address 
    SB  Set/Get TTL output value 
    SC  Set/Get control loop state 
    SE  Configure/Execute simultaneous started move 
    SL  Set/Get negative software limit 
    SR  Set/Get positive software limit 
    ST  Stop motion 
    SU  Set/Get encoder increment value 
    TB  Get command error string
    TE  Get last command error 
    TH  Get set-point position 
    TP  Get current position 
    TS  Get positioner error and controller state
    VA  Set/Get velocity     
    VE  Get controller revision information 
    ZT  Get all axis parameters 
    ZX  Set/Get SmartStage configuration 
            
    Usage
    -----
    import newport_smc100cc as smc100
    import time

    smc = smc100.SMC100CC()
    smc.rs232_set_up()
    smc.command('1VA?')
    '''
           
    def __init__(self):
        self.brand = 'Newport'
        self.model = 'SMC100CC'
              
    def rs232_set_up(self):
        self.rm = visa.ResourceManager()
        self.rm.list_resources()
        self.ser = self.rm.open_resource('ASRL1::INSTR')
        self.ser.write_termination='\r\n'
        self.ser.read_termination='\r\n'
        self.ser.baud_rate = 57600
        self.ser.data_bits = 8
        self.ser.parity = visa.constants.Parity.none
        self.ser.stop_bits = visa.constants.StopBits.one
        self.ser.flow_control = visa.constants.VI_ASRL_FLOW_XON_XOFF
        self.ser.timeout = 25000
        #return self.com

    def initialization(self):
        self.ser.write('1OR')

    def configuration(self):
        n_limit = self.ser.query('1SL?')
        self.negative_limit = float(n_limit[-3:])
        print(self.negative_limit)
        p_limit = self.ser.query('1SR?')
        self.positive_limit = float(p_limit[-2:])
        print(self.positive_limit)
        self.ser.write('1PW?')
        print(self.ser.read())
        self.ser.write('1PW0')
        #print(self.ser.read())
        self.ser.write('1PW?')
        print(self.ser.read())

    def current_position(self):        
        self.curr_pos = self.ser.query('1TP?')
        self.curr_pos = float(self.curr_pos[-(len(self.curr_pos)-3):])
        return self.curr_pos        

    def move_abs_mm(self, apos_mm):          
        comm = '1PA' + str(apos_mm)
        self.ser.write(comm)
        while True:
            self.current_position()
            if self.curr_pos == float(apos_mm):
                break
        return comm

    def move_rel_mm(self, rpos_mm):
        comm = '1PR' + str(rpos_mm)
        self.ser.write(comm)
        while True:
            self.current_position()
            if self.curr_pos == float(rpos_mm):
                break
        return comm

    def move_abs_fs(self, apos_fs):
        target = round(0.0003 * apos_fs, 1)
        comm = '1PA' + str(target)
        self.ser.write(comm)
        while True:
            self.current_position()
            if self.curr_pos == float(target):
                break                      

    def move_rel_fs(self, rpos_fs):
        target = round(0.0003 * apos_fs, 1)
        comm = '1PR' + str(rpos_fs)
        self.ser.write(comm)
        while True:
            self.current_position()
            if self.curr_pos == float(target):
                break    

    def rs232_close():
        self.ser.close()
