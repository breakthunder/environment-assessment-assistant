# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'backup.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Backup(object):
    def setupUi(self, Backup):
        Backup.setObjectName("Backup")
        Backup.resize(451, 566)
        Backup.setStyleSheet(".QWidget{background:transparent}")
        self.gridLayout = QtWidgets.QGridLayout(Backup)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(Backup)
        self.widget.setStyleSheet(".QWidget,QListView{background:rgb(250, 250, 250);border-radius:10px}\n"
".QPushButton{\n"
"    background-color: rgb(149, 142, 255);\n"
"    border-radius:10px;color:white}\n"
".QPushButton::hover{color:rgb(255, 140, 0)}\n"
".QPushButton:pressed{background-color:rgb(230, 221, 212)}")
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.listView = QtWidgets.QListView(self.widget)
        self.listView.setMinimumSize(QtCore.QSize(300, 500))
        self.listView.setObjectName("listView")
        self.gridLayout_2.addWidget(self.listView, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 1)

        self.retranslateUi(Backup)
        QtCore.QMetaObject.connectSlotsByName(Backup)

    def retranslateUi(self, Backup):
        _translate = QtCore.QCoreApplication.translate
        Backup.setWindowTitle(_translate("Backup", "选择备份文件"))
        self.label.setText(_translate("Backup", "选择一个备份文件"))
        self.pushButton.setText(_translate("Backup", "加载备份"))
