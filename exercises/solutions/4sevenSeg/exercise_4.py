#
# Solution de l'exercice_3: Flowing Digit avec asyncio co-routine
#
# U. Raich 4. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms
import uasyncio as asyncio

class HexDisplay():
    digits = {0:17,1:16,2:26,3:25}
    seven_seg = {"a": 23, "b":13, "c":14, "d": 19, "e": 18, "f":5, "g":27, "dp":12}
    digitVals = [["a","b","c","d","e","f"],     # 0
                 ["b","c"],                     # 1
                 ["a","b","g","e","d"],         # 2
                 ["a","b","c","d","g"],         # 3
                 ["f","g","b","c"],             # 4
                 ["a","f","g","c","d"],         # 5
                 ["a","f","g","c","d","e"],     # 6
                 ["a","b","c"],                 # 7
                 ["a","b","c","d","e","f","g"], # 8
                 ["a","b","c","f","g"],         # 9
                 ["a","b","c","e","f","g"],     # A
                 ["f","e","g","c","d"],         # b
                 ["a","f","e","d"],             # C
                 ["b","c","d","e","g"],         # d
                 ["a","f","g","d","e"],         # E
                 ["a","f","g","e"]]             # F
    
    def __init__(self):
        # initilize the GPIO pins selecting the digits
        self.digitTab = {}
        for digit in self.digits:
            self.digitTab[digit] = Pin(self.digits[digit],Pin.OUT)
        # initialize the digits controlling the LEDs
        self.ledTab = {}
        for key in self.seven_seg:
            # print(key)
            self.ledTab[key] = Pin(self.seven_seg[key],Pin.OUT)
        self.value = 0
        self.clear()
        self.dp=[False,False,False,False]
        #
        # start the co-routine refreshing the digits
        #
        asyncio.create_task(self.showValue())
        
    # clear all digits    
    def clear(self):
        for digit in self.digits:
            self.digitTab[digit].on()
        for key in self.seven_seg:
            self.ledTab[key].off()

    def setHexValue(self,value):
        if value > 0xffff or value < 0:
            print("Number cannot be displayed as hex number")
            return
        # print("Setting value to 0x{:04x}".format(value)) 
        self.value = value

    def setDecValue(self,value):
        if value > 0x9999 or value < 0:
            print("Number cannot be displayed as decimal number")
            return
        # print("Setting value to  0x{:04x}".format(hex2BCD(value)))
        self.value = self.hex2BCD(value)
        
    async def showValue(self):
        # print("showValue")
        # print("value: 0x{:x}".format(self.value))
        while True:
            mask = 0xf
            shift = 0
            for digit in range(4):
                digitValue = self.value & mask
                digitValue >>= shift
                # print("digit value: {:x}".format(digitValue))
                # print("shift: {:d}, mask: 0x{:x}".format(shift,mask))
                shift +=4
                mask <<= 4
                self.showHexDigit(digit,digitValue)
                await asyncio.sleep_ms(5)
            
    #
    # hex to BCD converter
    #
    def hex2BCD(self,value):
        thousands = value//1000
        value -= thousands*1000
        hundreds = value//100
        value -= hundreds*100
        tens = value//10
        value -= tens*10
        value = value | tens << 4 | hundreds << 8 | thousands << 12
        return value

    def showDP(self,digit,yes):
        self.dp[digit]=yes
        
    def showHexDigit(self,digit,value):
        # select only one digit
        # print(digit,value)
        self.clear()
        self.digitTab[digit].off()       # switch this digit on
        # display the number on the selected digit
        for key in self.seven_seg:
            if key in self.digitVals[value]:
                # print("Switch on ", self.ledTab[key])
                self.ledTab[key].on()
            else:
                # print("Switch off ", self.ledTab[key])
                self.ledTab[key].off()

        if self.dp[digit]:
            self.ledTab["dp"].on()
        else:
            self.ledTab["dp"].off()
  
