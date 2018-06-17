import os
import time
import shutil

from Public.HTMLTestReport import HTMLTestRunner


class RunCases:
    def __init__(self, device):
        self.test_report_root = './TestReport'
        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        date_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
        self.test_report_path = self.test_report_root + '/' + date_time + '-%s' % self.device['model']
        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

        self.file_name = self.test_report_path + '/' + 'TestReport.html'

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run(self, cases):
        with open(self.file_name, 'wb') as file:
            runner = HTMLTestRunner(stream=file, title=self.device['model']+'自动化测试报告', description='用例执行情况：')
            runner.run(cases)
            file.close()

            # shutil.copyfile(self.file_name, './TestReport/TestReport.html')

