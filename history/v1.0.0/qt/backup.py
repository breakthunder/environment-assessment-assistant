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
        Backup.resize(429, 544)
        self.gridLayout = QtWidgets.QGridLayout(Backup)
        self.gridLayout.setObjectName("gridLayout")
        self.listView = QtWidgets.QListView(Backup)
        self.listView.setMinimumSize(QtCore.QSize(300, 500))
        self.listView.setObjectName("listView")
        self.gridLayout.addWidget(self.listView, 1, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(Backup)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 100))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(Backup)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(Backup)
        QtCore.QMetaObject.connectSlotsByName(Backup)

    def retranslateUi(self, Backup):
        _translate = QtCore.QCoreApplication.translate
        Backup.setWindowTitle(_translate("Backup", "选择备份文件"))
        self.pushButton.setText(_translate("Backup", "加载备份"))
        self.label.setText(_translate("Backup", "选择一个备份文件"))
