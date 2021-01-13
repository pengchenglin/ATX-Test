import os

# 被测app下载链接
url = 'https://npmcdn.com/android-app-bootstrap@latest/android_app_bootstrap/build/outputs/apk/android_app_bootstrap-debug.apk'

project_path = os.path.dirname(os.path.abspath(__file__))
info_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_info.json')

# method获取设备的方式 SERVER,USB
#   SERVER：获取atx-server2上的设备
#   USB：获取本机链接的设备
# UDID：指定设备 如果多个 以'|'分隔  例如 '66J5T19227010959|5EF7N18105013559'
method = 'USB'
udid = ''



