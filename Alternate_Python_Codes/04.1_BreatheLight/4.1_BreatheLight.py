from machine import Pin,PWM
from utime import sleep_ms

USER_LED_PIN = 2
FREQ         = 10000 # PWM fequency: 10 kHz
pwm          = PWM(Pin(USER_LED_PIN),FREQ,0)
 
print("PWM on the user led")
try:
    while True:
        for i in range(0,1023):
            pwm.duty(i)
            sleep_ms(1)
            
        for i in range(0,1023):
            pwm.duty(1023-i)
            sleep_ms(1)  
except:
    pwm.deinit()
