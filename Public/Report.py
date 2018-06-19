#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import time
import zipfile
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, )),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(path_list):
    '''以Pubilc/index.html 生成 自动化测试报告.html'''
    name = "./TestReport/自动化测试报告.html"
    urls = path_list
    context = {
        'urls': urls
    }
    with open(name, 'w', encoding="utf-8") as f:
        html = render_template('index.html', context)
        f.write(html)
        f.close()

def _get_report_info(run):
    '''获取每个设备报告的参数'''
    report = run.test_report_path + '/TestReport.html'
    result = {}
    with open(report, 'r', encoding='utf-8') as f:
        res_str = re.findall("测试结果(.+%)", f.read())
        if res_str:
            res = re.findall(r"\d+", res_str[0])
            result["sum"] = res[0]
            result["pass"] = res[1]
            result['fail'] = res[2]
            result['error'] = res[3]
            result['passrate'] = re.findall('通过率 = (.+%)', res_str[0])[0]
        else:
            raise Exception("The TestReport.html in %s has no string'测试结果',please check out!!!" % run.get_path())
        f.close()
    with open(report, 'r', encoding='utf-8') as f:
        result['duration'] = re.findall("合计耗时 : </strong> (.+)</p>", f.read())[0].split('.')[0]
        f.close()
    return result



def create_statistics_report(runs):
    '''根据运行设备的数量生成统计报告，路径为
    ./TestReport/自动化测试报告.html'''
    report_path_list = []
    for run in runs:
        tmp_dic = {}
        tmp_dic['urls'] = re.findall("./TestReport/(.+$)", run.get_path())[0] + "/TestReport.html"
        tmp_dic['name'] = run.get_device()['model'] + "自动化测试报告"
        tmp_dic.update(_get_report_info(run))
        report_path_list.append(tmp_dic)
    create_index_html(report_path_list)
    print('Generate statistics report completed........ ')


def backup_report():
    '''备份旧报告 TestReport文件夹'''
    if not os.path.exists("./TestReport_backup"):
        os.mkdir("./TestReport_backup")
    if not os.path.exists("./TestReport"):
        os.mkdir("./TestReport")
    date_time = time.strftime('%Y-%m-%d_%H_%M_%S', time.localtime(time.time()))
    try:
        os.rename('./TestReport', './TestReport_backup/Backup_' + date_time)
    except PermissionError as e:
        raise e
    print('Backup TestReport dir success')


def zip_report():
    '''压缩TestReport文件夹'''
    name = 'TAX-Report ' + time.strftime("%Y-%m-%d %H.%M.%S", time.localtime())
    startdir = "./TestReport"  # 要压缩的文件夹路径
    file_news = './' + name + '.zip'  # 压缩后文件夹的名字
    z = zipfile.ZipFile(file_news, 'w', zipfile.ZIP_DEFLATED)  # 参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir, '')
        fpath = fpath and fpath + os.sep or ''
        for filename in filenames:
            z.write(os.path.join(dirpath, filename), fpath + filename)
            # z.write(os.path.join(dirpath, filename))
    z.close()
    print('Generate zip_report file %s completed........ ' % file_news)
