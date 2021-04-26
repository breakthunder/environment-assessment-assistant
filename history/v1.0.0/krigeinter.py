from pykrige.ok import OrdinaryKriging
import numpy as np
import cartopy.crs as ccrs
from PyQt5.QtCore import QCoreApplication
import matplotlib.pyplot as plt
# import fiona
# from shapely.geometry import Polygon, Point
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeat

class Krigeinter():
    C_PARAMETERS = {
        'left_top_lon': 0,
        'left_top_lat': 0,
        'right_bottom_lon': 0,
        'right_bottom_lat': 0,
        'x_split': 100,
        'y_split': 100,
        'levels': 64,
        'dpi': 300,
        'shp_path':None,
        'start_lon':0,
        'start_lat':0,
        'stop_lon':0,
        'stop_lat':0
    }
    def __init__(self, parameters=None):
        if parameters:
            print("载入配置文件！")
            self.parameters = parameters
        else:
            print("无传入参数！")
            self.parameters = self.C_PARAMETERS

    def do(self, lon, lat, data, name=""):
        gridlon = np.linspace(self.parameters['left_top_lon'],
                              self.parameters['right_bottom_lon'],
                              self.parameters['y_split'])
        gridlat = np.linspace(self.parameters['left_top_lat'],
                              self.parameters['right_bottom_lat'],
                              self.parameters['x_split'])
        OK = OrdinaryKriging(
            lon,
            lat,
            data,
            variogram_model="gaussian",
            nlags=6
        )
        zgrid, ss = OK.execute('grid', gridlon, gridlat)
        extent = [self.parameters['start_lon'],
                  self.parameters['stop_lon'],
                  self.parameters['start_lat'],
                  self.parameters['stop_lat']]
        print(extent,"extent")
        xgrid, ygrid = np.meshgrid(gridlon,gridlat)
        # 创建图形
        fig = plt.figure(dpi=self.parameters['dpi'])
        sub = fig.add_subplot(projection=ccrs.PlateCarree())
        # 设置经纬度
        gl = sub.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                           linewidth=0.2, color='k', alpha=0.5, linestyle='--')
        # 关闭上侧坐标显示
        gl.top_labels = False
        gl.right_labels = False

        # 检查是否在shp区域里
        # if self.parameters['shp_path']:

            # try:
            #     print("载入shp文件掩膜")
            #     shp = fiona.open(self.parameters['shp_path'])
            #     pol = next(iter(shp))
            #     polygon = Polygon(pol['geometry']['coordinates'][0])
            # except:
            #     raise Exception(QCoreApplication.translate("Krigeinter", "由于shp文件引发的错误，检查shp文件"))
            #
            # for i in range(xgrid.shape[0]):
            #     for j in range(xgrid.shape[1]):
            #         plon = xgrid[i][j]
            #         plat = ygrid[i][j]
            #         if not polygon.contains(Point(plon, plat)):
            #             zgrid[i][j] = np.nan
            #     # 读取shp文件之后画出边缘
            # try:
            #     reader = Reader(self.parameters['shp_path'])
            #     enshicity = cfeat.ShapelyFeature(reader.geometries(), ccrs.PlateCarree(), edgecolor='k', facecolor='none')
            #     sub.add_feature(enshicity, linewidth=0.7)
            # except:
            #     raise Exception(QCoreApplication.translate("Krigeinter", "由于shp文件引发的错误，检查shp文件"))

        # 画渐变颜色图
        cont = sub.contourf(xgrid, ygrid, zgrid, levels=self.parameters['levels'])
        # 添加颜色棒
        cb = fig.colorbar(cont, label=QCoreApplication.translate("Krigeinter", "指数范围"))
        # 设置可见范围
        sub.set_extent(extent)
        # 设置tittle
        tittle = QCoreApplication.translate("Krigeinter", "插值模拟结果")
        if name:
            tittle = tittle + '-' + name.capitalize()
        fig.canvas.set_window_title(tittle)
        plt.title(tittle,pad=10)
        plt.show()

