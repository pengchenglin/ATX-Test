#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uiautomator2 as u2
import time
from Public.BasePage import BasePage
from Public.Decorator import *
from PageObject.HomePage import HomePage
from PageObject import LoginPage
from Public.Test_data import get_test_data
import unittest


# @unittest.skip
class TestBootStrap(unittest.TestCase, BasePage):
    '''BootStrap demo测试'''

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start("com.github.android_app_bootstrap")  # restart app
        cls.test_data = get_test_data(cls.d)

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.github.android_app_bootstrap")  # restart app
        # cls.set_original_ime()

    # @setup
    # def setUp(self):
    #     pass
    #
    # @teardown
    # def tearDown(self):
    #     pass

    @testcase
    def test_01_login(self):
        '''登录'''
        LoginPage.LoginPage().wait_page()
        self.set_fastinput_ime()
        LoginPage.login(self.test_data['user_name'], self.test_data['password'])
        print('登录成功')

    @testcase
    def test_02_show_toast(self):
        '''获取toast'''
        self.d(resourceId="com.github.android_app_bootstrap:id/imageview").click()
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()
        self.d(text='Toast').click()
        toast1 = self.get_toast_message()
        assert 'Toast' in toast1
        print('点击Toast按钮后的toast信息为:\n%s' % toast1)
        # time.sleep(2)
        self.d(text='Show Dialog').click()
        toast2 = self.get_toast_message()
        self.assertIn('Hello', toast2)
        # self.assertEqual('Hello', toast2)
        print('点击Show Dialog后的toast信息为:\n%s' % toast2)

        self.back()
        self.back()

    @testcase
    def test_03_auto_click_alert(self):
        '''弹窗自动点击测试'''
        self.watch_device()
        HomePage().home_click()
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()
        self.d(text='Alert').click()
        self.d(text='Show Dialog').click()
        time.sleep(0.2)
        self.d(text='Show Dialog').click()
        time.sleep(0.2)
        self.d(text='Show Dialog').click()
        time.sleep(0.2)
        self.d(text='Show Dialog').click()
        self.screenshot()  # 手动截图
        time.sleep(3)  # 等待3秒内自动点击yes后，继续后面的操作
        self.back()
        self.back()
        self.unwatch_device()

    @testcase
    def test_04_webview_chromedriver(self):
        '''chromedriver webview测试 '''
        self.d(text='Baidu').click()
        time.sleep(3)
        driver = self.set_chromedriver()
        driver.find_element_by_id('index-kw').click()
        driver.find_element_by_id('index-kw').send_keys('Python')
        time.sleep(3)
        self.screenshot()  # 手动截图
        driver.find_element_by_id('index-bn').click()
        time.sleep(3)
        self.d(text=u"logo", className="android.view.View").click()
        driver.quit()

    @testcase
    def test_05_webview_u2(self):
        '''直接用u2操作webview'''
        # self.d(resourceId="index-form").child(className="android.widget.EditText").set_text("西湖美景")
        self.d(resourceId="index-kw", className="android.widget.EditText").set_text("西湖美景")
        self.d(text=u"百度一下", className="android.widget.Button").click()
        self.d(text=u"西湖十景_百度百科").click()
        time.sleep(4)
        for i in range(20):
            self.swipe_up()
            # time.sleep(0.1)
        self.screenshot()
        time.sleep(2)

    @testcase
    def test_06_Bar_click(self):
        '''主页操作并退出'''
        HomePage().home_click()
        HomePage().baidu_click()
        HomePage().webview_click()
        HomePage().personal_click()
        HomePage().personal_logout_click()

        LoginPage.LoginPage().wait_page()

    @testcase
    def test_07_login_again(self):
        '''再次登录'''
        LoginPage.LoginPage().login_click()

    @testcase
    def test_08_swipe(self):
        '''swipe 滑动测试'''
        HomePage().home_click()
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()
        self.d(text='Gesture').click()
        self.swipe_up()
        self.swipe_left()
        self.swipe_down()
        self.swipe_right()
