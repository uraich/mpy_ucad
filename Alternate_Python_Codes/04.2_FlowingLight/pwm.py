from machine import Pin,PWM

class myPWM():
    def __init__(self, pwm0: int=15, pwm1: int=2, pwm2: int=0, pwm3: int=4, pwm4: int=5, pwm5: int=18, pwm6: int=19, pwm7: int=21):
        self.ledTab = {}
        self.ledTab[0].append(PWM(Pin(pwm0,10000)))
        self.ledTab[1].append(PWM(Pin(pwm1,10000)))
        self.ledTab[2].append(PWM(Pin(pwm2,10000)))
        self.ledTab[3].append(PWM(Pin(pwm3,10000)))
        self.ledTab[4].append(PWM(Pin(pwm4,10000)))
        self.ledTab[5].append(PWM(Pin(pwm5,10000)))
        self.ledTab[6].append(PWM(Pin(pwm6,10000)))
        self.ledTab[7].append(PWM(Pin(pwm7,10000)))
                                  
        
    def ledcWrite(self,chn,value):
        self.ledTab[chn].duty(value)
    
    def deinit(self):
        for chn in range(8):
            self.ledTab[chn].deinit()
