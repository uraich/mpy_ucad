#!/usr/bin/python3
# This Python file uses the following encoding: utf-8
import sys,errno
from math import pi,sin
import socket
from PyQt5 import QtWidgets, QtCore, QtChart, uic
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtNetwork import QTcpServer,QTcpSocket,QHostAddress
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPainter

class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('oscilloscope.ui', self)

        self.osc_screen = self.findChild(
            QtChart.QChartView,'oscilloscope_screen')

        self.trig_slope = self.findChild(
            QtWidgets.QPushButton,'trigger_slope_pb')
        self.trig_slope.clicked.connect(self.trig_slope_changed)
        
        self.actionQuit.triggered.connect(self.quit)
        self.show()
        self.create_linechart()

    def create_linechart(self):
        series = QLineSeries(self)
        sinTab = self.calc_sine_function()
        for i in range(512):
            series.append(i,sinTab[i])     
            
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
        print("Trigger slope changed")
        
    def calc_sine_function(self):
        sinTable = [None]*512
        for i in range(512):
            sinTable[i] = (sin(2*i*pi/512) + 1) * 1.65 # sine function with values between 0 and 1.15V
        return sinTable
            
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
