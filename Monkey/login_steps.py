#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Public.decorator import *
import unittest

from Demo.Page import login

apk_path = '../apk/android_app_bootstrap-debug.apk'
pkg_name = 'com.github.android_app_bootstrap'


class abcd(unittest.TestCase, BasePage):
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()

    @testcase
    def test_install_login(self):
        '''安装启动android_app_bootstrap'''
        self.d.app_uninstall(pkg_name)
        self.local_install(apk_path)
        self.d.app_start(pkg_name)
        self.set_fastinput_ime()
        time.sleep(3)
        login.login_page().input_username('username')
        login.login_page().input_password('password')
        login.login_page().click_login_btn()



