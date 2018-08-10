# -*- coding:utf-8 -*-
from datetime import datetime, timedelta

### Sample ###

# 佛山雷达
# name: 20180726.132401.02.19.200.png
# size: 680x640
# http://www.fs121.com/pub/picture/radar/fs/20180726.132401.02.19.200.png
# http://www.fs121.com/FSRadar/FSRadarList.js?t=0.4490715192319039
# http://www.fs121.com/FSRadar/FSRadarsixHourList.js?t=0.22687507162827092

# 广州雷达
# name: 20180726.132401.02.19.200.png
# size: 680x533
# http://www.fs121.com/pub/picture/radar/gz/20180726.132401.02.19.200.png
# http://www.fs121.com/Radar/RadarList.js?t=0.8521045895979081
# http://www.fs121.com/Radar/RadarsixHourList.js?t=0.5161059767471264

# 肇庆雷达
# name: ZQR201807260524.GIF
# http://www.fs121.com/pub/picture/radar/zq/ZQR201807260524.GIF
# http://www.fs121.com/ZQRadar/ZQRadarList.js?t=0.5512130779614982
# http://www.fs121.com/ZQRadar/ZQRadarsixHourList.js?t=0.17747669797505017

# 全国雷达
# name: 20180726045400.jpg
# size: 1024x880
# http://www.fs121.com/pub/picture/radar/qg/20180726045400.jpg
# http://www.fs121.com/Handler/RadarListHandler.ashx?Type=QG
# http://www.fs121.com/Handler/RadarsixHourListHandler.ashx?Type=sixHourOfQG

# 中国天气网雷达
# http://www.weather.com.cn/radar/index.shtml?CHN


class RadarUrl:
    main_url = r'http://www.fs121.com'
    main_url_2 = r'http://www.fs121.gov.cn'
    index_url = r'http://www.fs121.com/wap/Radar.aspx'

    @staticmethod
    def radar_fs(start, end_format='00'):
        return r'http://www.fs121.com/pub/picture/radar' \
               r'/fs/{}{}.02.19.200.png'.format(datetime.strftime(start, '%Y%m%d.%H%M'), end_format)

    @staticmethod
    def radar_gz(start, end_format='00'):
        return r'http://www.fs121.com/pub/picture/radar' \
               r'/gz/{}{}.02.19.200.png'.format(datetime.strftime(start, '%Y%m%d.%H%M'), end_format)

    @staticmethod
    def radar_zq(start, end_format='00'):
        start -= timedelta(hours=8)
        return r'http://www.fs121.com/pub/picture/radar/zq/ZQR{}.GIF'.format(datetime.strftime(start, '%Y%m%d%H%M'))

    @staticmethod
    def radar_qg(start, end_format='00'):
        start -= timedelta(hours=8)
        return r'http://www.fs121.com/pub/picture/radar/qg/{}{}.jpg'.format(datetime.strftime(start, '%Y%m%d%H%M'), '00')


### Sample ###
#        index_url = r'http://www.weather.com.cn/weather1d/101280801.shtml'
#         data_url = r'http://d1.weather.com.cn/sk_2d/101280801.html'
#      dingzhi_url = r'http://d1.weather.com.cn/dingzhi/101280801.html'
# index_around_url = r'http://d1.weather.com.cn/index_around_2017/101280801.html'

# 城市代码查询
# http://toy1.weather.com.cn/search?cityname=顺德

class DataUrl:
    @staticmethod
    def index_url(code):
        return r'http://www.weather.com.cn/weather1d/{}.shtml'.format(code)

    @staticmethod
    def sk_2d_url(code):
        return r'http://d1.weather.com.cn/sk_2d/{}.html'.format(code)

    @staticmethod
    def dingzhi_url(code):
        return r'http://d1.weather.com.cn/dingzhi/{}.html'.format(code)

    @staticmethod
    def index_around_url(code):
        return r'http://d1.weather.com.cn/index_around_2017/{}.html'.format(code)
