from machine import Pin

USER_LED_PIN = 2
BUTTON_PIN   = 22
led = Pin(USER_LED_PIN, Pin.OUT)

#create button object from pin13,Set Pin13 to Input
button = Pin(BUTTON_PIN, Pin.IN,Pin.PULL_UP) 

print("Please press the button to switch the user led on")

try:
    while True:
      if not button.value():     
        led.on()      #Set led turn on
      else:
        led.off()     #Set led turn off
except:
    pass
