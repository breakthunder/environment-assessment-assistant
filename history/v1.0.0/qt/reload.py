# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reload.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import resources_rc

class Ui_reload(object):
    def setupUi(self, reload):
        reload.setObjectName("reload")
        reload.resize(300, 300)
        reload.setMinimumSize(QtCore.QSize(300, 300))
        reload.setMaximumSize(QtCore.QSize(300, 300))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/resources/clinet.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        reload.setWindowIcon(icon)
        self.groupBox = QtWidgets.QGroupBox(reload)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 101, 261))
        self.groupBox.setObjectName("groupBox")
        self.cu_check = QtWidgets.QCheckBox(self.groupBox)
        self.cu_check.setGeometry(QtCore.QRect(10, 20, 91, 19))
        self.cu_check.setObjectName("cu_check")
        self.as_check = QtWidgets.QCheckBox(self.groupBox)
        self.as_check.setGeometry(QtCore.QRect(10, 50, 91, 19))
        self.as_check.setObjectName("as_check")
        self.hg_check = QtWidgets.QCheckBox(self.groupBox)
        self.hg_check.setGeometry(QtCore.QRect(10, 80, 91, 19))
        self.hg_check.setObjectName("hg_check")
        self.pb_check = QtWidgets.QCheckBox(self.groupBox)
        self.pb_check.setGeometry(QtCore.QRect(10, 110, 91, 19))
        self.pb_check.setObjectName("pb_check")
        self.cd_check = QtWidgets.QCheckBox(self.groupBox)
        self.cd_check.setGeometry(QtCore.QRect(10, 140, 91, 19))
        self.cd_check.setObjectName("cd_check")
        self.cr_check = QtWidgets.QCheckBox(self.groupBox)
        self.cr_check.setGeometry(QtCore.QRect(10, 170, 91, 19))
        self.cr_check.setObjectName("cr_check")
        self.zn_check = QtWidgets.QCheckBox(self.groupBox)
        self.zn_check.setGeometry(QtCore.QRect(10, 200, 91, 19))
        self.zn_check.setObjectName("zn_check")
        self.mn_check = QtWidgets.QCheckBox(self.groupBox)
        self.mn_check.setGeometry(QtCore.QRect(10, 230, 91, 19))
        self.mn_check.setObjectName("mn_check")
        self.pushButton = QtWidgets.QPushButton(reload)
        self.pushButton.setGeometry(QtCore.QRect(160, 40, 91, 51))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(reload)
        QtCore.QMetaObject.connectSlotsByName(reload)

    def retranslateUi(self, reload):
        _translate = QtCore.QCoreApplication.translate
        reload.setWindowTitle(_translate("reload", "选择重金属"))
        self.groupBox.setTitle(_translate("reload", "重金属类型"))
        self.cu_check.setText(_translate("reload", "Cu"))
        self.as_check.setText(_translate("reload", "As"))
        self.hg_check.setText(_translate("reload", "Hg"))
        self.pb_check.setText(_translate("reload", "Pb"))
        self.cd_check.setText(_translate("reload", "Cd"))
        self.cr_check.setText(_translate("reload", "Cr"))
        self.zn_check.setText(_translate("reload", "Zn"))
        self.mn_check.setText(_translate("reload", "Mn"))
        self.pushButton.setText(_translate("reload", "重载"))
