from machine import Pin
from neopixel import NeoPixel

NEO_PIXEL_PIN = 26         # on my board the neopixel is connected to GPIO 26
NO_OF_LEDS    = 7
pin = Pin(NEO_PIXEL_PIN, Pin.OUT)
np = NeoPixel(pin, NO_OF_LEDS)

for i in range(0,NO_OF_LEDS):
    np[i] = (0,0,0)
    np.write()
