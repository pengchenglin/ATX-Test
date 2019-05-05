#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
多进程check_alive
Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量，不然python会挂掉
'''
from Public.ReadConfig import ReadConfig
from Public.atxserver2 import atxserver2
import uiautomator2 as u2
import subprocess
import re

from multiprocessing import Pool


def get_devices():
    '''get the devices from Pubilc/config.ini devices list
    return alive devices'''
    devices_ip = ReadConfig().get_devices_ip()
    print('Start check devices from config devices IP list: %s' % devices_ip)
    pool = Pool(processes=len(devices_ip))
    tmp_list = []
    for run in devices_ip:
        tmp_list.append(pool.apply_async(check_alive, args=(run,)))
    pool.close()
    pool.join()
    devices_list = []
    for i in tmp_list:
        if i.get():
            devices_list.append(i.get())
    return devices_list


def get_online_devices(devices):
    '''get the devices from ATX-Server
    return alive devices'''
    print('Start check %s  devices on ATX-Server' % len(devices))
    if devices:
        pool = Pool(processes=len(devices))
        tmp_list = []
        for run in devices:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    else:
        raise Exception('ATX-Server has no online device!!! ')


def atxserver2_online_devices(devices):
    '''
    get present_android_devices from atxserver2
    :return:
    '''
    print('Start check %s  present android devices on atxserver2' % len(devices))
    if devices:
        pool = Pool(processes=len(devices))
        tmp_list = []
        for run in devices:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    else:
        raise Exception('atxserver2 has no online device!!! ')


def connect_devices():
    '''get the devices USB connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('Start check %s devices connected on PC: ' % len(valid_serials))
        pool = Pool(processes=len(valid_serials))
        tmp_list = []
        for run in valid_serials:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    if len(valid_serials) == 0:
        print("No available android devices detected.")
        return []


def check_alive(device):
    if isinstance(device, dict):
        if 'ip' in device:  # atx-server
            d = u2.connect(device['ip'])
            if d.agent_alive:
                d.healthcheck()
                if d.alive:
                    print('%s is alive' % device['udid'])
                    print('atxagentUrl: %s:7912' % device['ip'])
                    dict_tmp = d.device_info
                    dict_tmp['ip'] = device['ip']
                    return dict_tmp
                else:
                    print('%s is not alive' % device['udid'])
                    return None
            else:
                print('The device  %s atx_agent is not alive,please checkout!' % device['udid'])
                return None
        else:  # atxserver2
            d = u2.connect(device['source']['atxAgentAddress'])
            if d.agent_alive:
                d.healthcheck()
                if d.alive:
                    print('%s is alive' % device['udid'])
                    print('atxagentUrl: %s' % device['source']['atxAgentAddress'])
                    dict_tmp = d.device_info
                    dict_tmp['ip'] = device['source']['atxAgentAddress']
                    atxserver2(ReadConfig().get_server_url()).using_device(device['udid'])
                    return dict_tmp
                else:
                    print('%s is not alive' % device['udid'])
                    return None
            else:
                print('The device  %s atx_agent is not alive,please checkout!' % device['udid'])
                return None

    else:
        d = u2.connect(device)
        if d.agent_alive:
            d.healthcheck()
            if d.alive:
                if re.match(r"(\d+\.\d+\.\d+\.\d)", device):  # config ip
                    dict_tmp = d.device_info
                    dict_tmp['ip'] = device
                    print('%s is alive' % device)
                    print('atxagentUrl: %s:7912' % device)
                else:  # usb devices
                    dict_tmp = d.device_info
                return dict_tmp
            else:
                print('%s is not alive' % device)
                return None
        else:
            print('The device atx_agent %s  is not alive,please checkout!' % device)
            return None


# if __name__ == '__main__':
    # devices_ip = get_devices()

    # devices = connect_devices()
    # devices = get_online_devices()
    # print(devices_ip)
    #
    # pool = Pool(processes=len(devices_ip))
    # tmp_list = []
    # for run in devices_ip:
    #     tmp_list.append(pool.apply_async(check_alive, args=(run,)))
    #     # alive_list.append(tmp)
    # pool.close()
    # pool.join()
    # print('All runs done........ ')
    # print(tmp_list)
    # for i in tmp_list:
    #     print(i.get())
    # print(get_devices())
    # print(get_online_devices())
    # print(connect_devices())

