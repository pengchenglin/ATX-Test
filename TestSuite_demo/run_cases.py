import os
import sys
# sys.path.append(os.path.split(os.path.split(os.path.abspath(''))[0])[0])
sys.path.append('..')
from Public.CaseStrategy import CaseStrategy
from Public.Drivers import Drivers
from Public.Report import *


if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    backup_report()

    cs = CaseStrategy()
    cases = cs.collect_cases(suite=False)
    Drivers().run(cases)

    # Generate zip_report file  压缩测试报告文件
    # zip_report()
