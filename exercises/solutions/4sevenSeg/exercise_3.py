#
# Solution de l'exercice_2: Horloge
# Le programme utilise la classe HexDigit pour:
# afficher le temps de l'horloge interne du ESP32
# U. Raich 4. Mai 2021
# Ce programme fait partie du cours IoT à
# l'Université Cheikh Anta Diop, Dakar, Sénégal
#

from hexDisplay import HexDisplay
from machine import Timer
import utime as time
from wifi_connect import connect

connect()

class Clock():
    def __init__(self):
        self.hexDisplay = HexDisplay()
        self.hexDisplay.clear()
        #
        # init the clock
        #
        now = time.localtime()
        print(now)
        print("{:d}:{:d}".format(now[3],now[4]))
        self.hour = now[3]
        self.min = now[4]
        self.dp = False

        self.hexDisplay.showDP(2,self.dp)

        #
        # start the 500ms periodic timer
        #
        tim = Timer(0)
        tim.init(period=500, mode=Timer.PERIODIC,callback = self.updateClock)

        while True:
            # update the display with the current time
            value = self.hour*100+self.min
            self.hexDisplay.showDecValue(value)
            
    def updateClock(self,timer):
        now = time.localtime()
        # print("{:d}:{:d}".format(now[3],now[4]))
        self.dp = not self.dp
        self.hexDisplay.showDP(2,self.dp)
        self.hour = now[3]
        self.min = now[4]
    
clock = Clock()
