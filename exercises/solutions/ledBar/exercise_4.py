#
# Solution de l'exercice_2: barre à LEDs 
# U. Raich 26. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms
class BinaryLed():
    bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}

    def __init__(self):
        self.leds = [None]*10
        for i in range(len(self.bar)):
            self.leds[i] = Pin(self.bar[i],Pin.OUT)

    def writeBin(self,value):
        if value > 0x3ff:
            print("Maximum value for 10 bits: 0x3ff or 1023")
            return
        mask = 1
        for i in range(10):
            if value & mask:
                self.leds[i].on()
            else:
                self.leds[i].off()
            mask <<= 1

binDisplay = BinaryLed()
for i in range(1024):
    binDisplay.writeBin(i)
    sleep_ms(50)
sleep_ms(200)
binDisplay.writeBin(0)
