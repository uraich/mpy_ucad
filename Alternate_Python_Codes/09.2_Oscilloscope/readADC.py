from machine import ADC,Pin
from utime import sleep_ms

ADC_PIN = 36

adc = ADC(Pin(ADC_PIN))
adc.atten(ADC.ATTN_11DB)

for _ in range(100):
    val = adc.read() >> 4
    print("0x%03x"%val)
    sleep_ms(20)
          