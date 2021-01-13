import time
import os
import zipfile

from multiprocessing import Pool
import uiautomator2 as u2
from Public.devices_new import *
# from Public.Devices import *
from Public.RunCases import RunCases
from Public.RunMaxim import RunMaxim
from Public.reportpath import ReportPath
from Public.basepage import BasePage
from Public.maxim_monkey import Maxim
from Public.log import Log
from Public.test_data import *
from Public.report import *
from logzero import logger


# from Public.chromedriver import ChromeDriver



class Drivers:
    @staticmethod
    def _run_cases(run, cases):
        log = Log()
        log.set_logger(run.get_device()['model'], run.get_path() + '/' + 'client.log')
        log.i('udid: %s' % run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # print(run.get_device())
            # 运行前准备
            base_page.unlock_device()
            base_page.set_fastinput_ime()  # 设置fastime输入法
            # base_page.d.shell('logcat -c')  # 清空logcat
            # 开始执行测试
            run.run(cases)

            # 结束后操作
            base_page.unwatch_device()
            base_page.set_original_ime()

            # 将logcat文件上传到报告
            # base_page.d.shell('logcat -d > /sdcard/logcat.log')
            # time.sleep(2)
            # base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))

            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s' % e)

    @staticmethod
    def _run_maxim(run, cases, command, actions, widget_black):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)
            Maxim().run_monkey(monkey_shell=command, actions=actions, widget_black=widget_black)

            base_page.d.shell('logcat -d > /sdcard/logcat.log')
            time.sleep(1)
            base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
            base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()
            if 'ip' in run.get_device():
                log.i('release device %s ' % run.get_device()['serial'])
                atxserver2().release_device(run.get_device()['serial'])

        except AssertionError as e:
            log.e('AssertionError, %s', e)

    def run(self, devices, cases, apk_info):
        if not devices:
            logger.error('There is no device found,test over.')
            return
        logger.info('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i], apk_info['folder']))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, cases,))
            time.sleep(2)
        logger.info('Waiting for all runs done........ ')
        pool.close()
        time.sleep(1)
        pool.join()
        logger.info('All runs done........ ')

        #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        build_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        title = '报告生成时间: %s<br />测试包地址： <a href="%s">%s</a>' \
                '<br />PackageName: %s<br /> Version: %s<br />VersionCode: %s' % (
                    build_time, apk_info['url'], apk_info['url'], apk_info["package"], apk_info["versionName"],
                    apk_info["versionCode"])

        create_statistics_report(runs, title=title,sreport_path=apk_info['folder'])

    def run_maxim(self, cases=None, command=None, actions=False, widget_black=False):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        devices = check_devives()
        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunMaxim(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_maxim,
                             args=(run, cases, command, actions, widget_black,))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')



