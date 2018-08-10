# -*- coding:utf-8 -*-
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import logging
import os
import inspect

from task import Task


class WeaService(win32serviceutil.ServiceFramework):
    # 服务名
    _svc_name_ = "WeaService"
    # 服务在windows系统中显示的名称
    _svc_display_name_ = "WeaService"
    # 服务的描述
    _svc_description_ = "定时下载中国天气网上的数据"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.logger = self.get_logger()
        self.task = Task(self.logger)

    def get_logger(self):
        logger = logging.getLogger('[WeaService]')

        # 获取当前文件夹路径
        file_abs_name = inspect.getfile(inspect.currentframe())

        # 创建一个handler，用于写入日志文件
        handler = logging.FileHandler(os.path.join(os.path.dirname(file_abs_name), "service.log"))

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(handler)

        # 日志等级(从高到低)：CRITICAL->ERROR->WARNING->INFO->DEBUG
        # 一旦设置了日志等级，则调用比等级低的日志记录函数则不会输出
        logger.setLevel(logging.INFO)

        return logger

    def SvcDoRun(self):
        # 把自己的代码放到这里，就OK
        # 等待服务被停止
        self.logger.info('Svc run...')
        self.task.run()

        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

    def SvcStop(self):
        self.logger.info('Svc down...')
        self.task.stop()
        # 先告诉SCM停止这个过程
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # 设置事件
        win32event.SetEvent(self.hWaitStop)


if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(WeaService)
            servicemanager.Initialize('WeaService', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except:
             win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(WeaService)
