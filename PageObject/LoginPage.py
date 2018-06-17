#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Public.BasePage import BasePage
from Public.Decorator import *
from uiautomator2 import UiObjectNotFoundError


class LoginPage(BasePage):
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
        self.d(resourceId="com.github.android_app_bootstrap:id/mobileNoEditText") \
            .set_text(text)

    @teststep
    def inputpassword(self, text):
        self.d(resourceId="com.github.android_app_bootstrap:id/codeEditText") \
            .set_text(text)

    @teststep
    def login_click(self):
        self.d(text='Login').click()


def login(username, password):
    page = LoginPage()
    page.input_username(username)
    page.inputpassword(password)
    page.login_click()
