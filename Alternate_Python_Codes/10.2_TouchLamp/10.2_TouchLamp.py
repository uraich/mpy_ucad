from machine import TouchPad, Pin
from utime import sleep_ms

PRESS_VAL=200    #Set a threshold to judge touch
RELEASE_VAL=400 #Set a threshold to judge release

TOUCHPAD_PIN = 4
LED_PIN      = 2

led=Pin(LED_PIN,Pin.OUT)
tp = TouchPad(Pin(TOUCHPAD_PIN,Pin.IN,Pin.PULL_UP))

isPressed = 0

def reverseGPIO():
    if led.value():
        led.value(0)
        print("Turn off led")
    else:
        led.value(1)
        print("Turn on led")
        
while True:
    if tp.read() < PRESS_VAL:
        if not isPressed:
            isPressed = 1
            reverseGPIO()
            print("Touch detected!")
            sleep_ms(50)
    if tp.read() > RELEASE_VAL:
        if isPressed:
            isPressed = 0
            print("Touch released!")
            sleep_ms(50)


