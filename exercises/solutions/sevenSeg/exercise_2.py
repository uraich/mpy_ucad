#
# Solution de l'exercice_2: LED clignotant
# Changez le numero de pin GPIO pour essayer chaque LED de l'affichage
# à sept segments
# U. Raich 3. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms

class HexDigit():
    # sept_seg est defini comme dict
    # la clef est le no du LED ("a".."g" et "dp"), la valeur est le no GPIO sur lequel
    # le LED est connecté

    sept_seg = {"a": 17, "b":16, "c":19, "d": 18, "e": 26, "f":22, "g":21, "dp":23}
    digits = [["a","b","c","d","e","f"],     # 0
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
        # init les GPIO pour chaque LED
        self.ledTab = {}
        for key in self.sept_seg:
            # print(key)
            self.ledTab[key] = Pin(self.sept_seg[key],Pin.OUT)

    def showDP(self,yesNo):
        if yesNo:
           self.ledTab["dp"].on()
        else:
            self.ledTab["dp"].off()
            
    def clear(self):
        for key in self.sept_seg:
            self.ledTab[key].off()
            
    def showDigit(self,digit):
        self.clear()
        for led in self.digits[digit]:
            self.ledTab[led].on()

hexDigit = HexDigit()
print("Switch every LED on and then off again")
for key in hexDigit.sept_seg:
    hexDigit.ledTab[key].on()
    sleep_ms(500)
    hexDigit.ledTab[key].off()
    sleep_ms(500)

print("show digits")
for i in range(16):
    hexDigit.showDigit(i)
    sleep_ms(1000)
print("Switch the decimal point")
hexDigit.showDP(True)
sleep_ms(1000)
hexDigit.showDP(False)
sleep_ms(1000)
print("Clear the display")
hexDigit.clear()
