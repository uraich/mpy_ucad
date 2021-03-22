#!/opt/bin/lv_micropython
import sys
from utime import sleep_ms

class ColorWheel:
    NEO_PIXEL_PIN = 26         # on my board the neopixel is connected to GPIO 26
    NO_OF_LEDS    = 7
    def __init__(self):
        self.red   = 0
        self.green = 0
        self.blue  = 0
        
        if sys.platform == "esp32":

            from machine import Pin
            from neopixel import NeoPixel
    
            # init data pin to control LEDs

            self.brightness=0.1             #brightness: 0-1.0
            
            pin = Pin(self.NEO_PIXEL_PIN, Pin.OUT)
            self.np = NeoPixel(pin, self.NO_OF_LEDS)
        
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

        print("red: {:03d}, green: {:03d}, blue: {:03d}".format(self.red,
                                                               self.green,
                                                               self.blue))
        return (self.red,self.green,self.blue)

    def show(self):
        if sys.platform == "esp32":
            for i in range(0,self.NO_OF_LEDS):
                self.np[i] = (int(self.red*self.brightness),
                              int(self.green*self.brightness),
                              int(self.blue*self.brightness))
            self.np.write()
            sleep_ms(200)
    
print("wheel running on ",sys.platform)
wheel = ColorWheel()
print("<60")
for pos in range(0,60,10):
    wheel.colors(pos)
    wheel.show()
    
print("60° .. 120°")
for pos in range(60,120,10):
    wheel.colors(pos)
    wheel.show()

print("120° .. 180°")
for pos in range(120,180,10):
    wheel.colors(pos)
    wheel.show()
        
print("180° .. 240°")
for pos in range(180,240,10):
    wheel.colors(pos)
    wheel.show()
        
print("240° .. 300°")
for pos in range(240,300,10):    
    wheel.colors(pos)
    wheel.show()
        
print("300° .. 360°")
for pos in range(300,360,10):    
    wheel.colors(pos)
    wheel.show()
        
