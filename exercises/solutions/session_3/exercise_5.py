#
# Solution de l'exercice_5: niveau de remplissage 
# Ceci est la classe de l'indicateur
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms

class LevelMeter():
    bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}

    def __init__(self):
        # init toutes les LEDs
        self.ledTab = {}
        for i in range(len(self.bar)):
            self.ledTab[i]=Pin(self.bar[i],Pin.OUT)
            # éteindre toutes les LEDs pour un début propre
            self.ledTab[i].off()

    def set_level(self,level):
        if level < 0 or level > 100:
            print("Niveau doit être donné en pourcentage (0..100)")
            return
        
        led_level = level//10
        # print(led_level)
        for i in range(10):
            if led_level > i:
                # print("Setting led %d on"%i)
                self.ledTab[i].on()
            else:
                # print("Setting led %d off"%i)
                self.ledTab[i].off()

level_meter = LevelMeter()

# test the level meter

for i in range(101):
    level_meter.set_level(i)
    sleep_ms(50)
sleep_ms(500)
# switch all leds off
print("set level 0")
level_meter.set_level(0)
