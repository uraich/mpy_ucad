#
# Solution de l'exercice_2: LED en movement
# Ceci est la classe ShiftLed demandé
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#
from machine import Pin
from utime import sleep_ms

class ShiftLed():
    bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}
    LEFT_TO_RIGHT = True
    RIGHT_TO_LEFT = False
    MAX_LED = 10
    
    def __init__(self):
        # init toutes les LEDs
        self.ledTab = {}
        for i in range(len(self.bar)):
            self.ledTab[i]=Pin(self.bar[i],Pin.OUT)
            # éteindre toutes les LEDs pour un début propre
            self.ledTab[i].off()
        self.delay = 200
        self.dir = self.LEFT_TO_RIGHT

    def set_speed(self,delay):     # delay: temps entre deux états led en ms
        self.delay = delay

    def set_dir(self,direction):
        self.dir = direction
        
    def oneCycle(self):            # un cycle complèt 
        if self.dir == self.LEFT_TO_RIGHT:
            for i in range(self.MAX_LED):
                self.ledTab[i].on()
                sleep_ms(self.delay)
                self.ledTab[i].off()

        elif self.dir == self.RIGHT_TO_LEFT:
            for i in range (self.MAX_LED):
                self.ledTab[self.MAX_LED-i-1].on()
                sleep_ms(self.delay)
                self.ledTab[self.MAX_LED-i-1].off()

