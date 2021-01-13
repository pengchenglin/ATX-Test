#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
# sys.path.append(os.path.split(os.path.split(os.path.abspath(''))[0])[0])
sys.path.append('..')
from Public.drivers import Drivers
from Public.report import *
from Public.test_data import *
import unittest
from Demo.TestSuite_demo.TestCase import test_01_install



if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    date = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    backup_report(date)

    suite = unittest.TestSuite()
    # suite.addTest(test_01_installapp.app_install('test_01_install'))
    suite.addTest(test_01_installapp.app_install('test_03_oversea'))
    suite.addTest(test_01_installapp.app_install('test_03_oversea_upload'))
    suite.addTest(test_01_installapp.app_install('test_04_alig_tencent'))
    suite.addTest(test_01_installapp.app_install('test_05_alig_tencent_export'))
    suite.addTest(test_01_installapp.app_install('test_06_noalig_wandoujia'))
    # suite.addTest(test_01_installapp.app_install('test_03_click_camera_btn'))
    # suite.addTest(test_01_installapp.app_install('test_04_login'))

    apks = download_channel_apks(url=ReadConfig().get_channel_url(), version=ReadConfig().get_channel_version())
    Drivers().run(suite, apks)

