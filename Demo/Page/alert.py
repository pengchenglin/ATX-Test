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


class alert_page(BasePage):
    @teststep
    def click_show_dialog(self):
        log.i('点击 show dialog 按钮')
        self.d(resourceId="com.github.android_app_bootstrap:id/alert_button").click()

    @teststep
    def select_dialog(self,yes =True):
        if yes:
            log.i('dialog 点击yes')
            self.d(resourceId="android:id/button1").click()
        else:
            log.i('dialog 点击No')
            self.d(resourceId="android:id/button2").click()




