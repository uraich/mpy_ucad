#
# Solution de l'exercice_6: LED clignotant avec interruptions timer
# Ce programme utilise 2 timers:
# toggle_timer fait clignoter la LED 
# duration_timer arrète le toggle_timer et fait sortir du programme
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin,Timer
from utime   import sleep_ms
import sys

LED_PIN = 2             # défini comme variable pour être changé plus facilement
                        # si une autre carte avec une LED connecté sur une autre
                        # pin GPIO est utilisé

led = Pin(LED_PIN,Pin.OUT) # GPIO pin est programmé comme sortie

def toggle(timer):
    led.value(not led.value()) # lit l'état de la LED et change son état

def stop(timer):
    toggle_timer.deinit()      # arrète le toggle_timer et éteint la LED 
    led.off()
    
toggle_timer = Timer(0)
toggle_timer.init(mode=Timer.PERIODIC, period=500, callback = toggle) 

duration_timer = Timer(1) # definit la durée pendent laquelle nous faisons clignoter la LED (ici 10 s)    
duration_timer.init(mode=Timer.ONE_SHOT, period=10000, callback = stop)
