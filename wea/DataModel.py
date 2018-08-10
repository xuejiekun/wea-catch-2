# -*- coding:utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 城市名
    name = Column(String(30), unique=True, nullable=False)
    name_eng = Column(String(30))

    # 代码
    code = Column(String(10))

    # 开始记录时间
    build_time = Column(DateTime, default=datetime.now())

    dats = relationship('Dat', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<Address id={} name={}>'.format(self.id, self.name)


class Dat(Base):
    __tablename__ = 'dat'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    # 温湿
    temp = Column(Float)
    tempf = Column(Float)
    humidity = Column(Float)

    # 雨
    rain = Column(Float)
    rain_24 = Column(Float)

    # 风
    wind = Column(String(6))
    wind_eng = Column(String(6))
    wind_speed = Column(String(6))
    wind_speed_eng = Column(String(12))

    # 气压, 能见度, aqi
    pressure = Column(Integer)
    visibility = Column(Float)
    aqi = Column(String(12))
    aqi_pm25 = Column(String(12))

    # 天气描述
    weather = Column(String(6))
    weather_eng = Column(String(12))
    weather_code = Column(String(6))

    # 记录时间
    logtime = Column(DateTime, nullable=False)

    address_id = Column(Integer, ForeignKey('address.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('logtime', 'address_id'),
    )

    def __repr__(self):
        return '<Dat id={} logtime={} temp={} humidity={}>'.format(self.id, self.logtime, self.temp, self.humidity)


# sample={'nameen': 'shunde', 'cityname': '顺德', 'city': '101280801',
#         'temp': '28', 'tempf': '82',
#         'WD': '东南风 ', 'wde': 'SE', 'WS': '2级', 'wse': '&lt;12km/h',
#         'SD': '90%',
#         'time': '20:20',
#         'weather': '阴', 'weathere': 'Overcast', 'weathercode': 'n02',
#         'qy': '1004',
#         'njd': '25.66km',
#         'sd': '90%',
#         'rain': '0.0', 'rain24h': '0',
#         'aqi': '', 'limitnumber': '',
#         'aqi_pm25': '',
#         'date': '07月25日(星期三)'}
