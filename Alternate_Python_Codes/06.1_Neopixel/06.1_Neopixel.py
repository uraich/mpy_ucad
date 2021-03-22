from machine import Pin
from neopixel import NeoPixel
from utime import sleep_ms

NEO_PIXEL_PIN = 26         # on my board the neopixel is connected to GPIO 26
NO_OF_LEDS    = 7
pin = Pin(NEO_PIXEL_PIN, Pin.OUT)
np = NeoPixel(pin, NO_OF_LEDS)

#brightness :0-255
brightness=10                                
colors=[[brightness,0,0],                    # red
        [0,brightness,0],                    # green
        [0,0,brightness],                    # blue
        [brightness,brightness,brightness],  # white
        [0,0,0]]                             # close
    
while True:
    for i in range(0,len(colors)):
        for j in range(0,NO_OF_LEDS):
            np[j]=colors[i]
            np.write()
            sleep_ms(50)
        sleep_ms(500)
    sleep_ms(500)
    
    
