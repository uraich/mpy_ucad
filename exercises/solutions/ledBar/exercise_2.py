#
# Solution de l'exercice_2: barre à LEDs 
# U. Raich 26. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms

# bar est defini comme dict
# la clef est le no du LED (0..9), la valeur est le no GPIO sur lequel
# le LED est connecté

bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}

leds = [None]*10

for i in range(10):
    print("led %d is on GPIO %d"%(i,bar[i]))
    leds[i] = (Pin((bar[i]),Pin.OUT))
    leds[i].off()

for i in range(10):
    print("LED ",i,end=" ")
    print(leds[i])
    for _ in range(5):
        leds[i].on()
        sleep_ms(500)
        leds[i].off()
        sleep_ms(500)
    
for i in range(10):
    leds[i].on()
sleep_ms(500)
for i in range(10):    
    leds[i].off()
