#
# Solution de l'exercice_4: LED clignotant en SOS
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime   import sleep_ms

LED_PIN = 2
SHORT = 200
LONG  = 500

led = Pin(LED_PIN,Pin.OUT)

def blink(duration):
    led.on()
    sleep_ms(duration)
    led.off()
    sleep_ms(duration)

try:
    while True:
        for _ in range(3):     # S
            blink(SHORT)

        for _ in range(3):     # O
            blink(LONG)
       
        for _ in range(3):     # S
            blink(SHORT)

        sleep_ms(1000)
        
except KeyboardInterrupt:
    led.off()
