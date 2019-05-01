#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wda
from Public.atxserver2 import atxserver2

ios_devices = atxserver2('http://192.168.3.41:4000').present_ios_devices()
if ios_devices:
    wdaUrl = ios_devices[0]['source']['wdaUrl']

c = wda.Client(wdaUrl)
print(c.status())
print(c.healthcheck())

with c.session('com.netease.cloudmusic') as d:
    d(label=u"每日推荐").click()
    d(label=u"返回").click()
    d(label=u"歌单").click()
    d(label=u"返回").click()
    d(label=u"排行榜").click()
    d(label=u"返回").click()
