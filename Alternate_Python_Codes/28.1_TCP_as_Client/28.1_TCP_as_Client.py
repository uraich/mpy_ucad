import network
import socket
import time

ssidRouter     =  "SSID of your wlan"   #Enter the router name
passwordRouter =  "your wlan password"  #Enter the router password
host           =  "192.168.0.x"         #input the remote server, find the IP address with findIP.py
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
client_socket.connect((host, port))  # connect to the server

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
  client_socket.send(message.encode())  # send message
  data = client_socket.recv(1024).decode()  # receive response
  
  print('Received from server: ' + data)  # show in terminal
  
  message = input(" -> ")  # again take input
  
client_socket.close()  # close the connection

