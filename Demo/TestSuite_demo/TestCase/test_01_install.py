#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from Public.basepage import BasePage
from Public.decorator import *
from Demo.Page import login
import unittest
import json
from Public.filetools import read_file
from Demo import dm_config
log = Log()
pkg_name = json.loads(read_file(dm_config.info_path))['package']
apkpath = json.loads(read_file(dm_config.info_path))['apk_path']


class apk_install(unittest.TestCase, BasePage):

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.github.android_app_bootstrap")

    @setup
    def setUp(self):
        self.startscreenrecord()

    @teardown
    def tearDown(self):
        self.stopscreenrecord()


    @testcase
    def test_01_install_apk(self):
        '''安装启动android_app_bootstrap'''

        self.d.app_uninstall(pkg_name)
        # self.d.app_install(apk_url)
        self.local_install(apkpath)
        watcher = self.watch_device("继续|确定")
        self.d.app_start(pkg_name)
        time.sleep(3)
        login.login_page().wait_page()
        self.unwatch_device(watcher)


    @testcase
    def test_03_screenshot(self):
        '''手动截图测试'''
        self.screenshot()
        self.d.toast.show('HELLO ATX', 2)
        time.sleep(0.5)
        self.screenshot()

    @testcase
    def test_02_fail(self):
        '''异常处理'''
        ele = self.d(text='Login')
        log.i(ele.get_text())
        try:
            #  实际是 Login
            self.assertEqual(ele.get_text(), '登录')
        except AssertionError:
            log.i('失败截图一张')
            raise
        finally:
            self.d(text='Login').click()
            log.i('手动截图一张')
            self.screenshot()

    @testcase
    def test_04_error(self):
        '''错误处理'''
        log.i('手动出错')
        raise Exception('手动ERROR!!!!!!!')


