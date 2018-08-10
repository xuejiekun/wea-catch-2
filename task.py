# -*- coding:utf-8 -*-
import inspect
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from wea import ScrapData, DataManager


class Task:
    def __init__(self, logger):
        self.logger = logger
        self.sched = BlockingScheduler()
        self.scrap = ScrapData()

        file_name_abs = inspect.getfile(inspect.currentframe())
        database = os.path.join(os.path.dirname(file_name_abs), 'test.db')
        self.db = DataManager('sqlite:///{}'.format(database), autocommit=False)

    def get_data(self):
        dat = self.scrap.get_data(101280801)

        sk_2d = dat.get_sk_2d()
        if sk_2d:
            self.db.add_wea_dat(dat.get_sk_2d())
            self.logger.info('get data')
        else:
            self.logger.info('not data')

    def test(self):
        self.logger.info('test')

    def run(self):
        self.logger.info('run')
        self.sched.add_job(self.get_data, 'cron', minute='0,30', misfire_grace_time=30)
        # self.sched.add_job(self.test, 'cron', second='0,10,20,30,40,50')
        self.sched.start()

    def stop(self):
        self.sched.shutdown(wait=False)
        self.db.close()
