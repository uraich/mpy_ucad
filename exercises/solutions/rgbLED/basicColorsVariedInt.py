from machine import Pin,PWM
from utime import sleep_ms

pins=[23,19,18]

#
# Solution de l'exercice_1: LED rgb, couleurs de base avec variation
# de l'intensité
# U. Raich 13. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

pwm0=PWM(Pin(pins[0]),10000)
pwm1=PWM(Pin(pins[1]),10000)
pwm2=PWM(Pin(pins[2]),10000)

def setColor(r,g,b):
    pwm0.duty(r)
    pwm1.duty(g)
    pwm2.duty(b)
    
for combination in range(1,8):
    for color in range(1024):
        if combination & 1:
            red = color
        else: 
            red = 0
        if combination & 2:
            green = color
        else: 
            green = 0
        if combination & 4:
            blue = color
        else: 
            blue = 0            
        setColor(red,green,blue)
        sleep_ms(10)
setColor(0,0,0)
