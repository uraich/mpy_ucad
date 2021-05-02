import time
from machine import Pin

class FlowingLED():
    bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:14, 2:27, 1:16, 0:17}
    def __init__(self):
        self.ledTab = {}
        # initialize a dict where the key is the led number and the value the initalize GPIO Pin
        for i in range(10):
            self.ledTab[i] = Pin(self.bar[i],Pin.OUT)

    def showled(self):                 
        for i in range(len(self.ledTab)):
            self.ledTab[i].on()
            time.sleep_ms(100)
            self.ledTab[i].off()
        for i in range(len(self.ledTab)):
            self.ledTab[9-i].on()
            time.sleep_ms(100)
            self.ledTab[9-i].off()

flowingLed = FlowingLED()
while True:
    flowingLed.showled()
