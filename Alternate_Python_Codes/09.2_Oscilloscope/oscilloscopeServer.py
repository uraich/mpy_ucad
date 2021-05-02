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
TRACE_LENGTH = 500
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
        self.traceBuf = bytearray(TRACE_LENGTH)
        
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
                    print("Read new message")
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
                        self.trace.no_trig = False
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
                elif cmd[0] == "meas":                   
                    if int(cmd[1]) == 1:
                        print("start measurement")
                        self.meas_task = asyncio.create_task(self.measure(sreader,swriter))
                        continue
                    else:
                        print("stop measurement")
                        self.trace_task.cancel()
                        self.meas_task.cancel()
                        continue
                        
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
        self.led(not self.led())
        await asyncio.sleep_ms(500)
        
    async def measure(self,sreader,swriter):
        print("measure task")
        self.trace_task = asyncio.create_task(self.trace.read_trace())
        await self.trace_task
        print("read trace ready")
        if self.trace.no_trig:
            swriter.write(self.trace.traceBuf)
        else:
            print("trigger_at: ",self.trace.triggeredAt)
            start_index = self.trace.triggeredAt - self.trace.trigPos
            if start_index < 0:
                start_index += 500
            j=0
            for i in range(start_index,500):
                self.traceBuf[j] = self.trace.traceBuf[i]
                j += 1
            for i in range(0,start_index):
                self.traceBuf[j] = self.trace.traceBuf[i]
                j+=1
            swriter.write(self.traceBuf)
        print("Sending result")
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
