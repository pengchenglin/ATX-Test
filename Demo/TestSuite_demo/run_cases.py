#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.split(os.path.split(os.path.abspath(''))[0])[0])
from Public.casestrategy import CaseStrategy
from Public.drivers import Drivers
from Public.report import *
from Public.test_data import *
from Demo import dm_config
from Public.devices_new import check_devives



if __name__ == '__main__':
    #备份旧的报告文件
    backup_report(dm_config.project_path)

    # # 准备测试包
    apk_info = prepare_apk('http://npmcdn.com/android-app-bootstrap@latest/android_app_bootstrap/build/outputs/apk/android_app_bootstrap-debug.apk',
                           dm_config.project_path,
                           dm_config.key)

    #测试设备准备
    devices = check_devives(dm_config.method, dm_config.udid)

    #测试cases准备
    cs = CaseStrategy()
    cases = cs.collect_cases(suite=False)

    #执行测试并生成报告
    Drivers().run(devices,cases,apk_info)

    # #删除测试apk
    # os.remove(apk_info['apk_path'])




