# -*- coding:utf-8 -*-
import os
from datetime import datetime

from wea import ScrapData, DataManager, ScrapPic
from wea.ImgTool import create_gif

def test_scrapdata():
    scrap = ScrapData()
    dat = scrap.get_data(101280801, save_file=False)

    db = DataManager('sqlite:///test.db', echo=False, autocommit=False)
    # db.create_table()
    sk_2d = dat.get_sk_2d()
    print(sk_2d)
    if sk_2d:
        print(db.add_wea_dat(sk_2d))

    db.close()
    print('Done')

def create_gif_from_pic(data_dir, loc, format):
    loc_dict = {'fs':ScrapPic.Foshan,
                'gz':ScrapPic.GuangZhou,
                'zq':ScrapPic.Zhaoqing,
                'qg':ScrapPic.China}
    print(loc_dict[loc])

    # date = datetime.now()
    date = datetime(2018, 8, 7)

    scrap = ScrapPic()
    scrap.get_pic_date(data_dir, loc_dict[loc], date, timeout=5, fail_delay=2, fail_num=1)
    source = os.path.join(data_dir, date.strftime('%Y%m%d'), loc)

    gif_name = '{}_{}.{}'.format(date.strftime('%Y%m%d'), loc, format)
    gif_name = os.path.join(format, gif_name)
    if not os.path.exists(format):
        os.makedirs(format, exist_ok=True)

    create_gif(gif_name, source, 10)

if __name__ == '__main__':
    create_gif_from_pic('data_dir', 'fs', 'mp4')
    # test_scrapdata()
