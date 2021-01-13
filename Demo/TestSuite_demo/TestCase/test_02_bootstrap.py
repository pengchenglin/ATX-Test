#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from Public.basepage import BasePage
from Public.decorator import *
from Demo.Page.home import home_page
from Demo.Page import login
import unittest
import json
from Public.filetools import read_file
from Demo import dm_config
log = Log()
pkg_name = json.loads(read_file(dm_config.info_path))['package']
apkpath = json.loads(read_file(dm_config.info_path))['apk_path']

# @unittest.skip
class TestBootStrap(unittest.TestCase, BasePage):
    '''BootStrap demo测试'''

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start("com.github.android_app_bootstrap")  # restart app

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.github.android_app_bootstrap")  # restart app
        # cls.set_original_ime()

    @setup
    def setUp(self):
        pass

    @teardown
    def tearDown(self):
        pass



    @testcase
    def test_01_login(self):
        '''登录'''
        login.login_page().wait_page()
        self.set_fastinput_ime()
        login.login_page().input_username('user_name')
        login.login_page().input_password('password')
        login.login_page().click_login_btn()


    @testcase
    def test_02_show_toast(self):
        '''获取toast'''
        self.d(resourceId="com.github.android_app_bootstrap:id/imageview").click()
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()
        self.d(text='Toast').click()
        toast1 = self.get_toast_message()
        assert 'Toast' in toast1
        log.i('点击Toast按钮后的toast信息为:\n%s' % toast1)
        # time.sleep(2)
        self.d(text='Show Dialog').click()
        toast2 = self.get_toast_message()
        self.assertIn('Hello', toast2)
        # self.assertEqual('Hello', toast2)
        log.i('点击Show Dialog后的toast信息为:\n%s' % toast2)

        self.back()
        self.back()

    @testcase
    def test_03_auto_click_alert(self):
        '''弹窗自动点击测试'''
        self.watch_device('yes')
        home_page().click_tab(1)
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
        self.d(resourceId="index-kw", className="android.widget.EditText").set_text("西湖")
        self.d(text=u"百度一下", className="android.widget.Button").click()
        time.sleep(2)
        self.d(textContains=u"百度百科").click()
        time.sleep(4)
        for i in range(5):
            self.swipe_up()
        time.sleep(2)

    @testcase
    def test_06_Bar_click(self):
        '''主页操作并退出'''
        home_page().click_tab(1)
        home_page().click_tab(2)
        home_page().click_tab(3)
        home_page().click_tab(4)
        home_page().click_logout_btn()
        login.login_page().wait_page()

    @testcase
    def test_07_login_again(self):
        '''再次登录'''
        login.login_page().click_login_btn()

    @testcase
    def test_08_swipe(self):
        '''swipe 滑动测试'''
        home_page().click_tab(1)
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()
        self.d(text='Gesture').click()
        self.swipe_up()
        self.swipe_left()
        self.swipe_down()
        self.swipe_right()

if __name__ == '__main__':
    from Public.log import Log
    from Public.reportpath import ReportPath
    from Public.filetools import mk_dir

    debug_folder = mk_dir('./debug')
    Log().set_logger('udid', os.path.join(debug_folder, 'log.log'))
    ReportPath().set_path(debug_folder)
    BasePage().set_driver(None)
    suite = unittest.TestSuite()
    # suite.addTest(TestBootStrap('test_05_webview_u2'))
    suite.addTest(TestBootStrap('test_04_webview_chromedriver'))
    runner = unittest.TextTestRunner()
    runner.run(suite)