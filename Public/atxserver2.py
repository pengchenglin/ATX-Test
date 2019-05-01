#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

some fields we often use
===============================================
field	     e.g.
brand        google
version      6.0.1
sdk	         23
serial	     0642f8d6f0ec9d1a
model        Nexus 5
....         ...
===============================================
"""

import logging

from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage, JSONStorage
import requests
import re

logger = logging.getLogger(__name__)

TinyDB.DEFAULT_STORAGE = MemoryStorage

token = '57aca3bd69534b9bb386247bebef4f67'


class atxserver2(object):
    """
    According to users requirements to select devices
    """

    def __init__(self, url):
        """
        Construct method
        """
        self._db = TinyDB(storage=MemoryStorage)
        if url and re.match(r"(http://)?(\d+\.\d+\.\d+\.\d+:\d+)", url):
            if '://' not in url:
                url = 'http://' + url
            else:
                url = url
            self._url = url
            self.load()
        else:
            logger.error('Atx server addr error')
        self.load()

    def load(self, **kwargs):
        """
        Use the data which got from stf platform to crate query db

        :return: the len of records in the db's table
        """
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        res = requests.get(self._url + '/api/v1/devices', **kwargs).json()
        if res is not None:
            eids = self._db.insert_multiple(res['devices'])
            return len(eids)
        else:
            return 0

    def find(self, cond=None):
        """
        According condition to filter devices and return
        :param cond: condition to filter devices
        :type cond: where
        :return: stf_selector object and its db contains devices
        """
        if cond is not None:
            res = self._db.search(cond)
            self.purge()
            self._db.insert_multiple(res)
        return self

    def devices(self):
        """
        return all devices that meeting the requirement
        :return: list of devices
        """
        return self._db.all()

    def refresh(self):
        """
        reload the devices info from stf
        :return: the len of records in the db's table
        """
        self.purge()
        return self.load()

    def count(self):
        """
        count the records in the db's table
        :return: the len of records in the db's table
        """
        return len(self._db.all())

    def purge(self):
        """
        remove all the data from the db
        :return:
        """
        self._db.purge()

    def ready_devices(self):
        '''查找标记为ready的设备'''
        self.refresh()
        devices = self.find(where('ready') == True).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def online_devices(self):
        '''查找online 的设备'''
        self.refresh()
        devices = self.find(where('present') == True).devices()
        if len(devices) > 0:
            return devices
        else:
            return False

    def present_ios_devices(self, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        self.refresh()
        self.find(where('platform') == 'apple').devices()
        devices = self.find(where('present') == True).devices()
        if len(devices) > 0:
            return [requests.get(self._url + '/api/v1/user/devices/' + device['udid'], **kwargs).json()['device'] for
                    device in devices]
        else:
            return False

    def present_android_devices(self, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        self.refresh()
        self.find(where('platform') == 'android').devices()
        devices = self.find(where('present') == True).devices()
        if len(devices) > 0:
            return [requests.get(self._url + '/api/v1/user/devices/' + device['udid'], **kwargs).json()['device'] for
                    device in devices]
        else:
            return False

    # def model_devices(self, model):
    #     '''查找特定型号的设备'''
    #     self.refresh()
    #     devices = self.find(where('model') == model).devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False
    #
    # def brand_devices(self, brand):
    #     '''查找特定品牌的设备'''
    #     self.refresh()
    #
    #     devices = self.find(where('brand') == brand).devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False
    #
    # def sdk_devices(self, sdk):
    #     '''查找特定SDK的设备'''
    #     self.refresh()
    #     devices = self.find(where('sdk') == sdk).devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False
    #
    # def version_devices(self, version):
    #     '''查找特定SDK的设备'''
    #     self.refresh()
    #     devices = self.find(where('version') == version).devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False
    #
    # def serial_devices(self, serial):
    #     '''查找特定serial的设备'''
    #     self.refresh()
    #     devices = self.find(where('serial') == serial).devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False
    #
    # def all_devices(self):
    #     '''返回所有的设备'''
    #     self.refresh()
    #     devices = self.find().devices()
    #     if len(devices) > 0:
    #         return devices
    #     else:
    #         return False


if __name__ == '__main__':
    # atxserver2('http://192.168.3.41:4000').refresh()
    online_devices = atxserver2('http://192.168.3.41:4000').present_ios_devices()

    import json

    print(json.dumps(online_devices))
    # res = requests.get('http://192.168.3.41:4000/api/v1/user/devices/00008020-00180CEA26F8002E',headers={"Authorization": "Bearer " + '57aca3bd69534b9bb386247bebef4f67'})
    # print(res.text)
