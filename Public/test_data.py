#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
需要安装第三方库
BeautifulSoup 解析Url获取apk下载链接地址
pip install beautifulsoup4

apkutils
A library that gets infos from APK.
https://github.com/mikusjelly/apkutils
pip install apkutils

"""
import os
import json
# from Public.readconfig import ReadConfig
from Public.filetools import *
import wget
import shutil
import subprocess
import zipfile
from Public import config
import requests
from bs4 import BeautifulSoup
import re
import apkutils
import json
from logzero import logger
from Public.log import Log
log = Log()


#
# def generate_test_data(devices):
#     dict_tmp = {}
#     for d in devices:
#         dict_tmp[d['serial']] = {}
#         dict_tmp[d['serial']]['user_name'] = ReadConfig().get_testdata('user_name')[devices.index(d)]
#         dict_tmp[d['serial']]['password'] = ReadConfig().get_testdata('password')[devices.index(d)]
#     with open(data_path, "w") as f:
#         json.dump(dict_tmp, f, ensure_ascii=False)
#         f.close()
#     logger.info("Test data data.json generated success")
#
#
# def get_test_data(d):
#     with open(data_path, 'r', encoding='UTF-8') as f:
#         data = json.load(f)
#     return data[d.device_info['serial']]


def get_apk(url,d_path=None):
    '''
    :param url: url地址或者本地路径
    :param keyword: url qa地址匹配的关键字
    :return: 返回apk的参数url apk_name apk_path
    '''
    # if d_path:
    #     folder = os.path.join(d_path, 'apk')
    # else:
    #     folder = os.path.join(os.getcwd(), 'apk')
    folder = os.path.join(d_path, 'apk')
    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        pass
    if re.match(r"^https?://", url):
        if url.split('.')[-1] in ['apk', 'aab']:
            apk = {'url': url,
                   'apk_name': url.split('/')[-1].replace(':', '_'),
                   'apk_path': os.path.join(folder, url.split('/')[-1].replace(':', '_'))
                   }
        else:
            raise Exception('not a bundle download url')
        return apk
    elif os.path.exists(url):
        try:
            shutil.copy(url, os.path.join(folder, os.path.basename(url)))
        except shutil.SameFileError:
            pass
        apk = {'url': url,
               'apk_name': os.path.basename(url),
               'apk_path': os.path.join(folder, os.path.basename(url))}
        return apk
    else:
        raise Exception('apk链接或文件路径错误，请重试')


def _download(apk):
    logger.info('开始下载  %s ,请稍后......' % apk['apk_name'])
    file = wget.download(apk['url'], apk['apk_path'])
    if os.path.exists(apk['apk_path']):
        shutil.move(file, apk['apk_path'])
    logger.info('下载路径：%s' % apk['apk_path'])


def download_apk(apk, overwrite=False):
    if os.path.exists(apk['apk_path']):
        if overwrite:
            _download(apk)
            return apk['apk_path']
        else:
            logger.info('%s 已存在' % apk['apk_name'])
            return apk['apk_path']
    else:
        _download(apk)
        return apk['apk_path']


def build_apks(bunlde_path=None, ks_path=None):
    tmp_apks_path = os.path.join(os.path.dirname(bunlde_path), 'tmp.apks')
    try:
        logger.info('begin build_apks ')
        output = subprocess.check_output(
            config.build_apks_code(bunlde_path, ks_path, tmp_apks_path)).decode('utf-8')
        logger.info(output)
        if os.path.exists(tmp_apks_path):
            logger.info('apks_path:%s' % tmp_apks_path)
            return tmp_apks_path
        else:
            logger.error('没有找到build apks的文件')
            return None
    except Exception as e:
        logger.error(e)
        logger.error('创建apks异常请重试')


def trans_aab2apk(aab_path, ks_path=None):
    local_path = os.path.dirname(aab_path)
    apk_path = os.path.splitext(aab_path)[0] + '.apk'
    tmp_apks = build_apks(bunlde_path=aab_path, ks_path=ks_path)
    logger.info('从apks 解压apk')
    apks = zipfile.ZipFile(tmp_apks, 'r')
    for f in apks.namelist():
        if 'universal.apk' in f:
            apks.extract(f, local_path)
            _apk_path = os.path.join(local_path, f)
            shutil.move(_apk_path, apk_path)
            os.remove(tmp_apks)
            os.remove(aab_path)
            return apk_path
    else:
        os.remove(tmp_apks)
        logger.error('apks %s 没有找到universal.apk' % apk_path)
        return None


def get_apk_info(bundle_path):
    if os.path.splitext(os.path.basename(bundle_path))[-1][1:] == 'aab':
        path = trans_aab2apk(bundle_path, config.ks_path)
    else:
        path = bundle_path

    tmp = apkutils.APK(path).get_manifest()
    info = {'package': str(tmp.get('@package')),
            'versionCode': str(tmp.get('@android:versionCode')),
            'versionName': str(tmp.get('@android:versionName')),
            }
    return info


def write_config(config_path, info):
    '''修改配置文件'''
    del_files(config_path)
    write_file(config_path, json.dumps(info, indent=4), is_cover=True)


def get_apk_activity(path):
    tmp = apkutils.APK(path).get_manifest()
    data = tmp['application']['activity']
    activity_list = []
    for activity in data:
        activity_list.append(activity['@android:name'])
    return activity_list


def prepare_apk(url, folder):
    '''
    装备被测app 并获取信息  aab会被转换成apk
    :param url: 本地apk或aab的绝对路径  或者 安装包的下载链接  或者 公司android对应项目的测试包下载网页
    :param keyword: 公司android对应项目的测试包下载网页需要指定获取包的关键字
    :param folder: 被测试app项目的根目录 apk下载 报告生成依赖这个路径
    :return:
    '''
    apk = get_apk(url, folder)
    download_apk(apk)
    if apk['apk_path'].split('.')[-1] == 'aab':

        ks = config.ks_path
        path = trans_aab2apk(apk['apk_path'], ks_path=ks)
    elif apk['apk_path'].split('.')[-1] == 'apk':
        path = apk['apk_path']
    else:
        raise Exception('file not apk or aab ,please retry')

    info = get_apk_info(path)
    info.update(apk)
    info['apk_path'] = path
    info['folder'] = folder
    write_config(os.path.join(folder, 'app_info.json'),info)
    return info


if __name__ == '__main__':
    info = get_apk_info('/Users/linpengcheng/Desktop/GitHub/Viva_Android_UITest/VivaCut/TestSuite_01_Install/apk/VivaCut-00WebDownload.apk')
    print(info)