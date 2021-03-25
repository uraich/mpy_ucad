#!/usr/bin/python3
# Python3 code to display hostname and
# IP address
  
# Importing socket library
import socket
  
# Function to display hostname and
# IP address
def get_Host_name_IP():
    host_name = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('192.255.255.255',1))
    print(s.getsockname()[0])
    s.close()
        
# Driver code
get_Host_name_IP() #Function call
  

