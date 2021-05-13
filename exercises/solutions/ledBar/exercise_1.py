#
# Solution de l'exercice_2: LED clignotant
# Changez le numero de pin GPIO pour essayer chaque LED de la barre LED
# U. Raich 27. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms

LED_PIN = 27  # changez ce numero de pin pour verifier que chaqu'un des LEDs
              # marche comme attendu

led = Pin(LED_PIN,Pin.OUT)

for _ in range(5):
    led.on()
    sleep_ms(500)
    led.off()
    sleep_ms(500)
