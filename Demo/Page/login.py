#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Public.BasePage import BasePage
from Public.maxim_monkey import Maxim
from Public.Decorator import *
from uiautomator2 import UiObjectNotFoundError


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





def login(username, password):
    page = LoginPage()
    page.input_username(username)
    page.inputpassword(password)
    page.login_click()
