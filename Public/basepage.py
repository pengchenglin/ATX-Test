import os
import time
import uiautomator2 as u2
from uiautomator2 import UiObjectNotFoundError
import re
from Public.reportpath import ReportPath
from Public.test_data import get_apk_info
from Public.config import internalapp,unlock_apk
# from Public.chromedriver import ChromeDriver
# from Public.ports import Ports

from Public.log import Log
log = Log()


class BasePage(object):
    @classmethod
    def set_driver(cls, dri):
        cls.d = u2.connect(dri)
        # cls.d.debug = True
        # cls.d.implicitly_wait(10.0)

    def get_driver(self):
        return self.d

    @classmethod
    def local_install(cls, apk_path, clear=False, uninstall=True):
        '''
        安装本地apk 覆盖安装，不需要usb链接
        :param apk_path: apk文件本地路径
        '''
        packagename = get_apk_info(apk_path)['package']
        log.i('apk info ----> %s' % get_apk_info(apk_path))

        if clear:
            log.i("Clear Device %s folder" % packagename)
            if packagename in internalapp:
                for f in internalapp[packagename]['app_folder']:
                    log.i('remove folder :%s' % f)
                    cls.d.shell('rm -rf %s' % f)   # 删除app的本地所在文件夹
            else:
                log.i('internalapp%s的配置信息' % packagename)
        else:
            pass
        if uninstall:
            cls.d.app_uninstall(packagename)
        else:
            pass
        file_name = os.path.basename(apk_path)
        dst = '/data/local/tmp/' + file_name
        log.i('pushing %s to device' % file_name)
        cls.d.push(apk_path, dst,show_progress=True)
        log.i('start install %s' % dst)
        if cls.d.device_info['brand'] == 'vivo':
            '''Vivo 手机通过打开文件管理 安装app'''
            with cls.d.session("com.android.filemanager") as s:
                s(resourceId="com.android.filemanager:id/allfiles").click()
                s(resourceId="com.android.filemanager:id/file_listView").scroll.to(textContains=file_name)
                s(textContains=file_name).click()
                s(resourceId="com.android.packageinstaller:id/continue_button").click()
                s(resourceId="com.android.packageinstaller:id/ok_button").click()
                log.i(s(resourceId="com.android.packageinstaller:id/checked_result").get_text())

        elif cls.d.device_info['brand'] == 'OPPO':
            with cls.d.session("com.coloros.filemanager") as s:
                s(resourceId="com.coloros.filemanager:id/action_file_browser").click()
                s(className="android.app.ActionBar$Tab", instance=1).click()
                s(resourceId="com.coloros.filemanager:id/viewPager").scroll.to(textContains=file_name)
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
                          ).click(offset=(0.5, 0.2))
                    elif s(text=u"知道了").exists:
                        raise Exception('已经安装高版本，请卸载重装')
                btn_done.click()

        else:
            watcher = cls.watch_device('允许|继续安装|允许安装|始终允许|安装|重新安装|同意|确定')
            r = cls.d.shell(['pm', 'install', '-r', dst], stream=True)
            id = r.text.strip()
            print(time.strftime('%H:%M:%S'), id)
            cls.unwatch_device(watcher)

        packages = list(map(lambda p: p.split(':')[1], cls.d.shell('pm list packages').output.splitlines()))
        if packagename in packages:
            cls.d.shell(['rm', dst])
        else:
            raise Exception('%s 安装失败' % apk_path)

    @classmethod
    def unlock_device(cls):
        '''unlock.apk install and launch,
        Android 10 上面无效  需要允许这个app的权限才行，可以提前先安装后 手动获取权限
        '''
        pkgs = re.findall('package:([^\s]+)', cls.d.shell(['pm', 'list', 'packages', '-3'])[0])
        if 'io.appium.unlock' in pkgs:
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')
        else:
            #  appium unlock.apk 下载安装
            log.i('installing io.appium.unlock')
            cls.local_install(unlock_apk, clear=False,uninstall=False)
            cls.d.app_start('io.appium.unlock')
            cls.d.shell('input keyevent 3')


    @classmethod
    def back(cls):
        '''点击返回
        页面没有加载完的时候，会出现返回失败的情况，使用前确认页面加载完成'''
        log.i('press back btn')
        time.sleep(1)
        cls.d.press('back')
        time.sleep(1)

    @classmethod
    def identify(cls):
        cls.d.open_identify()

    # def set_chromedriver(self, device_ip=None, package=None, activity=None, process=None):
    #     driver = ChromeDriver(self.d, Ports().get_ports(1)[0]). \
    #         driver(device_ip=device_ip, package=package, attach=True, activity=activity, process=process)
    #     return driver

    @classmethod
    def watch_device(cls, keyword):
        '''
        如果存在元素则自动点击
        :param keyword: exp: keyword="yes|允许|好的|跳过"
        '''
        # for i in keyword.split("|"):
        #     cls.d.watcher.when(i).click()
        # cls.d.watcher.start()
        # time.sleep(2)

        ctx = cls.d.watch_context(autostart=False)
        for i in keyword.split("|"):
            ctx.when("%s" % i).click()
        ctx.start()
        return ctx

    @classmethod
    def unwatch_device(cls, ctx=None):
        '''关闭watcher '''
        # cls.d.watcher.reset()
        # cls.d.watcher.stop()
        # time.sleep(2)
        ctx.stop()


    @classmethod
    def get_toast_message(cls):
        message = cls.d.toast.get_message(3, 3)
        cls.d.toast.reset()
        return message

    @classmethod
    def set_fastinput_ime(cls):
        log.i('set fastinput ime')
        cls.d.set_fastinput_ime(True)

    @classmethod
    def set_original_ime(cls):
        log.i('set original ime')
        cls.d.set_fastinput_ime(False)

    @classmethod
    def screenshot(cls,text='Manual_'):
        '''截图并打印特定格式的输出，保证用例显示截图'''
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screenshot_name = text + date_time + '.PNG'     # HTMLTestReport
        # screenshot_name = 'screenshot_' + cls.__qualname__ + '-' + date_time + '.png'     # ExtentHTMLRunner
        path = os.path.join(ReportPath().get_path(), screenshot_name)
        cls.d.screenshot(path)
        log.i('IMAGE:' + screenshot_name)   # HTMLTestReport
        # print(screenshot_name)       # ExtentHTMLRunner


    @classmethod
    def startscreenrecord(cls):
        '''开始录屏'''
        date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        screenrecord_name = date_time + '.mp4'  # HTMLTestReport
        # screenshot_name = 'screenshot_' + cls.__qualname__ + '-' + date_time + '.png'     # ExtentHTMLRunner
        path = os.path.join(ReportPath().get_path(), screenrecord_name)
        cls.d.screenrecord(path)
        log.i('IMAGE:' + screenrecord_name)  # HTMLTestReport


    @classmethod
    def stopscreenrecord(cls):
        '''结束录屏'''
        time.sleep(0.5)
        cls.d.screenrecord.stop()


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
    def _get_element_size(element,per=50):
        '''获取滑动对应坐标'''
        # rect = element.info['visibleBounds']
        rect = element.info['bounds']
        # print(rect)
        x_center = (rect['left'] + rect['right']) / 2
        y_center = (rect['bottom'] + rect['top']) / 2
        x_d = (rect['right']-rect['left'])*(0.5-per/200)  # x轴缩短距离
        y_d = (rect['bottom']-rect['top'])*(0.5-per/200)  # y轴缩短距离
        x_left = rect['left']+x_d
        y_up = rect['top']+y_d
        x_right = rect['right']-x_d
        y_down = rect['bottom']-y_d

        return x_left, y_up, x_center, y_center, x_right, y_down

    def _swipe(self, fromX, fromY, toX, toY, steps):
        self.d.swipe(fromX, fromY, toX, toY, duration=1,steps=steps)

    def swipe_up(self, element=None, steps=40, per=50):
        """
        swipe up
        :param per:滑动距离占元素总长的百分占比
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        log.i('swipe up')
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element, per)
            fromX = x_center
            fromY = y_down
            toX = x_center
            toY = y_up
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = (0.5+per/200) * y
            toX = 0.5 * x
            toY = (0.5-per/200) * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_down(self, element=None, steps=40, per=50):
        """
        swipe down
        :param per:滑动距离占元素总长的百分占比
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        log.i('swipe_down')
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element,per)

            fromX = x_center
            fromY = y_up
            toX = x_center
            toY = y_down
        else:
            x, y = self._get_window_size()
            fromX = 0.5 * x
            fromY = (0.5-per/200) * y
            toX = 0.5 * x
            toY = (0.5+per/200) * y

        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_left(self, element=None, steps=40,per=50):
        """
        swipe left
        :param per:滑动距离占元素总长的百分占比
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        log.i('swipe left')
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element,per)
            fromX = x_right
            fromY = y_center
            toX = x_left
            toY = y_center
        else:
            x, y = self._get_window_size()
            fromX = (0.5+per/200) * x
            fromY = 0.5 * y
            toX = (0.5-per/200) * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def swipe_right(self, element=None, steps=40, per=50):
        """
        swipe right
        :param per:滑动距离占元素总长的百分占比
        :param element: UI element, if None while swipe window of phone
        :param steps: steps of swipe for Android, The lower the faster
        :return: None
        """
        if element:
            x_left, y_up, x_center, y_center, x_right, y_down = self._get_element_size(element,per)
            fromX = x_left
            fromY = y_center
            toX = x_right
            toY = y_center
        else:
            log.i('swipe right')
            x, y = self._get_window_size()
            fromX = (0.5-per/200) * x
            fromY = 0.5 * y
            toX = (0.5+per/200) * x
            toY = 0.5 * y
        self._swipe(fromX, fromY, toX, toY, steps)

    def _find_element_by_swipe(self, direction, value, element=None, steps=40, max_swipe=6):
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
                time.sleep(0.05)
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

    def find_element_by_swipe_up(self, value, element=None, steps=40, max_swipe=40):
        return self._find_element_by_swipe('up', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_down(self, value, element=None, steps=40, max_swipe=40):
        return self._find_element_by_swipe('down', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_left(self, value, element=None, steps=40, max_swipe=40):
        return self._find_element_by_swipe('left', value,
                                           element=element, steps=steps, max_swipe=max_swipe)

    def find_element_by_swipe_right(self, value, element=None, steps=40, max_swipe=40):
        return self._find_element_by_swipe('right', value,
                                           element=element, steps=steps, max_swipe=max_swipe)



if __name__ == '__main__':
    d =BasePage()
    d.set_driver('')
    Log().set_logger('udid', './log.log')
    # d.unlock_device()
    # d.find_element_by_swipe_up(d.d(textContains='镜头数'))
    # time.sleep(3)
    # d.d(text='工程镜头数').click()
    # d.swipe_down(steps=100,per=50)
    # time.sleep(2)
    # d.swipe_left(steps=100,per=50)
    # time.sleep(2)
    # d.swipe_right(steps=100,per=50)
    # time.sleep(2)
    # d.swipe_up(steps=100,per=50)
    # time.sleep(2)
