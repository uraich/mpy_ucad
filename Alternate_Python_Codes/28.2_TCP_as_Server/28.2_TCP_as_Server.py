import network
import socket
import time

ssidRouter     =  "WLAN18074253"        #Enter the router name
passwordRouter =  "Q4k6V35sFauw"        #Enter the router password
port           =   5000                 #input the remote port

def connectWifi(ssid,passwd):
  wlan=network.WLAN(network.STA_IF)
  
  if wlan.isconnected() == True:
    print("Already connected on address ",wlan.ifconfig()[0])
    return wlan.ifconfig()[0]
  
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
          
  print("wlan connected to address ",wlan.ifconfig()[0])
  return wlan.ifconfig()[0]

# connect to wifi
ip = connectWifi(ssidRouter,passwordRouter)
          
# The server code
server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind(('', port))  # bind host address and port together

# configure how many client the server can listen simultaneously
print("Listening to any machine on port ",port)    
server_socket.listen(1)
conn, address = server_socket.accept()  # accept new connection
print("From server: Connection from: " + str(address))
conn.send("Connected to " + ip)

while True:
  # receive data stream. it won't accept data packet greater than 1024 bytes
  data = conn.recv(1024).decode()
  if not data:
    # if data is not received break
    break
  print("from connected user: " + str(data))
  data = input(' -> ')
  conn.send(data.encode())  # send data to the client
  
conn.close()  # close the connection
