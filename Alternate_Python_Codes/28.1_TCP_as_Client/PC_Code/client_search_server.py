#!/usr/bin/python3
import sys,socket
HOST_IP = "192.168.0."
def client_program():
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    print("Connecting to ",host,":",port)
    server_ip = ""
    for i in range(10,100):
        try:
            host_ip = HOST_IP + str(i)
            print("Trying to connect to " + host_ip)
            client_socket.connect((host_ip, port))  # connect to the server
            break
        except:
            pass

    if host_ip == '':
        print("No server found, giving up")
        sys.exit()
        
    message = input(" -> ")  # take input
    
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())  # send message
        data = client_socket.recv(1024).decode()  # receive response

        print('Received from server: ' + data)  # show in terminal

        message = input(" -> ")  # again take input

    client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()
