import os
import platform


class Ports:
    @staticmethod
    def is_using(port):
        """判断端口号是否被占用"""

        if platform.system() == 'Windows':
            # Windows
            cmd = "netstat -an | findstr %s" % port
        else:
            # Mac OS
            cmd = "netstat -an | grep %s" % port

        if os.popen(cmd).readlines():
            return True
        else:
            return False

    def get_ports(self, count):
        """获得3456端口后一系列free port"""
        port = 3456
        port_list = []
        while True:
            if len(port_list) == count:
                break

            if not self.is_using(port) and (port not in port_list):
                port_list.append(port)
            else:
                port += 1

        return port_list
