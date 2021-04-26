from PyQt5.QtWidgets import QDialog, QMessageBox
from eaa.qt.settingwindow import *
from PyQt5.QtCore import *


class setting_window(QDialog):
    CONTAIN = ['cu', 'as', 'hg', 'pb', 'cd', 'cr', 'zn', 'mn']
    def __init__(self, _pr, _hr, parent=None):

        super().__init__(parent)
        self.init_lang()
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.ui = Ui_setting_window()
        self.ui.setupUi(self)
        self.pr = _pr
        self.hr = _hr
        self.do_init()
        self.flag = False
        # 绑定槽和函数
        self.ui.pushButton.clicked.connect(self.do_save)

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

    def do_init(self):
        # #获取当前各个定值
        # #背景值
        # self.ui.bg_pb.setText(str(self.pr.cr_value['pb']))
        # self.ui.bg_cd.setText(str(self.pr.cr_value['cd']))
        # self.ui.bg_cr.setText(str(self.pr.cr_value['cr']))
        # #T值
        # self.ui.t_pb.setText(str(self.pr.tr_value['pb']))
        # self.ui.t_cd.setText(str(self.pr.tr_value['cd']))
        # self.ui.t_cr.setText(str(self.pr.tr_value['cr']))

        # 根据INDEX_LIST的内容去获取当前各个定值
        try:
            # 生态分析的参数获取
            for i in self.CONTAIN:
                if i not in self.pr.INDEX_LIST:
                    exec("self.ui.bg_{}.setEnabled(False)".format(i))
                    exec("self.ui.t_{}.setEnabled(False)".format(i))

            for i in self.pr.INDEX_LIST:
                try:
                    exec("self.ui.bg_{}.setText(str(self.pr.parameters['cr_value']['{}']))".format(i, i))
                    exec("self.ui.t_{}.setText(str(self.pr.parameters['tr_value']['{}']))".format(i, i))
                except:
                    pass
            self.ui.k.setText(str(self.pr.parameters['k_value']))
            self.ui.decimals_pr.setText(str(self.pr.parameters['decimals']))

            # 健康分析的参数获取
            # print("==============获取参数====================")
            for x, y in self.hr.parameters.items():
                print(x, y)
                try:
                    if isinstance(y, list):
                        exec("self.ui.{}_a.setText(str(self.hr.parameters['{}'][0]))".format(x.lower(), x))
                        exec("self.ui.{}_c.setText(str(self.hr.parameters['{}'][1]))".format(x.lower(), x))
                    elif isinstance(y, dict):
                        # 斜率系数和参考剂量
                        for k, v in y.items():
                            exec("self.ui.{}_{}.setText(str(self.hr.parameters['{}']['{}']))".format(x,k,x,k))
                    else:
                        exec("self.ui.{}.setText(str(self.hr.parameters['{}']))".format(x.lower(), x))
                except:
                    pass
            self.ui.decimals_hr.setText(str(self.hr.parameters['decimals']))
            # 显示dpi
            self.ui.dpi.setText(str(self.pr.parameters['dpi']))

            # print("==============获取参数====================")


        except Exception as e:
            # 2=有的参数并未获取到值
            self.wrong_message(e, 2)

    def do_save(self):
        # 根据输入设置值
        try:


            # 生态风险部分
            for i in self.pr.INDEX_LIST:
                for x, y in [("cr_value", "bg"),
                             ("tr_value", "t")]:
                    # self.pr.tr_value['pb'] = float(self.ui.t_pb.toPlainText())
                    # self.ui.t_pb.toPlainText()
                    _ = "self.pr.parameters['{}']['{}'] = float(self.ui.{}_{}.toPlainText())".format(x, i, y, i)
                    exec(_)
            # 保存地质积累指数的修正值
            self.pr.parameters['k_value'] = float(self.ui.k.toPlainText())
            self.pr.parameters['decimals'] = int(float(self.ui.decimals_pr.toPlainText()))
            print("背景值:{}\n毒性系数:{}\n修正系数{}".format(self.pr.parameters['cr_value'], self.pr.parameters['tr_value'], self.pr.parameters['k_value']), "\n")


            # 健康风险部分
            count = 0
            for x,y in self.hr.parameters.items():
                try:
                    count+=1
                    print(count, x, y)
                    if isinstance(y, list):
                        _ = "self.hr.parameters['{}'][0] = float(self.ui.{}_a.toPlainText())".format(x, x.lower())
                        exec(_)
                        _ = "self.hr.parameters['{}'][1] = float(self.ui.{}_c.toPlainText())".format(x, x.lower())
                        exec(_)
                    elif isinstance(y, dict):
                        # 保存参考剂量和斜率系数
                        for k in y:
                            # 取字典的每一个key
                            exec("self.hr.parameters['{}']['{}'] = float(self.ui.{}_{}.toPlainText())".format(x, k, x, k))
                            # exec("print(self.ui.{}_{}.toPlainText())".format(x, k))
                    else:
                        _ = "self.hr.parameters['{}'] = float(self.ui.{}.toPlainText())".format(x, x.lower())
                        exec(_)
                except Exception as e:
                    if x == "decimals":
                        exec("self.hr.parameters['{}'] = int(float(self.ui.{}_hr.toPlainText()))".format(x, x.lower()))
                        continue
                    elif x == "standard":
                        continue
                    else:
                        # 3=请重试
                        self.wrong_message(e, 3)
                        return

            # 保存dpi
            self.pr.parameters['dpi'] = int(self.ui.dpi.toPlainText())
            self.hr.parameters['dpi'] = int(self.ui.dpi.toPlainText())

            self.flag = True


        except Exception as e:
            # 1=填写所有参数
            self.wrong_message(e, 1)
            return



        self.close()

    # 报错
    def wrong_message(self, e, flag):
        title = QCoreApplication.translate("MyWindow", "出现错误！")
        if flag == 1:
            message = QCoreApplication.translate("MyWindow", "填写所有参数。")
        elif flag == 2:
            message = QCoreApplication.translate("MyWindow", "有的参数并未获取到值。")
        else:
            message = QCoreApplication.translate("MyWindow", "请重试。")

        QMessageBox.information(self, title, message + "\n{}".format(e))