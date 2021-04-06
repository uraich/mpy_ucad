#
# Solution de l'exercice_5: une classe Led
# La classe doit être transferé dans /lib sur l'ESP32 avant utilisation:
# Si /lib n'existe pas encore sur le ESP32:
# ampy mkdir /lib
# ampy put Led.py /lib/Led.py
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime   import sleep_ms

OFF = False
ON  = True

class Led():

    def __init__(self,ledPinNo=2):         # l'utilisateur peut definir la pin
                                           # par default c'est pin 2
        self.led = Pin(ledPinNo,Pin.OUT)
        self.led.off()                     # eteint la LED au début

        self.ledState=OFF

    def on(self):
        self.led.on()
        self.ledState=ON

    def off(self):
        self.led.off()
        self.ledState=OFF

    def toggle(self):
        if self.ledState:
            self.off()
        else:
            self.on()

    def state(self):
        return self.ledState
        
