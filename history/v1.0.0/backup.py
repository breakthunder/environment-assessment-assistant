from PyQt5.QtWidgets import QDialog, QAbstractItemView
from eaa.qt.backup import *
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import *
import os

class Backup_window(QDialog):
    def __init__(self, parent=None):
        self.listdir = []
        self.model = QStringListModel()
        self.choose = ""
        self.flag = False
        self.init_lang()

        super().__init__(parent)
        self.ui = Ui_Backup()
        self.ui.setupUi(self)
        # 绑定槽和函数
        self.ui.pushButton.clicked.connect(self.do_open)
        self.init_list()

    def init_lang(self):
        # 启动前初始化语言
        regSetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        Language = regSetting.value("Language", "CN")
        print(Language)
        # 翻译器对象
        _trans = QTranslator()
        if Language == "CN":
            _trans.load("qt/appLang_CN.qm")
            print("载入中文")
        else:
            _trans.load("qt/appLang_EN.qm")
            print("load english")
        QCoreApplication.installTranslator(_trans)
    def do_open(self):
        current = self.ui.listView.currentIndex().data()
        self.choose = current
        self.flag = True
        self.close()
    def init_list(self):
        path = os.path.join(os.getcwd(), "save")
        listdir = os.listdir(path)
        data = [i[:-4] for i in listdir if i.endswith(".npy")]
        data.reverse()
        self.model.setStringList(data)
        self.ui.listView.setModel(self.model)
        self.ui.listView.setEditTriggers(QAbstractItemView.NoEditTriggers)
