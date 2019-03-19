import os
import time
import uiautomator2 as u2
from uiautomator2 import UiObjectNotFoundError
import re
from Public.chromedriver import ChromeDriver
from Public.Ports import Ports
from Public.ReportPath import ReportPath
from Public.Test_data import get_apk_info

import warnings


# u2.DEBUG = True

class BasePage(object):
    @classmethod
    def set_driver(cls, dri):
        cls.d = u2.connect(dri)

    def get_driver(self):
        return self.d

    # def current_app(self):
    #     """
    #     Return: dict(package, activity, pid?)
    #     """
    #     # try: adb shell dumpsys activity top
    #     _activityRE = re.compile(
    #         r'(?P<package>[^/]+)/(?P<activity>[^/\s]+) \w+ pid=(?P<pid>\d+)'
    #     )
    #     # m1=self.shell('dumpsys activity top | grep ACTIVITY')[0].split('ACTIVITY')[-1].strip()
    #     m = _activityRE.search(self.d.shell('dumpsys activity top | grep ACTIVITY')[0].split('ACTIVITY')[-1].strip())
    #     if m:
    #         return dict(
    #             package=m.group('package'),
    #             activity=m.group('activity'),
    #             pid=int(m.group('pid')))
    #
    #     # try: adb shell dumpsys window windows
    #     _focusedRE = re.compile(
    #         'mFocusedApp=.*ActivityRecord{\w+ \w+ (?P<package>.*)/(?P<activity>.*) .*'
    #     )
    #     m = _focusedRE.search(self.d.shell('dumpsys window windows | grep Focused')[0])
    #     if m:
    #         return dict(
    #             package=m.group('package'), activity=m.group('activity'))
    #     # empty result
    #     warnings.warn("Couldn't get focused app", stacklevel=2)
    #     return dict(package=None, activity=None)

    @classmethod
    def local_install(cls, apk_path):
        '''
        安装本地apk 覆盖安装，不需要usb链接
        :param apk_path: apk文件本地路径
        '''
        packagename = get_apk_info(apk_path)['package']

        file_name = os.path.basename(apk_path)
        dst = '/data/local/tmp/' + file_name
        print('start to install %s' % file_name)
        cls.d.push(apk_path, dst)
        print('start install %s' % dst)
        if cls.d.device_info['brand'] == 'vivo':
            '''Vivo 手机通过打开文件管理 安装app'''
            with cls.d.session("com.android.filemanager") as s:
                s(resourceId="disk_info_parent").click()
                s(resourceId="file_listView").scroll.to(textContains=file_name)
                s(textContains=file_name).click()
                s(resourceId="continue_button").click()
                s(resourceId="ok_button").click()
                print(s(resourceId="checked_result").get_text())

        elif cls.d.device_info['brand'] == 'OPPO':
            with cls.d.session("com.coloros.filemanager") as s:
                s(text=u"所有文件").click()
                s(className="android.widget.ListView").scroll.to(textContains=file_name)
                s(textContains=file_name).click()

                btn_done = cls.d(className="android.widget.Button", text=u"完成")
                while not btn_done.exists:
                    s(text="继续安装旧版本").click_exists()
                    s(text="重新安装").click_exists()
                    # 自动清除安装包和残留
                    if s(resourceId=
                         "com.android.packageinstaller:id/install_confirm_panel"
                         ).exists:
                        # 通过偏移点击<安装>
                        s(resourceId=
                          "com.android.packageinstaller:id/bottom_button_layout"
                          ).click(offset=(0.75, 0.5))
                btn_done.click()
        else:
            cls.watch_device('允许|继续安装|允许安装|始终允许|安装|重新安装')
            r = cls.d.shell(['pm', 'install', '-r', dst], stream=True)
            id = r.text.strip()
            print(time.strftime('%H:%M:%S'), id)
            cls.unwatch_device()
        packages = list(map(lambda p: p.split(':')[1], cls.d.shell('pm list packages').output.splitlines()))
        if packagename in packages:
            cls.d.shell(['rm', dst])
        else:
            raise Exception('%s 安装失败' % apk_path)

    @classmethod
    def unlock_device(cls):
        '''unlock.apk install and launch'''
        pkgs = re.findall('package:([^\s]+)', cls.d.shell(['pm', 'list', 'packages', '-3'])[0])
        if 'io.appium.unlock' in pkgs:
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')
        else:
            #  appium unlock.apk 下载安装
            print('installing io.appium.unlock')
            cls.d.app_install('https://raw.githubusercontent.com/pengchenglin/ATX-GT/master/apk/unlock.apk')
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')

    @classmethod
    def back(cls):
        '''点击返回
        页面没有加载完的时候，会出现返回失败的情况，使用前确认页面加载完成'''
        time.sleep(1)
        cls.d.press('back')
        time.sleep(1)


    @classmethod
    def identify(cls):
        cls.d.open_identify()

    def set_chromedriver(self, device_ip=None, package=None, activity=None, process=None):
        driver = ChromeDriver(self.d, Ports().get_ports(1)[0]). \
            driver(device_ip=device_ip, package=package, attach=True, activity=activity, process=process)
        return driver

    @classmethod
    def watch_device(cls, keyword):
        '''
        如果存在元素则自动点击
        :param keyword: exp: keyword="yes|允许|好的|跳过"
        '''
        cls.d.watchers.watched = False
        for i in keyword.split("|"):
            cls.d.watcher(i).when(text=i).click(text=i)
        print('Starting watcher,parameter is %s' % keyword.split("|"))
        cls.d.watchers.watched = True
        time.sleep(2)

    @classmethod
    def unwatch_device(cls):
        '''关闭watcher '''
        print('Stop all watcher')
        cls.d.watchers.remove()
        cls.d.watchers.watched = False

    @classmethod
    def get_toast_message(cls):
        message = cls.d.toast.get_message(3, 3)
        cls.d.toast.reset()
        return message

    @classmethod
    def set_fastinput_ime(cls):
        cls.d.set_fastinput_ime(True)

    @classmethod
    def set_original_ime(cls):
        cls.d.set_fastinput_ime(False)

    @classmethod
    def screenshot(cls):
        '''截图并打印特定格式的输出，保证用例显示截图'''
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screenshot_name = 'Manual_' + date_time + '.PNG'
        path = os.path.join(ReportPath().get_path(), screenshot_name)
        cls.d.screenshot(path)
        print('IMAGE:' + screenshot_name)

    @staticmethod
    def find_message(elements, text):
        '''查找元素列表中是否存在 text'''
        count = elements.count
        while count > 0:
            count = count - 1
            message = elements[count].info['text']
            if text in message:
                return True
            elif count == 0:
                return False
        else:
            return False

    def _get_window_size(self):
        window = self.d.window_size()
        x = window[0]
        y = window[1]
        return x, y

    @staticmethod
    def _get_element_size(element):
        # rect = element.info['visibleBounds']
        rect = element.info['bounds']
        # print(rect)
        x_center = (rect['left'] + rect['right']) / 2
        y_center = (rect['bottom'] + rect['top']) / 2
        x_left = rect['left']
        y_up = rect['top']
        x_right = rect['right']
        y_down = rect['bottom']

        return x_left, y_up, x_center, y_center, x_right, y_down

    def _swipe(self, fromX, fromY, toX, toY, steps):
        self.d.swipe(fromX, fromY, toX, toY, steps)

    def swipe_up(self, element=None, steps=0.2):
        """
        swipe up
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_center
            toY = y_up
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.5 * x
            toY = 0.25 * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_down(self, element=None, steps=0.2):
        """
        swipe down
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)

            fromX = x_center
            fromY = y_center
            toX = x_center
            toY = y_down
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.5 * x
            toY = 0.75 * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_left(self, element=None, steps=0.2):
        """
        swipe left
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_left
            toY = y_center
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.25 * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_right(self, element=None, steps=0.2):
        """
        swipe right
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element)
            fromX = x_center
            fromY = y_center
            toX = x_right
            toY = y_center
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = 0.5 * y
            toX = 0.75 * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def _find_element_by_swipe(self, direction, value, element=None, steps=0.2, max_swipe=6):
        """
        :param direction: swip direction exp: right left up down
        :param value: The value of the UI element location strategy. exp: d(text='Logina')
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :param max_swipe: the max times of swipe
        :return: UI element
        """
        times = max_swipe
        for i in range(times):
            try:
                if value.exists:
                    return value
                else:
                    raise UiObjectNotFoundError
            except UiObjectNotFoundError:
                if direction == 'up':
                    self.swipe_up(element=element, steps=steps)
                elif direction == 'down':
                    self.swipe_down(element=element, steps=steps)
                elif direction == 'left':
                    self.swipe_left(element=element, steps=steps)
                elif direction == 'right':
                    self.swipe_right(element=element, steps=steps)
                if i == times - 1:
                    raise UiObjectNotFoundError

    def find_element_by_swipe_up(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('up', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_down(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('down', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_left(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('left', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_right(self, value, element=None, steps=0.2, max_swipe=6):
        return self._find_element_by_swipe('right', value,
                                           element=element, steps=steps, max_swipe=max_swipe)
