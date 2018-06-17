# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# extension for https://sites.google.com/a/chromium.org/chromedriver/
# Experimental, maybe change in the future
# Created by <hzsunshx> 2017-01-20


from __future__ import absolute_import

import atexit
import six
from selenium import webdriver
import psutil as pt
import os


if six.PY3:
    import subprocess
    from urllib.error import URLError
else:
    from urllib2 import URLError
    import subprocess32 as subprocess


def getPidByName(Str):
    pids = pt.process_iter()
    pidList = []
    for pid in pids:
        if pid.name() == Str:
            pidList.append(int(pid.pid))
    return pidList


class ChromeDriver(object):
    def __init__(self, d, port):
        self._d = d
        self._port = port

    def _launch_webdriver(self):
        # print("start chromedriver instance")
        p = subprocess.Popen(['chromedriver', '--port=' + str(self._port)])
        try:
            p.wait(timeout=2.0)
            return False
        except subprocess.TimeoutExpired:
            return True

    def driver(self, device_ip=None, package=None, attach=True, activity=None, process=None):
        """
        Args:
            - package(string): default current running app
            - attach(bool): default true, Attach to an already-running app instead of launching the app with a clear data directory
            - activity(string): Name of the Activity hosting the WebView.
            - process(string): Process name of the Activity hosting the WebView (as given by ps).
                If not given, the process name is assumed to be the same as androidPackage.

        Returns:
            selenium driver
        """
        app = self._d.current_app()
        capabilities = {
            'chromeOptions': {
                'androidDeviceSerial': device_ip or self._d.serial,
                'androidPackage': package or app['package'],
                'androidUseRunningApp': attach,
                'androidProcess': process or app['package'],
                'androidActivity': activity or app['activity'],
            }
        }

        try:
            dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)
        except URLError:
            self._launch_webdriver()
            dr = webdriver.Remote('http://localhost:%d' % self._port, capabilities)

        # always quit driver when done
        atexit.register(dr.quit)
        return dr

    @staticmethod
    def kill():
        # # for windows
        # pid = getPidByName('chromedriver.exe')
        # for i in pid:
        #     os.popen('taskkill /PID %d /F' % i)

        # for mac
        pid = getPidByName('chromedriver')
        for i in pid:
            os.popen('kill -9 %d' % i)

        print('All chromedriver pid killed')


# if __name__ == '__main__':
    import uiautomator2 as u2

    # d = u2.connect()
    # driver = ChromeDriver(d).driver()
    # elem = driver.find_element_by_link_text(u"登录")
    # elem.click()
    # driver.quit()
    # ChromeDriver.kill()
