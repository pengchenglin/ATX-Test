#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.split(os.path.abspath(''))[0])
from Public.casestrategy import CaseStrategy
from Public.drivers import Drivers
from Public.report import *
from Public.test_data import *
from Demo import dm_config
from Public.devices_new import check_devives

from Public.config import test_apk

if __name__ == '__main__':
    # 备份旧的报告文件
    backup_report(dm_config.project_path)   # 备份旧的测试报告文件夹到TestReport_backup下

    # # 准备测试包
    apk_info = prepare_apk(test_apk,  # 被测app的url下载地址，也可以直接填写本地的地址
                           dm_config.project_path)  # 当前测试app的文件夹所在地址绝对路径，config文件里写好的不用动

    # 测试设备准备
    devices = check_devives(dm_config.method,  # method可以是USB 或者SERVER ，
                            dm_config.udid)  # 如果连接到多台设备的，udid是指定特定设备用的

    # 测试cases准备
    cs = CaseStrategy()  # 遍历目录，找到所有的测试ceses
    cases = cs.collect_cases(suite=True)
    print(cases)

    # 执行测试并生成报告
    Drivers().run(devices, cases, apk_info,retry=3,save_last_try=True)

    # # 删除测试apk
    # os.remove(apk_info['apk_path'])