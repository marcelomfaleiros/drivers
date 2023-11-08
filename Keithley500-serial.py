# encoding: utf-8
""" 
    Author: Marcelo Meira Faleiros
    State University of Campinas
    
"""

import serial
import time

ser = serial.Serial(timeout=10)

ser.port = 'COM1'
ser.baudrate = 9600
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 2
ser.dsrdtr = True
ser.rtscts = True

ser.open()

for i in range(5):
    ser.write(b'\r')
    time.sleep(0.1)

    ser.write(b'I')
    ser.write(b'EC;0')
    ser.write(b'H;1')
    ser.write(b'X;0')
    ser.write(b'TC;2')
    ser.write(b'TB;4')

    time.sleep(0.5)

    ser.write(b'C')

    ser.write(b'OA;09;IFC')

#ser.close()
