#
# Solution de l'exercice_1: LED rgb, couleurs de base
# U. Raich 13. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin,PWM
from utime import sleep_ms

pins=[23,19,18]

leds = []

# etteindre toutes les LEDs
def clear():
    for led in leds:
        led.off()

for pin in pins:
    leds.append(Pin(pin,Pin.OUT))
    
clear()

try:
    while True:
        for color in range(1,8):
            mask = 1
            # controller les 3 LEDs
            for rgb in range(3):
                # si le bit == 1, allumer la LED
                if color & mask:
                    leds[rgb].on()
                    print(rgb," on")
                else:
                    leds[rgb].off()
                    print(rgb," off")
                mask <<= 1
            sleep_ms(500)
    
except KeyboardInterrupt:
    clear()

