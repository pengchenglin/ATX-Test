#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Public.BasePage import BasePage
from Public.Decorator import *
from uiautomator2 import UiObjectNotFoundError

class HomePage(BasePage):
    @teststep
    def wait_page(self):
        try:
            if self.d(text='HOME').wait(timeout=15):
                pass
            else:
                raise Exception('Not in HonePage')
        except Exception:
            raise Exception('Not in HonePage')

    @teststep
    def home_click(self):
        self.d(text='HOME').click()

    @teststep
    def home_list_click(self):
        self.d(text='list').click()

    @teststep
    def webview_click(self):
        self.d(text='Webview').click()

    @teststep
    def baidu_click(self):
        self.d(text='Baidu').click()

    @teststep
    def personal_click(self):
        self.d(text='PERSONAL').click()

    @teststep
    def personal_logout_click(self):
        self.d(text='Logout').click()


def logout():
    page = HomePage()
    page.webview_click()
    page.baidu_click()
    page.webview_click()
    page.personal_click()
    page.personal_logout_click()
