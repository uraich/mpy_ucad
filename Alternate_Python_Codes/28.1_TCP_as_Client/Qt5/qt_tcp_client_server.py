#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys,errno
import socket
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpServer,QTcpSocket,QHostAddress

class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow.ui', self)

        self.actionQuit.triggered.connect(self.quit)
        self.local_ip_text = self.findChild(
            QtWidgets.QLineEdit, 'local_ip_text')
        self.hostname = self.get_ip()[0]
        self.local_ip = self.get_ip()[1]
        self.local_ip_text.setText(self.local_ip)
        print('Hostname: ' + self.hostname + ', ip: ' + self.local_ip)
        self.local_port_text = self.findChild(
            QtWidgets.QLineEdit, 'local_port_text')
        
        self.server_ip_text = self.findChild(
            QtWidgets.QLineEdit, 'server_ip_text')
        self.server_port_text = self.findChild(
            QtWidgets.QLineEdit, 'server_port_text')
        
        self.send_text = self.findChild(
            QtWidgets.QTextEdit, 'send_text')
        
        self.receive_text = self.findChild(
            QtWidgets.QTextEdit, 'receive_text')
        
        self.listen_pb = self.findChild(
            QtWidgets.QPushButton, 'listen_pb')
        self.listen_pb.clicked.connect(self.start_listening)

        self.connect_pb = self.findChild(
            QtWidgets.QPushButton, 'connect_pb')
        self.connect_pb.clicked.connect(self.connect_to_server)

        self.clr_rec_button = self.findChild(
            QtWidgets.QPushButton, 'clr_rec_button')
        self.clr_rec_button.clicked.connect(self.clr_rec)

        self.clr_sent_button = self.findChild(
            QtWidgets.QPushButton, 'clr_sent_button')
        self.clr_sent_button.clicked.connect(self.clr_sent)

        self.send_button = self.findChild(
            QtWidgets.QPushButton, 'send_button')
        # self.send_button.clicked.connect(self.send_msg)

        self.rec_text = self.findChild(
            QtWidgets.QTextEdit, 'rec_text')

        self.send_text = self.findChild(
            QtWidgets.QTextEdit, 'send_text')

        self.client_server_tab = self.findChild(
            QtWidgets.QTabWidget, 'client_server_tab')
        self.client_server_tab.currentChanged.connect(self.tabChanged)

        self.connected = False
        self.listening = False
        self.tcp_server = None
        self.server_socket = None
        # self.new_client = QtCore.pyqtSignal(QTcpSocket)
        self.show()
    
    def tabChanged(self, index):        
        print("tab changed")
        self.listen_pb.setText("Start Listening")
        if self.connected:
            self.connected = False
            self.connect_pb.setChecked(False)
        self.clr_rec()
        self.clr_sent()
        
    def accept_error(self, socket_error):
        """
        An error occurred.

        :param socket_error: QAbstractSocket::SocketError
        """
        print('accept error %s', socket_error)
        
    def new_connection(self):
        print("accept connection")
        while self.tcp_server.hasPendingConnections():
            # returns a new QTcpSocket
            self.server_socket = self.tcp_server.nextPendingConnection()
        print("Connected")
        self.server_socket.readyRead.connect(self.server_read)
        self.server_socket.disconnected.connect(self.client_disconnected)
        ip = self.get_ip()
        connected_text = 'Connected to ' + self.hostname + ' at ' + self.local_ip + '\r\n' 
        self.server_socket.write(bytes(connected_text,encoding="ascii"))
        self.send_text.insertPlainText(connected_text)
        self.server_socket.flush()
        self.listen_pb.setText('Connected')   
        
    def client_disconnected(self):
        print("Client disconnected")
        self.server_socket.close()
        self.listening = False
        self.client_server_tab.setTabEnabled(1,True)
        self.tcp_server.close()
        self.listen_pb.setText('Start Listening')
        self.listen_pb.setChecked(False)
        
    def server_read(self):
        print("Reading from server socket")
        data = self.server_socket.readAll()
        msgstring = bytes(data).decode()
        print(msgstring)
        print(data,type(data))
        self.receive_text.insertPlainText(msgstring + '\n')
        echo_string = 'From ' + self.hostname + ' at ' + self.local_ip + ': ' + msgstring + '\r\n'
        self.server_socket.write(bytes(echo_string,encoding="ascii"))
        self.server_socket.flush()
        self.send_text.insertPlainText(echo_string)
        
    def start_listening(self):
        if self.listening:
            self.listen_pb.setChecked(True)
            return
            
        host_ip = str(self.local_ip_text.text())
        print(host_ip)
        port = int(str(self.local_port_text.text()))        
        print(host_ip + " is listening on port ",port)
        
        if not self.tcp_server:
            print("create tcp server")
        
            self.tcp_server = QTcpServer(self)
            self.tcp_server.setMaxPendingConnections(1)
            self.tcp_server.acceptError.connect(self.accept_error)
            self.tcp_server.newConnection.connect(self.new_connection)
            self.listening = True
            self.listen_pb.setText('Listening')
            self.client_server_tab.setTabEnabled(1,False)            
            print("start listening")
            
        if not self.tcp_server.listen(QHostAddress.Any, port):
            raise RuntimeError('Network error: cannot listen')


    def connect_to_server(self):
        if self.connected or self.listening:
            self.connect_pb.setChecked(True)
            return
        server_ip = str(self.server_ip_text.text())
        port = int(str(self.local_port_text.text()))
        print("Server IP: ", server_ip)
        if server_ip.find('xxx') != -1:
            print("bad IP")
            QMessageBox.about(self,
                'Bad Server IP', 'Please give a correct Server IP\n'
                'IP is ' + server_ip)
            self.connect_pb.setChecked(False)
            return
        else:
            self.client_socket = QTcpSocket(self)
            print("Connecting to " + server_ip +":",port)
            self.client_socket.connectToHost(server_ip, port)
            self.client_socket.waitForConnected(1000)
            self.client_socket.readyRead.connect(self.client_read)
              
        if self.client_socket.state() != QTcpSocket.ConnectedState:
            QMessageBox.about(self,
                              'Connection failed', 'Please check IP address and port number\nIs the server running?')
            self.connect_pb.setChecked(False)
            return
        
        print("Connection established")
        self.connect_pb.setText("Connected")
        self.client_server_tab.setTabEnabled(0,False)
        print("Connecting send button")
        self.send_button.clicked.connect(self.send_msg)
        self.connected = True

    def client_read(self):
        print("Reading from client socket")
        data = self.client_socket.readAll()
        msgstring = bytes(data).decode()
        print(msgstring)
        print(data,type(data))
        self.receive_text.insertPlainText(msgstring + '\n')
        
    def connection_error(self,socketError):
        QMessageBox.about(self,
                          'Connection failed', 'Please check IP address and port number\nIs the server running?')
        self.connect_pb.setChecked(False)
        return
    
    def clr_rec(self):
        self.receive_text.clear()

    def clr_sent(self):
        self.send_text.clear()

    def send_msg(self):
        print('send msg')
        if not self.connected:
            QMessageBox.about(self,
                'Not yet connected', 'Please connect to the TCP Server first')
        message = str(self.send_text.toPlainText())
        if message == "":
            print("Empty message")
        else:
            print("Message: " + message)
            if message.lower() == 'bye':
                self.client_socket.write(bytes(message,encoding="ascii"))                
                self.client_socket.close()
                self.connected = False
                self.connect_pb.setText("Connect to Server")
                self.connect_pb.setChecked(False)
                self.client_server_tab.setTabEnabled(0,True)
                self.send_button.clicked.disconnect(self.send_msg)
                return
            
            self.client_socket.write(bytes(message,encoding="ascii"))
            self.send_text.clear()
            #
            # wait for the answer
            #
            data = self.client_socket.readAll()
            msg_string = bytes(data).decode()
            # data = self.client_socket.recv(1024).decode()
            self.receive_text.insertPlainText(msg_string)
            self.send_text.clear()
                
    def quit(self):
        app.exit()

#
# gets the hostname and IP address of the local server
#

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        hostname = socket.gethostname()
        try:
            # doesn't even have to be reachable
            s.connect(('192.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return (hostname, IP)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

# if__name__ == "__main__":
#     pass
