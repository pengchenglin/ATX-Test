#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
多进程check_alive
Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量，不然python会挂掉
'''
from Public.ReadConfig import ReadConfig
from Public.ATX_Server import ATX_Server
import uiautomator2 as u2
import subprocess
import re

from multiprocessing import Pool


def get_devices():
    '''get the devices from Pubilc/config.ini devices list
    return alive devices'''
    devices_ip = ReadConfig().get_devices_ip()
    print('Connect devices from config devices IP list %s' % devices_ip)
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


def get_online_devices():
    '''get the devices from ATX-Server
    return alive devices'''
    devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
    print('There has %s online devices on ATX-Server' % len(devices))
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


def connect_devices():
    '''get the devices USB connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('There has %s devices connected on PC: ' % len(valid_serials))
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
        d = u2.connect(device['ip'])
        if d.agent_alive:
            d.healthcheck()
            if d.alive:
                print('%s is alive' % device['udid'])
                return d.device_info
            else:
                print('%s is not alive' % device['udid'])
                return None
        else:
            print('The device atx_agent %s  is not alive,please checkout!' % device['udid'])
            return None
    else:
        d = u2.connect(device)
        if d.agent_alive:
            d.healthcheck()
            if d.alive:
                print('%s is alive' % device)
                return d.device_info
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