import pyqtgraph as pg
from functools import partial
import pyvisa as visa
from pyvisa.constants import StopBits, Parity
import os
import time
import keyboard

rm = visa.ResourceManager()
keithley = rm.open_resource("COM6", baud_rate=9600, data_bits=8, parity=Parity.none, stop_bits=StopBits.one)
arduino = rm.open_resource("COM3", baud_rate = 9600)
arduino.write("4")

win = pg.GraphicsWindow(title="Signal from serial port") # creates a window
p = win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
curve = p.plot()    

windowWidth = 500                       # width of the window displaying the curve
Xm = linspace(0,0,windowWidth)          # create array that will contain the relevant time series     
ptr = -windowWidth                      # set first x position

x = []
y = []

#pw = pg.plot()
#timer = pg.QtCore.QTimer()

def keithley_setup():
   keithley.write("*RST") 
   keithley.write(":SOUR:FUNC VOLT")   
   keithley.write(":SOUR:VOLT:RANG:AUTO 1")
   keithley.write(":SENS:FUNC 'CURR:DC' ")
   keithley.write(":SENS:CURR:RANG:AUTO 1")
   keithley.write(":FORM:ELEM CURR")   
   keithley.write(":SENS:CURR:PROT 1")   
   keithley.write(":SOUR:DEL 0.5")

                    # create an empty "plot" (a curve to plot)

def update():
   x = []
   y = []
   Vi = 0
   Vf = 1
   Vstep = 0.1
   keithley_setup()     
   keithley.write(":SOUR:VOLT:LEV 0")
   keithley.write(":OUTP ON")    
   while (Vi <= Vf):
      if keyboard.is_pressed("Escape"):
            break
      meas = keithley.query(":MEAS?")      
      x.append(Vi)             
      y.append(float(meas))
      pw.plot(x, y, clear=True)
      Vi += Vstep      
      keithley.write(":SOUR:VOLT:LEV " + str(Vi))   
   keithley.write(":OUTP OFF")
   keithley.write(":SOUR:VOLT:LEV 0")
    
timer.timeout.connect(update)
timer.start(16)
