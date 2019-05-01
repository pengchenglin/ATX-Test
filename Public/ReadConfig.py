#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os


proDir = os.path.split(os.path.realpath(__file__))[0]
#将path分割成路径名和文件名
configPath = os.path.join(proDir, "config.ini")
#将多个路径组合后返回

class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='UTF-8')

    def get_method(self):
        value = self.cf.get("DEVICES", 'method')
        return value

    def get_server_url(self):
        value = self.cf.get("DEVICES", "server")
        return value

    def get_devices_ip(self):
        value = self.cf.get("DEVICES", "IP")
        return value.split('|')

    def get_apk_url(self):
        value = self.cf.get("APP", "apk_url")
        return value

    def get_apk_path(self):
        value = self.cf.get("APP", "apk_path")
        return value

    def get_pkg_name(self):
        value = self.cf.get("APP", "pkg_name")
        return value

    def get_testdata(self, name):
        value = self.cf.get("TESTDATA", name)
        return value.split('|')


# if __name__ == '__main__':
#     print(ReadConfig().get_pkg_name())
#     print(ReadConfig().get_testdata('user_name'))
