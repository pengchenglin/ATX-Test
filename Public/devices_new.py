#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
多进程check_alive
Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量，不然python会挂掉
'''
from Public.atxserver2 import atxserver2
import uiautomator2 as u2
import adbutils
import re
from multiprocessing import Pool
from logzero import logger


def atxserver2_online_devices(devices):
    '''
    get present_devices from atxserver2
    :return:
    '''
    logger.info('Start check %s  present android devices on atxserver2' % len(devices))
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


def connect_devices(udids=None):
    '''get the devices USB connected on PC
    return alive devices'''
    # output = subprocess.check_output(['adb', 'devices'])
    # pattern = re.compile(
    #     r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    # matches = pattern.findall(output.decode())
    # serials = [m[0] for m in matches if m[1] == 'device']
    serials = [m.serial for m in adbutils.adb.device_list()]
    if not udids:
        valid_serials = serials
    else:
        valid_serials = [i for i in udids.split('|') if i in serials]
    if valid_serials:
        logger.info('There has %s devices connected on PC: ' % len(valid_serials))
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
        logger.error("No available android devices detected.")
        return []


def check_alive(device):
    if isinstance(device, dict): # atxserver2
        d = u2.connect(device['source']['atxAgentAddress'])
        # if d.agent_alive:
        #     d.healthcheck()
        #     if d.alive:
        #         logger.info('%s is alive' % device['udid'])
        #         logger.info('atxagentUrl: %s' % device['source']['atxAgentAddress'])
        #         dict_tmp = d.device_info
        #         dict_tmp['ip'] = device['source']['atxAgentAddress']
        #         atxserver2().using_device(device['udid'])
        #         return dict_tmp
        #     else:
        #         logger.error('%s is not alive' % device['udid'])
        #         return None
        # else:
        #     logger.error('The device atx_agent %s  is not alive,please checkout!' % device['udid'])
        #     return None
        if d.exists():
            logger.info('%s is alive' % device['udid'])
            logger.info('atxagentUrl: %s' % device['source']['atxAgentAddress'])
            dict_tmp = d.device_info
            dict_tmp['ip'] = device['source']['atxAgentAddress']
            atxserver2().using_device(device['udid'])
            return dict_tmp
        else:
            logger.error('%s is not alive' % device['udid'])
            return None

    else:  # USB
        d = u2.connect(device)
        # if d.agent_alive:
        #     d.healthcheck()
        #     if d.alive:
        #         if re.match(r"(\d+\.\d+\.\d+\.\d)", device):  # config ip
        #             dict_tmp = d.device_info
        #             dict_tmp['ip'] = device
        #             logger.info('%s is alive' % device)
        #         else:  # usb devices
        #             dict_tmp = d.device_info
        #         return dict_tmp
        #     else:
        #         logger.error('%s is not alive' % device)
        #         return None
        # else:
        #     logger.error('The device atx_agent %s  is not alive,please checkout!' % device)
        #     return None
        if d.exists():
            if re.match(r"(\d+\.\d+\.\d+\.\d)", device):  # config ip
                dict_tmp = d.device_info
                dict_tmp['ip'] = device
                logger.info('%s is alive' % device)
            else:  # usb devices
                dict_tmp = d.device_info
            return dict_tmp
        else:
            logger.error('%s is not alive' % device)
            return None


def check_devives(method='USB', udids=None):
    # 根据method 获取android设备
    if method == 'SERVER':
        if not udids:
            logger.info('Get available online devices from atxserver2...')
            devices = atxserver2_online_devices(atxserver2().present_android_devices())
            logger.info('\nThere has %s online devices in atxserver2' % len(devices))
        else:
            logger.info('Get available UDID devices %s from atxserver2...' % udids)
            devices = atxserver2_online_devices(atxserver2().present_udid_devices(udids))
            logger.info('\nThere has %s available udid devices in atxserver2' % len(devices))

    elif method == 'USB':
        if not udids:
            # get  devices connected PC with USB
            logger.info('Get available USB devices connected on PC... ')
            devices = connect_devices()
            logger.info('\nThere has %s  USB devices alive ' % len(devices))
        else:
            logger.info('Get available UDID devices %s connected on PC...' % udids)
            devices = connect_devices(udids)
            logger.info('\nThere has %s available udid connected on PC...' % len(devices))

    else:
        raise Exception('Config.ini method illegal:method =%s' % method)

    return devices

if __name__ == '__main__':

    #
    # d = u2.connect()
    # d.screenrecord('1.mp4')
    # time.sleep(3)
    # d.screenrecord.stop()
    #
    # # print(d.healthcheck)
    # # print(d.alive)
    # # print(d.agent_alive)
    # pprint(check_devives())
    # # d.app_start('com.videoeditorcn.android')
    print(connect_devices())