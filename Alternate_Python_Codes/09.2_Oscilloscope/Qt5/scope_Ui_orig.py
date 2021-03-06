# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scope.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qwt import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(736, 502)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.triggerLine = QtWidgets.QFrame(self.centralwidget)
        self.triggerLine.setGeometry(QtCore.QRect(50, 200, 381, 16))
        self.triggerLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.triggerLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.triggerLine.setObjectName("triggerLine")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(230, 60, 21, 331))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 10, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.scope_screen = QwtPlot(self.centralwidget)
        self.scope_screen.setGeometry(QtCore.QRect(0, 60, 431, 361))
        brush = QtGui.QBrush(QtGui.QColor(114, 159, 207))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.scope_screen.setCanvasBackground(brush)
        self.scope_screen.setAutoReplot(True)
        self.scope_screen.setObjectName("scope_screen")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(460, 50, 254, 374))
        self.widget.setObjectName("widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.trig_level_label = QtWidgets.QLabel(self.widget)
        self.trig_level_label.setObjectName("trig_level_label")
        self.gridLayout_2.addWidget(self.trig_level_label, 0, 0, 1, 1)
        self.trig_pos_label = QtWidgets.QLabel(self.widget)
        self.trig_pos_label.setObjectName("trig_pos_label")
        self.gridLayout_2.addWidget(self.trig_pos_label, 0, 1, 1, 1)
        self.Knob_2 = QwtKnob(self.widget)
        self.Knob_2.setUpperBound(3.3)
        self.Knob_2.setObjectName("Knob_2")
        self.gridLayout_2.addWidget(self.Knob_2, 1, 0, 1, 1)
        self.Knob = QwtKnob(self.widget)
        self.Knob.setUpperBound(500.0)
        self.Knob.setTotalSteps(250)
        self.Knob.setObjectName("Knob")
        self.gridLayout_2.addWidget(self.Knob, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.no_trigger_btn = QtWidgets.QRadioButton(self.widget)
        self.no_trigger_btn.setChecked(True)
        self.no_trigger_btn.setObjectName("no_trigger_btn")
        self.gridLayout.addWidget(self.no_trigger_btn, 0, 0, 1, 1)
        self.trigger_slope_label = QtWidgets.QLabel(self.widget)
        self.trigger_slope_label.setObjectName("trigger_slope_label")
        self.gridLayout.addWidget(self.trigger_slope_label, 0, 1, 1, 1)
        self.normal_trigger_btn = QtWidgets.QRadioButton(self.widget)
        self.normal_trigger_btn.setObjectName("normal_trigger_btn")
        self.gridLayout.addWidget(self.normal_trigger_btn, 1, 0, 1, 1)
        self.trigger_slope_pb = QtWidgets.QPushButton(self.widget)
        self.trigger_slope_pb.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/risingEdge.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/fallingEdge.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        icon.addPixmap(QtGui.QPixmap(":/icons/risingEdge.png"), QtGui.QIcon.Selected, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/fallingEdge.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.trigger_slope_pb.setIcon(icon)
        self.trigger_slope_pb.setIconSize(QtCore.QSize(48, 48))
        self.trigger_slope_pb.setCheckable(True)
        self.trigger_slope_pb.setFlat(True)
        self.trigger_slope_pb.setObjectName("trigger_slope_pb")
        self.gridLayout.addWidget(self.trigger_slope_pb, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.ip_label = QtWidgets.QLabel(self.widget)
        self.ip_label.setObjectName("ip_label")
        self.verticalLayout.addWidget(self.ip_label)
        self.server_ip_text = QtWidgets.QLineEdit(self.widget)
        self.server_ip_text.setObjectName("server_ip_text")
        self.verticalLayout.addWidget(self.server_ip_text)
        self.connect_pb = QtWidgets.QPushButton(self.widget)
        self.connect_pb.setCheckable(True)
        self.connect_pb.setObjectName("connect_pb")
        self.verticalLayout.addWidget(self.connect_pb)
        self.start_stop_pb = QtWidgets.QPushButton(self.widget)
        self.start_stop_pb.setCheckable(True)
        self.start_stop_pb.setObjectName("start_stop_pb")
        self.verticalLayout.addWidget(self.start_stop_pb)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 736, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Uli\'s Oscilloscope"))
        self.label.setText(_translate("MainWindow", "Virtual Oscilloscope"))
        self.trig_level_label.setText(_translate("MainWindow", "Trigger Level"))
        self.trig_pos_label.setText(_translate("MainWindow", "Trigger Position"))
        self.no_trigger_btn.setText(_translate("MainWindow", "no Trigger"))
        self.trigger_slope_label.setText(_translate("MainWindow", "Trigger slope"))
        self.normal_trigger_btn.setText(_translate("MainWindow", "normal Trigger"))
        self.ip_label.setText(_translate("MainWindow", "IP address of Scope Server"))
        self.server_ip_text.setText(_translate("MainWindow", "192.168.0.xxx"))
        self.connect_pb.setText(_translate("MainWindow", "Connect to Scope"))
        self.start_stop_pb.setText(_translate("MainWindow", "Start Measurement"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

import icons_rc
