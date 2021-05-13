#
# Solution de l'exercice_2: LED en movement
# Ceci est le programme qui appelle les méthodes de la classe ShiftLed 
# U. Raich 6. Avril 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from shiftLed import ShiftLed

shift = ShiftLed()
print("5 cycles gauche à droite")
for i in range(5):
    shift.oneCycle()

shift.set_dir(shift.RIGHT_TO_LEFT)
print("5 cycles droite à gauche")
for i in range(5):
    shift.oneCycle()

shift.set_dir(shift.LEFT_TO_RIGHT)
print("5 cycles gauche à droite avec une vitesse plus élevé")
shift.set_speed(50)
for i in range(5):
    shift.oneCycle()
    
shift.set_dir(shift.RIGHT_TO_LEFT)
print("5 cycles droite à gauche plus lentes")
shift.set_speed(500)
for i in range(5):
    shift.oneCycle()