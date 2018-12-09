#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

sys.path.append('.')
from Public.CaseStrategy import CaseStrategy
from Public.Drivers import Drivers
from Public.Report import *


if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    now = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
    backup_report('./TestReport', './TestReport_History', now)

    cs = CaseStrategy()
    cases = cs.collect_cases(suite=True)
    Drivers().run(cases)

    # Generate zip_report file  压缩测试报告文件
    # zip_report()