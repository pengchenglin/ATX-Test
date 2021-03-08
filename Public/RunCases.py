import os
import time
import shutil

from Public.HTMLTestReport import HTMLTestRunner
# from Public.ExtentHTMLTestRunner import HTMLTestRunner

class RunCases:
    def __init__(self, device,folder):
        self.test_report_root = os.path.join(folder, 'TestReport')
        # self.test_report_root = os.path.join(os.getcwd(), 'TestReport')
        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        # date_time = time.strftime('%Y%m%d%H%M%S_', time.localtime(time.time()))
        self.test_report_path = os.path.join(self.test_report_root, self.device['model'].replace(':', '_').replace(' ', '')+'_'+self.device['serial'])
        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

        self.file_name = os.path.join(self.test_report_path, 'TestReport.html')

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run(self, cases,retry,save_last_try):
        with open(self.file_name, 'wb') as file:
            runner = HTMLTestRunner(stream=file, title=self.device['model']+'自动化测试报告', description='用例执行情况：',retry=retry,save_last_try=save_last_try)
            runner.run(cases)
            file.close()

            # shutil.copyfile(self.file_name, './TestReport/TestReport.html')

