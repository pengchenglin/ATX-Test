#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uiautomator2 as u2
from logzero import logger
import time
import os

from Public.basepage import BasePage
from Public.decorator import *
from uiautomator2 import UiObjectNotFoundError

from Public.log import Log
from Public.config import maxin_path

log = Log()
# maxin_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'Maxim')


# 参考网站：
# Maxim-高速 Android Monkey 工具使用记录： https://testerhome.com/topics/11884
# 基于 Android Monkey 二次开发，实现高速点击的 Android Monkey 自动化工具 fastmonkey ：https://testerhome.com/topics/11719


class Maxim(BasePage):

    @classmethod
    def command(cls, package, runtime, mode=None, whitelist=False, blacklist=False, throttle=None, options=None,
                off_line=True):
        '''
        monkey命令封装
        :param package:被测app的包名
        :param runtime: 运行时间 minutes分钟
        :param mode: 运行模式
            uiautomatormix(混合模式,70%控件解析随机点击，其余30%按原Monkey事件概率分布)、
            pct-uiautomatormix n ：可自定义混合模式中控件解析事件概率 n=1-100
            uiautomatordfs：DFS深度遍历算法（优化版）（注 Android5不支持dfs）(u2和dsf冲突 无法使用）
            uiautomatortroy：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
            None: 默认原生 monkey
        :param whitelist: activity白名单  需要将awl.strings 配置正确
        :param blacklist: activity黑名单  需要将awl.strings 配置正确
        :param throttle: 在事件之间插入固定的时间（毫秒）延迟
        :param options: 其他参数及用法同原始Monkey
        :param off_line: 是否脱机运行 默认Ture
        :return: shell命令
        '''
        classpath = 'CLASSPATH=/sdcard/monkey.jar:/sdcard/framework.jar exec app_process /system/bin tv.panda.test.monkey.Monkey'
        package = ' -p ' + package
        runtime = ' --running-minutes ' + str(runtime)
        if mode:
            mode = ' --' + mode
        else:
            mode = ''
        if throttle:
            throttle = ' --throttle ' + str(throttle)
        else:
            throttle = ''
        if options:
            options = ' ' + options
        else:
            options = ''
        if whitelist:
            whitelist = ' --act-whitelist-file /sdcard/awl.strings'
        else:
            whitelist = ''
        if blacklist:
            blacklist = ' --act-blacklist-file /sdcard/awl.strings'
        else:
            blacklist = ''

        off_line_cmd = ' >/sdcard/monkeyout.txt 2>/sdcard/monkeyerr.txt &'
        if off_line:
            monkey_shell = (
                ''.join([classpath, package, runtime, mode, whitelist, blacklist, throttle, options, off_line_cmd]))
        else:
            monkey_shell = (
                ''.join([classpath, package, runtime, mode, whitelist, blacklist, throttle, options]))

        return monkey_shell

    #  Maxim 文件夹说明：
    # awl.strings：存放activity白名单
    # max.xpath.actions：特殊事件序列
    # max.xpath.selector：TROY模式（支持特殊事件、黑控件等） 配置 max.xpath.selector troy控件选择子来定制自有的控件选择优先级
    # max.widget.black：黑控件 黑区域屏蔽
    # max.strings 随机输入字符，内容可自定义配置

    @classmethod
    def run_monkey(cls, monkey_shell, actions=False, widget_black=False):
        '''
        清理旧的配置文件并运行monkey，等待运行时间后pull log文件到电脑
        :param monkey_shell: shell命令 uiautomatortroy 时 max.xpath.selector文件需要配置正确
        :param actions: 特殊事件序列 max.xpath.actions文件需要配置正确
        :param widget_black: 黑控件 黑区域屏蔽 max.widget.black文件需要配置正确
        :return:
        '''
        log.i('MONKEY_SHELL:%s' % monkey_shell)
        cls.clear_env()
        cls.push_jar()
        if monkey_shell.find('awl.strings') != -1:
            cls.push_white_list()
        if monkey_shell.find('uiautomatortroy') != -1:
            cls.push_selector()
        if actions:
            cls.push_actions()
        if widget_black:
            cls.push_widget_black()
        cls.set_AdbIME()
        runtime = monkey_shell.split('running-minutes ')[1].split(' ')[0]
        log.i('starting run monkey')
        log.i('It will be take about %s minutes,please be patient ...........................' % runtime)
        # restore uiautomator server
        cls.d.service('uiautomator').stop()
        time.sleep(2)
        cls.d.shell(monkey_shell)
        time.sleep(int(runtime) * 60 + 30)
        log.i('Maxim monkey run end>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # restore uiautomator server
        cls.d.service('uiautomator').start()

    @classmethod
    def push_jar(cls):
        print(os.path.join(maxin_path, 'monkey.jar'))
        cls.d.push(os.path.join(maxin_path, 'monkey.jar'), '/sdcard/monkey.jar')
        cls.d.push(os.path.join(maxin_path, 'framework.jar'), '/sdcard/framework.jar')
        log.i('push jar file--->monkey.jar framework.jar')

    @classmethod
    def push_white_list(cls):
        cls.d.push(os.path.join(maxin_path, 'awl.strings'), '/sdcard/awl.strings')
        log.i('push white_list file---> awl.strings ')

    @classmethod
    def push_actions(cls):
        cls.d.push(os.path.join(maxin_path, 'max.xpath.actions'), '/sdcard/max.xpath.actions')
        log.i('push actions file---> max.xpath.actions ')

    @classmethod
    def push_selector(cls):
        cls.d.push(os.path.join(maxin_path, 'max.xpath.selector'), '/sdcard/max.xpath.selector')
        log.i('push selector file---> max.xpath.selector ')

    @classmethod
    def push_widget_black(cls):
        cls.d.push(os.path.join(maxin_path,'max.widget.black'), '/sdcard/max.widget.black')
        log.i('push widget_black file---> max.widget.black ')

    @classmethod
    def push_string(cls):
        cls.d.push(os.path.join(maxin_path, 'max.strings'), '/sdcard/max.strings')
        log.i('push string file---> max.strings ')

    @classmethod
    def clear_env(cls):
        log.i('Clearing monkey env')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        cls.d.shell('rm -r /sdcard/max.widget.black')
        cls.d.shell('rm -r /sdcard/max.xpath.selector')
        cls.d.shell('rm -r /sdcard/max.xpath.actions')
        cls.d.shell('rm -r /sdcard/awl.strings')
        cls.d.shell('rm -r /sdcard/monkey.jar')
        cls.d.shell('rm -r /sdcard/framework.jar')
        cls.d.shell('rm -r /sdcard/max.strings')
        cls.d.shell('rm -r /sdcard/monkeyerr.txt')
        cls.d.shell('rm -r /sdcard/monkeyout.txt')
        log.i('Clear monkey env success')

    @classmethod
    def set_AdbIME(cls):
        log.i('setting AdbIME as default')
        ime = cls.d.shell('ime list -s').output
        if 'adbkeyboard' in ime:
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
        else:
            cls.local_install(os.path.join(maxin_path, 'ADBKeyBoard.apk'))
            cls.d.shell('ime enable com.android.adbkeyboard/.AdbIME')
            cls.d.shell('ime set com.android.adbkeyboard/.AdbIME')
            log.i('install adbkeyboard and set as default')
        cls.push_string()


if __name__ == '__main__':
    log.set_logger('udid', './log.log')
    maxim = Maxim()
    maxim.set_driver(None)
    command = maxim.command(package='com.quvideo.xiaoying', runtime=2, mode='uiautomatormix', throttle=100,
                            options=' -v -v ', whitelist=True, off_line=True)
    maxim.run_monkey(command)
