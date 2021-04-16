#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys,errno

from PyQt5 import QtWidgets, QtCore, QtChart, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpServer,QTcpSocket,QHostAddress
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis
from PyQt5.QtCore import QPointF, Qt, QTimer
from PyQt5.QtGui import QPainter, QIcon, QPixmap

from pulse_gen_display import PulseGenDisplay
from pulseGen_Ui import Ui_MainWindow

class PulseGen(QtWidgets.QMainWindow,Ui_MainWindow):
    
    GENERATOR_PORT = 5000
    def __init__(self,parent=None):
                
        super(PulseGen, self).__init__(parent)
        self.setupUi(self)
        self.pulse_gen_display = PulseGenDisplay()
        self.display_data = [0]*500

        self.pulse_height_max = self.pulse_height_dial.maximum()
        self.pulse_height_min = self.pulse_height_dial.minimum()

        self.pulse_gen_display.pulse_height = self.pulse_height_max
        # set pulse height
        self.pulse_gen_display.pulse_height = self.pulse_height_max
        self.pulse_height_dial.setValue(self.pulse_gen_display.pulse_height)
        self.pulse_height_dial.actionTriggered.connect(self.avoid_wrapping)
        self.pulse_height_dial.valueChanged.connect(self.pulse_height_changed)
    
        self.pulse_height_text.setText(str(self.pulse_gen_display.pulse_height))

        # don't allow editing
        self.pulse_height_text.textChanged.connect(self.no_editing)
        
        # pulse shape
        for pulse_form in self.pulse_gen_display.pulse_shape.keys():
            self.pulse_shape_combo.addItem(pulse_form)
        self.pulse_shape_combo.currentIndexChanged.connect(self.pulse_shape_changed)
            
        current_pulse_form = self.pulse_shape_combo.currentText()
        self.pulse_gen_display.pulse_form = self.pulse_gen_display.pulse_shape[current_pulse_form]
        print("Current pulse form: " + current_pulse_form + " code: " + str(self.pulse_gen_display.pulse_form))
        
        for pulse_freq in self.pulse_gen_display.frequencies.keys():
            self.gen_freq_combo.addItem(pulse_freq)
            
        current_pulse_freq = self.gen_freq_combo.currentText()
        self.pulse_gen_display.pulse_T = self.pulse_gen_display.frequencies[current_pulse_freq]
        print("Current pulse T: " + str(self.pulse_gen_display.pulse_T))
        self.gen_freq_combo.currentIndexChanged.connect(self.pulse_freq_changed)
                
        for display_freq in self.pulse_gen_display.frequencies.keys():
            self.display_freq_combo.addItem(display_freq)
        self.display_freq_combo.currentIndexChanged.connect(self.display_freq_changed)
            
        current_display_freq = self.display_freq_combo.currentText()
        self.pulse_gen_display.display_T = self.pulse_gen_display.frequencies[current_display_freq]
        print("Current display T: " + str(self.pulse_gen_display.display_T))            

        self.start_stop_pb.clicked.connect(self.start_stop_meas)
        self.connect_pb.clicked.connect(self.connect)
        
        self.gen_chart = QChart()
        self.gen_chart.legend().hide()
        self.x_axis = QValueAxis()
        self.x_axis.setMax(500*self.pulse_gen_display.display_T)
        self.x_axis.setMin(0)
        self.y_axis = QValueAxis()
        self.y_axis.setMax(3.3)
        self.y_axis.setMin(0)
        self.gen_chart.addAxis(self.x_axis,Qt.AlignBottom)
        self.gen_chart.addAxis(self.y_axis,Qt.AlignLeft)
        self.generator_screen.setChart(self.gen_chart)
        # display the initial pulse
        self.pulse_gen_display.calc_pulse()
        self.pulse_gen_display.get_display_data()
            
        self.series = QLineSeries()
        
        for i in range(500):
            self.series.append(i*self.pulse_gen_display.display_T,
                               self.pulse_gen_display.display_data[i]*self.pulse_gen_display.calib)
        self.gen_chart.addSeries(self.series)            
        self.series.attachAxis(self.x_axis)
        self.series.attachAxis(self.y_axis)
        self.display_pulse()

        self.pulse_height_timer = QTimer()
        self.pulse_height_timer.setSingleShot(True)
        self.pulse_height_timer.timeout.connect(self.pulse_height_ready)
        
        self.genRunning = False
        self.actionQuit.triggered.connect(self.quit)
        
        self.client_socket = QTcpSocket(self)
        self.connected=False
        self.show()

    def no_editing(self):
        self.pulse_height_text.setText(str(self.pulse_gen_display.pulse_height))
        
    def avoid_wrapping(self,val):
        if val == QtWidgets.QAbstractSlider.SliderMove:
            minDistance = 1
            if self.pulse_height_dial.value() == self.pulse_height_max \
               and self.pulse_height_dial.sliderPosition()<self.pulse_height_max-minDistance:
                self.pulse_height_dial.setSliderPosition(self.pulse_height_max)
            elif self.pulse_height_dial.value() == self.pulse_height_min \
               and self.pulse_height_dial.sliderPosition()>self.pulse_height_min+minDistance:
                self.pulse_height_dial.setSliderPosition(self.pulse_height_min)
        
    def pulse_shape_changed(self):
        '''
        if self.genRunning:
            print("Current shape index: ",self.pulse_shape_combo.currentIndex())
            print("current pulse form: ",self.pulse_gen_display.pulse_form)
            if self.pulse_shape_combo.currentIndex() == self.pulse_gen_display.pulse_form:
                return
            QMessageBox.warning(self,
                                'Pulse generation is active',
                                'Pulse generator is running\nPlease stop pulse generation before changing parameters')
            self.pulse_shape_combo.setCurrentIndex(self.pulse_gen_display.pulse_form)
            return
        '''
        print("pulse shape changed")
        current_pulse_form = self.pulse_shape_combo.currentText()
        self.pulse_gen_display.pulse_form = self.pulse_gen_display.pulse_shape[current_pulse_form]
        print("Current pulse form: " + current_pulse_form + " code: " + str(self.pulse_gen_display.pulse_form))
        self.display_pulse()
        if not self.connected:
            return
        else:
            pulse_form_msg = "pulse_shape=" + str(self.pulse_gen_display.pulse_form) + "\n"
            print("Sending: " + pulse_form_msg)
            self.client_socket.write(bytes(pulse_form_msg,encoding="ascii"))
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
            
    def pulse_freq_changed(self):
        
        new_freq = self.gen_freq_combo.currentText()
        self.pulse_gen_display.pulse_T= self.pulse_gen_display.frequencies[new_freq]
        print("Pulse frequency changed to " + new_freq + "T: " + str(self.pulse_gen_display.pulse_T))
        self.display_pulse()
        
        '''
        if self.genRunning:
            if self.pulse_gen_display.frequencies[self.gen_freq_combo.currentText()] == self.pulse_gen_display.pulse_T:
                return

            QMessageBox.warning(self,
                                'Pulse generation is active',
                                'Pulse generator is running\nPlease stop pulse generation before changing parameters')
            index = 0
            for freq in self.pulse_gen_display.frequencies.keys():
                print("freq: ",freq)
                print("val: ",self.pulse_gen_display.frequencies[freq])
                if self.pulse_gen_display.frequencies[freq] == self.pulse_gen_display.pulse_T:
                    self.gen_freq_combo.setCurrentIndex(index)
                    break                     
                index += 1
            return
        '''
        if not self.connected:
            return
        else:
            pulse_T_msg = "pulse_T=" + str(self.pulse_gen_display.pulse_T) + "\n"
            print("Sending: " + pulse_T_msg)
            self.client_socket.write(bytes(pulse_T_msg,encoding="ascii"))
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
        
    def display_freq_changed(self):
        new_freq = self.display_freq_combo.currentText()
        self.pulse_gen_display.display_T= self.pulse_gen_display.frequencies[new_freq]
        self.display_pulse()
        
    def pulse_height_changed(self):       
        self.pulse_gen_display.pulse_height = self.pulse_height_dial.value()
        self.pulse_height_text.setText(str(self.pulse_gen_display.pulse_height))
        self.display_pulse()
        self.pulse_height_timer.start(500)
        
    def pulse_height_ready(self):
        print("Timeout")
        if not self.connected:
            return
        else:
            pulse_height_msg = "pulse_height=" + str(self.pulse_gen_display.pulse_height) + "\n"
            print("Sending: " + pulse_height_msg)
            self.client_socket.write(bytes(pulse_height_msg,encoding="ascii"))
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())   
        
    def connect(self):
        if self.connected:
            self.client_socket.close()
            self.connected=False
            self.connect_pb.setChecked(False)
            self.connect_pb.setText("Connect to Pulse Generator")
            return
        server_ip = str(self.server_ip_text.text())
        port = self.GENERATOR_PORT
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
        self.connect_pb.setText("Connected")
        
        self.client_socket.waitForReadyRead()
        connectMsg = self.client_socket.readAll()
        msgstring = bytes(connectMsg).decode()
        print("Connection message:" + msgstring)
        
        print("Send generator settings")
        pulse_form_msg = "pulse_shape=" + str(self.pulse_gen_display.pulse_form) + "\n"
        print("Sending: " + pulse_form_msg)
        self.client_socket.write(bytes(pulse_form_msg,encoding="ascii"))
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        pulse_T_msg = "pulse_T=" + str(self.pulse_gen_display.pulse_T) + "\n"
        print("Sending: " + pulse_T_msg)
        self.client_socket.write(bytes(pulse_T_msg,encoding="ascii"))
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        pulse_height_msg = "pulse_height=" + str(self.pulse_gen_display.pulse_height) + "\n"
        print("Sending: " + pulse_height_msg)
        self.client_socket.write(bytes(pulse_height_msg,encoding="ascii"))
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())                      

        running_msg = 'running?=\n'
        print("Sending: " + running_msg)
        self.client_socket.write(bytes(running_msg,encoding="ascii"))
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        response = bytes(responseMsg).decode()
        print("reponse msg: ",response)
        if response == 'yes\n':
            print("task is running")
        elif response == 'no\n':
            print("task is not running")
        else:
            print("Don't know if task is running")

        self.connected = True
            
    def start_stop_meas(self):
        if not self.connected:
            QMessageBox.about(self,
                'You must be connected to the generator server\n'
                              'please connect and try again')
            return
        
        if self.start_stop_pb.isChecked():
            print("Start generation")
            # send current generator settings
            
            self.start_stop_pb.setText("Stop Pulse Generation")
            msg = 'start=\n'
            print("Sending: " + msg)
            self.client_socket.write(msg.encode())
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
            self.genRunning=True
        else:
            print("Stop generation")
            self.start_stop_pb.setText("Start Pulse Generation")
            msg = 'stop=\n'
            self.client_socket.write(msg.encode())
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())           
            self.genRunning = False
            
    def readTrace(self):
        print("Message from the generator")
        data = self.server_socket.readAll()
        msgstring = bytes(data).decode()
        print(msgstring)
        print(data,type(data))
        
    def display_pulse(self):
        self.pulse_gen_display.calc_pulse()
        self.pulse_gen_display.get_display_data()
        
        self.x_axis.setMax(500*self.pulse_gen_display.display_T)
        data_points = self.series.pointsVector()
        for i in range(500):
            data_points[i].setX(i*self.pulse_gen_display.display_T)
            data_points[i].setY(self.pulse_gen_display.display_data[i]*self.pulse_gen_display.calib)
        self.series.replace(data_points)
                                
    def quit(self):
        app.exit()

app = QtWidgets.QApplication(sys.argv)
pg = PulseGen()
pg.show()
app.exec_()
