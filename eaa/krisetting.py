from eaa.qt.intersetting import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog, QGraphicsDropShadowEffect, \
    QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class setting_window(QDialog):
    def __init__(self, _ir, parent=None):
        self.flag = False

        super().__init__(parent)
        self._set_none_broder()
        self.init_lang()
        # self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ir = _ir
        self.do_init()
        # 绑定槽和函数
        self.ui.confirm.clicked.connect(self.do_save)

    def init_lang(self):
        # 启动前初始化语言
        regSetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        Language = regSetting.value("Language", "CN")
        print(Language)
        # 翻译器对象
        _trans = QTranslator()
        if Language == "CN":
            _trans.load("languages/appLang_CN.qm")
            print("载入中文")
        else:
            _trans.load("languages/appLang_EN.qm")
            print("load english")
        QCoreApplication.installTranslator(_trans)
    def _set_none_broder(self):
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(Qt.gray)
        self.setGraphicsEffect(effect)
    def do_init(self):
        # 设置有效输入
        vint = QIntValidator()
        vdou = QDoubleValidator()
        self.ui.left_top_lon.setValidator(vdou)
        self.ui.left_top_lat.setValidator(vdou)
        self.ui.right_bottom_lon.setValidator(vdou)
        self.ui.right_bottom_lat.setValidator(vdou)
        self.ui.x_split.setValidator(vint)
        self.ui.y_split.setValidator(vint)
        self.ui.levels.setValidator(vint)
        self.ui.dpi.setValidator(vint)
        self.ui.boder_start_lon.setValidator(vdou)
        self.ui.boder_stop_lon.setValidator(vdou)
        self.ui.boder_start_lat.setValidator(vdou)
        self.ui.boder_stop_lat.setValidator(vdou)
        # 获取数值
        self.ui.left_top_lon.setText(str(self.ir.parameters['left_top_lon']))
        self.ui.left_top_lat.setText(str(self.ir.parameters['left_top_lat']))
        self.ui.right_bottom_lon.setText(str(self.ir.parameters['right_bottom_lon']))
        self.ui.right_bottom_lat.setText(str(self.ir.parameters['right_bottom_lat']))
        self.ui.x_split.setText(str(self.ir.parameters['x_split']))
        self.ui.y_split.setText(str(self.ir.parameters['y_split']))
        self.ui.levels.setText(str(self.ir.parameters['levels']))
        self.ui.dpi.setText(str(self.ir.parameters['dpi']))
        self.ui.path.setText(self.ir.parameters['shp_path'])
        self.ui.boder_start_lon.setText(str(self.ir.parameters['start_lon']))
        self.ui.boder_stop_lon.setText(str(self.ir.parameters['stop_lon']))
        self.ui.boder_start_lat.setText(str(self.ir.parameters['start_lat']))
        self.ui.boder_stop_lat.setText(str(self.ir.parameters['stop_lat']))

    def do_save(self):
        try:
            self.ir.parameters['left_top_lon'] = float(self.ui.left_top_lon.text())
            self.ir.parameters['left_top_lat'] = float(self.ui.left_top_lat.text())
            self.ir.parameters['right_bottom_lon'] = float(self.ui.right_bottom_lon.text())
            self.ir.parameters['right_bottom_lat'] = float(self.ui.right_bottom_lat.text())
            self.ir.parameters['x_split'] = int(self.ui.x_split.text())
            self.ir.parameters['y_split'] = int(self.ui.y_split.text())
            self.ir.parameters['levels'] = int(self.ui.levels.text())
            self.ir.parameters['dpi'] = int(self.ui.dpi.text())
            self.ir.parameters['shp_path'] = self.ui.path.text()
            self.ir.parameters['start_lon'] = float(self.ui.boder_start_lon.text())
            self.ir.parameters['stop_lon'] = float(self.ui.boder_stop_lon.text())
            self.ir.parameters['start_lat'] = float(self.ui.boder_start_lat.text())
            self.ir.parameters['stop_lat'] = float(self.ui.boder_stop_lat.text())
            self.flag = True
            self.close()
        except Exception as e:
            title = QCoreApplication.translate("setting_window", "出现错误！")
            message = QCoreApplication.translate("setting_window", "保存错误，请检查是否都输入了正确的数值！")
            QMessageBox.information(self, title, message + "\n{}".format(e))
            return
    @pyqtSlot()
    def on_openfile_clicked(self):
        try:
            title = QCoreApplication.translate("setting_window", "选择shp文件")
            file_name = QFileDialog.getOpenFileName(self, title, "", "shp File (*.shp)")[0]
            self.ui.path.setText(file_name)
        except Exception as e:
            print(e)
            return
