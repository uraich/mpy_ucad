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
        MainWindow.resize(930, 585)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.scope_screen = QwtPlot(self.centralwidget)
        self.scope_screen.setGeometry(QtCore.QRect(0, 60, 551, 361))
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        self.scope_screen.setCanvasBackground(brush)
        self.scope_screen.setAutoReplot(False)
        self.scope_screen.setObjectName("scope_screen")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(590, 10, 311, 531))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setGeometry(QtCore.QRect(10, 290, 291, 231))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 100, 281, 121))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.time_base_label = QtWidgets.QLabel(self.layoutWidget)
        self.time_base_label.setObjectName("time_base_label")
        self.horizontalLayout_2.addWidget(self.time_base_label)
        self.time_base_combo = QtWidgets.QComboBox(self.layoutWidget)
        self.time_base_combo.setObjectName("time_base_combo")
        self.horizontalLayout_2.addWidget(self.time_base_combo)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.ip_label = QtWidgets.QLabel(self.layoutWidget)
        self.ip_label.setObjectName("ip_label")
        self.verticalLayout_2.addWidget(self.ip_label)
        self.server_ip_text = QtWidgets.QLineEdit(self.layoutWidget)
        self.server_ip_text.setObjectName("server_ip_text")
        self.verticalLayout_2.addWidget(self.server_ip_text)
        self.connect_pb = QtWidgets.QPushButton(self.layoutWidget)
        self.connect_pb.setCheckable(True)
        self.connect_pb.setObjectName("connect_pb")
        self.verticalLayout_2.addWidget(self.connect_pb)
        self.layoutWidget1 = QtWidgets.QWidget(self.frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 10, 281, 56))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.singleShot_btn = QtWidgets.QRadioButton(self.layoutWidget1)
        self.singleShot_btn.setChecked(True)
        self.singleShot_btn.setObjectName("singleShot_btn")
        self.gridLayout.addWidget(self.singleShot_btn, 0, 0, 1, 1)
        self.repetitive_btn = QtWidgets.QRadioButton(self.layoutWidget1)
        self.repetitive_btn.setObjectName("repetitive_btn")
        self.gridLayout.addWidget(self.repetitive_btn, 1, 0, 1, 1)
        self.start_stop_pb = QtWidgets.QPushButton(self.layoutWidget1)
        self.start_stop_pb.setCheckable(True)
        self.start_stop_pb.setObjectName("start_stop_pb")
        self.gridLayout.addWidget(self.start_stop_pb, 0, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget2.setGeometry(QtCore.QRect(11, 11, 281, 178))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.trig_level_label = QtWidgets.QLabel(self.layoutWidget2)
        self.trig_level_label.setObjectName("trig_level_label")
        self.gridLayout_2.addWidget(self.trig_level_label, 0, 0, 1, 1)
        self.trig_pos_label = QtWidgets.QLabel(self.layoutWidget2)
        self.trig_pos_label.setObjectName("trig_pos_label")
        self.gridLayout_2.addWidget(self.trig_pos_label, 0, 1, 1, 1)
        self.trigger_level_knob = QwtKnob(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trigger_level_knob.sizePolicy().hasHeightForWidth())
        self.trigger_level_knob.setSizePolicy(sizePolicy)
        self.trigger_level_knob.setUpperBound(3.3)
        self.trigger_level_knob.setObjectName("trigger_level_knob")
        self.gridLayout_2.addWidget(self.trigger_level_knob, 1, 0, 1, 1)
        self.trigger_pos_knob = QwtKnob(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trigger_pos_knob.sizePolicy().hasHeightForWidth())
        self.trigger_pos_knob.setSizePolicy(sizePolicy)
        self.trigger_pos_knob.setUpperBound(500.0)
        self.trigger_pos_knob.setTotalSteps(250)
        self.trigger_pos_knob.setObjectName("trigger_pos_knob")
        self.gridLayout_2.addWidget(self.trigger_pos_knob, 1, 1, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.frame_3)
        self.layoutWidget3.setGeometry(QtCore.QRect(11, 201, 281, 79))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.trigger_slope_label = QtWidgets.QLabel(self.layoutWidget3)
        self.trigger_slope_label.setObjectName("trigger_slope_label")
        self.gridLayout_4.addWidget(self.trigger_slope_label, 0, 1, 1, 1)
        self.normal_trigger_btn = QtWidgets.QRadioButton(self.layoutWidget3)
        self.normal_trigger_btn.setObjectName("normal_trigger_btn")
        self.gridLayout_4.addWidget(self.normal_trigger_btn, 1, 0, 1, 1)
        self.trigger_slope_pb = QtWidgets.QPushButton(self.layoutWidget3)
        self.trigger_slope_pb.setEnabled(True)
        self.trigger_slope_pb.setMaximumSize(QtCore.QSize(48, 48))
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
        self.gridLayout_4.addWidget(self.trigger_slope_pb, 1, 1, 1, 1)
        self.no_trigger_btn = QtWidgets.QRadioButton(self.layoutWidget3)
        self.no_trigger_btn.setChecked(True)
        self.no_trigger_btn.setObjectName("no_trigger_btn")
        self.gridLayout_4.addWidget(self.no_trigger_btn, 0, 0, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.layoutWidget5 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget5.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.layoutWidget6 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget6.setGeometry(QtCore.QRect(0, 0, 2, 2))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 930, 22))
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
        self.time_base_label.setText(_translate("MainWindow", "Time Base"))
        self.ip_label.setText(_translate("MainWindow", "IP address of Scope Server"))
        self.server_ip_text.setText(_translate("MainWindow", "192.168.0.144"))
        self.connect_pb.setText(_translate("MainWindow", "Connect to Scope"))
        self.singleShot_btn.setText(_translate("MainWindow", "Single Shot"))
        self.repetitive_btn.setText(_translate("MainWindow", "Repetitive"))
        self.start_stop_pb.setText(_translate("MainWindow", "Start Measurement"))
        self.trig_level_label.setText(_translate("MainWindow", "Trigger Level"))
        self.trig_pos_label.setText(_translate("MainWindow", "Trigger Position \n"
"[% of full scale]"))
        self.trigger_slope_label.setText(_translate("MainWindow", "Trigger slope"))
        self.normal_trigger_btn.setText(_translate("MainWindow", "normal Trigger"))
        self.no_trigger_btn.setText(_translate("MainWindow", "no Trigger"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

import icons_rc
