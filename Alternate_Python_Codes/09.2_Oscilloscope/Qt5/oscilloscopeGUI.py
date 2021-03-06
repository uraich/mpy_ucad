#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys,errno
from math import pi,sin
import time
import icons

from PyQt5 import QtWidgets, QtCore, QtChart, uic
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QTcpServer,QTcpSocket,QHostAddress
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import QTcpServer,QTcpSocket,QHostAddress
from PyQt5.Qwt import *

from scope_Ui import  Ui_MainWindow

class Oscilloscope(QtWidgets.QMainWindow,Ui_MainWindow):
    
    SCOPE_PORT = 5000
    frequencies = {'5 kHz':  0.2,
                   '2 kHz':  0.5,
                   '1 kHz':  1,
                   '500 Hz': 2,
                   '200 Hz': 5,
                   '100 Hz': 10}
    
    TRIG_SLOPE_RISING  = 0
    TRIG_SLOPE_FALLING = 1
    
    def __init__(self,parent=None):
 
        super(Oscilloscope, self).__init__(parent)
        self.setupUi(self)

        self.time_base = 0.2
        self.trigger_level = 1.65
        self.trigger_pos = 35
        self.trigger_slope = self.TRIG_SLOPE_RISING
        self.no_trigger = True
        self.connected = False
        self.singleShot = True
        self.ok = False
        self.measuring = False
        self.client_socket = QTcpSocket(self)
        
        # setup screen
        self.scope_screen.setTitle("Uli's virtual Oscilloscope")
        self.scope_screen.insertLegend(QwtLegend())
        self.scope_screen.setAxisScale(1,0,3.3,0.5)

        self.scope_screen.setAxisTitle(QwtPlot.xBottom, "Time [ms]")
        self.scope_screen.setAxisScale(QwtPlot.xBottom,0.0, 100)
        
        self.scope_screen.setAxisTitle(QwtPlot.yLeft, "Signal")
        self.scope_screen.setAxisScale(QwtPlot.yLeft ,0.0, 3.3)
        
        self.canvas = QwtPlotCanvas()
        self.canvas.setLineWidth( 1 )
        self.canvas.setFrameStyle( QFrame.Box | QFrame.Plain )
        
        self.canvasPalette = QPalette( Qt.gray )
        self.canvasPalette.setColor( QPalette.Foreground, QColor( 133, 190, 232 ) ) 
        self.canvas.setPalette( self.canvasPalette )

        self.scope_screen.setCanvas( self.canvas )

        #  ...a vertical for the trigger position
        self.tpos_marker = QwtPlotMarker()
        # self.tpos_marker.setLabel( QwtText( "trigger pos" ) )
        self.tpos_marker.setLabelAlignment( Qt.AlignLeft | Qt.AlignBottom )
        self.tpos_marker.setLabelOrientation( Qt.Vertical )
        self.tpos_marker.setLineStyle( QwtPlotMarker.VLine )
        self.tpos_marker.setLinePen( Qt.black, 0, Qt.DashDotLine )
        self.tpos_marker.setXValue( int(self.time_base * 5 * self.trigger_pos) )
        self.tpos_marker.attach( self.scope_screen )
        
        #  ...a horizontal line for the trigger level
        self.tl_marker = QwtPlotMarker()
        # self.tl_marker.setLabel( QwtText( "trigger level" ) )
        self.tl_marker.setLabelAlignment( Qt.AlignLeft | Qt.AlignBottom )
        self.tl_marker.setLabelOrientation( Qt.Horizontal )
        self.tl_marker.setLineStyle( QwtPlotMarker.HLine )
        self.tl_marker.setLinePen( Qt.black, 0, Qt.DashDotLine )
        self.tl_marker.setYValue( 1.6 )
        self.tl_marker.attach( self.scope_screen )
        
        grid = QwtPlotGrid()
        grid.attach(self.scope_screen)

        self.curve = QwtPlotCurve()
        self.curve.setTitle("Trace")
        self.curve.setPen(Qt.green,2)
        self.curve.setRenderHint( QwtPlotItem.RenderAntialiased, True )
        
        self.curve.attach(self.scope_screen)

        self.scope_screen.replot()

        for pulse_freq in self.frequencies.keys():
            self.time_base_combo.addItem(pulse_freq)
        self.time_base_combo.currentIndexChanged.connect(self.time_base_changed)
        
        self.trigger_slope_pb.clicked.connect(self.trig_slope_changed)
        self.actionQuit.triggered.connect(self.quit)

        self.risingEdgeIcon =  QIcon()
        self.risingEdgeIcon.addPixmap(QPixmap(":/icons/risingEdge.png"))
        self.fallingEdgeIcon =  QIcon()
        self.fallingEdgeIcon.addPixmap(QPixmap(":/icons/fallingEdge.png"))

        self.start_stop_pb.clicked.connect(self.start_stop_meas)
        self.server_ip_text = self.findChild(
            QtWidgets.QLineEdit,'server_ip_text')

        self.trigger_level_knob.valueChanged.connect(self.trig_lvl_changed)
        self.trigger_level_knob.setValue(self.trigger_level)
        
        self.trigger_pos_knob.setUpperBound(self.time_base*500)
        self.trigger_pos_knob.setValue(self.trigger_pos)      
        self.trigger_pos_knob.valueChanged.connect(self.trig_pos_changed)

        self.no_trigger_btn.clicked.connect(self.trigger_changed)
        self.normal_trigger_btn.clicked.connect(self.trigger_changed)

        self.connect_pb.clicked.connect(self.connect)

        self.singleShot_btn.clicked.connect(self.singleShotChanged)
        self.repetitive_btn.clicked.connect(self.singleShotChanged)
        
        self.normal_trigger_btn.clicked.connect(self.triggerChanged)
        self.no_trigger_btn.clicked.connect(self.triggerChanged)
        
        # timers for the knobs
        self.triglvl_timer = QTimer()
        self.triglvl_timer.setSingleShot(True)
        self.triglvl_timer.timeout.connect(self.triglvl_ready)
        
        self.trigpos_timer = QTimer()
        self.trigpos_timer.setSingleShot(True)
        self.trigpos_timer.timeout.connect(self.trigpos_ready)
          
        self.trace=None
        self.connected=False

    def singleShotChanged(self):
        if self.measuring:
            QMessageBox.about(self,
                'Measuring', 'Measurement in progress\n'
                              'Please stop it before changing parameters')
            self.repetitive_btn.setChecked(True)
            return
        if self.singleShot_btn.isChecked():
            print("Single shot enabled")
            self.singleShot = True
        else:
            print("single shot disabled")
            self.singleShot = False
            
    def triggerChanged(self):
        if self.no_trigger_btn.isChecked():
            print("trigger disabled")
            self.no_trigger = True
        else:
            print("trigger enabled")
            self.no_trigger = False
            
        if self.connected:
            # notrig
            if self.no_trigger:
                no_trig_msg = "notrig=1\n"
            else:
                no_trig_msg = "notrig=0\n"
                
            print("Sending: " + no_trig_msg)
            self.client_socket.write(bytes(no_trig_msg,encoding="ascii"))
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
                
    def triglvl_ready(self):
        # trigger level
        trig_lvl_msg = "triglvl=" + str(self.trigger_level) + "\n"
        print("Sending: " + trig_lvl_msg)
        self.client_socket.write(bytes(trig_lvl_msg,encoding="ascii"))       
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())        
        
    def trigpos_ready(self):
        # trigger pos
        trig_pos_msg = "trigpos=" + str(int(self.trigger_pos*5)) + "\n"
        print("Sending: " + trig_pos_msg)
        self.client_socket.write(bytes(trig_pos_msg,encoding="ascii"))        
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
    def trigger_changed(self):
        if self.measuring:
            QMessageBox.about(self,
                'Measuring', 'Measurement in progress\n'
                              'Please stop it before changing parameters')
            if self.no_trigger:
                self.no_trigger_btn.setChecked(True)
            else:
                self.normal_trigger_btn.setChecked(True)
            return
        
        if self.normal_trigger_btn.isChecked():
            self.no_trigger = False
            # print("normal trigger")
        else:
            self.no_trigger = True
            # print("no trigger")
        
    def trig_lvl_changed(self,new_trig_lvl):
        if self.measuring:
            QMessageBox.about(self,
                'Measuring', 'Measurement in progress\n'
                              'Please stop it before changing parameters')
            self.tl_marker.setYValue( self.trigger_level )
            return
        print("new trigger level: ",new_trig_lvl)
        self.trigger_level = new_trig_lvl
        self.tl_marker.setYValue(new_trig_lvl)
        self.scope_screen.replot()
        if self.connected:
            self.triglvl_timer.start(500)

    def trig_pos_changed(self,new_trig_pos):
        if self.measuring:
            QMessageBox.about(self,
                'Measuring', 'Measurement in progress\n'
                              'Please stop it before changing parameters')
            self.tpos_marker.setXValue( int(self.trigger_pos * 5 * self.time_base) )
            return
        print("new trigger position: ",new_trig_pos)
        self.trigger_pos = new_trig_pos
        self.tpos_marker.setXValue(int(new_trig_pos * 5 * self.time_base) )
        self.scope_screen.replot()
        if self.connected:
            self.trigpos_timer.start(500)
            
    def connect(self):
        server_ip = str(self.server_ip_text.text())
        port = self.SCOPE_PORT
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
              
        if self.client_socket.state() != QTcpSocket.ConnectedState:
            QMessageBox.about(self,
                              'Connection failed', 'Please check IP address and port number\nIs the server running?')
            self.connect_pb.setChecked(False)
            return
        
        print("Connection established")
        self.connect_pb.setText("Connected")

        # await the connection message of the server
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("connection  msg: ",bytes(responseMsg).decode())
        
        # notrig
        self.msg = None
        if self.no_trigger:
            no_trig_msg = "notrig=1\n"
        else:
            no_trig_msg = "notrig=0\n"
        print("Sending: " + no_trig_msg)
        self.client_socket.write(bytes(no_trig_msg,encoding="ascii"))
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        # time base
        pulse_T_msg = "pulse_T=" + str(self.time_base) + "\n"
        print("Sending: " + pulse_T_msg)
        self.client_socket.write(bytes(pulse_T_msg,encoding="ascii"))       
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        # trigger level
        trig_lvl_msg = "triglvl=" + str(self.trigger_level) + "\n"
        print("Sending: " + trig_lvl_msg)
        self.client_socket.write(bytes(trig_lvl_msg,encoding="ascii"))       
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        # trigger pos
        trig_pos_msg = "trigpos=" + str(int(self.trigger_pos/self.time_base)) + "\n"
        print("Sending: " + trig_pos_msg)
        self.client_socket.write(bytes(trig_pos_msg,encoding="ascii"))        
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        # trigger slope
        trig_slope_msg = "trigslope=" + str(self.trigger_slope) + "\n"
        print("Sending: " + trig_slope_msg)
        self.client_socket.write(bytes(trig_slope_msg,encoding="ascii"))
        
        self.client_socket.waitForReadyRead()
        responseMsg = self.client_socket.readAll()
        print("reponse msg: ",bytes(responseMsg).decode())
        
        self.connected = True

    def time_base_changed(self):
        self.time_base = self.frequencies[self.time_base_combo.currentText()]
        print("new time base: ", self.time_base)
        self.scope_screen.setAxisScale(QwtPlot.xBottom,0.0, self.time_base * 500)
        self.scope_screen.replot()
        # change the trigger position to % of new time base
        self.tpos_marker.setXValue( int(self.time_base * 5 * self.trigger_pos) )
        x = []
        y = []
        self.curve.setSamples(x,y)
        self.scope_screen.replot()
        
        if self.connected:
            # time base
            pulse_T_msg = "pulse_T=" + str(self.time_base) + "\n"
            print("Sending: " + pulse_T_msg)
            self.client_socket.write(bytes(pulse_T_msg,encoding="ascii"))       
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
        
    def start_stop_meas(self):
        if not self.connected:
            if self.start_stop_pb.isChecked():
                QMessageBox.about(self,
                                  'Not Connected', 'Not connected to the oscilloscpe server\nPlease connect first')
                self.start_stop_pb.setChecked(False)
            return
        
        if self.start_stop_pb.isChecked():
            self.start_stop_pb.setText("Stop measurement")
            start_stop_msg = "meas=1\n"
            print("Sending " + start_stop_msg)
            self.client_socket.write(start_stop_msg.encode())
            self.client_socket.readyRead.connect(self.readTrace)
            self.measuring = True
        else:
            self.start_stop_pb.setText("Start measurement")
            start_stop_msg = "meas=0\n"
            print("Sending " + start_stop_msg)
            self.client_socket.write(start_stop_msg.encode())
            time.sleep(10)
            self.client_socket.readyRead.disconnect(self.readTrace)
            self.measuring = False

    def readTrace(self):
        dataMsg = self.client_socket.readAll().data()
        print("reponse msg from : Reading trace data:\n",dataMsg, type(dataMsg))
        y = [float(i)*0.01289 for i in list(dataMsg)]       # conversion factor: 3.3V/256
        x = [i*self.time_base for i in range(500)]
        self.curve.setSamples(x,y)
        self.scope_screen.replot()
        if self.singleShot:
            self.start_stop_pb.setText("Start measurement")
            self.start_stop_pb.setChecked(False)
            self.client_socket.readyRead.disconnect(self.readTrace)
            self.measuring = False
            return
        else:
            start_stop_msg = "meas=1\n"
            print("Sending " + start_stop_msg)
            self.client_socket.write(start_stop_msg.encode())
            
    def create_linechart(self):
        series = QLineSeries(self)
        for i in range(512):
            series.append(i,int.from_bytes(self.trace[i],"big"))     
            
        self.osc_chart = QChart()
        self.osc_chart.addSeries(series)
        self.osc_chart.createDefaultAxes()
        self.osc_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.osc_chart.setTitle("ESP32 Oscilloscope")

        self.osc_chart.legend().setVisible(True)
        self.osc_chart.legend().setAlignment(Qt.AlignBottom)
        self.osc_screen.setChart(self.osc_chart)
        
    def quit(self):
        app.exit()

    def trig_slope_changed(self):
        if self.measuring:
            QMessageBox.about(self,
                'Measuring', 'Measurement in progress\n'
                              'Please stop it before changing parameters')
            if self.trigger_slope == self.TRIG_SLOPE_RISING:
                self.trigger_slope_pb.setIcon(self.risingEdgeIcon)
            else:
                self.trigger_slope_pb.setIcon(self.fallingEdgeIcon)
            return
        
        # print("Trigger slope changed")
        if self.trigger_slope_pb.isChecked():
            self.trigger_slope_pb.setIcon(self.fallingEdgeIcon)
            self.trigger_slope = self.TRIG_SLOPE_FALLING
        else:
            self.trigger_slope_pb.setIcon(self.risingEdgeIcon)
            self.trigger_slope = self.TRIG_SLOPE_RISING
        if self.connected:
            # send new value to scope server
            trig_slope_msg = "trigslope=" + str(self.trigger_slope) + "\n"
            print("Sending: " + trig_slope_msg)
            self.client_socket.write(bytes(trig_slope_msg,encoding="ascii"))
            
            self.client_socket.waitForReadyRead()
            responseMsg = self.client_socket.readAll()
            print("reponse msg: ",bytes(responseMsg).decode())
    
app = QtWidgets.QApplication(sys.argv)
scope = Oscilloscope()
scope.show()
app.exec_()
