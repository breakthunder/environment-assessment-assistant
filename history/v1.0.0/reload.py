from eaa.qt.reload import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog
from PyQt5.QtCore import *
class reload_window(QDialog):
    #Qdialog 模态对话框
    CONTAIN = ['mn', 'cu', 'as', 'hg', 'pb', 'cd', 'cr', 'zn']
    def __init__(self, source_list, parent=None):

        super().__init__(parent)
        self.init_lang()
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.ui = Ui_reload()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.do_check)
        self.index = source_list
        # 初始化标签选择
        self.do_init_check(source_list)
        # 设置一个标识变量
        self.flag = False

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

    def do_init_check(self, source_list):
        # 初始化标签选择
        for i in source_list:
            _ = "self.ui.{}_check.setChecked(1)".format(i)
            exec(_)

    def do_check(self):
        #判断有什么类型加入了
        #顺序有影响
        check_box = [self.ui.mn_check.isChecked(),
                     self.ui.cu_check.isChecked(),
                     self.ui.as_check.isChecked(),
                     self.ui.hg_check.isChecked(),
                     self.ui.pb_check.isChecked(),
                     self.ui.cd_check.isChecked(),
                     self.ui.cr_check.isChecked(),
                     self.ui.zn_check.isChecked(),
                     ]
        outcome = [y for x, y in enumerate(self.CONTAIN) if check_box[x]]
        print("reload", "：", outcome)
        self.index = outcome
        # 改写标志，标识已经点击确定了，而不是关闭
        self.flag = True
        self.close()
