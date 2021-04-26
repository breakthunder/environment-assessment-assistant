import sys, os, json, time
import pandas as pd
import numpy as np
# qt
from PyQt5.QtMultimedia import QSoundEffect, QSound

from eaa.qt.mainwindow import *
# QT
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QDesktopWidget, \
    QGraphicsDropShadowEffect, QMenu, QToolButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import *
# 自己写的
from eaa.potentialrisk import potentialrisk
from eaa.krigeinter import Krigeinter
from eaa.healthrisk import healthrisk
from eaa import reload, setting, backup, krisetting
# 全局变量
CHECK_INDEX = ('cu', 'as', 'hg', 'pb', 'cd', 'cr', 'zn', 'mn')

class MyWindow(QMainWindow):
    # 这里是一个默认值，会被reload函数给改写，之后可以直接引用该值
    INDEX = ('pb', 'cd', 'cr')
    inter = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # ================================
        self.center()
        self._set_none_broder()
        # =================================
        # 初始化语言
        self._init_lang()
        # 连接函数和槽
        self._init_tool_button()
        # 设置函数
        self.ui.setting.triggered.connect(lambda: self.do_setting())
        self.ui.reload.triggered.connect(lambda: self.do_reload())
        self.ui.backup.triggered.connect(self.do_load_backup)
        # 潜在风险指数法
        self.ui.potential_button.clicked.connect(self.do_potential_risk)
        self.ui.import_from_file.clicked.connect(self.do_import_from_file)
        self.ui.export_pr.clicked.connect(lambda: self.export_excel_eco(1))
        # 普通指数法
        self.ui.import_from_file_sp.clicked.connect(self.sp_do_import_from_file)
        self.ui.potential_button_sp.clicked.connect(self.sp_do_caculate)
        self.ui.export_sp.clicked.connect(lambda: self.export_excel_eco(2))
        # 内梅洛法
        self.ui.import_from_file_nl.clicked.connect(self.nl_do_import_from_file)
        self.ui.potential_button_nl.clicked.connect(self.nl_do_caculate)
        self.ui.export_nl.clicked.connect(lambda: self.export_excel_eco(3))
        # 地积累指数
        self.ui.import_from_file_ml.clicked.connect(self.ml_do_import_from_file)
        self.ui.potential_button_ml.clicked.connect(self.ml_do_caculate)
        self.ui.export_ml.clicked.connect(lambda: self.export_excel_eco(4))
        # EPA模型
        self.ui.import_from_file_epa.clicked.connect(self.epa_do_import_from_file)
        self.ui.potential_button_epa.clicked.connect(self.epa_do_caculate)
        self.ui.export_epa.clicked.connect(self.export_excel_epa)

        # 判断有没有保存配置文件
        if os.path.exists("setting.json"):
            print("载入文件")
            self.do_load_from_setting_file()
            title = QCoreApplication.translate("MyWindow", "提示")
            message = QCoreApplication.translate("MyWindow", "已经载入配置文件！")
            # QMessageBox.information(self, "提示", "已载入配置文件！")
            QMessageBox.information(self, title, message)
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +message)
        else:
            # 选择要计算的类型，更新了INDEX的内容
            # 根据选择创建一个用于计算的类,并且初始化表格
            self.PR = potentialrisk()
            self.HR = healthrisk()
            self.IR = Krigeinter()
            self.do_reload()
            # 输入背景值和毒性系数的参数
            self.do_setting()
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                               QCoreApplication.translate("MyWindow", "欢迎使用风险评价助手！"))

# 初始化==================================


    def _set_none_broder(self):
        # 无边框
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        # 添加阴影
        self.setAttribute(Qt.WA_TranslucentBackground)
        # effect = QGraphicsDropShadowEffect(self)
        # effect.setBlurRadius(12)
        # effect.setOffset(0, 0)
        # effect.setColor(Qt.gray)
        # self.setGraphicsEffect(effect)

    def _init_tool_button(self):
        # 初始化设置按钮ui
        _ = QMenu()
        _.addAction(self.ui.setting)
        _.addAction(self.ui.reload)
        _.addAction(self.ui.backup)
        _.addAction(self.ui.inter_set)
        self.ui.tool_menu.setPopupMode(QToolButton.InstantPopup)
        self.ui.tool_menu.setMenu(_)
        # 初始化语言按钮
        _ = QMenu()
        _.addAction(self.ui.lang_cn)
        _.addAction(self.ui.lang_en)
        self.ui.tool_lang.setPopupMode(QToolButton.InstantPopup)
        self.ui.tool_lang.setMenu(_)
        # 设置插值按钮
        _ = QMenu()
        _.addAction(self.ui.inter_open)
        _.addAction(self.ui.inter_close)
        self.ui.tool_inter.setPopupMode(QToolButton.InstantPopup)
        self.ui.tool_inter.setMenu(_)
        # 设置关于按钮
        _ = QMenu()
        _.addAction(self.ui.about_author)
        _.addAction(self.ui.website)
        _.addAction(self.ui.aboutsoftware)
        _.addAction(self.ui.aboutqt)
        self.ui.tool_about.setPopupMode(QToolButton.InstantPopup)
        self.ui.tool_about.setMenu(_)
        # 设置最小化和关闭按钮
        self.ui.close.clicked.connect(self.close)
        self.ui.max.clicked.connect(lambda: self.showNormal() if self.isMaximized() else self.showMaximized())
        self.ui.min.clicked.connect(self.showMinimized)

    # ==================================================
    # 定义一个函数使得窗口居中显示

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(int(newLeft), int(newTop))
# ==============初始化函数============================
    def set_index(self, dir):
        # 设置index并且初始化表格
        for i in dir:
            if not i in CHECK_INDEX:
                if i in('lat','lon'):
                    # 输入的是经纬度
                    message = QCoreApplication.translate("MyWindow", "检测到表格有经纬度数据，但是并没有开启插值计算模式，请检查设置！")
                else:
                    # 其他的
                    message = QCoreApplication.translate("MyWindow", "检测到表格中有不支持的重金属，请去除该重金属的列！")
                title = QCoreApplication.translate("MyWindow", "出现错误！")
                QMessageBox.information(self, title, message)
                return 0
        self.INDEX = dir
        self.PR.INDEX_LIST = dir
        self.HR.INDEX_LIST = dir
        self.do_table_init()
        return 1

    def _init_lang(self):
        # 载入语言
        # 创建注册表
        QCoreApplication.setOrganizationName("haut")
        QCoreApplication.setApplicationName("RiskAssessment")
        regSetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        Language = regSetting.value("Language", "CN")
        # 翻译器对象
        self._trans = QTranslator()
        if Language == "CN":
            self._trans.load("languages/appLang_CN.qm")
            print("载入中文")
        else:
            self._trans.load("languages/appLang_EN.qm")
            print("load english")
        QCoreApplication.installTranslator(self._trans)
        self.ui.retranslateUi(self)

    def do_table_init(self):
        print("有", len(self.INDEX), "个项目。")
        # 初始化潜在指数法
        # 设置行列
        self.ui.potential_table.setColumnCount(len(self.INDEX) + 1)
        print("初始创建{}行。".format(self.ui.spinBox_pages_number.value()))
        self.ui.potential_table.setRowCount(self.ui.spinBox_pages_number.value())
        label = [i.capitalize() for i in self.INDEX]
        label.insert(0, QCoreApplication.translate("MyWindow", "点位名称"))
        self.ui.potential_table.setHorizontalHeaderLabels(label)
        # 清理表格
        self.ui.potential_table.clearContents()
    # ===============================
        # 初始化单项指数法
        self.ui.potential_table_sp.setColumnCount(len(self.INDEX) + 1)
        print("初始创建{}行。".format(self.ui.spinBox_pages_number_sp.value()))
        self.ui.potential_table_sp.setRowCount(self.ui.spinBox_pages_number_sp.value())
        label = [i.capitalize() for i in self.INDEX]
        label.insert(0, QCoreApplication.translate("MyWindow", "点位名称"))
        self.ui.potential_table_sp.setHorizontalHeaderLabels(label)
        # 清理表格
        self.ui.potential_table_sp.clearContents()
        self.ui.potential_table_sp.clearContents()
    # ===============================
        # 初始化内梅洛指数法
        self.ui.potential_table_nl.setColumnCount(len(self.INDEX) + 1)
        print("初始创建{}行。".format(self.ui.spinBox_pages_number_nl.value()))
        self.ui.potential_table_nl.setRowCount(self.ui.spinBox_pages_number_nl.value())
        label = [i.capitalize() for i in self.INDEX]
        label.insert(0, QCoreApplication.translate("MyWindow", "点位名称"))
        self.ui.potential_table_nl.setHorizontalHeaderLabels(label)
        # 清理表格
        self.ui.potential_table_nl.clearContents()
        self.ui.potential_table_nl.clearContents()
    # ===============================
        # 初始化地积累指数
        self.ui.potential_table_ml.setColumnCount(len(self.INDEX) + 1)
        print("初始创建{}行。".format(self.ui.spinBox_pages_number_ml.value()))
        self.ui.potential_table_ml.setRowCount(self.ui.spinBox_pages_number_ml.value())
        label = [i.capitalize() for i in self.INDEX]
        label.insert(0, QCoreApplication.translate("MyWindow", "点位名称"))
        self.ui.potential_table_ml.setHorizontalHeaderLabels(label)
        # 清理表格
        self.ui.potential_table_ml.clearContents()
        self.ui.potential_table_ml.clearContents()
    # ===============================
        # 初始化EPA
        self.ui.potential_table_epa.setColumnCount(len(self.INDEX) + 1)
        print("初始创建{}行。".format(self.ui.spinBox_pages_number_epa.value()))
        self.ui.potential_table_epa.setRowCount(self.ui.spinBox_pages_number_epa.value())
        label = [i.capitalize() for i in self.INDEX]
        label.insert(0, QCoreApplication.translate("MyWindow", "点位名称"))
        self.ui.potential_table_epa.setHorizontalHeaderLabels(label)
        # 清理表格
        self.ui.potential_table_epa.clearContents()
        self.ui.potential_table_epa.clearContents()
# ===================================================================
    @pyqtSlot()
    def on_btn_pages_confirm_clicked(self):
        #改样本数
        self.ui.potential_table.setRowCount(self.ui.spinBox_pages_number.value())

    @pyqtSlot()
    def on_btn_pages_confirm_sp_clicked(self):
        # 改样本数
        self.ui.potential_table_sp.setRowCount(self.ui.spinBox_pages_number_sp.value())

    @pyqtSlot()
    def on_btn_pages_confirm_nl_clicked(self):
        # 改样本数
        self.ui.potential_table_nl.setRowCount(self.ui.spinBox_pages_number_nl.value())

    @pyqtSlot()
    def on_btn_pages_confirm_ml_clicked(self):
        # 改样本数
        self.ui.potential_table_ml.setRowCount(self.ui.spinBox_pages_number_ml.value())

    @pyqtSlot()
    def on_btn_pages_confirm_epa_clicked(self):
        # 改样本数
        self.ui.potential_table_epa.setRowCount(self.ui.spinBox_pages_number_epa.value())
    @pyqtSlot()
    def on_lang_cn_triggered(self):
        # 切换为中文
        print("cn")
        QCoreApplication.removeTranslator(self._trans)
        self._trans = QTranslator()
        self._trans.load("languages/appLang_CN.qm")
        QCoreApplication.installTranslator(self._trans)
        regsetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        regsetting.setValue("Language","CN")
        self.ui.retranslateUi(self)
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "中文模式"))
        return
    @pyqtSlot()
    def on_lang_en_triggered(self):
        # 切换为英文
        QCoreApplication.removeTranslator(self._trans)
        self._trans = QTranslator()
        self._trans.load("languages/appLang_EN.qm")
        QCoreApplication.installTranslator(self._trans)
        regsetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
        regsetting.setValue("Language", "EN")
        self.ui.retranslateUi(self)
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "Switch to English"))
        return

    @pyqtSlot()
    # 绑定查看评价内容的按钮
    def on_assessment_pr_clicked(self):
        try:
            self.do_show_data(self.PR.assess_pr_1, self.PR.assess_pr_2,1)
        except Exception as e:
            self.wrong_message(e)


    @pyqtSlot()
    def on_assessment_ml_clicked(self):
        try:
            self.do_show_data(self.PR.assess_ml, self.PR.value_ml, 4)
        except Exception as e:
            self.wrong_message(e)

    @pyqtSlot()
    def on_assessment_nl_clicked(self):
        try:
            self.do_show_data(self.PR.assess_nl1, self.PR.assess_nl2, 3)
        except Exception as e:
            self.wrong_message(e)

    @pyqtSlot()
    def on_assessment_sp_clicked(self):
        try:
            self.do_show_data(self.PR.assess_sp, self.PR.value_sp,2)
        except Exception as e:
            self.wrong_message(e)

    @pyqtSlot()
    def on_assessment_epa_clicked(self):
        try:
            self.do_show_data(self.HR.assess_epa1, self.HR.assess_epa2, 5)
        except Exception as e:
            self.wrong_message(e)

    @pyqtSlot()
    def on_inter_open_triggered(self):
        self.inter = True
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow",
                                "打开插值计算模式（开启插值计算模式后，计算耗时会有不同程度的增加）"))

    @pyqtSlot()
    def on_inter_close_triggered(self):
        self.inter = False
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "关闭插值计算模式"))

    @pyqtSlot()
    # 设置插值计算的参数
    def on_inter_set_triggered(self):
        try:
            win = krisetting.setting_window(self.IR, self)
            win.exec()
            if win.flag:
                # 保存文件
                self.do_save_to_file()
        except Exception as e:
            self.wrong_message(e)

    @pyqtSlot()
    def on_website_triggered(self):
        title = QCoreApplication.translate("MyWindow", "官方网站")

        message = '''
        <p style="text-indent:2em;">河南工业大学：
        <span><a href="http://www.haut.edu.cn" 
        target="_blank" style="text-decoration: none;color: blue;">haut.edu.cn</a></span> </p>
        <p style="text-indent:2em;">
            河南工业大学环境工程学院：<span>
            <a href="http://hjgc.haut.edu.cn" target="_blank" 
            style="text-decoration: none;color: blue;">hjgc.haut.edu.cn</a></span> 
        </p>'''
        QMessageBox.about(self, title, message)

    @pyqtSlot()
    def on_about_author_triggered(self):
        title = QCoreApplication.translate("MyWindow", "关于作者")

        message = '''
                    <p style="text-indent:2em;">
                    @深山老妖&nbsp;&nbsp;<span><a href="https://weibo.com/u/2661913683" target="_blank" style="text-decoration: none;color: blue;">新浪微博</a></span> 
                    </p>
                    '''
        QMessageBox.about(self, title, message)

    @pyqtSlot()
    def on_aboutsoftware_triggered(self):
        title = QCoreApplication.translate("MyWindow", "关于本软件")

        message = '''
                            <p>
                                =============================
                            </p>
                            <p>
                                软件版本v1.0.0
                            </p>
                            <p>
                                有任何bug，请向作者<a href="https://weibo.com/u/2661913683" target="_blank" style="text-decoration: none;color: blue;">新浪微博</a>或者<a href="https://github.com/breakthunder/environment-assessment-assistant" style="text-decoration: none;color: blue;">github</a>页面提交
                            </p>
                            <p>
                                =============================
                            </p>
                            <p>
                                本软件使用Python编写
                            </p>
                            <p>
                                nuitka编译为可执行文件
                            </p>
                            <p>
                                编写过程中，使用的第三方库numpy（BSD协议）、pandas（BSD协议）
                            </p>
                            <p>
                                cartopy（LGPLv3协议）、fiona（BSD协议）、matplotlib（MIT协议）
                            </p>
                            <p>
                                pyqt5（GPL协议）等第三方库
                            </p>
                            <p>
                                =============================
                            </p>
                            <p>
                                本软件遵循GPLv3协议开源，具体请见<a href="https://github.com/breakthunder/environment-assessment-assistant" style="text-decoration: none;color: blue;">github</a>页面
                            </p>
                            <p>
                                =============================
                            </p>
                 '''
        QMessageBox.about(self, title, message)

    @pyqtSlot()
    def on_aboutqt_triggered(self):
        QMessageBox.aboutQt(self)

# 重写事件函数===========================================

    # 加上简单的移动功能
    def mousePressEvent(self, event):
        # """鼠标点击事件"""
        if event.button() == Qt.LeftButton:
            self.mPos = event.pos()
        event.accept()

    def mouseReleaseEvent(self, event):
        # '''鼠标弹起事件'''
        self.mPos = None
        event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.mPos:
            self.move(self.mapToGlobal(event.pos() - self.mPos))
        event.accept()

    def mouseDoubleClickEvent(self, event):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()
        event.accept()

    def dragEnterEvent(self, event):
        # 检查是否符合要求，不符合直接拒绝事件
        if event.mimeData().urls()[0].path().endswith('.xls') or event.mimeData().urls()[0].path().endswith('xlsx'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        print("开始进入拖放事件")
        # 拖动进入开始计算
        event.accept()
        filename = event.mimeData().urls()[0].path()[1:]
        print(filename)
        current_tab = self.ui.tabWidget.currentIndex()
        if current_tab == 1:
            self.epa_do_excel_caculate(filename)
        else:
            current_tab = self.ui.maintab.currentIndex()
            if current_tab == 0:
                self.pr_do_excel_caculate(filename)
            elif current_tab == 1:
                self.sp_do_excel_caculate(filename)
            elif current_tab == 2:
                self.nl_do_excel_caculate(filename)
            else:
                self.ml_do_excel_caculate(filename)

    def closeEvent(self, QCloseEvent):
        # 创建一个消息盒子（提示框）
        reply = QMessageBox.question(self,
                                     QCoreApplication.translate("MyWindow", "提示"),
                                     QCoreApplication.translate("MyWindow", "请在关闭之前先保存好资料，是否要退出？"),
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCloseEvent.ignore()
            self.close_animation = QPropertyAnimation(self, b'windowOpacity')
            self.close_animation.setDuration(100)
            self.close_animation.setStartValue(1)
            self.close_animation.setEndValue(0.5)
            self.close_animation.setEasingCurve(QEasingCurve.BezierSpline)
            self.close_animation.finished.connect(sys.exit)
            self.close_animation.start()

        else:
            QCloseEvent.ignore()

    def showEvent(self, event):
        self.setWindowOpacity(0)
        event.accept()
        self.show_animation = QPropertyAnimation(self, b'windowOpacity')
        self.show_animation.setDuration(100)
        self.show_animation.setStartValue(0)
        self.show_animation.setEndValue(1)
        self.show_animation.setEasingCurve(QEasingCurve.BezierSpline)
        self.show_animation.start()

# ===================================================================

    def do_load_backup(self, flag=None):
        try:
            win = backup.Backup_window(self)
            win.exec()
            if not win.flag:
                return
            file = win.choose
            print(file)
            # 加载保存的配置文件
            with open(os.path.join(os.getcwd(), "save", file) + ".json") as f:
                data = json.load(f)
            print(data)
            pr_parameters = data['pr_parameters']
            hr_parameters = data['hr_parameters']
            ir_parameters = data['ir_parameters']
            index = data['index']
            self.INDEX = index
            # 以INDEX创建计算类
            self.PR = potentialrisk(index, pr_parameters)
            self.HR = healthrisk(index, hr_parameters)
            self.IR = Krigeinter(ir_parameters)
            # 初始化表格
            self.do_table_init()
            # 加载保存的浓度文件
            current_tab = self.ui.tabWidget.currentIndex()
            if current_tab == 1:
                table = self.ui.potential_table_epa
            else:
                current_tab = self.ui.maintab.currentIndex()
                if current_tab == 0:
                    table = self.ui.potential_table
                elif current_tab == 1:
                    table = self.ui.potential_table_sp
                elif current_tab == 2:
                    table = self.ui.potential_table_nl
                else:
                    table = self.ui.potential_table_ml

            data = np.load(os.path.join(os.getcwd(), "save",  file) + ".npy")[1:, :]
            print(data, data.shape)
            row, column = data.shape
            table.setRowCount(row)
            for i in range(row):
                for n in range(column):
                    _ = QTableWidgetItem(data[i][n])
                    table.setItem(i, n, _)
            print("加载文件成功!!!!")
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "成功加载备份文件：") +
                                   file)
        except Exception as e:
            print(e)
    # 保存输入的数据
    def do_backup(self, flag):
        try:
            data = None
            _ = [i for i in self.INDEX]
            _.insert(0, "-")
            header = np.array(_)[None, :]
            if flag == 1:
                data = np.concatenate((np.array(self.PR.plt_label_pr)[:, np.newaxis], self.PR.pr_data), axis=1)
            elif flag == 2:
                data = np.concatenate((np.array(self.PR.plt_label_sp)[:, np.newaxis], self.PR.sp_data), axis=1)
            elif flag == 3:
                data = np.concatenate((np.array(self.PR.plt_label_nl)[:, np.newaxis], self.PR.nl_data), axis=1)
            elif flag == 4:
                data = np.concatenate((np.array(self.PR.plt_label_ml)[:, np.newaxis], self.PR.ml_data), axis=1)
            else:
                # flag=5
                data = np.concatenate((np.array(self.HR.plt_label_epa)[:, np.newaxis], self.HR.epa_data), axis=1)

            data = np.concatenate((header, data), axis=0)
            path = os.path.join(os.getcwd(), "save", time.strftime("%Y-%m-%d=%H-%M-%S"))
            if not os.path.exists(os.path.join(os.getcwd(), "save")):
                os.mkdir(os.path.join(os.getcwd(), "save"))
            np.save(path, data)
            print(data.dtype)
            # 保存配置文件
            data = dict()
            path = os.path.join(os.getcwd(), "save", time.strftime("%Y-%m-%d=%H-%M-%S.json"))
            with open(path, "w") as f:
                data['pr_parameters'] = self.PR.parameters
                data['hr_parameters'] = self.HR.parameters
                data['ir_parameters'] = self.IR.parameters
                data['index'] = self.INDEX
                json.dump(data, f)
            print("备份完成")
        except Exception as e:
            return 0
# ===================================================================

# 设置相关的函数
    def do_load_from_setting_file(self):
        try:
            with open("setting.json") as f:
                data = json.load(f)
                print(data)
                pr_parameters = data['pr_parameters']
                hr_parameters = data['hr_parameters']
                ir_parameters = data['ir_parameters']
                index = data['index']
            self.INDEX = index
            # 以INDEX创建计算类
            self.PR = potentialrisk(index, pr_parameters)
            self.HR = healthrisk(index, hr_parameters)
            self.IR = Krigeinter(ir_parameters)
            # 初始化表格
            self.do_table_init()
        except Exception as e:
            title = QCoreApplication.translate("MyWindow", "出现错误！")
            message = QCoreApplication.translate("MyWindow", "文件可能损坏，请重试，如果还打不开，请删除setting.json文件")
            QMessageBox.information(self, title, message + "\n".format(e))
            exit()
    def do_save_to_file(self):
        # 保存参数到json文件
        try:
            # pr,hr传入的就是parameters
            # 把设置储存到配置文件里
            data = dict()
            with open("setting.json", "w") as f:
                data['pr_parameters'] = self.PR.parameters
                data['hr_parameters'] = self.HR.parameters
                data['ir_parameters'] = self.IR.parameters
                data['index'] = self.INDEX
                json.dump(data, f)
            print("保存成功！")
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "保存成功"))
        except Exception as e:
            title = QCoreApplication.translate("MyWindow", "出现错误！")
            message = QCoreApplication.translate("MyWindow", "保存失败，请重试!")
            QMessageBox.information(self, title, message + "\n".format(e))

    def do_setting(self):
        # 打开设置页面
        # self.setting_window = setting.setting_window(_pr)
        # self.setting_window.setAttribute(Qt.WA_DeleteOnClose)
        # # self.layout().addWidget(setting_window)
        # self.setting_window.show()
        app = setting.setting_window(self.PR, self.HR,self)
        app.exec()
        if app.flag:
            self.do_save_to_file()
        else:
            return

    def do_reload(self):
        try:
            # 打开重载界面，选择模型参数里要多少个重金属
            # self.reload = reload.reload_window(self)
            # self.reload.exec()
            # 启动窗口，传入INDEX列表
            print(self.INDEX)
            reload_window = reload.reload_window(self.INDEX,self)
            reload_window.exec()
            # 判断是否点击了确定，或者是直接退出
            if reload_window.flag:
                # 更新INDEX列表
                self.INDEX = reload_window.index
                # 根据选择创建一个用于计算的类
                # # 生态风险计算类
                # self.PR = potentialrisk(self.INDEX)
                # # 健康风险计算类
                # self.HR = healthrisk(self.INDEX)
                # 修改计算类的index值
                self.PR.INDEX_LIST = self.INDEX
                self.HR.INDEX_LIST = self.INDEX
                # 初始化表格
                self.do_table_init()
                # 保存参数
                self.do_save_to_file()
            else:
                print("直接退出了。", self.INDEX, end='\n')
        except Exception as e:
            print(e)

# 基础功能函数，公用=========================================
    def wait_message(self):
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                               QCoreApplication.translate("MyWindow", "正在进行克里金插值法计算，绘图需要一定时间，请耐心等候！"))
    def done_message(self):
        self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                               QCoreApplication.translate("MyWindow", "绘图完成！"))
    def report(self, v=None):
        # 显示评价结果
        # v = True时，是epa
        if v == 5:
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "USEPA模型：") +
                                   self.HR.report)
        elif v == 1:
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "潜在风险指数法：") +
                                   self.PR.report)
        elif v == 2:
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "单因子风险指数法：") +
                                   self.PR.report)
        elif v == 3:
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "内梅罗指数法：") +
                                   self.PR.report)
        elif v == 4:
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "地累积指数法：") +
                                   self.PR.report)

    # 报错
    def wrong_message(self, e):
        title = QCoreApplication.translate("MyWindow", "出现错误！")
        message = QCoreApplication.translate("MyWindow", "检查输入的内容是否有缺漏，是否正确。")
        QMessageBox.information(self, title, message + "\n{}".format(e))

    def warning_message(self, e):
        title = QCoreApplication.translate("MyWindow", "出现错误！")
        message = QCoreApplication.translate("MyWindow", "检查文件的经纬度设置是否正确！是否开启了插值计算模式！")
        QMessageBox.information(self, title, message + "\n{}".format(e))
    # 导入excel文件
    def import_excel(self):
        title = QCoreApplication.translate("MyWindow", "选择要导入的excel文件")
        file_name = QFileDialog.getOpenFileName(self, title, "", "Excel File (*.xls *.xlsx)")[0]
        return file_name

    # 选择保存的文件路径
    def export_excel_eco(self, flag):
        # flag控制不同的模型的保存方式
        try:
            title = QCoreApplication.translate("MyWindow", "选择保存的位置")
            file_name = QFileDialog.getSaveFileName(self, title, "", "Excel File (*.xls);;Excel File (*.xlsx)")[0]
            if not file_name:
                return
            self.PR.do_export_excel(file_name, flag)
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "已保存到：") +
                                   file_name)
            print("保存到：", file_name)

        except Exception as e:
            self.wrong_message(e)

    def export_excel_epa(self):
        # flag控制不同的模型的保存方式
        try:
            title = QCoreApplication.translate("MyWindow", "选择保存的位置")
            file_name = QFileDialog.getSaveFileName(self, title, "", "Excel File (*.xls);;Excel File (*.xlsx)")[0]
            if not file_name:
                return
            self.HR.do_export_excel(file_name)
            self.ui.textbox.append(time.strftime("[%Y-%m-%d %H:%M:%S]  ") +
                                   QCoreApplication.translate("MyWindow", "已保存到：") +
                                   file_name)
            print("保存到：", file_name)
        except Exception as e:
            self.wrong_message(e)

    # 保存文件
    def save_file(self):
        file_name = self.export_excel()
        print(file_name)
    def do_get_table_label(self,index):
        # 提取表格的内容
        # 检查index 默认单项
        if index == 1:
            # 潜在污染
            table = self.ui.potential_table
        elif index == 2:
            # 单项指数
            table = self.ui.potential_table_sp
        elif index == 3:
            table = self.ui.potential_table_nl
        elif index == 4:
            table = self.ui.potential_table_ml
        elif index == 5:
            table = self.ui.potential_table_epa
        # 把表格的内容转化为字典
        value = []
        # 取每一行的第一列，也就是点位名字
        for y in range(table.rowCount()):
            try:
                value.append(str(table.item(y, 0).text()))
            except:
                value.append("#")

        return value

    def do_table_to_disk(self,index=1):
        # 提取表格的内容
        # 检查index 默认单项
        if index == 1:
            # 潜在污染
            table = self.ui.potential_table
        elif index == 2:
            # 单项指数
            table = self.ui.potential_table_sp
        elif index == 3:
            table = self.ui.potential_table_nl
        elif index == 4:
            table = self.ui.potential_table_ml
        elif index == 5:
            table = self.ui.potential_table_epa
        # 把表格的内容转化为字典
        value = dict()
        for x, i in enumerate(self.INDEX):
            value[i] = []
            # 与表格的行数确定循环次数
            for y in range(table.rowCount()):
                # x+1 跳过第一列，因为第一列是点位名称
                value[i].append(float(table.item(y, x+1).text()))
        return value

    # def do_show_data_lable(self, data_ri:dict):
    #     # 把∑E显示到标签上
    #     for i in self.INDEX:
    #         _ = "self.ui.potential_{}_e.setText(str(data_ri['{}']))".format(i, i)
    #         exec(_)

    def do_show_data(self, data_er=None, data_ri=None, index=1):
        # index=1 代表是潜在风险指数法，index = 2 代表单项指数法
        # 使用的是Self.value的值去显示
        # #显示到 tableview
        # row = self.ui.potential_table.rowCount()
        # column = self.ui.potential_table.columnCount()

        # 取有效小数
        # data_ri = data_ri.round(self.PR.parameters['decimals'])

        # 找出用于显示的表格
        if index == 1:
            ui_out = self.ui.potential_out
            lable = QCoreApplication.translate("MyWindow", "潜在风险总值")
            # lable = "潜在风险总值"
        elif index == 2:
            ui_out = self.ui.potential_out_sp
            lable = QCoreApplication.translate("MyWindow", "单项污染指数总值")
            # lable = "单项污染指数总值"
        elif index == 3:
            ui_out = self.ui.potential_out_nl
            lable = QCoreApplication.translate("MyWindow", "内梅洛指数")
            # lable = "内梅洛指数"
        elif index == 4:
            ui_out = self.ui.potential_out_ml
            lable = QCoreApplication.translate("MyWindow", "地质积累指数")
            # lable = "地质积累指数"
        elif index == 5:
            ui_out = self.ui.potential_out_epa
            lable = QCoreApplication.translate("MyWindow", "健康风险指数")
            # lable = "健康风险指数"
        # column = len(data_er)
        # row = len(data_ri)
        column = data_er.shape[1]
        row = data_er.shape[0]
        # self.model = QStandardItemModel(row, column+1, self)
        self.model = QStandardItemModel(row, column + 1, self)

        # 创建表头
        _ = QStandardItem(lable)
        self.model.setHorizontalHeaderItem(column, _)
        # self.model.setVerticalHeaderLabels(("∑E",))
        # 设置首字母大写
        self.model.setHorizontalHeaderLabels([i.capitalize() for i in self.INDEX])
        # 连接显示模型
        ui_out.setModel(self.model)

        # 设置item值
        for n, i in enumerate(self.INDEX):
            for y in range(row):
                item = QStandardItem(str(data_er[y, n]))
                # item = QStandardItem(str(data_er[i][y]))
                # 填充到第y行n列
                self.model.setItem(y, n, item)

        # _ = QStandardItem(str(data_total))
        # self.model.setItem(0, column, _)
        #设置最后一列的总值

        for i in range(row):
            item = QStandardItem(str(data_ri[i]))
            #最后一列的索引是列数-1，但是column已经是列数-1了
            self.model.setItem(i, column, item)


# 潜在风险指数法============================================
    def do_import_from_file(self):
        # #从文件导入数据
        file_name = self.import_excel()

        #加载后保存为类的一个变量 array
        if file_name:
            try:
                self.pr_do_excel_caculate(file_name)
            except Exception as e:
                self.warning_message(e)

        else:
            return

    def pr_do_excel_caculate(self, file_name):
        print(file_name)
        data = pd.read_excel(file_name)
        if not self.inter:
            # 未使用插值法
            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            index = [i.lower() for i in list(data)[1:]]
            if not self.set_index(index):
                return 0

            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            excel = data.values[:, 1:].astype(np.float64)
            self.PR.plt_label_pr = data.values[:, 0].tolist()
            er, ri = self.PR.do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(er, ri, index=1)
            # self.do_show_data_lable(ri)

            # 显示评价内容
            self.report(1)
            self.do_backup(1)
        else:
            # 使用插值法
            index = [i.lower() for i in list(data)[3:]]
            if not self.set_index(index):
                return 0

            excel = data.values[:, 3:].astype(np.float64)
            lon = data.values[:, 1].astype(np.float64)
            lat = data.values[:, 2].astype(np.float64)
            self.PR.plt_label_pr = data.values[:, 0].tolist()
            er, ri = self.PR.do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(er, ri, index=1)
            # self.do_show_data_lable(ri)

            # 显示评价内容
            self.report(1)
            self.do_backup(1)
            self.wait_message()
            self.IR.do(lon, lat, ri)
            self.done_message()

    def do_potential_risk(self):
        # 计算潜在风险指数
        try:
            # 把表格的内容转化为字典
            data = self.do_table_to_disk(index=1)
            # 提取点位名称列表
            self.PR.plt_label_pr = self.do_get_table_label(1)
            # 获取到计算潜在风险指数完成的结果的值
            # outcome = self.PR.all(value)
            # 获取到计算潜在风险指数完成的结果的值
            data = np.array(list(data.values())).T
            print(data.dtype)
            er, ri = self.PR.do_caculate(data)
            # # 把∑E显示到标签上
            # self.do_show_data_lable(outcome[0])

            # 显示到tableview
            self.do_show_data(er, ri, index=1)
            # 显示评价内容
            self.report(1)
            self.do_backup(1)

        except Exception as e:
            self.wrong_message(e)

    # 普通指数法=========================================================================
    def sp_do_import_from_file(self):
        # #从文件导入数据
        file_name = self.import_excel()

        #加载后保存为类的一个变量 array
        if file_name:
            try:
                self.sp_do_excel_caculate(file_name)
            except Exception as e:
                self.warning_message(e)

        else:
            return

    def sp_do_excel_caculate(self,file_name):
        print(file_name)
        data = pd.read_excel(file_name)
        if not self.inter:
            # 未使用插值法
            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            index = [i.lower() for i in list(data)[1:]]
            if not self.set_index(index):
                return 0

            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            excel = data.values[:, 1:].astype(np.float64)
            self.PR.plt_label_sp = data.values[:, 0].tolist()
            PI, singma_P = self.PR.sp_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(PI, singma_P, index=2)

            # 显示评价内容
            self.report(2)
            self.do_backup(2)
        else:
            # 使用插值法
            index = [i.lower() for i in list(data)[3:]]
            if not self.set_index(index):
                return 0

            excel = data.values[:, 3:].astype(np.float64)
            lon = data.values[:, 1].astype(np.float64)
            lat = data.values[:, 2].astype(np.float64)
            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            self.PR.plt_label_sp = data.values[:, 0].tolist()
            PI, singma_P = self.PR.sp_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(PI, singma_P, index=2)

            # 显示评价内容
            self.report(2)
            self.do_backup(2)
            self.wait_message()
            # 分别画出不同的金属的图形
            for i in range(PI.shape[1]):
                print(PI[:, i])
                self.IR.do(lon, lat, PI[:, i], self.INDEX[i])
            self.done_message()

    def sp_do_caculate(self):
        try:
            # 把表格的内容转化为字典
            data = self.do_table_to_disk(index=2)
            # 提取点位名称列表
            self.PR.plt_label_sp = self.do_get_table_label(2)
            # 获取到计算潜在风险指数完成的结果的值
            data = np.array(list(data.values())).T
            print(data)
            outcome = self.PR.sp_do_caculate(data)
            # 显示到tableview
            self.do_show_data(*outcome,index=2)
            # 显示评价内容
            self.report(2)
            self.do_backup(2)

        except Exception as e:
            self.wrong_message(e)

    # 内梅洛法=========================================================================
    def nl_do_import_from_file(self):
        # #从文件导入数据
        file_name = self.import_excel()
        # 加载后保存为类的一个变量 array
        if file_name:
            try:
                self.nl_do_excel_caculate(file_name)
            except Exception as e:
                self.warning_message(e)
        else:
            return

    def nl_do_excel_caculate(self, file_name):
        data = pd.read_excel(file_name)
        print(file_name)
        if not self.inter:
            # 未使用插值法
            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            index = [i.lower() for i in list(data)[1:]]
            if not self.set_index(index):
                return 0

            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            excel = data.values[:, 1:].astype(np.float64)
            self.PR.plt_label_nl = data.values[:, 0].tolist()
            PI, PN = self.PR.nl_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(PI, PN, index=3)
            # 显示评价内容
            self.report(3)
            self.do_backup(3)
        else:
            # 使用插值法
            index = [i.lower() for i in list(data)[3:]]
            if not self.set_index(index):
                return 0

            excel = data.values[:, 3:].astype(np.float64)
            lon = data.values[:, 1].astype(np.float64)
            lat = data.values[:, 2].astype(np.float64)
            self.PR.plt_label_nl = data.values[:, 0].tolist()
            PI, PN = self.PR.nl_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(PI, PN, index=3)
            # 显示评价内容
            self.report(3)
            self.do_backup(3)
            self.wait_message()
            self.IR.do(lon, lat, PN)
            self.done_message()

    def nl_do_caculate(self):
        try:
            # 把表格的内容转化为字典
            data = self.do_table_to_disk(index=3)
            # 提取点位名称列表
            self.PR.plt_label_nl = self.do_get_table_label(3)
            # 获取到计算潜在风险指数完成的结果的值
            data = np.array(list(data.values())).T
            print(data)
            PI,PN = self.PR.nl_do_caculate(data)
            # 显示到tableview
            self.do_show_data(PI, PN, index=3)
            # 显示评价内容
            self.report(3)
            self.do_backup(3)

        except Exception as e:
            self.wrong_message(e)

    # 地质累积指数ML=========================================================================
    def ml_do_import_from_file(self):
        # #从文件导入数据
        file_name = self.import_excel()

        # 加载后保存为类的一个变量 array
        if file_name:

            try:
                self.ml_do_excel_caculate(file_name)
            except Exception as e:
                self.warning_message(e)

        else:
            return

    def ml_do_excel_caculate(self,file_name):
        print(file_name)
        # 选中表格中的重金属类型
        data = pd.read_excel(file_name)
        if not self.inter:
            # 未使用插值法
            # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
            index = [i.lower() for i in list(data)[1:]]
            # 设置重金属类型
            if not self.set_index(index):
                return 0

            excel = data.values[:, 1:].astype(np.float64)
            self.PR.plt_label_ml = data.values[:, 0].tolist()
            i_dict, i_total = self.PR.ml_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(i_dict, i_total, index=4)
            # 显示评价内容
            self.report(4)
            self.do_backup(4)
        else:
            # 使用插值法
            index = [i.lower() for i in list(data)[3:]]
            # 设置重金属类型
            if not self.set_index(index):
                return 0

            excel = data.values[:, 3:].astype(np.float64)
            lon = data.values[:, 1].astype(np.float64)
            lat = data.values[:, 2].astype(np.float64)

            self.PR.plt_label_ml = data.values[:, 0].tolist()
            i_dict, i_total = self.PR.ml_do_caculate(excel)
            # 显示到tableview和lable
            self.do_show_data(i_dict, i_total, index=4)
            # 显示评价内容
            self.report(4)
            self.do_backup(4)
            self.wait_message()
            # 分别画出不同的金属的图形
            for i in range(i_dict.shape[1]):
                print(i_dict[:, i])
                self.IR.do(lon, lat, i_dict[:, i], self.INDEX[i])
            self.done_message()

    def ml_do_caculate(self):
        try:
            # 把表格的内容转化为字典
            data = self.do_table_to_disk(index=4)
            # 提取点位名称列表
            self.PR.plt_label_ml = self.do_get_table_label(4)
            # 获取到计算潜在风险指数完成的结果的值
            data = np.array(list(data.values())).T
            print(data)
            i_dict,i_total = self.PR.ml_do_caculate(data)
            # 显示到tableview
            self.do_show_data(i_dict, i_total, index=4)
            # 显示评价内容
            self.report(4)
            self.do_backup(4)

        except Exception as e:
            self.wrong_message(e)
# 健康风险分析模型EPA=========================================================================
    def epa_do_import_from_file(self):
        # #从文件导入数据
        file_name = self.import_excel()

        # 加载后保存为类的一个变量 array
        if file_name:
            try:
                self.epa_do_excel_caculate(file_name)
            except Exception as e:
                self.warning_message(e)
        else:
            return

    def epa_do_excel_caculate(self,file_name):
        print(file_name)
        # 提取第一列到最后一列，就是data 提取第一列转为列表传入PR类，是点位名称列表
        data = pd.read_excel(file_name)
        # 判断是成人还是儿童被选中
        if self.ui.children.isChecked():
            # 儿童被选中
            flag = 1
        else:
            # 成人被选中
            flag = 0
        # 判断计算的AT值
        if self.ui.at.isChecked():
            at = True
        else:
            at = False
        # 判断是否插值
        if not self.inter:
            # 未使用插值法
            index = [i.lower() for i in list(data)[1:]]
            excel = data.values[:, 1:].astype(np.float64)

            if not self.set_index(index):
                return 0

            self.HR.plt_label_epa = data.values[:, 0].tolist()
            i_dict, i_total = self.HR.epa_do_caculate(excel, flag=flag, at=at)
            # 显示到tableview和lable
            self.do_show_data(i_dict, i_total, index=5)
            # 显示评价内容
            self.report(5)
            self.do_backup(5)
        else:
            # 使用插值法
            index = [i.lower() for i in list(data)[3:]]
            if not self.set_index(index):
                return 0

            excel = data.values[:, 3:].astype(np.float64)
            lon = data.values[:, 1].astype(np.float64)
            lat = data.values[:, 2].astype(np.float64)

            self.HR.plt_label_epa = data.values[:, 0].tolist()
            i_dict, i_total = self.HR.epa_do_caculate(excel, flag=flag, at=at)
            # 显示到tableview和lable
            self.do_show_data(i_dict, i_total, index=5)
            # 显示评价内容
            self.report(5)
            self.do_backup(5)

            self.wait_message()
            self.IR.do(lon, lat, i_total)
            self.done_message()

    def epa_do_caculate(self):
        try:
            # 把表格的内容转化为字典
            data = self.do_table_to_disk(index=5)
            # 提取点位名称列表
            self.HR.plt_label_epa = self.do_get_table_label(5)
            # 获取到计算潜在风险指数完成的结果的值
            data = np.array(list(data.values())).T
            print(data)

            # 判断是成人还是儿童被选中
            if self.ui.children.isChecked():
                # 儿童被选中
                flag = 1
            else:
                # 成人被选中
                flag = 0
            # 判断计算的AT值
            if self.ui.at.isChecked():
                at = True
            else:
                at = False

            i_dict, i_total = self.HR.epa_do_caculate(data, flag=flag, at=at)
            # 显示到tableview
            self.do_show_data(i_dict, i_total, index=5)
            # 显示评价内容
            self.report(5)
            self.do_backup(5)

        except Exception as e:
            self.wrong_message(e)
# =========================================================================


if __name__ == '__main__':
    # 启动界面，不用修改
    app = QApplication(sys.argv)

    # 启动前初始化语言
    # QCoreApplication.setOrganizationName("haut")
    # QCoreApplication.setApplicationName("RiskAssessment")
    # regSetting = QSettings(QCoreApplication.organizationName(), QCoreApplication.applicationName())
    # Language = regSetting.value("Language", "CN")
    # # 翻译器对象
    # _trans = QTranslator()
    # if Language == "CN":
    #     _trans.load("qt/appLang_CN.qm")
    #     print("载入中文")
    # else:
    #     _trans.load("qt/appLang_EN.qm")
    #     print("load english")
    # QCoreApplication.installTranslator(_trans)

    mywin = MyWindow()
    mywin.show()
    sys.exit(app.exec_())

