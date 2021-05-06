# IR class
#
# reads the IR remote control through a GPIO pin
# timeList keeps the intervals between signal changes
# ir_bitBuffer keeps the individual bits extracted from the pulse lengths
# read returns the IR code
# The program is based on 23.1_Infrared_Remote.py from the
# Freenove's Python tutorial, which is part of Freenove's ESP32 Ultimate starter kit

# Modifications by U. Raich
# for the IoT course at the Université Cheikh Anta Diop, Dakar, Senegal

from machine import Pin
from utime import ticks_us,ticks_diff,sleep_ms

class IR(object):
    def __init__(self, ir_gpio):
        # define IR data pin as input
        self.irRecv = Pin(ir_gpio, Pin.IN, Pin.PULL_UP)
        # define an interrupt handler that triggers on any state change
        # of the IR data line 
        self.irRecv.irq(
            trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING,
            handler=self.__irInt)
        self.logList = []
        self.index = 0
        self.start = 0

    def __irInt(self, source):
        pulseTime = ticks_us()
        if self.start == 0:
            self.start = pulseTime
            self.index = 0
            return
        self.logList.append(ticks_diff(pulseTime, self.start))
        self.logList
        self.start = pulseTime
        self.index += 1

    def read(self):
        sleep_ms(200) 
        if ticks_diff(
                ticks_us(),
                self.start) > 800000 and self.index > 0:
            self.bitBuffer=[]
            try:
                for i in range(3,66,2):
                    if self.logList[i]>800:
                        self.bitBuffer.append(1)
                    else:
                        self.bitBuffer.append(0)
            except:
                print("IR read error, please try again")
                return
            irValue=0
            # get 32 bits
            if len(self.bitBuffer) < 32:
                print("read error, length of IR buffer is {:d}".format(len(self.bitBuffer)))
                return
            for i in range(0,32):
                irValue=irValue<<1
                if self.bitBuffer[i]==1:
                    irValue |= 1
                    
            # reset
            self.timeList = self.logList
            self.logList = []
            self.index = 0
            self.start = 0
            return irValue
