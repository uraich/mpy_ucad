# This is a slightly modified version of Freenove's 04.2FlowingLight.py example
# It has been extended from 8 LEDs to all 10 LEDs of the LED bar.
# The particular problem here is that only 8 PWM channels are available on the ESP32.
# Therefore 8 Leds are lighted with the light intensity given by the PWM duty cycle.
# The pwm channels for which the duty cycle value is zero are de-initialized to reduce the number
# of used PWM channels to eight.
# Copyright U. Raich, 26.4.2021
# The Program is released under the MIT licence

from machine import Pin,PWM
from pwm import myPWM
import time

class myPWM():
    
    bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}

    def __init__(self):
        self.pwmList = [None]*10

    def ledcWrite(self,valueTab):
        #print("value: ",value)
        for i in range(len(valueTab)):
            chn = valueTab[i][0]
            value = valueTab[i][1]
            # print("chn: {:d} value: {:d}".format(chn,value))
            # deinit unused pwm channels
            if value == 0:
                chn = valueTab[i][0]
                if self.pwmList[chn]:
                    # print("deinit channel ",chn)
                    self.pwmList[chn].deinit()
                    self.pwmList[chn] = None
                    led = Pin(self.bar[chn],Pin.OUT)
                    led.off()
        for i in range(len(valueTab)):
            if valueTab[i][1] != 0:
                chn = valueTab[i][0]              
                if not self.pwmList[chn]:
                    pwmLed = PWM(Pin(self.bar[chn]),10000)
                    self.pwmList[chn] = pwmLed
                self.pwmList[chn].duty(valueTab[i][1])
            
    def deinit(self):
        for i in range(len(self.pwmList)):
            if self.pwmList[i]:
                self.pwmList[i].deinit()

mypwm = myPWM()
chns=[0,1,2,3,4,5,6,7,8,9]
dutys=[0,0,0,0,0,0,0,0,0,0,1023,512,256,128,64,32,16,8,0,0,0,0,0,0,0,0,0,0,0,0]
delayTimes=50

valueTab = [None]*10

try:
    while True:
        for i in range(0,20):
            # print("cycle: ",i)
            for j in range(0,10):
                valueTab[j] = (chns[j],dutys[i+j])
                #print("value: {:d} on channel {:d}".format(dutys[i+j],chns[j]))
            mypwm.ledcWrite(valueTab)
            time.sleep_ms(delayTimes)
            
        for i in range(0,20):
            for j in range(0,10):
                valueTab[j] = (chns[9-j],dutys[i+j])
                # print("value: {:d} on channel {:d}".format(dutys[i+j],chns[j]))
            mypwm.ledcWrite(valueTab)
            time.sleep_ms(delayTimes)
except:
   mypwm.deinit()
