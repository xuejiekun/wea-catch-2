# -*- coding:utf-8 -*-
import time
import json
from datetime import datetime
from html import unescape
from sqlalchemy import and_

from sky.base import BaseRequests, BaseORM
from .DataModel import Address, Dat, Base
from .Url import DataUrl


class DataManager(BaseORM):

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_address(self, name, name_eng=None, code=None):
        addr = self.session.query(Address).filter(Address.name == name).first()
        if not addr:
            print('add address')
            addr = Address(name=name, name_eng=name_eng, code=code)
            self.session.add(addr)
            self.session.commit()
        return addr

    def add_data(self, logtime, address_id, temp, tempf, humidity,
                 rain, rain_24,
                 wind, wind_eng, wind_speed, wind_speed_eng,
                 pressure, visibility, aqi, aqi_pm25,
                 weather, weather_eng, weather_code):
        dat = self.session.query(Dat).filter(and_(Dat.logtime == logtime, Dat.address_id==address_id)).first()
        if not dat:
            print('add data')
            dat = Dat(logtime=logtime, address_id=address_id,
                      temp=temp, tempf=tempf, humidity=humidity, rain=rain, rain_24=rain_24,
                      wind=wind, wind_eng=wind_eng, wind_speed=wind_speed, wind_speed_eng=wind_speed_eng,
                      pressure=pressure, visibility=visibility, aqi=aqi, aqi_pm25=aqi_pm25,
                      weather=weather, weather_eng=weather_eng, weather_code=weather_code)
            self.session.add(dat)
            self.session.commit()
        return dat

    def add_wea_dat(self, dat):
        addr = self.add_address(name=dat['cityname'], name_eng=dat['nameen'], code=dat['city'])

        data = self.add_data(logtime=dat['logtime'], address_id=addr.id,
                             temp=dat['temp'], tempf=dat['tempf'], humidity=dat['sd'],
                             rain=dat['rain'], rain_24=dat['rain24h'],
                             wind=dat['WD'], wind_eng=dat['wde'],
                             wind_speed=dat['WS'], wind_speed_eng=dat['wse'],
                             pressure=dat['qy'], visibility=dat['njd'],
                             aqi=dat['aqi'], aqi_pm25=dat['aqi_pm25'],
                             weather=dat['weather'], weather_eng=dat['weathere'], weather_code=dat['weathercode'])
        return addr, data

class WeaData:

    def __init__(self, sk_2d, dingzhi, index_around):
        self.sk_2d = sk_2d
        self.dingzhi = dingzhi
        self.index_around = index_around

    def get_sk_2d(self):
        if not self.sk_2d:
            return None

        dat = json.loads(unescape(self.sk_2d)[13:])
        dat['sd'] = dat['sd'][:-1]
        dat['njd'] = dat['njd'][:-2]
        # 从now()获取年月日, dat['time']获取时分秒
        dat['logtime'] = datetime.strptime('{} {}'.format(datetime.now().strftime('%Y-%m-%d'), dat['time']),
                                           '%Y-%m-%d %H:%M')
        return dat


class ScrapData(BaseRequests):

    def get_data(self, code, fail_delay=5, fail_num=5, save_file=False):
        self.get_page(DataUrl.index_url(code))
        self.set_referer(DataUrl.index_url(code))

        item = {'sk_2d': DataUrl.sk_2d_url,
                'dingzhi': DataUrl.dingzhi_url,
                'index_around': DataUrl.index_around_url}
        content = dict()

        for i in item:
            url = item[i](code)

            # TIMEOUT
            ct = 0
            while not self.get_page(url, params={'_': int(time.time() * 1000)}):
                print('请求超时, 等待{}s重连'.format(fail_delay))
                time.sleep(fail_delay)
                ct += 1
                if ct == fail_num: break

            if ct == fail_num:
                content[i] = None
            else:
                content[i] = self.text('utf-8')
                if save_file:
                    self.save_as_html('{}.html'.format(i))

        self.clear_referer()
        return WeaData(content['sk_2d'], content['dingzhi'], content['index_around'])
