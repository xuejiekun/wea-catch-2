# -*- coding: utf-8 -*-
import os
import time
import glob
from datetime import datetime, timedelta

from sky.base import BaseRequests
from .Url import RadarUrl


class ScrapPic(BaseRequests):
    SUCCESS = 0
    EXIST = 1
    EXPIRE = 2
    TIMEOUT = 3
    NOTFOUND = 4

    Foshan = RadarUrl.radar_fs
    GuangZhou = RadarUrl.radar_gz
    Zhaoqing = RadarUrl.radar_zq
    China = RadarUrl.radar_qg

    class DownPath:
        def __init__(self, data_dir, url_func, start, end_format='00'):
            # 下载目录
            self.url = url_func(start, end_format)
            self.loc = self.url.split('/')[-2]

            # /data_dir/start/loc
            self.down_dir = os.path.join(data_dir, start.strftime('%Y%m%d'),  self.loc)

            self.name = self.url.split('/')[-1]
            self.name_abs = os.path.join(self.down_dir, self.name)

            self.gen_url = url_func(start, '*')
            self.gen_name = self.gen_url.split('/')[-1]
            self.gen_name_abs = os.path.join(self.down_dir, self.gen_name)

    def get_init(self):
        self.get_page(RadarUrl.index_url)
        self.set_referer(RadarUrl.index_url)

    def get_end(self):
        self.clear_referer()

    def get_pic(self, data_dir, loc, start, end_format='00', timeout=10,
                success_delay=1, fail_delay=5, fail_num=5, overwrite=False):
        # 处理下载路径
        pic = self.DownPath(data_dir, loc, start, end_format)
        if not os.path.exists(pic.down_dir):
            os.makedirs(pic.down_dir, exist_ok=True)

        # EXIST
        if glob.glob(pic.gen_name_abs) and not overwrite:
            print('[{}]数据文件已存在，不用下载.'.format(pic.name))
            return self.EXIST

        # TIMEOUT
        ct = 0
        while not self.get_page(pic.url, timeout=timeout):
            print('请求超时, 等待{}s重连'.format(fail_delay))
            time.sleep(fail_delay)
            ct += 1
            if ct == fail_num:
                return self.TIMEOUT

        # EXPIRE
        if self.response.url == RadarUrl.main_url or \
                self.response.url == RadarUrl.main_url_2:
            print('[{}] 已过期'.format(pic.name))
            return self.EXPIRE

        if self.response.status_code == 404:
            print('[{}] 找不到'.format(pic.name))
            return self.NOTFOUND

        # SUCCESS
        self.save_as_pic(pic.name_abs)
        print('下载完毕: {}'.format(self.response.url))
        time.sleep(success_delay)
        return self.SUCCESS

    def get_pic_on_range(self, data_dir, loc, start, end, end_format='00', timeout=10,
                         success_delay=1, fail_delay=5, fail_num=5, overwrite=False):
        while start < end:
            self.get_pic(data_dir, loc, start, end_format, timeout=timeout,
                         success_delay=success_delay, fail_delay=fail_delay, fail_num=fail_num, overwrite=overwrite)
            start += timedelta(minutes=6)

    def get_pic_date(self, data_dir, loc, date, timeout=10,
                          success_delay=1, fail_delay=5, fail_num=5, overwrite=False):
        start = datetime(date.year, date.month, date.day)
        if date.date() == datetime.now().date():
            end = datetime.now()
        else:
            end = datetime(date.year, date.month, date.day+1)

        self.get_init()
        self.get_pic_on_range(data_dir, loc, start, end, '00', timeout=timeout,
                              success_delay=success_delay, fail_delay=fail_delay, fail_num=fail_num, overwrite=overwrite)
        self.get_pic_on_range(data_dir, loc, start, end, '01', timeout=timeout,
                              success_delay=success_delay, fail_delay=fail_delay, fail_num=fail_num, overwrite=overwrite)

    def get_pic_today(self, data_dir, loc, timeout=10,
                      success_delay=1, fail_delay=5, fail_num=5, overwrite=False):
        self.get_pic_date(data_dir, loc, datetime.now(), timeout=timeout,
                          success_delay=success_delay, fail_delay=fail_delay, fail_num=fail_num, overwrite=overwrite)
