#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Public.drivers import Drivers
from Public.report import *
from Public.maxim_monkey import Maxim
import unittest
from Monkey import login_steps

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    data = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    # backup_report('./MaximReport')
    cases = unittest.TestSuite()

    cases.addTest(login_steps.abcd('test_install_login'))
    command = Maxim().command(package='com.github.android_app_bootstrap', runtime=1, mode='uiautomatordfs',
                              throttle=500,
                              options=' -v -v ', whitelist=True)
    print(command)

    Drivers().run_maxim(cases=cases, command=command, actions=True, widget_black=False)
