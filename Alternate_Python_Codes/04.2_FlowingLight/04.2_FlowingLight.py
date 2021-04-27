# Le programme 04.2FlowingLight de Freenove amelioré.
# Je me suis debarrassé des répétitions dans myPWM en utilisant un "dict"

from machine import Pin,PWM
from pwm import myPWM
import time

class myPWM():
    
    # Vous pouvez modifier les valeurs de paramètres par default ici ou vous pouvez specifier vous connexions
    # quand vous créez l'instance de la classe myPWM
    
    def __init__(self, pwm0: int=17, pwm1: int=16, pwm2: int=27, pwm3: int=14, pwm4: int=12, pwm5: int=13, pwm6: int=5, pwm7: int=23):
        self.ledTab = {}
        self.ledTab[0] = PWM(Pin(pwm0,10000))
        self.ledTab[1] = PWM(Pin(pwm1,10000))
        self.ledTab[2] = PWM(Pin(pwm2,10000))
        self.ledTab[3] = PWM(Pin(pwm3,10000))
        self.ledTab[4] = PWM(Pin(pwm4,10000))
        self.ledTab[5] = PWM(Pin(pwm5,10000))
        self.ledTab[6] = PWM(Pin(pwm6,10000))
        self.ledTab[7] = PWM(Pin(pwm7,10000))
        
    def ledcWrite(self,chn,value):
        self.ledTab[chn].duty(value)
    
    def deinit(self):
        for chn in range(8):
            self.ledTab[chn].deinit()
            
mypwm = myPWM()
chns=[0,1,2,3,4,5,6,7];
dutys=[0,0,0,0,0,0,0,0,1023,512,256,128,64,32,16,8,0,0,0,0,0,0,0,0];
delayTimes=50

try:
    while True:
        for i in range(0,16):
            for j in range(0,8):
                mypwm.ledcWrite(chns[j],dutys[i+j])
            time.sleep_ms(delayTimes)
            
        for i in range(0,16):
            for j in range(0,8):
                mypwm.ledcWrite(chns[7-j],dutys[i+j])
            time.sleep_ms(delayTimes)
except:
    mypwm.deinit()
