import time

from functools import wraps
from Public.BasePage import BasePage
from Public.ReportPath import ReportPath
from Public.Log import Log
import os

flag = 'IMAGE:'
log = Log()


def _screenshot(name):
    date_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    screenshot = name + '-' + date_time + '.PNG'
    # path = ReportPath().get_path() + '/' + screenshot
    path = os.path.join(ReportPath().get_path(), screenshot)
    driver = BasePage().get_driver()
    driver.screenshot(path)
    return screenshot


def teststep(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s' % func.__qualname__)
            ret = func(*args, **kwargs)
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')
            raise AssertionError(e)

            # if flag in str(e):
            #     raise AssertionError(e)
            # else:
            #     raise AssertionError(flag + _screenshot(func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('\t<-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')
            raise Exception(e)

            # if flag in str(e):
            #     raise Exception(e)
            # else:
            #     raise Exception(flag + _screenshot(func.__qualname__))

    return wrapper


def teststeps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.i('--> %s' % func.__qualname__)
            ret = func(*args, **kwargs)
            log.d('  <-- %s, %s', func.__qualname__, 'Success')
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'AssertionError', 'Error')
            raise AssertionError(e)

            # if flag in str(e):
            #     raise AssertionError(e)
            # else:
            #     raise AssertionError(flag + _screenshot(func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('  <-- %s, %s, %s', func.__qualname__, 'Exception', 'Error')
            raise Exception(e)

            # if flag in str(e):
            #     raise Exception(e)
            # else:
            #     raise Exception(flag + _screenshot(func.__qualname__))

    return wrapper


def _wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            log.d('--> %s', func.__qualname__)
            ret = func(*args, **kwargs)
            log.d('<-- %s, %s\n', func.__qualname__, 'Success')
            return ret
        except AssertionError as e:
            log.e('AssertionError, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'AssertionError', 'Fail')

            if flag in str(e):
                raise AssertionError(e)
            else:
                raise AssertionError(flag + _screenshot(func.__qualname__))
        except Exception as e:
            log.e('Exception, %s', e)
            log.e('<-- %s, %s, %s\n', func.__qualname__, 'Exception', 'Error')

            if flag in str(e):
                raise Exception(e)
            else:
                raise Exception(flag + _screenshot(func.__qualname__))

    return wrapper


def testcase(func):
    return _wrapper(func)


def setup(func):
    return _wrapper(func)


def teardown(func):
    return _wrapper(func)


def setupclass(func):
    return _wrapper(func)


def teardownclass(func):
    return _wrapper(func)
