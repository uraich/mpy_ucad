from machine import Pin,PWM,ADC
from utime import sleep_ms

USER_LED_PIN = 2
ADC_PIN      = 36

pwm =PWM(Pin(USER_LED_PIN,Pin.OUT),1000)
adc=ADC(Pin(ADC_PIN))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_10BIT)

try:
    while True:
        adcValue=adc.read()
        pwm.duty(adcValue)
        print(adc.read())
        sleep_ms(100)
except:
    pwm.deinit()





