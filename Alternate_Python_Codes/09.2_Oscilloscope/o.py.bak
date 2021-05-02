# userver.py Demo of simple uasyncio-based echo server

# Released under the MIT licence
# Copyright (c) Peter Hinch 2019-2020

import usocket as socket
import uasyncio as asyncio

from wifi_connect import connect, getIPAddress
from machine import Pin,ADC
from utime import sleep_ms, sleep_us

from trace import Trace
LED_PIN = 2
ADC_PIN = 36


class Trace():
    
    TRACE_LENGTH=500
    TRIG_SLOPE_RISING  = 0
    TRIG_SLOPE_FALLING = 1
    
    def __init__(self):
        print("Init trace")
        self.traceBuf = bytearray(self.TRACE_LENGTH)
        self.pulse_T   = 10   # sample freq: 100 Hz (10 ms between samples)
        self.trigLevel =  100
        self.trigPos = 250
        self.trigSlope = self.TRIG_SLOPE_FALLING
        self.traceIndex = 0
        self.sampleCount = 0
        self.singleShot = 1
        self.no_trig = False
        self.trigCond = False
        self.triggeredAt = 0
        self.led = Pin(LED_PIN, Pin.OUT, value=0)

    async def read_trace(self):
        print("read trace started")
        self.adc = ADC(Pin(ADC_PIN))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
        
        self.sampleCount = 0
        self.traceIndex = 0
        self.trigCond = False
        if self.pulse_T < 1:
            delay = int(self.pulse_T*1000)
            print("delay: {:d}us".format(delay))
        else:
            print("delay: {:d}ms".format(int(self.pulse_T)))
            
        print("Waiting for trigger")
        while not self.trig():
            pass
        else:
            print("Trigger seen")
            self.triggeredAt = self.traceIndex
            print("Triggered at trace buffer index ",self.triggeredAt)
            print("value: ",self.traceBuf[self.traceIndex-1])
        if self.no_trig:
            maxcount = 500-1
        else:
            maxcount = 500 - self.trigPos
        print("maxcount: ",maxcount)
        
        for i in range(maxcount):
            value = self.adc.read() 
            self.traceBuf[self.traceIndex] = value >> 4 # restrict to 8 bits
            # print(value)
            self.traceIndex += 1
            if self.traceIndex == 500:                  # traceBuf is a circular buffer
                 self.traceIndex = 0
            if self.pulse_T < 1:
                sleep_us(delay)
            else:
                sleep_ms(int(self.pulse_T))
                await asyncio.sleep_ms(0)
                
        self.led.value(not self.led.value())
        # await asyncio.sleep_ms(0)
        # print("Writing data to disk")
        # self.writeToDisk()
        
    
    def writeToDisk(self):
        f = open("/data/trace.txt","w")
        start_index = self.triggeredAt - self.trigPos
        if start_index < 0:
            start_index += 500
        for i in range(start_index,500):
            f.write(str(self.traceBuf[i]) + "\n")
        for i in range(0,start_index):
            f.write(str(self.traceBuf[i]) + "\n")
        # for i in range(500):
        #     f.write(str(self.traceBuf[i]) + "\n")
        j = 0
        for i in range(start_index,500):
            if not j % 10 and j != 0:
                print("")
            print(self.traceBuf[i],end =" ")
            j += 1
        for i in range(0,start_index):
            if not j % 10 and j != 0:
                print("")
            print(self.traceBuf[i],end =" ")
            j += 1          
        f.close()
               
    # detect a trigger
    
    async def trig(self):
        value = self.adc.read() >> 4
        self.traceBuf[self.traceIndex] = value
        self.traceIndex += 1
        if self.traceIndex == 500:      # the trace buffer is a circular buffer
            self.traceIndex = 0
            
        self.sampleCount += 1
        if self.sampleCount > 500:
            self.sampleCount = 500
            
        # if no_trig is set, start measurement immediately 
        if self.no_trig:
            return True

        if self.trigSlope == self.TRIG_SLOPE_RISING:
            if self.trigCond and value > self.trigLevel and self.sampleCount > self.trigPos:
                print("trigCond: ", self.trigCond,end= " ")
                print("value: %d, trigger level: %d"%(value,self.trigLevel))
                return True
            elif value <= self.trigLevel:
                self.trigCond = True
                await asyncio.sleep_ms(0)
                return False
            else:
                await asyncio.sleep_ms(0)
        else:            
            if self.trigCond and value < self.trigLevel and self.sampleCount > self.trigPos:
                print("trigCond: ", self.trigCond,end= " ")
                print("value: %d, trigger level: %d"%(value,self.trigLevel))                
                return True
            elif value >= self.trigLevel:
                self.trigCond = True
                await asyncio.sleep_ms(0)
                return False
            else:
                await asyncio.sleep_ms(0)


class Server:
    
    def __init__(self, host='0.0.0.0', port=5000, backlog=5, timeout=20000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout

        self.trace = Trace()
        self.trace.no_trig = True
        self.trace.trigLevel = 0
        self.trace.trigPos = 100
        self.trace.pulse_T = 0.2
        
        self.led = Pin(LED_PIN,Pin.OUT)
        self.adc = ADC(Pin(ADC_PIN))
        
    async def readPulse(self,tms):
        print("Reading a trace")
        if self.pulse_T < 1:
            delay = int(self.pulse_T*1000)
            for i in range(500):
                self.trace[i] = self.adc.read() >> 4
            asyncio.sleep_us(delay)
        else:
            for i in range(500):
                self.trace[i] = self.adc.read() >> 4
                asyncio.sleep_ms(int(self.pulse_T))

    async def run(self):
        print('Awaiting client connection.')
        self.cid = 0
        self.server = await asyncio.start_server(self.run_client, self.host, self.port, self.backlog)
        while True:
            await asyncio.sleep(100)

    async def run_client(self, sreader, swriter):
        self.cid += 1
        print('Got connection from client', self.cid)
        connectMsg = "Connected to " + ip + "\n"
        print("Sending connect message: " + connectMsg)
        swriter.write(connectMsg.encode('utf8'))
        await swriter.drain()
            
        try:
            while True:
                try:
                    res = await asyncio.wait_for(sreader.readline(), self.timeout)
                except asyncio.TimeoutError:
                    print("timeout on read")
                    res = b''   
                if res == b'':
                    raise OSError

                cmdMsg = res.decode()
                print('Received from client: ' + cmdMsg)

                cmd = cmdMsg.split("=")
                print("cmd[0]: ",cmd[0])
                if cmd[0] == "notrig":
                    print("no trigger cmd with value: " + cmd[1])
                    if int(cmd[1]) == 1:
                        self.trace.no_trig = True
                    else:
                        self.no_trigger = False
                elif cmd[0] == "triglvl":
                    newTrigLevel = int (float(cmd[1]) * 256/3.3)
                    print("trigger level cmd with value: {:d}".format(newTrigLevel) )
                    self.trace.trigLevel = newTrigLevel
                elif cmd[0] == "pulse_T":
                    print("time base: " + cmd[1])
                    self.trace.pulse_T = float(cmd[1])                    
                elif cmd[0] == "trigpos":
                    print("trigger position cmd with value: " + cmd[1])
                    self.trace.trigPos = int(cmd[1])
                elif cmd[0] == "trigslope":
                    print("trigslope cmd with value: " + cmd[1])
                    self.trace.trigSlope = int(cmd[1])
                elif cmd[0] == "singleshot":
                    print("single shot cmd with value: " + cmd[1])
                    self.trace.singleShot = int(cmd[1])   
                elif cmd[0] == "meas":                   
                    print("Starting task")
                    if int(cmd[1]) == 1:
                        print("start measurement")
                        response = 'ok\n'
                        print("send ok")
                        swriter.write(response.encode('ascii'))
                        await swriter.drain()                       
                        # trace_task = asyncio.create_task(self.heartbeat())
                        # return
                    
                        self.meas_task = asyncio.create_task(self.trace.read_trace())
                        # self.meas_task = asyncio.create_task(self.trace.read_trace())
                        await self.meas_task
                        print("read trace ready")
                        swriter.write(self.trace.traceBuf)
                        await swriter.drain()
                        return
                    else:
                        print("stop measurement")
                        self.meas_task.cancel()
                        
                response = 'ok\n'
                print("send ok")
                swriter.write(response.encode('ascii'))
                await swriter.drain()

        except OSError:
            pass
        print('Client {} disconnect.'.format(self.cid))
        await sreader.wait_closed()
        print('Client {} socket closed.'.format(self.cid))

    async def heartbeat(self):
        while True:
            adc = ADC(Pin(ADC_PIN))
            adc.atten(ADC.ATTN_11DB)
            adc.width(ADC.WIDTH_12BIT)
            self.led(not self.led())
            print(adc.read())
            sleep_ms(200)
            self.led(not self.led())
            print(adc.read())
            sleep_ms(200)
            await asyncio.sleep_ms(0)

    def measure(self,sreader,swriter):
        print("measure task")
        trace_task = asyncio.create_task(self.trace.read_trace())
        await trace_task
        print("read trace ready")
        swriter.write(self.trace.traceBuf)
        await swriter.drain()
        
    async def close(self):
        print('Closing server')
        self.server.close()
        await self.server.wait_closed()
        print('Server closed.')
        
# connect to wifi first
connect()
ip = getIPAddress()
server = Server()
try:
    asyncio.run(server.run())
except KeyboardInterrupt:
    print('Interrupted')  # This mechanism doesn't work on Unix build.
finally:
    asyncio.run(server.close())
    _ = asyncio.new_event_loop()
