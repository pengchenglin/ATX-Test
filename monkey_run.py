#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

# sys.path.append('.')
from Public.Drivers import Drivers
from Public.Report import *
from Public.maxim_monkey import Maxim

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下

    command = Maxim().command(package='com.quvideo.xiaoying', runtime=1, mode='uiautomatormix', throttle=100,
                              options=' -v -v ', whitelist=False)
    Drivers().run_maxim(command)

    # Generate zip_report file  压缩测试报告文件
    # zip_report()