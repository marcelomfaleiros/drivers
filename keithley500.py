# encoding: utf-8

""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas, Brazil

"""

import serial
import time

class Keithley500():
    def __init__(self):
            
        self.ser = serial.Serial(timeout=10)

    def initialize_rs232(self, adress):
        self.ser.port = adress
        self.ser.baudrate = 9600
        self.ser.bytesize = 8
        self.ser.parity = 'N'
        self.ser.stopbits = 2
        self.ser.dsrdtr = True
        self.ser.rtscts = True

        self.ser.open()

    def initialize_keithley500(self):
        for i in range(5):
            self.ser.write(b'\r')
            time.sleep(0.1)

            self.ser.write(b'I')
            self.ser.write(b'EC;0')
            self.ser.write(b'H;1')
            self.ser.write(b'X;0')
            self.ser.write(b'TC;2')
            self.ser.write(b'TB;4')

            time.sleep(0.5)

            self.ser.write(b'C')

            self.ser.write(b'OA;09;IFC')

    def close_rs232(self):
        self.ser.close()
