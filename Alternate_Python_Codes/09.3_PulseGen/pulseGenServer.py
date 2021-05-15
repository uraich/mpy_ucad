# userver.py Demo of simple uasyncio-based echo server

# Released under the MIT licence
# Copyright (c) Peter Hinch 2019-2020

import usocket as socket
import uasyncio as asyncio

from wifi_connect import connect, getIPAddress
from machine import Pin,DAC
from utime import sleep_ms, sleep_us
from math import sin,pi
LED_PIN = 2
DAC_PIN = 26
class Server:
    
    pulse_shape = {'Rectangular' : 0,
                   'Triangular'  : 1,
                   'Sawtooth'    : 2,
                   'Sinusoidal'  : 3}

    frequencies = {'5 kHz':  0.2,
                   '2 kHz':  0.5,
                   '1 kHz':  1,
                   '500 Hz': 2,
                   '200 Hz': 5,
                   '100 Hz': 10}
    
    def __init__(self, host='0.0.0.0', port=5000, backlog=5, timeout=20000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        self.pulse_data = [0]*500
        
        self.pulse_height = 0
        self.pulse_T = 0
        self.pulse_form = 0
        self.pulse_height_old = self.pulse_height
        self.pulse_T_old = self.pulse_T
        self.pulse_form_old = self.pulse_form
        
        self.generating = False
        self.led = Pin(LED_PIN,Pin.OUT)
        self.dac = DAC(Pin(DAC_PIN))

    def delay_us(self,delay):
        for _ in range(delay):
            pass
        
    def calc_pulse(self):
        data_length = 500
        print("pulse_T: {:f} data_length: {:d}".format(self.pulse_T,data_length))
        if self.pulse_form == self.pulse_shape['Rectangular']:
            print("Calculate rectangular wave form")
            j = 0
            for i in range(data_length):
                if j < 250:
                    self.pulse_data[i] = 0
                else:
                    self.pulse_data[i] = self.pulse_height
                j += 1

        elif self.pulse_form == self.pulse_shape['Sawtooth']:
            print("Calculate sawtooth wave form")
            j = 0
            value = 0
            increment = self.pulse_height / 500
            for i in range(data_length):
                self.pulse_data[i] = int(value)
                value += increment

        elif self.pulse_form == self.pulse_shape['Triangular']:
            print("Calculate triangular wave form")
            j = 0
            value = 0
            increment = self.pulse_height / 250
            for i in range(data_length):
                self.pulse_data[i] = int(value)
                j += 1
                if j < 250:
                    value += increment
                elif j >= 250 and j < 500:
                    value -= increment

        elif self.pulse_form == self.pulse_shape['Sinusoidal']:
            print("Calculate sine wave")
            for i in range(data_length):
                self.pulse_data[i] = int((sin(2*i*pi/500) + 1)*(self.pulse_height/2))

    async def genPulse(self):
        print("running pulse generation")
        self.pulse_height_old = self.pulse_height
        self.pulse_T_old = self.pulse_T
        self.pulse_form_old = self.pulse_form
        self.calc_pulse()
        if self.pulse_T < 1:
            delay = int(self.pulse_T*1000)
            print("delay: {:d} us".format(delay))
        else:
            print("delay: {:d} ms".format(int(self.pulse_T)))
                
        while True:
            if self.pulse_height_old != self.pulse_height or\
               self.pulse_T_old != self.pulse_T or\
                   self.pulse_form_old != self.pulse_form:
                self.calc_pulse()
                self.pulse_height_old = self.pulse_height
                self.pulse_T_old = self.pulse_T
                self.pulse_form_old = self.pulse_form
                
            for i in range(500):
                self.dac.write(self.pulse_data[i])    # set the pulse level
                if self.pulse_T == 0.2:
                    for _ in range(27):
                        pass
                elif self.pulse_T == 0.5:
                    for _ in range(120):
                        pass
                elif self.pulse_T == 1:
                    for _ in range(270):
                        pass
                elif self.pulse_T == 2:
                    for _ in range(600):
                        pass
                elif self.pulse_T == 5:
                    for _ in range(280):
                        pass
                    await asyncio.sleep_ms(0)   
                    for _ in range(280):
                        pass
                else:
                    for j in range(3):
                        for _ in range(140):
                            pass
                        await asyncio.sleep_ms(0)   

            await asyncio.sleep_ms(0)     
            self.led(not self.led())
  
    async def heartbeat(self):
        print("running heartbeat")
        while True:
            for i in range(500):
                sleep_us(200)
            self.led(not self.led())
            await asyncio.sleep_ms(0)
        
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
                if cmd[0] == "pulse_shape":
                    print("pulse shape cmd with value: " + cmd[1])
                    self.pulse_form = int(cmd[1])
                    response = 'ok\n'                    
                elif cmd[0] == "pulse_height":
                    print("pulse height cmd with value: " + cmd[1])
                    self.pulse_height = int(cmd[1])
                    response = 'ok\n'
                elif cmd[0] == "pulse_T":
                    print("pulse_T cmd with value: " + cmd[1])
                    self.pulse_T = float(cmd[1])
                    response = 'ok\n'
                elif cmd[0] == "start":                   
                    print("Starting task")
                    # self.heartbeat_task = asyncio.create_task(self.heartbeat())
                    self.gen_task = asyncio.create_task(self.genPulse())
                    response = 'ok\n'
                elif cmd[0] == "stop":
                    print("Stopping task")
                    # self.heartbeat_task.cancel()
                    self.gen_task.cancel()
                    response = 'ok\n'
                elif cmd[0] == "running?":
                    if self.generating:
                        response = 'yes\n'
                    else:
                        response = 'no\n'
                elif cmd[0] == "pulse_height?":
                    response = str(self.pulse_height) + '\n'
                    
                elif cmd[0] == "pulse_T?":
                    response = str(self.pulse_T) + '\n'
                    
                elif cmd[0] == "pulse_shape?":
                    response = str(self.pulse_form + '\n')
                    
                swriter.write(response.encode('ascii'))
                await swriter.drain()  
        except OSError:
            pass
        print('Client {} disconnect.'.format(self.cid))
        await sreader.wait_closed()
        print('Client {} socket closed.'.format(self.cid))

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
