#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
import time
from Public.BasePage import BasePage
from Public.Decorator import *
from PageObject import login
import unittest

from Public.ReadConfig import ReadConfig
apk_url = ReadConfig().get_apk_url()
pkg_name = ReadConfig().get_pkg_name()
apk_path = ReadConfig().get_apk_path()


class apk_install(unittest.TestCase, BasePage):

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.github.android_app_bootstrap")

    @testcase
    def test_01_install_apk(self):
        '''安装启动android_app_bootstrap'''
        self.d.app_uninstall(pkg_name)
        # self.d.app_install(apk_url)
        self.local_install(apk_path)
        self.d.app_start(pkg_name)
        time.sleep(3)
        login.login_page().wait_page()


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
        print(ele.get_text())
        try:
            #  实际是 Login
            self.assertEqual(ele.get_text(), '登录')
        except AssertionError:
            print('失败截图一张')
            raise
        finally:
            self.d(text='Login').click()
            print('手动截图一张')
            self.screenshot()

    @testcase
    def test_04_error(self):
        '''错误处理'''
        print('手动出错')
        raise Exception('手动ERROR!!!!!!!')


