# flash.py Heartbeat code for simple uasyncio-based echo server

# Released under the MIT licence
# Copyright (c) Peter Hinch 2019
# Simplified for ESP32 only by Uli Raich

import uasyncio as asyncio
from utime import sleep_ms

async def heartbeat(tms):
    from machine import Pin
    led = Pin(2, Pin.OUT, value=1)

    while True:
        led(not led())
        sleep_ms(200)
        led(not led())
        sleep_ms(200)
        await asyncio.sleep_ms(0)
