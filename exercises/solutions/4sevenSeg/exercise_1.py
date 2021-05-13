#
# Solution de l'exercice_1: LEDs clignotant
# Ce programme allume chaque LED des 4 digits à sept segment
# Il a été developpé pour un affichage à cathode commun
# Pour un affichage à anode commun, le courant doit être inversé:
# digits[i] = on
# les leds: off
# Le dict digitTab contient les pin GPIO qui selectionne un des 4 digits
# Le dict ledTab contient les GPIO pour les 8 LED (7 segments + dp)
# U. Raich 3. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from machine import Pin
from utime import sleep_ms

def clear():
    for digit in digits:
        digitTab[digit].on()
    for key in seven_seg:
        ledTab[key].off()

digits = {0:25,1:26,2:16,3:17}

digitTab = {}
for digit in digits:
    digitTab[digit] = Pin(digits[digit],Pin.OUT)
    digitTab[digit].on()

seven_seg = {"a": 23, "b":13, "c":14, "d": 19, "e": 18, "f":5, "g":27, "dp":12}

ledTab = {}
for key in seven_seg:
    # print(key)
    ledTab[key] = Pin(seven_seg[key],Pin.OUT)

# Set digit to low to enable the digit
for i in range(4):
    # now cycle though all segments to make sure they are correctly connected
    clear()
    digitTab[i].off()
    for key in ledTab:
        ledTab[key].on()
        sleep_ms(500)
        ledTab[key].off()
        sleep_ms(500)
    
