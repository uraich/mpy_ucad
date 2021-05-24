# shiftReg class
#
# A driver for the 74HC575 shift register

# Copyright (c) U. Raich, 23.5.2021
# The programm is part of the IoT course
# at the Université Cheikh Anta Diop, Dakar, Senegal

from machine import Pin
from utime import sleep_ms

class ShiftReg():
    def __init__(self,serial_in = 18, serial_clk = 19, register_clk = 5, clr = 23, oe = 13):
        self.ser_in = Pin(serial_in,Pin.OUT)
        self.ser_clk = Pin(serial_clk,Pin.OUT)
        self.reg_clk = Pin(register_clk,Pin.OUT)
        self.clr = Pin(clr,Pin.OUT)
        self.oe = Pin(oe,Pin.OUT)
        self.ser_in.off()
        self.ser_clk.off()
        self.clr.on()           # clr is active low
        self.oe.on()            # disable output
        
    def enable_output(self,yesno):
        if yesno:
            self.oe.off()
        else:
            self.oe.on()

    def transfer2reg(self):
        # transfer the data to the output register
        self.reg_clk.on()       
        self.reg_clk.off()
        
    def pulse_ser_clk(self):
        # pulse the serial clk
        self.ser_clk.on()       
        self.ser_clk.off()

    def clear(self):
        self.clr.off()      # clear the shift register
        self.clr.on()
        self.transfer2reg()
    
    def shift(self,bit):
        # set the bit
        if bit:
            self.ser_in.on()
        else:
            self.ser_in.off()
        #print(bit)
        
        self.pulse_ser_clk()
        shift_reg.transfer2reg()
        
    def display_val(self,val):
        if val < 0 or val > 1023:
            print ("Allowed values: 0..1023")
            return
        self.enable_output(False) # disable output until output register is ready 
        mask = 0x200
        for _ in range(10):
            if val & mask:
                self.shift(1)
            else:
                self.shift(0)
            mask >>=1
        self.enable_output(True)
        
#
# main program
#

shift_reg = ShiftReg()
shift_reg.clear()
shift_reg.enable_output(True)
for _ in range(10):
    shift_reg.shift(1)               # shift a 1 into the shift register
    sleep_ms(500)
    
for _ in range(10):
    shift_reg.shift(0)               # shift a 0 into the shift register
    sleep_ms(500)
    
shift_reg.clear()
print("Display 0x3f")
shift_reg.display_val(0x3ff)
sleep_ms(1000)

print("Display 0")
shift_reg.display_val(0)
sleep_ms(1000)

print("Display 0x2aa")
shift_reg.display_val(0x2aa)
sleep_ms(1000)

print("Display 0x155")
shift_reg.display_val(0x155)
sleep_ms(1000)

print("Flowing Water Light")

shift_reg.clear()
shift_reg.shift(1)               # shift a 1 into the first LED
sleep_ms(200)

for _ in range(10):
    # move from right to left
    for i in range(9):           # shifting in zeroes moves the lighted LED by 1 pos
        shift_reg.shift(0)
        sleep_ms(200)
    data = 0x100
    #move from left to right
    for i in range(9):
        shift_reg.display_val(data)
        data >>=1
        sleep_ms(200)
print("All done")        
shift_reg.clear()
