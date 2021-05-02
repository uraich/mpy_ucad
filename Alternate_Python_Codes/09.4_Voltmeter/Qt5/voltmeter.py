#!/usr/bin/python3
import sys
from voltmeter_ui import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.Qwt import *
from PyQt5.QtNetwork import QTcpSocket

class Voltmeter(QtWidgets.QMainWindow, Ui_MainWindow):
    VOLTMETER_PORT = 5000
    
    def __init__(self, parent=None):
        super(Voltmeter, self).__init__(parent)
        self.setupUi(self)
        self.needle = QwtDialSimpleNeedle(QwtDialSimpleNeedle.Arrow)
        self.Dial.setNeedle(self.needle)
        self.Dial.setValue(1.5)
        self.lcdNumber.display(1.5)
        self.actionQuit.triggered.connect(self.quit)
        self.connect_pb.clicked.connect(self.connect)
        self.calib = 3.3/256
        self.client_socket = QTcpSocket(self)
        self.connected = False

    def connect(self):
        if self.connected:
            self.client_socket.close()
            self.connect_pb.setChecked(False)
            self.connect_pb.setText("Connect to Voltmeter")
            return
        print("Connecting")
        server_ip = str(self.ip_address_text.text())
        
        port = self.VOLTMETER_PORT
        print("Server IP: ", server_ip)
        if server_ip.find('xxx') != -1:
            print("bad IP")
            QMessageBox.about(self,
                'Bad Server IP', 'Please give a correct Server IP\n'
                'IP is ' + server_ip)
            self.connect_pb.setChecked(False)
            return
        else:
            print("Connecting to " + server_ip +":",port)
            self.client_socket.connectToHost(server_ip, port)
            self.client_socket.waitForConnected(1000)
              
        if self.client_socket.state() != QTcpSocket.ConnectedState:
            QMessageBox.warning(self,
                              'Connection failed', 'Please check IP address and port number\nIs the server running?')
            self.connect_pb.setChecked(False)
            return
        
        print("Connection established")
        self.client_socket.readyRead.connect(self.treatMeas)
        self.connect_pb.setText("Connected")

    def treatMeas(self):
        # get new values and display them
        msg = self.client_socket.readAll()
        newValue = int(bytes(msg).decode())
        print("new value: ",newValue)
        response = 'ok\n'
        self.client_socket.write(bytes(response,encoding="ascii"))
        newVoltage = int(newValue) * self.calib
        print(newVoltage)
        self.lcdNumber.display(newVoltage)
        self.Dial.setValue(newVoltage)
        
    def quit(self):
        app.exit()

    
app = QtWidgets.QApplication(sys.argv)
v = Voltmeter()
v.show()
app.exec_()

