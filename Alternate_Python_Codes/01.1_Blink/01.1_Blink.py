from utime import sleep_ms
from machine import Pin
import sys

USER_LED = 2

led=Pin(USER_LED,Pin.OUT)   #create LED object on the user LED on the CPU card
try:
    while True:
        led.on()            #Set led turn on
        sleep_ms(1000)
        led.off()           #Set led turn off
        sleep_ms(1000)

except KeyboardInterrupt:
    print("Keyboard Interrupt resetting LED")
    led.off()
    sys.exit()





