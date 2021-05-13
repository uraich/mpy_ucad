from machine import Pin
from utime import sleep_ms

bar = {9: 18, 8:19, 7:23, 6: 5, 5: 13, 4:12, 3:11, 2:27, 1:25, 0:26}
led = [None]*10

for i in range(2):
    led[i] = Pin((bar[i]),Pin.OUT)

for i in range(2):
    for _ in range(5):
        led[i].on()
        sleep_ms(500)
        led[i].off()
        sleep_ms(500)
