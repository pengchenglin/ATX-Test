#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from Public.basepage import BasePage
# from uiautomator2 import UiObjectNotFoundError
from Public.decorator import *
from Public.log import Log
from Demo import dm_config
import json
from Public.filetools import read_file
package = json.loads(read_file(dm_config.info_path))['package']
log = Log()


class login_page(BasePage):
    @teststep
    def wait_page(self):
        try:
            if self.d(text='Login').wait(timeout=15):
                return True
            else:
                raise Exception('Not in LoginPage')
        except Exception:
            raise Exception('Not in LoginPage')

    @teststep
    def input_username(self, text):
        log.i('输入用户名:%s'% text)
        self.d(resourceId="com.github.android_app_bootstrap:id/mobileNoEditText") \
            .set_text(text)

    @teststep
    def input_password(self, text):
        log.i('输入密码:%s'% text)
        self.d(resourceId="com.github.android_app_bootstrap:id/codeEditText") \
            .set_text(text)

    @teststep
    def click_login_btn(self):
        log.i('点击登录按钮')
        self.d(resourceId="com.github.android_app_bootstrap:id/login_button").click()






