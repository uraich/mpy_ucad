#
# Solution de l'exercice_3: LED rgb en arc en ciel
# U. Raich 13. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#
import sys
from utime import sleep_ms
from machine import Pin,PWM
from neopixel import NeoPixel

MAX_INTENSITY = 1023

class ColorWheel:
    pins={"red":23, "green": 19,"blue" :18}

    def __init__(self):
        self.red   = 0
        self.green = 0
        self.blue  = 0

        # init data pins en pwm pour contrôler la LED
        self.leds = {}
        for pin in self.pins:
            self.leds[pin] = PWM(Pin(self.pins[pin]),freq=10000,duty=0)
        self.clear()
            
    def clear(self):
     # etteindre toutes les LEDs
         for led in self.leds:
             self.leds[led].duty(0)
             
    def colors(self,pos):
        if pos<60:
            self.red=MAX_INTENSITY
            self.green=int(1024*pos/60)
            self.blue=0
        elif pos >=60 and pos < 120:
            self.red=MAX_INTENSITY-int(MAX_INTENSITY*(pos-60)/60)
            self.green = MAX_INTENSITY
            self.blue = 0
        elif pos >=120 and pos < 180:
            self.red = 0
            self.blue = int(MAX_INTENSITY*(pos-120)/60)
            self.green = MAX_INTENSITY
        elif pos >= 180 and pos < 240:
            self.red = 0
            self.green = MAX_INTENSITY-int(MAX_INTENSITY*(pos-180)/60)
            self.blue = MAX_INTENSITY
        elif pos >= 240 and pos < 300:
            self.red = int(MAX_INTENSITY*(pos-240)/60)
            self.green = 0
            self.blue = MAX_INTENSITY
        else:
            self.red = MAX_INTENSITY
            self.green = 0
            self.blue = MAX_INTENSITY - int(MAX_INTENSITY*(pos-300)/60)

        # print("red: {:03d}, green: {:03d}, blue: {:03d}".format(self.red,
        #                                                        self.green,
        #                                                        self.blue))
        return (self.red,self.green,self.blue)

    def show(self):
        self.leds["red"].duty(self.red)
        self.leds["green"].duty(self.green)
        self.leds["blue"].duty(self.blue)
        sleep_ms(100)

    def print_colors(self):
        print("red: {:03d}, green: {:03d}, blue: {:03d}".format(wheel.red,wheel.green,wheel.blue))
        
print("wheel running on ",sys.platform)
wheel = ColorWheel()
printFlag = True
try:
    while True:
        if printFlag:
            print("<60")
        for pos in range(0,60,5):
            wheel.colors(pos)
            wheel.show()
            if printFlag:
               wheel.print_colors()
        
        if printFlag:
            print("60° .. 120°")
        for pos in range(60,120,5):
            wheel.colors(pos)
            wheel.show()
            if printFlag:
                wheel.print_colors()
            
        if printFlag:
            print("120° .. 180°")
        for pos in range(120,180,5):
            wheel.colors(pos)
            wheel.show()
            if printFlag:
                wheel.print_colors()
            
        if printFlag:
            print("180° .. 240°")
        for pos in range(180,240,5):
            wheel.colors(pos)
            wheel.show()
            if printFlag:
                wheel.print_colors()
            
        if printFlag:
            print("240° .. 300°")
        for pos in range(240,300,5):    
            wheel.colors(pos)
            wheel.show()
            if printFlag:
                wheel.print_colors()
            
        if printFlag:
            print("300° .. 360°")
        for pos in range(300,360,5):    
            wheel.colors(pos)
            wheel.show()
            if printFlag:
                wheel.print_colors()
                
        printFlag = False
    
except KeyboardInterrupt:
    wheel.clear()
            
