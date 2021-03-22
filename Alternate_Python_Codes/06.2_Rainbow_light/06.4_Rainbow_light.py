#!/opt/bin/lv_micropython
import sys
from utime import sleep_ms
from machine import Pin
from neopixel import NeoPixel

NEO_PIXEL_PIN = 26         # on my board the neopixel is connected to GPIO 26
NO_OF_LEDS    = 7
    
class ColorWheel:

    def __init__(self):
        self.red   = 0
        self.green = 0
        self.blue  = 0
        
    def colors(self,pos):
        if pos<60:
            self.red=255
            self.green=int(255*pos/60)
            self.blue=0
        elif pos >=60 and pos < 120:
            self.red=255-int(255*(pos-60)/60)
            self.green = 255
            self.blue = 0
        elif pos >=120 and pos < 180:
            self.red = 0
            self.blue = int(255*(pos-120)/60)
            self.green = 255
        elif pos >= 180 and pos < 240:
            self.red = 0
            self.green = 255-int(255*(pos-180)/60)
            self.blue = 255
        elif pos >= 240 and pos < 300:
            self.red = int(255*(pos-240)/60)
            self.green = 0
            self.blue = 255
        else:
            self.red = 255
            self.green = 0
            self.blue = 255 - int(255*(pos-300)/60)

        # print("red: {:03d}, green: {:03d}, blue: {:03d}".format(self.red,
        #                                                        self.green,
        #                                                        self.blue))
        return (self.red,self.green,self.blue)
    
pin = Pin(NEO_PIXEL_PIN, Pin.OUT)
np = NeoPixel(pin, NO_OF_LEDS)
brightness = 0.1

wheel = ColorWheel()

wheel_pos =[None]*NO_OF_LEDS

print("Each led shows all colors of the color wheel")
print("The color wheel starting position of led i is i * 360° / no of leds")

for led in range(NO_OF_LEDS):
    wheel_pos[led] = int(360/NO_OF_LEDS*led)
    # print("wheel pos for led {:d}: {:d}".format(led,wheel_pos[led]))

while True:
    for i in range(360):
        for led in range(NO_OF_LEDS):        
            colors = wheel.colors((wheel_pos[led]+i)%360)
            np[led] = (int(colors[0]*brightness),
                       int(colors[1]*brightness),
                       int(colors[2]*brightness))
            np.write()
        sleep_ms(2)
            
        
        
