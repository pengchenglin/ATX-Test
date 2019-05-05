#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from Public.ReadConfig import ReadConfig

proDir = os.path.split(os.path.realpath(__file__))[0]
data_path = os.path.join(proDir, "data.json")


def generate_test_data(devices):
    dict_tmp = {}
    for d in devices:
        dict_tmp[d['serial']] = {}
        dict_tmp[d['serial']]['user_name'] = ReadConfig().get_testdata('user_name')[devices.index(d)]
        dict_tmp[d['serial']]['password'] = ReadConfig().get_testdata('password')[devices.index(d)]
    with open(data_path, "w") as f:
        json.dump(dict_tmp, f, ensure_ascii=False)
        f.close()
    print("Test data data.json generated success")


def get_test_data(d):
    # with open(data_path, 'r', encoding='UTF-8') as f: #mac
    with open(data_path, 'r') as f:
        data = json.load(f)
    return data[d.device_info['serial']]


import apkutils

def get_apk_info(path):
    tmp = apkutils.APK(path).get_manifest()
    info = {}
    info['versionCode'] = str(tmp.get('@android:versionCode'))
    info['versionName'] = str(tmp.get('@android:versionName'))
    info['package'] = str(tmp.get('@package'))
    # # 获取appkey和channel
    # data =tmp['application']['meta-data']
    # for key in data:
    #     if key['@android:name'] == 'UMENG_CHANNEL':
    #         info['channel'] = str(key['@android:value'])
    #         continue
    #     elif key['@android:name'] == 'XiaoYing_AppKey':
    #         info['appkey'] = str(key['@android:value'])
    #         continue
    # if not 'channel' in info:
    #     info['channel'] = ''
    # if not 'appkey' in info:
    #     info['appkey'] = ''
    return info


def get_apk_activity(path):
    tmp = apkutils.APK(path).get_manifest()
    data = tmp['application']['activity']
    activity_list =[]
    for activity in data:
        activity_list.append(activity['@android:name'])
    return activity_list