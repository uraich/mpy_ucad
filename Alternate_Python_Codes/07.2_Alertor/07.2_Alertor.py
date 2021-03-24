from machine import Pin,PWM
from math import sin,pi
from utime import sleep_ms

BUTTON_PIN = 22
BUZZER_PIN = 18

button=Pin(BUTTON_PIN,Pin.IN,Pin.PULL_UP)
passiveBuzzer=PWM(Pin(BUZZER_PIN),2000,512)

def alert():
    for x in range(0,36):
        sinVal=sin(x*10*pi/180)
        toneVal=2000+int(sinVal*500)
        print(toneVal)
        passiveBuzzer.freq(toneVal)
        sleep_ms(10)
try:
    while True:
        if not button.value():
            alert()   
        else:
            passiveBuzzer.freq(0)
except:
    passiveBuzzer.deinit()
