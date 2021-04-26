from eaa.qt.intersetting import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QFileDialog
from PyQt5.QtCore import *


class setting_window(QDialog):
    def __init__(self, _ir, parent=None):
        self.flag = False

        super().__init__(parent)
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
            _trans.load("qt/appLang_CN.qm")
            print("载入中文")
        else:
            _trans.load("qt/appLang_EN.qm")
            print("load english")
        QCoreApplication.installTranslator(_trans)

    def do_init(self):
        self.ui.left_top_lon.setText(str(self.ir.parameters['left_top_lon']))
        self.ui.left_top_lat.setText(str(self.ir.parameters['left_top_lat']))
        self.ui.right_bottom_lon.setText(str(self.ir.parameters['right_bottom_lon']))
        self.ui.right_bottom_lat.setText(str(self.ir.parameters['right_bottom_lat']))
        self.ui.x_split.setText(str(self.ir.parameters['x_split']))
        self.ui.y_split.setText(str(self.ir.parameters['y_split']))
        self.ui.levels.setText(str(self.ir.parameters['levels']))
        self.ui.dpi.setText(str(self.ir.parameters['dpi']))
        self.ui.path.setPlainText(self.ir.parameters['shp_path'])
        self.ui.boder_start_lon.setText(str(self.ir.parameters['start_lon']))
        self.ui.boder_stop_lon.setText(str(self.ir.parameters['stop_lon']))
        self.ui.boder_start_lat.setText(str(self.ir.parameters['start_lat']))
        self.ui.boder_stop_lat.setText(str(self.ir.parameters['stop_lat']))

    def do_save(self):
        self.ir.parameters['left_top_lon'] = float(self.ui.left_top_lon.toPlainText())
        self.ir.parameters['left_top_lat'] = float(self.ui.left_top_lat.toPlainText())
        self.ir.parameters['right_bottom_lon'] = float(self.ui.right_bottom_lon.toPlainText())
        self.ir.parameters['right_bottom_lat'] = float(self.ui.right_bottom_lat.toPlainText())
        self.ir.parameters['x_split'] = int(self.ui.x_split.toPlainText())
        self.ir.parameters['y_split'] = int(self.ui.y_split.toPlainText())
        self.ir.parameters['levels'] = int(self.ui.levels.toPlainText())
        self.ir.parameters['dpi'] = int(self.ui.dpi.toPlainText())
        self.ir.parameters['shp_path'] = self.ui.path.toPlainText()
        self.ir.parameters['start_lon'] = float(self.ui.boder_start_lon.toPlainText())
        self.ir.parameters['stop_lon'] = float(self.ui.boder_stop_lon.toPlainText())
        self.ir.parameters['start_lat'] = float(self.ui.boder_start_lat.toPlainText())
        self.ir.parameters['stop_lat'] = float(self.ui.boder_stop_lat.toPlainText())
        self.flag = True
        self.close()

    @pyqtSlot()
    def on_openfile_clicked(self):
        try:
            title = QCoreApplication.translate("setting_window", "选择shp文件")
            file_name = QFileDialog.getOpenFileName(self, title, "", "shp File (*.shp)")[0]
            self.ui.path.setPlainText(file_name)
        except Exception as e:
            print(e)
            return
