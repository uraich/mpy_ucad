#!/usr/bin/python3
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind(('', port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    print("Server running on " + host + " with IP: " + get_ip())
    print("Listening to any machine on port ",port)    
    server_socket.listen(1)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    conn.send(("From server: Connected to " + get_ip()).encode())
    
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        '''
        if data == 'bye':
            conn.close()
            server_socket.close()
        '''
        if not data:
            conn.close()
            print("Connection closed")
            break
        else:
            print("from connected user: " + str(data))
            conn.send(("From server at "+ host + ": " +data).encode())  # send data to the client

    
if __name__ == '__main__':
    server_program()
