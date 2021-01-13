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

from Public.config import SERVER, token

url = SERVER
token = token

if url and re.match(r"(http://)?(\d+\.\d+\.\d+\.\d+:\d+)", url):
    if '://' not in url:
        url = 'http://' + url
    else:
        url = url

logger = logging.getLogger(__name__)
TinyDB.DEFAULT_STORAGE = MemoryStorage


class atxserver2(object):
    """
    According to users requirements to select devices
    """

    def __init__(self):
        """
        Construct method
        """
        self._db = TinyDB(storage=MemoryStorage)
        self.load()

    def load(self, **kwargs):
        """
        Use the data which got from stf platform to crate query db

        :return: the len of records in the db's table
        """
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        res = requests.get(url + '/api/v1/devices', **kwargs).json()
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
        self._db.purge_tables()

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
            return [requests.get(url + '/api/v1/user/devices/' + device['udid'], **kwargs).json()['device'] for
                    device in devices]
        else:
            return []

    def present_android_devices(self, udid=None, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        self.refresh()
        self.find(where('platform') == 'android').devices()
        if udid:
            self.find(where('udid') == udid).devices()
        devices = self.find(where('present') == True).devices()
        if len(devices) > 0:
            return [requests.get(url + '/api/v1/user/devices/' + device['udid'], **kwargs).json()['device'] for
                    device in devices]
        else:
            return []

    def present_udid_devices(self, udids, **kwargs):
        '''

        :param kwargs:
        :param udids:
        :return:
        '''
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        present_udid_devices_list = []
        for udid in udids.split('|'):
            self.refresh()
            self.find(where('udid') == udid).devices()
            device = self.find(where('present') == True).devices()
            if device:
                present_udid_devices_list.append(
                    requests.get(url + '/api/v1/user/devices/' + udid, **kwargs).json()['device'])
            else:
                pass
        if len(present_udid_devices_list) > 0:
            return present_udid_devices_list
        else:
            return []

    def using_device(self, udid, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        # kwargs['json'] = {"udid": udid}
        ret = requests.post(url + '/api/v1/user/devices', json={"udid": udid, "idleTimeout": 10800}, **kwargs)
        if ret.status_code == 200:
            print(ret.json())
            return True
        else:
            return False

    def using_device_info(self, udid, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        # kwargs['json'] = {"udid": udid}
        ret = requests.get(url + '/api/v1/user/devices' + udid, **kwargs)
        if ret.status_code == 200:
            print(ret.json())
            return ret.json()
        else:
            return None

    def release_device(self, udid, **kwargs):
        kwargs['headers'] = {"Authorization": "Bearer " + token}
        ret = requests.delete(url + '/api/v1/user/devices/' + udid, **kwargs)
        if ret.status_code == 200:
            print(ret.json())
            return True
        else:
            return False
