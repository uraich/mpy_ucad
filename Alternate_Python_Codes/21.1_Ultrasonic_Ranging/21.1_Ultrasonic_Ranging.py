from machine import Pin
from utime import ticks_us, ticks_diff, sleep_us, sleep_ms
from micropython import const

TRIG = const(5)
ECHO = const(23)
SPEED_IN_AIR = const(330)       # speed of sound in air: 330 m/s

class HC_SR04(object):
    def __init__(self,trig=TRIG,echo=ECHO):
        self.trig = Pin(trig,Pin.OUT)
        self.echo = Pin(echo,Pin.IN,Pin.PULL_UP)

    # trigger a measurement
    
    def trigger(self):
        self.trig.value(1)      # trigger a measurement
        sleep_us(10)            # keep the trigger signal high for 10 us
        self.trig.value(0)

    # read the length of the echo signal
    
    def get_echo(self):
        while (self.echo.value() == 0):
            pass                # wait until the echo signal goes high
        start = ticks_us()
        while (self.echo.value() == 1):
            pass
        stop = ticks_us()
        signal_length = ticks_diff(stop,start)
        # print("signal length [us]: ",signal_length)
        return signal_length

    # from the time it takes the echo to come back, calculate the distance
    
    def distance(self,echo_time):
        dist = (SPEED_IN_AIR*100/2)*echo_time/1000000  # cm
        # print("Distance: ", dist," cm")
        return dist
        
    def measure(self):
        self.trigger()
        return self.get_echo()
    

hc_sr04 = HC_SR04()
while True:
    echo_time = hc_sr04.measure()
    distance = hc_sr04.distance(echo_time)
    print("Distance: {:f} [cm]".format(distance))
