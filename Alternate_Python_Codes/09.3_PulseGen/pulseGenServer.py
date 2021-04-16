# userver.py Demo of simple uasyncio-based echo server

# Released under the MIT licence
# Copyright (c) Peter Hinch 2019-2020

import usocket as socket
import uasyncio as asyncio

from wifi_connect import connect, getIPAddress
from machine import Pin
from utime import sleep_ms

class Server:
    
    def __init__(self, host='0.0.0.0', port=5000, backlog=5, timeout=20000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        
        self.pulse_height = 0
        self.pulse_T = 0
        self.pulse_shape = 0
        self.generating = False
        self.led = Pin(2,Pin.OUT)
        
    async def heartbeat(self,tms):
        print("running heartbeat")
        while True:
            self.led(not self.led())
            sleep_ms(200)
            self.led(not self.led())
            sleep_ms(200)
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
                    self.pulse_shape = int(cmd[1])
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
                    self.heartbeat_task = asyncio.create_task(self.heartbeat(500))
                    response = 'ok\n'
                elif cmd[0] == "stop":
                    print("Stopping task")
                    self.heartbeat_task.cancel()
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
                    response = str(self.pulse_shape) + '\n'
                    
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
