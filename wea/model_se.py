# -*- coding:utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, DateTime, Text
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)
    build_time = Column(DateTime, default=datetime.now())   #strftime('%Y-%m-%d %H:%M:%S')

    dats = relationship('Dat', backref='address', lazy='dynamic')

    def __repr__(self):
        return '<Address id={} name={}>'.format(self.id, self.name)


class Dat(Base):
    __tablename__ = 'dat'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)

    logtime = Column(DateTime, nullable=False)
    temp = Column(Float)
    humidity = Column(Float)
    wdir = Column(String(10))
    speed = Column(Float)
    alarm_text = Column(Text(80))
    alarm_detail = Column(Text(100))

    address_id = Column(Integer, ForeignKey('address.id', ondelete='CASCADE'), nullable=False)

    __table_args__ = (
        UniqueConstraint('logtime', 'address_id'),
    )

    def __repr__(self):
        return '<Dat id={} logtime={} temp={} humidity={}>'.format(self.id, self.logtime, self.temp, self.humidity)
