from machine import Pin,ADC
from utime import sleep_ms
import usocket as socket

ADC_PIN = 36

from wifi_connect import connect, getIPAddress

class Server:
    
    def __init__(self, host='0.0.0.0', port=5000, backlog=5, timeout=20000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.timeout = timeout
        self.adc = ADC(Pin(ADC_PIN))
        self.adc.atten(ADC.ATTN_11DB)
        self.currentVoltage = -1

    def startMeas(self):
        # The server code
        self.server_socket = socket.socket()  # get instance
        # look closely. The bind() function takes tuple as argument
        self.server_socket.bind(('', self.port))  # bind host address and port together
        while True:
            # configure how many client the server can listen simultaneously
            print("Listening to any machine on port ",self.port)    
            self.server_socket.listen(1)
            conn, address = self.server_socket.accept()  # accept new connection
            print("From server: Connection from: " + str(address))
            conn.send("Connected to " + ip)

            while True:
                sum = 0
                for _ in range(50):
                    newVoltage = self.adc.read() >> 4 # reduce to 8 bits
                    sum += newVoltage
                average = int(sum/50)
                
                if abs(average - self.currentVoltage) > 1:
                    self.currentVoltage = average
                    print("New value: ",average)
                    conn.send(str(average).encode())  # send data to the client
                    response = conn.recv(128).decode()
                    print("Response from client: " + response)
                    if not response:
                        # if data is not received break
                        break
                
# connect to wifi first
connect()
ip = getIPAddress()
server = Server()
server.startMeas()
