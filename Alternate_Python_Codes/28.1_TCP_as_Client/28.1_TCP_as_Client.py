import network
import socket
import time,sys

ssidRouter     =  "WLAN18074253"        #Enter the router name
passwordRouter =  "Q4k6V35sFauw"        #Enter the router password
host           =  "192.168.0.20 "       #input the remote server, find the IP address with findIP.py
port           =   5000                 #input the remote port


def connectWifi(ssid,passwd):
  wlan=network.WLAN(network.STA_IF)
  
  if wlan.isconnected() == True:
    print("Already connected")
    return
  
  if wlan.active():
    print("Station is already active")
  else:
    print ("Activating station")
    if not wlan.active(True):
      print("Cannot activate station! giving up ...")
      sys.exit()
            
  wlan.connect(ssid,passwd)
  while(wlan.ifconfig()[0]=='0.0.0.0'):
    time.sleep(1)

  print(wlan.ifconfig())
  return True


connectWifi(ssidRouter,passwordRouter)
  
client_socket = socket.socket()  # instantiate
print("Connecting to ",host,":",port)
try:
  client_socket.connect((host, port))  # connect to the server
except OSError as error:
        print("Connection failed, please check IP address and port number")
        print("Is the server started?")
        sys.exit()

data = client_socket.recv(1024).decode()  # receive response
print(data)

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
  client_socket.send(message.encode())  # send message
  data = client_socket.recv(1024).decode()  # receive response
  
  print('Received from server: ' + data)  # show in terminal
  
  message = input(" -> ")  # again take input
  
client_socket.close()  # close the connection

