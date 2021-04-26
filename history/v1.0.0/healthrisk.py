import numpy as np
from PyQt5.QtCore import *
from matplotlib import pyplot as plt
import xlwt

class healthrisk():

    # 可以被改变
    C_INDEX_LIST = ['pb', 'cd', 'cr']

    # 各个参数 存放在字典里
    C_PARAMETERS = {
        'dpi': 300,
        'decimals': 10,
        'IR': [100, 200],
        'CF': 0.000001,
        'EF': 230,
        'ED': [24, 6],
        'BW': [70, 15],
        'AT': [25550, 8760],
        'SA': [5700, 2800],
        'AF': 0.2,
        'ABS': 0.001,
        'BR': [20, 7.6],
        'PEF': 1360000000,
        # 'PM10': 0.15,
        # 'DAIR': [15, 7.5],
        # 'PIAF': 0.75,
        # 'FSPO': 0.5,
        'rfdm': {
            'cd': 1e-3,
            'pb': 3.5e-3,
            'cr': 3e-3,
            'zn': 3e-1,
            'hg': 3e-4,
            'cu': 4e-2,
            'as': 3e-4,
            'mn': 4.6e-2

        },
        'rfdb': {
            'cd': 1e-3,
            'pb': 3.52e-3,
            'cr': 2.86e-5,
            'zn': 3e-1,
            'hg': 7.66e-5,
            'cu': 4.02e-2,
            'as': 3.01e-4,
            'mn': 1.43e-5
        },
        'rfds': {
            'cd': 1e-5,
            'pb': 5.25e-4,
            'cr': 6e-5,
            'zn': 6e-2,
            'hg': 2.1e-5,
            'cu': 1.2e-2,
            'as': 1.23e-4,
            'mn': 1.84e-3
        },
        #斜率系数
        'sfm': {
            'cd': 6.1,
            'pb': 8.5e-3,
            'cr': 5.01e-1,
            'zn': 0,
            'hg': 0,
            'cu': 0,
            'as': 1.5,
            'mn': 0
        },
        'sfb': {
            'cd': 6.3,
            'pb': 4.2e-2,
            'cr': 4.2e1,
            'zn': 0,
            'hg': 0,
            'cu': 0,
            'as': 1.51e1,
            'mn': 0
        },
        'sfs': {
            'cd': 6.1,
            'pb': 1.7e-2,
            'cr': 2e1,
            'zn': 0,
            'hg': 0,
            'cu': 0,
            'as': 3.66,
            'mn': 0
        },
        'standard': {
            'hq': 1,
            'cr': {
                'low': 0.000001,
                'high': 0.0001
            }
        }


    }


    def __init__(self, index_list=None, parameters=None):
        self.report = ""
        self.plt_label_epa = []
        self.epa_data = None
        # 若导入了index_list 则使用导入的，否则用默认的
        if index_list:
            print("有自定义列表！")
            self.INDEX_LIST = index_list
        else:
            print("无传入列表！")
            self.INDEX_LIST = self.C_INDEX_LIST


        if parameters:
            print("有参数传入！HR")
            self.parameters = parameters
        else:
            print("无传入参数！")
            self.parameters = self.C_PARAMETERS
        print("========HR===========", self.parameters)
# ===========工具函数=============
    def do_turn_dict_to_list(self,data_dict):
        # 取参数中选中的重金属元素的对应值组成数组
        out = list()
        for i in self.INDEX_LIST:
            out.append(data_dict[i])
        return out

    def do_turn_array_to_dict(self,data_array):
        out = dict()
        # 取小数有效位数
        data_array = data_array.round(self.parameters['decimals'])
        data_array = data_array.T.tolist()
        for n,i in enumerate(self.INDEX_LIST):
            out[i] = data_array[n]

        return out

    def find_frist_point(self, data):
        # data 是一个array
        # 获得最大污染的金属种类，也就是data矩阵列加和后取最大值
        data_m = data.sum(0)
        frist_metal_index = int(np.argmax(data_m))
        data_p = data.sum(1)
        frist_point_index = int(np.argmax(data_p))
        # 返回值第一个是优先控制污染物，第二个是优先控制点位(索引从0开始，所以要＋1)
        return self.INDEX_LIST[frist_metal_index], frist_point_index+1

    def do_report(self, data):
        frist_metal, frist_point = self.find_frist_point(data)
        report = QCoreApplication.translate("healthrisk", "优先控制污染物是{}，优先控制点是[{}]:{}")
        self.report = report.format(frist_metal, frist_point, self.plt_label_epa[frist_point-1])
        print("优先控制污染物是{}，优先控制点是{}".format(frist_metal.capitalize(), frist_point,self.plt_label_epa[frist_point-1]))

    # 画图函数，x轴是点位，y轴是各个金属的指数值
    def show_plt_all(self, data1, data2):
        # 通常data1是指数值， data2是浓度值
        plt.close()
        # 修复中文乱码
        plt.rcParams['font.family'] = 'SimHei'
        plt.rcParams['axes.unicode_minus'] = False
        fig = plt.figure(dpi=self.parameters['dpi'])
        fig.subplots_adjust(hspace=0.4, wspace=0.5)
        # 绘制第一个图
        ax = plt.subplot(1, 2, 1)
        x, y = data1.shape
        width = 0.1
        for i in range(y):
            n = np.arange(x) + i * width
            plt.bar(n, data1[:, i], label=self.INDEX_LIST[i].capitalize(), alpha=0.7, width=width)

        ylable = QCoreApplication.translate("healthrisk", "风险指数")
        title = QCoreApplication.translate("healthrisk", "点位-各重金属健康风险指数图")

        plt.ylabel(ylable)
        plt.title(title,pad=10)
        plt.xticks(np.arange(x) + width, self.plt_label_epa)
        plt.legend()
        # ===================
        # 绘制第二个图
        ax = plt.subplot(1, 2, 2)
        x, y = data2.shape
        width = 0.1
        for i in range(y):
            n = np.arange(x) + i * width
            plt.bar(n, data2[:, i], label=self.INDEX_LIST[i].capitalize(), alpha=0.7, width=width)

        ylable = QCoreApplication.translate("healthrisk", "浓度值(mg/kg)")
        title = QCoreApplication.translate("healthrisk", "点位-各重金属浓度值图")

        plt.ylabel(ylable)
        plt.title(title,pad=10)
        plt.xticks(np.arange(x) + width, self.plt_label_epa)
        plt.legend()
        # ===================
        fig.canvas.set_window_title(QCoreApplication.translate("healthrisk", "计算结果"))
        plt.show()
        return

    # 导出excel结果表格
    def do_export_excel(self, filename):
        file = xlwt.Workbook(encoding='utf-8')
        sheet_c = file.add_sheet(QCoreApplication.translate("healthrisk", "浓度值"))
        sheet_o = file.add_sheet(QCoreApplication.translate("healthrisk", "指数值"))
        sheet_a = file.add_sheet(QCoreApplication.translate("healthrisk", "评价结果"))
        # 创建第一列header
        _ = [i.capitalize() for i in self.INDEX_LIST]
        _.insert(0, QCoreApplication.translate("healthrisk", "点位名称"))
        header = np.array(_)[np.newaxis, :]

        label = np.array(self.plt_label_epa)[:, np.newaxis]

        data_c = np.concatenate((label, self.epa_data), axis=1)
        data_c = np.concatenate((header, data_c), axis=0)
        # 在header后面添加总值两个字，因为下面的数据有总值
        header = np.append(header, QCoreApplication.translate("healthrisk", "综合"))[np.newaxis, :]


        data_o = np.concatenate((self.value1, self.value2[:, np.newaxis]), axis=1)
        data_o = np.concatenate((label, data_o), axis=1)
        data_o = np.concatenate((header, data_o), axis=0)

        data_a = np.concatenate((self.assess_epa1, self.assess_epa2[:, np.newaxis]), axis=1)
        data_a = np.concatenate((label, data_a), axis=1)
        data_a = np.concatenate((header, data_a), axis=0)


        # 写浓度值
        row, column = data_c.shape
        for r in range(row):
            for c in range(column):
                sheet_c.write(r, c, data_c[r, c])
        # 写指数值
        row, column = data_o.shape
        for r in range(row):
            for c in range(column):
                # 优先使用浮点数输出
                try:
                    sheet_o.write(r, c, float(data_o[r, c]))
                except:
                    sheet_o.write(r, c, data_o[r, c])

        # 写评价结果
        row, column = data_a.shape
        for r in range(row):
            for c in range(column):
                sheet_a.write(r, c, data_a[r, c])

        # 保存
        file.save(filename)
# ======================================
    def epa_do_caculate(self, data, flag=0, at=False):
        #保存浓度值
        self.epa_data = data

        print("==================计算开始==================")
        # flag=0 代表成人 flag=1 代表小孩
        # addm 经口摄入，adds 皮肤 addb 呼吸
        # BW*AT 的值先计算
        # 判断at值采取哪一个
        if at:
            bwat = self.parameters['BW'][flag]*self.parameters['AT'][0]
        else:
            bwat = self.parameters['BW'][flag]*self.parameters['AT'][1]

        addm = (data*self.parameters['IR'][flag]*self.parameters['CF']*self.parameters['EF']*self.parameters['ED'][flag])/bwat
        adds = (data*self.parameters['SA'][flag]*self.parameters['AF']*self.parameters['ABS']*self.parameters['CF']*self.parameters['EF']*self.parameters['ED'][flag])/bwat
        # addb = (data*self.parameters['PM10']*self.parameters['DAIR'][flag]*self.parameters['PIAF']*self.parameters['FSPO']*self.parameters['CF']*self.parameters['EF']*self.parameters['ED'][flag])/bwat
        addb = (data*self.parameters['BR'][flag]*self.parameters['CF']*self.parameters['EF']*self.parameters['ED'][flag])/(bwat*self.parameters['PEF'])
        print(addm, "addm", adds, "adds", addb, "addb", sep='\n')

        if at:
            sfm = np.diag(self.do_turn_dict_to_list(self.parameters['sfm']))
            sfb = np.diag(self.do_turn_dict_to_list(self.parameters['sfb']))
            sfs = np.diag(self.do_turn_dict_to_list(self.parameters['sfs']))
            print(sfb,sfm,sfs)

            # 计算cri(∑ add*sf)
            crm = addm.dot(sfm)
            crb = addm.dot(sfb)
            crs = addm.dot(sfs)
            cri = crm + crb + crs
            # 计算TCR
            tcr = cri.sum(1)
            # 转为字典
            # cri_dict = self.do_turn_array_to_dict(cri)
            # print(cri_dict)
            print("==================计算完成==================")
            # 报告
            self.do_report(cri)
            # 画图
            self.show_plt_all(cri, self.epa_data)
            # 评估结果 2代表制
            self.assess_epa1 = self.assess(cri, 2)
            self.assess_epa2 = self.assess(tcr, 2)
            tcr = tcr.round(self.parameters['decimals'])
            cri = cri.round(self.parameters['decimals'])

            self.value1 = cri
            self.value2 = tcr
            return cri, tcr


        else:
            # 创建对角阵并且取逆
            rfdm = np.linalg.inv(np.diag(self.do_turn_dict_to_list(self.parameters['rfdm'])))
            print(rfdm)
            rfds = np.linalg.inv(np.diag(self.do_turn_dict_to_list(self.parameters['rfds'])))
            rfdb = np.linalg.inv(np.diag(self.do_turn_dict_to_list(self.parameters['rfdb'])))
            print(rfdb, rfdm, rfds)

            # 计算HQI(∑ add/rfd)
            hqi = addm.dot(rfdm) + adds.dot(rfds) + addb.dot(rfdb)
            # 计算HI 就是算hqi的行和
            hi = hqi.sum(1)
            print(hqi, hi)
            # 转为字典
            # hqi_dict = self.do_turn_array_to_dict(hqi)
            # print(hqi_dict)
            print("==================计算完成==================")
            # 报告
            self.do_report(hqi)
            # 画图
            self.show_plt_all(hqi, self.epa_data)
            # 评估结果
            self.assess_epa1 = self.assess(hqi, 1)
            self.assess_epa2 = self.assess(hi, 1)
            # 取有效位数 1代表非制
            hqi = hqi.round(self.parameters['decimals'])
            hi = hi.round(self.parameters['decimals'])

            self.value1 = hqi
            self.value2 = hi
            return hqi, hi

    def assess(self, data, flag=None):
        if flag == 1:
            # 非致
            outcome = np.empty(data.shape, np.dtype('U30'))
            v = data < self.parameters['standard']['hq']
            outcome[v] = QCoreApplication.translate("healthrisk", '低风险')

            v = data >= self.parameters['standard']['hq']
            outcome[v] = QCoreApplication.translate("healthrisk", '高风险')

            print(outcome)
            return outcome
        elif flag == 2:
            # 制
            outcome = np.empty(data.shape, np.dtype('U30'))
            v = data < self.parameters['standard']['cr']['low']
            outcome[v] = QCoreApplication.translate("healthrisk", '低风险')

            v = np.logical_and(data >= self.parameters['standard']['cr']['low'],
                               data < self.parameters['standard']['cr']['high'])
            outcome[v] = QCoreApplication.translate("healthrisk", '可接受风险')

            v = data >= self.parameters['standard']['cr']['high']
            outcome[v] = QCoreApplication.translate("healthrisk", '高风险')

            print(outcome)
            return outcome