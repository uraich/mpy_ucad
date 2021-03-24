from machine import Pin,PWM
import time, sys
print("Testing the buzzer")
print("Program written for the workshop on IoT at the")
print("African Internet Summit 2019")
print("Copyright: U.Raich")
print("Released under the Gnu Public License")


print("Running on ESP32") 
pwmPin = Pin(18)
    
pwm=PWM(pwmPin)

pwm.freq(500)
pwm.duty(512)

time.sleep(1)
pwm.deinit()
