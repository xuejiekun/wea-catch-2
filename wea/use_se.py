# -*- coding: utf-8 -*-
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from sky.base import BaseORM
from sky.base.database import SQLite3
from model_se import Address, Dat, Base

url_1 = r'http://www.weather.com.cn/data/sk/101280801.html'
url_2 = r'http://www.weather.com.cn/weather1d/101280801.shtml'


class WeaDataFrame:

    def __init__(self, logtime, temp=None, humidity=None, wdir=None, speed=None, alarm_text=None, alarm_detail=None, city=None):
        self.logtime = logtime
        self.temp = temp
        self.humidity = humidity
        self.wdir = wdir
        self.speed = speed
        self.alarm_text = alarm_text
        self.alarm_detail = alarm_detail

        self.city = city

    def __repr__(self):
        return 'time     : {}\n' \
               'temp     : {}℃\n' \
               'humidity : {}%\n' \
               'wdir     : {}\n' \
               'speed    : {}\n' \
               'city     : {}'.format(self.logtime, self.temp,
                                      self.humidity, self.wdir,
                                      self.speed, self.city)


class WebFrame:

    def __init__(self, page_source):
        self.bsobj = BeautifulSoup(page_source, 'lxml')

        # 主体
        self.sk = self.bsobj.find('div', {'class': 'sk'})
        # 预警
        self.alarm = self.sk.find('div', {'class': 'sk_alarm'})
        # 时间
        self.logtime = self.sk.find('p', {'class': 'time'})
        # 湿度
        self.humidity = self.sk.find('div', {'class': 'zs h'})
        # 风
        self.wind = self.sk.find('div', {'class': 'zs w'})
        # 温度
        self.temp = self.sk.find('div', {'class': 'tem'})

        # 城市
        self.city = self.bsobj.find('div', {'id':'select'})

    def analyze_time(self):
        if self.logtime:
            return datetime.strptime('{} {}'.format(datetime.now().strftime('%Y-%m-%d'),
                                                   self.logtime.text.split('|')[0][:-3]),
                                    '%Y-%m-%d %H:%M')
        return None

    def analyze_temp(self):
        if self.temp:
            return float(self.temp.find('span').text)
        return None

    def analyze_humidity(self):
        if self.humidity:
            return float(self.humidity.find('em').text[:-1])
        return None

    def analyze_alarm(self):
        if self.alarm:
            alarms = self.alarm.findAll('a')

            alarm_text = ''
            alarm_detail = ''
            ct = 1
            for alarm in alarms:
                alarm_text += '{}.{} '.format(ct, alarm.text)
                alarm_detail += '{}.{} '.format(ct, alarm['title'])
                ct += 1
            if alarm_text:
                return alarm_text, alarm_detail
        return None, None

    def analyze_wind(self):
        if self.wind:
            wdir = self.wind.find('span').text[:-1]
            speed = float(self.wind.find('em').text[:-1])
            return wdir, speed
        return None, None

    def analyze_city(self):
        if self.city:
            return self.city.find('span').text
        return None

    def get_data(self):
        wdir, speed = self.analyze_wind()
        alarm_text, alarm_detail = self.analyze_alarm()

        return WeaDataFrame(logtime=self.analyze_time(),
                            temp=self.analyze_temp(),
                            humidity=self.analyze_humidity(),
                            wdir=wdir, speed=speed,
                            alarm_text=alarm_text, alarm_detail=alarm_detail,
                            city=self.analyze_city())


class DataManager(BaseORM):

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_address(self, name):
        addr = self.session.query(Address).filter(Address.name == name).first()
        if not addr:
            print('add address')
            addr = Address(name=name)
            self.session.add(addr)
            self.session.commit()
        return addr

    def add_data(self, logtime, address_id, temp=None, humidity=None, wdir=None, speed=None, alarm_text=None, alarm_detail=None):
        dat = Dat(logtime=logtime, address_id=address_id,
                  temp=temp, humidity=humidity,
                  wdir=wdir, speed=speed,
                  alarm_text=alarm_text, alarm_detail=alarm_detail)
        print('add data')
        self.session.add(dat)
        self.session.commit()
        return dat

    def add_wea_data(self, dat):
        addr = self.add_address(dat.city)
        return self.add_data(logtime=dat.logtime, address_id=addr.id,
                             temp=dat.temp, humidity=dat.humidity,
                             wdir=dat.wdir, speed=dat.speed,
                             alarm_text=dat.alarm_text, alarm_detail=dat.alarm_detail)


def build_browser():
    options = Options()
    options.add_argument('-headless')

    browser = webdriver.Firefox(executable_path='geckodriver', firefox_options=options)
    return  browser


if __name__ == '__main__':
    browser = build_browser()
    browser.get(r'http://www.weather.com.cn/weather1d/101280801.shtml')

    wf = WebFrame(browser.page_source)

    # with open('index.html', 'r', encoding='utf-8') as fp:
    #     wf = WebFrame(fp.read())

    dat = wf.get_data()

    db = DataManager('sqlite:///data.db', echo=False, autocommit=False)
    db.create_table()
    db.add_wea_data(dat)
    db.close()

    #db = SQLite3(database='data.db')
    #db.cursor.execute('insert into address(name)values (?)', ('广州',))
    #db.close()

    print('Message:')
