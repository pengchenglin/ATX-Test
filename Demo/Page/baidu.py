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


class baidu_page(BasePage):
    @teststep
    def set_text(self,text="西湖"):
        log.i('搜索栏输入%s'% text)
        self.d(resourceId="index-kw", className="android.widget.EditText").set_text(text)

    @teststep
    def click_search_btn(self):
        log.i('点击百度一下搜索按钮')
        self.d(text=u"百度一下", className="android.widget.Button").click()





