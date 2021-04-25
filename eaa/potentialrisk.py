import numpy as np
from matplotlib import pyplot as plt
from PyQt5.QtCore import *
import xlwt


class potentialrisk():

    # 可以被改变
    C_INDEX_LIST = ['pb', 'cd', 'cr']
    # 背景值
    C_PARAMETERS = {
        # 岩石差异引起背景值变动而取的修正系数
        'k_value': 1.5,
        # 创建类时要输入原始值和背景值
        'decimals': 3,
        'dpi': 300,
        'cr_value': {
            'pb': 15.4,
            'cd': 0.12,
            'cr': 19.1,
            'zn': 1,
            'hg': 1,
            'cu': 1,
            'as': 1,
            'mn': 1
        },
        # Tr值
        'tr_value': {
            'pb': 5,
            'cd': 30,
            'cr': 2,
            'zn': 1,
            'hg': 40,
            'cu': 5,
            'as': 10,
            'mn': 0
        },
        # 判断标准
        'standard': {
            'single': {
                'clean': 1,
                'low': 2,
                'medium': 3,
            },
            'hakanson': {
                'er': {
                    'low': 40,
                    'medium': 80,
                    'high': 160,
                    'ultra': 320},
                'ri': {
                    'low': 150,
                    'medium': 300,
                    'high': 600}
            },
            'igeo': {
                'none': 0,
                'light': 1,
                'low': 2,
                'medium': 3,
                'high': 4,
                'ultra': 5
            },
            'nl': {
                'safe': 0.7,
                'low': 1,
                'medium': 2,
                'high': 3
            }
        }
    }

    def __init__(self, index_list=None, parameters=None):
        # 创建储存的变量
        self.report = ""
        self.ml_data = None
        self.nl_data = None
        self.pr_data = None
        self.sp_data = None
        self.plt_label_pr = []
        self.plt_label_sp = []
        self.plt_label_ml = []
        self.plt_label_nl = []
        # 若导入了index_list 则使用导入的，否则用默认的
        if index_list:
            print("有自定义列表！")
            self.INDEX_LIST = index_list
        else:
            print("无传入列表！")
            self.INDEX_LIST = self.C_INDEX_LIST

        if parameters:
            print("载入配置文件PR！")
            self.parameters = parameters
        else:
            print("无传入参数！")
            self.parameters = self.C_PARAMETERS

        print("========PR===========", self.parameters)
        # # 背景值
        # self.cr_value = self.BG
        # # 毒性系数
        # self.tr_value = self.TR
        # # 岩石差异引起背景值变动而取的修正系数
        # self.k_value = self.K

        # #把原始值保存
        # self.orgin_value = value
        # 初始化保存结果的字典
        # self.init_outcome()
        print("已经创建计算类，index值为{}".format(self.INDEX_LIST))

# 未使用numpy时的代码，抛弃

# 未使用numpy时的代码，抛弃
    # def init_outcome(self):
    #     # 创建储每一个重金属计算值的的字典
    #     self.value_cf = dict()
    #     self.value_er = dict()
    #     self.value_ri = list()
    #     # 在字典下创建每一个不同重金属对应的列表
    #     for i in self.INDEX_LIST:
    #         exec("self.value_cf['{}'] = list()".format(i))
    #         exec("self.value_er['{}'] = list()".format(i))

    # def excute_to_Cf(self, index):
    #     for i in self.orgin_value[index]:
    #         self.value_cf[index].append(i/self.cr_value[index])
    #
    # def excute_to_Cf_all(self):
    #     for i in self.INDEX_LIST:
    #         self.excute_to_Cf(i)
    #
    #
    #     print("除以背景值:", self.value_cf)
    #
    # def excute_to_Er(self, index):
    #     for i in self.value_cf[index]:
    #         self.value_er[index].append(i*self.tr_value[index])
    #
    # def excute_to_Er_all(self):
    #     for i in self.INDEX_LIST:
    #         self.excute_to_Er(i)
    #     print("乘以毒性系数", self.value_er)
    #
    # def excute_to_Ri(self):
    #     for y in range(len(self.value_er['pb'])):
    #         value = 0
    #         for i in self.INDEX_LIST:
    #             value += self.value_er[i][y]
    #         self.value_ri.append(value)
    #
    #     print("各个点的总指数", self.value_ri)
    #
    #
    # def all(self,value):
    #     self.init_outcome()
    #     self.orgin_value = value
    #     print("原始数据:", self.orgin_value)
    #     print("毒性系数:{}\n背景值:{}".format(self.tr_value, self.cr_value))
    #     self.excute_to_Cf_all()
    #     self.excute_to_Er_all()
    #     self.excute_to_Ri()
    #     # self.total_risk = sum(self.value_ri.values())
    #     out = (self.value_er, self.value_ri)
    #     print()
    #     return out


# =============工具函数=========================


    def do_turn_dict_to_list(self, dic):
        # 取参数中选中的重金属元素的对应值组成数组
        # 把无序字典按照INDEX_LIST的顺序转换为有序的列表，方便计算
        out = list()
        for i in self.INDEX_LIST:
            out.append(float(dic[i]))

        return tuple(out)

    def do_turn_array_to_dict(self, data):
        # 把array数据转化为字典
        # 带名字的
        outcome = dict()
        # 取有效小数位
        data = data.round(self.parameters['decimals'])

        data = data.tolist()
        print(data)

        for n, i in enumerate(self.INDEX_LIST):
            outcome[i] = data[n]

        return outcome

    def decimal(self, data):
        print(data.dtype,"========")
        try:
            data = data.round(self.parameters['decimals'])
            return data
        except Exception as e:
            print("没有成果的取有效位数\n", e)
            return data

    def find_frist_point(self, data):
        # data 是一个array
        # 获得最大污染的金属种类，也就是data矩阵列加和后取最大值
        data_m = data.sum(0)
        frist_metal_index = int(np.argmax(data_m))
        data_p = data.sum(1)
        frist_point_index = int(np.argmax(data_p))
        # 返回值第一个是优先控制污染物，第二个是优先控制点位(索引从0开始，所以要＋1)
        return self.INDEX_LIST[frist_metal_index], frist_point_index+1

    def do_report(self, data, label):
        frist_metal, frist_point = self.find_frist_point(data)
        print("优先控制污染物是{}，优先控制点是{}".format(frist_metal, frist_point))
        report = QCoreApplication.translate("potentialrisk", "优先控制污染物是{}，优先控制点是[{}]:{}")
        self.report = report.format(frist_metal.capitalize(), frist_point, label[frist_point-1])

    # 画图函数，x轴是点位，y轴是各个金属的指数值
    def show_plt_all(self, data1, data2, plt_label):
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
            n = np.arange(x) + i*width
            plt.bar(n, data1[:, i], label=self.INDEX_LIST[i].capitalize(), alpha=0.7, width=width)

        ylable = QCoreApplication.translate("potentialrisk", "风险指数")
        title = QCoreApplication.translate("potentialrisk", "点位-各重金属生态风险指数图")

        plt.ylabel(ylable)
        plt.title(title,pad=10)
        plt.xticks(np.arange(x) + width, plt_label)
        plt.legend()
        # ===================
        # 绘制第二个图
        ax = plt.subplot(1, 2, 2)
        x, y = data2.shape
        width = 0.1
        for i in range(y):
            n = np.arange(x) + i * width
            plt.bar(n, data2[:, i], label=self.INDEX_LIST[i].capitalize(), alpha=0.7, width=width)

        ylable = QCoreApplication.translate("potentialrisk", "浓度值")
        title = QCoreApplication.translate("potentialrisk", "点位-各重金属浓度值图")

        plt.ylabel(ylable)
        plt.title(title,pad=10)
        plt.xticks(np.arange(x) + width, plt_label)
        plt.legend()
        # ===================
        fig.canvas.manager.set_window_title(QCoreApplication.translate("potentialrisk", "计算结果"))
        plt.show()
        return

    # 导出excel结果表格
    def do_export_excel(self, filename, flag):
        file = xlwt.Workbook(encoding='utf-8')
        sheet_c = file.add_sheet(QCoreApplication.translate("potentialrisk", "浓度值"))
        sheet_o = file.add_sheet(QCoreApplication.translate("potentialrisk", "指数值"))
        sheet_a = file.add_sheet(QCoreApplication.translate("potentialrisk", "评价结果"))
        # 创建第一列header
        _ = [i.capitalize() for i in self.INDEX_LIST]
        _.insert(0, QCoreApplication.translate("potentialrisk", "点位名称"))
        header = np.array(_)[np.newaxis, :]
        if flag == 1:
            # 潜在
            label = np.array(self.plt_label_pr)[:, np.newaxis]

            data_c = np.concatenate((label, self.pr_data), axis=1)
            data_c = np.concatenate((header, data_c), axis=0)
            # 在header后面添加总值两个字，因为下面的数据有总值
            header = np.append(header, QCoreApplication.translate("potentialrisk", "综合"))[np.newaxis, :]

            data_o = np.concatenate((self.excel_Er, self.excel_Ri_process[:, np.newaxis]), axis=1)
            data_o = np.concatenate((label, data_o), axis=1)
            data_o = np.concatenate((header, data_o), axis=0)

            data_a = np.concatenate((self.assess_pr_1, self.assess_pr_2[:, np.newaxis]), axis=1)
            data_a = np.concatenate((label, data_a), axis=1)
            data_a = np.concatenate((header, data_a), axis=0)

        elif flag == 2:
            # 单因子

            label = np.array(self.plt_label_sp)[:, np.newaxis]
            data_c = np.concatenate((label, self.sp_data), axis=1)
            data_c = np.concatenate((header, data_c), axis=0)
            # 在header后面添加总值两个字，因为下面的数据有总值
            header = np.append(header, QCoreApplication.translate("potentialrisk", "综合"))[np.newaxis, :]

            data_o = np.concatenate((self.PI, self.value_sp[:, np.newaxis]), axis=1)
            data_o = np.concatenate((label, data_o), axis=1)
            data_o = np.concatenate((header, data_o), axis=0)

            _ = np.full((self.assess_sp.shape[0], 1), "-")
            data_a = np.concatenate((self.assess_sp, _), axis=1)
            data_a = np.concatenate((label, data_a), axis=1)
            data_a = np.concatenate((header, data_a), axis=0)

        elif flag == 3:
            # 内梅罗

            label = np.array(self.plt_label_nl)[:, np.newaxis]
            data_c = np.concatenate((label, self.nl_data), axis=1)
            data_c = np.concatenate((header, data_c), axis=0)
            # 在header后面添加总值两个字，因为下面的数据有总值
            header = np.append(header, QCoreApplication.translate("potentialrisk", "综合"))[np.newaxis, :]

            data_o = np.concatenate((self.value_nl, self.pn_process[:, np.newaxis]), axis=1)
            data_o = np.concatenate((label, data_o), axis=1)
            data_o = np.concatenate((header, data_o), axis=0)

            data_a = np.concatenate((self.assess_nl1, self.assess_nl2[:, np.newaxis]), axis=1)
            data_a = np.concatenate((label, data_a), axis=1)
            data_a = np.concatenate((header, data_a), axis=0)

        else:
            # 地积累
            # flag=4

            label = np.array(self.plt_label_ml)[:, np.newaxis]
            data_c = np.concatenate((label, self.ml_data), axis=1)
            data_c = np.concatenate((header, data_c), axis=0)
            # 在header后面添加总值两个字，因为下面的数据有总值
            header = np.append(header, QCoreApplication.translate("potentialrisk", "综合"))[np.newaxis, :]

            data_o = np.concatenate((self.i, self.value_ml[:, np.newaxis]), axis=1)
            data_o = np.concatenate((label, data_o), axis=1)
            data_o = np.concatenate((header, data_o), axis=0)

            _ = np.full((self.assess_ml.shape[0], 1), "-")
            data_a = np.concatenate((self.assess_ml, _), axis=1)
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
                sheet_o.write(r, c, data_o[r, c])

        # 写评价结果
        row, column = data_a.shape
        for r in range(row):
            for c in range(column):
                sheet_a.write(r, c, data_a[r, c])

        # 保存
        file.save(filename)

# ==============================================================
# 尝试使用numpy进行简化计算代码
    # 潜在指数法==========================================
    def do_caculate(self, data):
        #保存浓度值
        self.pr_data = data
        # 创建两个对角阵，储存的是背景值和毒性系数
        # 使用do_turn_dict_to_list把字典转换为元组用于创建对角阵
        bg_value = np.diag(self.do_turn_dict_to_list(self.parameters['cr_value']))
        print(bg_value, "背景值", end="\n")
        tr_value = np.diag(self.do_turn_dict_to_list(self.parameters['tr_value']))
        print(tr_value, "毒性系数", end="\n")
        # 从excel导入的原始数据 也是array类型
        excel_data = data
        # 通过矩阵计算，算出值 原始浓度值除以背景值,既是乘背景值矩阵的逆矩阵
        # np.linalg.inv(self.bg_value)将 self.bg_value 这个矩阵求逆
        excel_Pi = excel_data.dot(np.linalg.inv(bg_value))
        # 乘以毒性系数
        excel_Er = excel_Pi.dot(tr_value)
        # 求行和，既RI每个点位的风险总值
        excel_Ri = np.sum(excel_Er, 1)

        # 把Ri和Er拼成大矩阵
        # excel_Total = np.column_stack((excel_Er, excel_Ri))
        print(excel_data, excel_Pi, excel_Er, excel_Ri, sep="\n\n", end="\n\n")
        # excel_Er_dict = self.do_turn_array_to_dict(excel_Er.T)

        # 报告
        self.do_report(excel_Er, self.plt_label_pr)
        self.assess_pr_1 = self.assessment(excel_Er, 2)
        self.assess_pr_2 = self.assessment(excel_Ri, 5)

        # 取有效位数
        excel_Ri_process = self.decimal(excel_Ri)
        excel_Er = self.decimal(excel_Er)
        # 画图
        self.show_plt_all(excel_Er, self.pr_data, self.plt_label_pr)

        # 保存指数值
        self.excel_Er = excel_Er
        self.excel_Ri_process = excel_Ri_process

        return excel_Er, excel_Ri_process

    # SP===================================================
    def sp_do_caculate(self,data):
        #保存浓度值
        self.sp_data = data
        # 使用do_turn_dict_to_list把字典转换为元组用于创建对角阵
        bg_value = np.diag(self.do_turn_dict_to_list(self.parameters['cr_value']))
        print(bg_value, "背景值", end="\n")
        # 通过矩阵计算，算出值 原始浓度值除以背景值,既是乘背景值矩阵的逆矩阵
        # np.linalg.inv(self.bg_value)将 self.bg_value 这个矩阵求逆. 并且把每一行相加,得到一个点的单项污染指数
        PI = data.dot(np.linalg.inv(bg_value))

        # 转为字典
        # pi_dict = self.do_turn_array_to_dict(PI.T)
        sigma_p = np.sum(PI, 1)

        # 进行报告
        self.do_report(PI, self.plt_label_sp)
        # 评价判断
        self.assess_sp = self.assessment(PI, 1)
        # 取有效位数
        sigma_p = self.decimal(sigma_p)
        PI = self.decimal(PI)

        # 画图
        self.show_plt_all(PI, self.sp_data, self.plt_label_sp)

        # 保存指数值
        self.PI = PI
        self.value_sp = sigma_p
        return PI, sigma_p
    # NL=====================================================
    # 内梅罗
    def nl_do_caculate(self, data):
        #保存浓度值
        self.nl_data = data
        # 使用do_turn_dict_to_list把字典转换为元组用于创建对角阵
        bg_value = np.diag(self.do_turn_dict_to_list(self.parameters['cr_value']))
        print(bg_value, "背景值", end="\n")
        # 通过矩阵计算，算出值 原始浓度值除以背景值,既是乘背景值矩阵的逆矩阵
        # np.linalg.inv(self.bg_value)将 self.bg_value 这个矩阵求逆. 并且把每一行相加,得到一个点的单项污染指数
        pn_raw = data.dot(np.linalg.inv(bg_value))
        # 转换为字典
        # pn_dict = self.do_turn_array_to_dict(pn_raw.T)

        # 计算PN
        # 取各点的最大值和平均值
        pmax = pn_raw.max(1)
        pavg = pn_raw.mean(1)
        pn_total = np.sqrt((np.square(pmax)+np.square(pavg))/2)



        # 进行报告，因为参数计算的原因，无法使用do_report函数
        frist_metal = self.INDEX_LIST[int(np.argmax(pn_raw.sum(0)))]
        frist_point = int(np.argmax(pn_total)) + 1
        print("优先控制污染物是{}，优先控制点是{}".format(frist_metal, frist_point))
        # 创建self.report
        report = QCoreApplication.translate("potentialrisk", "优先控制污染物是{}，优先控制点是[{}]:{}")
        self.report = report.format(frist_metal.capitalize(), frist_point, self.plt_label_nl[frist_point-1])

        # 评价
        self.assess_nl1 = self.assessment(pn_raw, 1)
        self.assess_nl2 = self.assessment(pn_total, 4)
        # 取有效位数
        pn_process = self.decimal(pn_total)
        pn_raw = self.decimal(pn_raw)

        # 画图
        self.show_plt_all(pn_raw, self.nl_data, self.plt_label_nl)

        self.value_nl = pn_raw
        self.pn_process = pn_process
        return pn_raw, pn_process
    # ML=====================================================
    # 地积累指数
    def ml_do_caculate(self, data):
        #保存浓度值
        self.ml_data = data
        bg_value = np.diag(self.do_turn_dict_to_list(self.parameters['cr_value']))
        k = self.parameters['k_value']
        print(bg_value, "背景值",k,"修正系数", end="\n")
        i = np.log2(data.dot(np.linalg.inv(bg_value))/k)
        # 转为字典
        # i_dict = self.do_turn_array_to_dict(i.T)
        i_total = np.sum(i, 1)

        print(i, i_total)

        # 报告
        self.do_report(i, self.plt_label_ml)

        # 评价
        self.assess_ml = self.assessment(i,3)
        # 取有效位数 i_dict在i_dict = self.do_turn_array_to_dict(i.T)取过了
        i_total = self.decimal(i_total)
        i = self.decimal(i)

        # 画图
        self.show_plt_all(i, self.ml_data, self.plt_label_ml)
        self.i = i
        self.value_ml = i_total
        return i, i_total

    # 评价结果判断
    def assessment(self, data, flag=None):
        if flag == 1:
            # 单因子指数法
            outcome = np.empty(data.shape, np.dtype('U30'))
            # 单因子指数法判断
            claen = data < self.parameters['standard']['single']['clean']
            outcome[claen] = QCoreApplication.translate("potentialrisk", '清洁土壤')

            # print(claen)
            low = np.logical_and(data >= self.parameters['standard']['single']['clean'],
                                 data < self.parameters['standard']['single']['low'])
            outcome[low] = QCoreApplication.translate("potentialrisk", '轻度污染')
            # print(low)

            medium = np.logical_and(data >= self.parameters['standard']['single']['low'],
                                    data < self.parameters['standard']['single']['medium'])
            outcome[medium] = QCoreApplication.translate("potentialrisk", '中度污染')
            # print(medium)

            high = data >= self.parameters['standard']['single']['medium']
            # print(high)
            outcome[high] = QCoreApplication.translate("potentialrisk", '重度污染')
            print(outcome)
            return outcome

        elif flag == 2:
            # 潜在风险指数法
            outcome = np.empty(data.shape, np.dtype('U30'))
            clean = data < self.parameters['standard']['hakanson']['er']['low']
            outcome[clean] = QCoreApplication.translate("potentialrisk", '低污染')

            low = np.logical_and(data >= self.parameters['standard']['hakanson']['er']['low'],
                                 data < self.parameters['standard']['hakanson']['er']['medium'])
            outcome[low] = QCoreApplication.translate("potentialrisk", '中度污染')

            medium = np.logical_and(data >= self.parameters['standard']['hakanson']['er']['medium'],
                                 data < self.parameters['standard']['hakanson']['er']['high'])
            outcome[medium] = QCoreApplication.translate("potentialrisk", '较重污染')

            high = np.logical_and(data >= self.parameters['standard']['hakanson']['er']['high'],
                                 data < self.parameters['standard']['hakanson']['er']['ultra'])
            outcome[high] = QCoreApplication.translate("potentialrisk", '重度污染')

            ultra = data >= self.parameters['standard']['hakanson']['er']['ultra']
            outcome[ultra] = QCoreApplication.translate("potentialrisk", '严重污染')
            print(outcome)
            return outcome
        elif flag == 3:
            # 地积累指数法
            outcome = np.empty(data.shape, np.dtype('U30'))
            v = data < self.parameters['standard']['igeo']['none']
            outcome[v] = QCoreApplication.translate("potentialrisk", '无污染')

            v = np.logical_and(data >= self.parameters['standard']['igeo']['none'],
                                 data < self.parameters['standard']['igeo']['light'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '轻微污染')

            v = np.logical_and(data >= self.parameters['standard']['igeo']['light'],
                                 data < self.parameters['standard']['igeo']['low'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '轻度污染')

            v = np.logical_and(data >= self.parameters['standard']['igeo']['low'],
                                 data < self.parameters['standard']['igeo']['medium'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '中度污染')

            v = np.logical_and(data >= self.parameters['standard']['igeo']['medium'],
                                 data < self.parameters['standard']['igeo']['high'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '偏重污染')

            v = np.logical_and(data >= self.parameters['standard']['igeo']['high'],
                                 data < self.parameters['standard']['igeo']['ultra'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '重度污染')

            v = data >= self.parameters['standard']['igeo']['ultra']
            outcome[v] = QCoreApplication.translate("potentialrisk", '严重污染')

            print(outcome)
            return outcome
        elif flag == 4:
            # 内梅罗指数法
            outcome = np.empty(data.shape, np.dtype('U30'))
            v = data < self.parameters['standard']['nl']['safe']
            outcome[v] = QCoreApplication.translate("potentialrisk", '安全土壤')

            v = np.logical_and(data >= self.parameters['standard']['nl']['safe'],
                                 data < self.parameters['standard']['nl']['low'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '警戒级别污染土壤')

            v = np.logical_and(data >= self.parameters['standard']['nl']['low'],
                                 data < self.parameters['standard']['nl']['medium'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '轻度污染土壤')

            v = np.logical_and(data >= self.parameters['standard']['nl']['medium'],
                                 data < self.parameters['standard']['nl']['high'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '中度污染土壤')

            v = data >= self.parameters['standard']['nl']['high']
            outcome[v] = QCoreApplication.translate("potentialrisk", '重度污染土壤')

            print(outcome)
            return outcome
        elif flag == 5:
            # 潜在风险指数的ri部分
            outcome = np.empty(data.shape, np.dtype('U30'))
            v = data < self.parameters['standard']['hakanson']['ri']['low']
            outcome[v] = QCoreApplication.translate("potentialrisk", '低污染')

            v = np.logical_and(data >= self.parameters['standard']['hakanson']['ri']['low'],
                                 data < self.parameters['standard']['hakanson']['ri']['medium'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '中度污染')

            v = np.logical_and(data >= self.parameters['standard']['hakanson']['ri']['medium'],
                                 data < self.parameters['standard']['hakanson']['ri']['high'])
            outcome[v] = QCoreApplication.translate("potentialrisk", '重度污染')

            v = data >= self.parameters['standard']['hakanson']['ri']['high']
            outcome[v] = QCoreApplication.translate("potentialrisk", '严重污染')

            print(outcome)
            return outcome
        else:
            return 0
