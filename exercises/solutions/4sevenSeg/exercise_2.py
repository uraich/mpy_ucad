#
# Solution de l'exercice_2: La classe HexDisplay
# La classe affiche des valeurs en hex ou en décimale sur une
# affichage à sept segments avec 4 digits
# Ce programme a été developpé pour un affichage à cathode commun
# Pour un affichage à anode commun, le courant doit être inversé:
# digits[i] = on
# les leds: off
# U. Raich 3. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms,sleep

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
        self.digitTab = {}
        for digit in self.digits:
            self.digitTab[digit] = Pin(self.digits[digit],Pin.OUT)
        self.ledTab = {}
        for key in self.seven_seg:
            # print(key)
            self.ledTab[key] = Pin(self.seven_seg[key],Pin.OUT)
        self.clear()
        
    # clear all digits
    def clear(self):
        for digit in self.digits:
            self.digitTab[digit].on()
        for key in self.seven_seg:
            self.ledTab[key].off()

    def showHexValue(self,value):
        # print("value: 0x{:x}".format(value))
        if value > 0xffff or value < 0:
            print("Number cannot ne displayed")
            return
        
        mask = 0xf
        shift = 0
        for digit in range(4):
            digitValue = value & mask
            digitValue >>= shift
            # print("digit value: {:x}".format(digitValue))
            # print("shift: {:d}, mask: 0x{:x}".format(shift,mask))
            shift +=4
            mask <<= 4
            self.showHexDigit(digit,digitValue)
            sleep_ms(5)
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
    
    def showDecValue(self,value):
        if value < 0 or value > 9999:
            print("Value cannot be displayed")
            return
        self.showHexValue(self.hex2BCD(value))
        
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
        

hexDisplay = HexDisplay()
hexDisplay.clear()
'''
for i in range(4):
    hexDisplay.clear()
    hexDisplay.showHexDigit(i,8)
    sleep_ms(500)
hexDisplay.clear()
'''
print("1234 in hex= 0x{:x}".format(1234))
for i in range(100):
    hexDisplay.showHexValue(1234)

print("1234 in dec= 0x{:d}".format(1234))
for i in range(100):
    hexDisplay.showDecValue(1234)
    
base = 0
while True:
    for i in range(16):
        if base > 15:
            base = 0
        value = base << 12 | ((base+1) % 16) << 8 | ((base+2) % 16) << 4 | (base+3) % 16
        base += 1

        for tim in range(25):       # showDigit takes 20 ms, we therefore show the number for 500 ms
            hexDisplay.showHexValue(value)


