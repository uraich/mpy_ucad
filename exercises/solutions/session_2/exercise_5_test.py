#
# Solution de l'exercice_5, deuxième partie:
# Ce programme essaie tout la fonctionalité de la classe Led
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from Led import Led
from utime import sleep_ms

led = Led()         # crée une instance de la classe Led

def print_state():  # imprime l'état de la LED
    if led.state():
        print("LED is on")
    else:
        print("LED is off")
        
print("Switch LED on")
led.on()            # enclenche la LED
sleep_ms(1000)
print("Switch LED off")
led.off()           # déclenche la LED
sleep_ms(1000)

print("Toggle LED and print its state")
led.toggle()
print_state()
sleep_ms(1000)
led.toggle()
print_state()
sleep_ms(1000)
led.off()
