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


class home_page(BasePage):
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
    def click_tab(self, inst=1):
        '''
        点击底部tab
        :param inst: tab的位数
        :return:
        '''
        ele = self.d(resourceId="android:id/tabs").child(className="android.widget.LinearLayout", instance=inst - 1)
        text = ele.child(resourceId="com.github.android_app_bootstrap:id/textview").get_text()
        ele.child(resourceId="com.github.android_app_bootstrap:id/imageview").click()
        log.i('点击Tab %s' % text)

    @teststep
    def click_list_btn(self):
        log.i('点击list按钮')
        self.d(resourceId="com.github.android_app_bootstrap:id/list_button").click()

    @teststep
    def select_list_action(self, text='Gesture'):
        log.i('功能列表点击 %s' % text)
        self.d(text=text).click()

    @teststep
    def click_logout_btn(self):
        log.i('点击退出按钮')
        self.d(resourceId="com.github.android_app_bootstrap:id/logout_button").click()
