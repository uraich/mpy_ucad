#
# Solution de l'exercice_2: LED clignotant
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime   import sleep_ms

LED_PIN = 2             # défini comme variable pour être changé plus facilement
                        # si une autre carte avec une LED connecté sur une autre
                        # pin GPIO est utilisé

led = Pin(LED_PIN,Pin.OUT) # GPIO pin est programmé comme sortie

try:
    while True:
        led.on()
        sleep_ms(500)
        led.off()
        sleep_ms(500)
except KeyboardInterrupt:
    led.off()            # eteint la LED avant de sortir du programme
