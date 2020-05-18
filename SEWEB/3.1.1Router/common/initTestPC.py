#! -*-conding:utf-8 -*-
#@Time: 2019/4/17 0017 18:48
#@swzhou
'''
清理chrome 进程，释放内存占用
'''


import os
import socket
import time
import unittest
from common.ReadConfig import getweb
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
batSameIP = getweb('batSameIP')

class initTestPC(unittest.TestCase):

    def setUp(self):
        print('initTestPC start')
        # pass

    def test_initTestPC(self):
        #清理进程
        os.system('taskkill /im chromedriver.exe /F')
        os.system('taskkill /im chrome.exe /F')

        os.system('taskkill /im geckodriver.exe /F')
        os.system('taskkill /im Firefox.exe /F')

        os.system('taskkill /im "tftpd32.exe" /F')
        os.system('taskkill /im "Thunder.exe" /F')

        #退回pcmac地址以及判断IP
        # 1、调用bat脚本 MAC地址修改回
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            pcaddr2 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr2, n)
            if '192.168.' not in str(pcaddr2):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            #  仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')

        #2、 将IP改回自动获取（设置dns为自动获取）
        os.system(('%s' % batpath + 'changeDhcpIp.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if '192.168.' not in str(pcaddr1):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址')
        #3、判断IP地址是否是1.39(bat中设置1网段的IP为1.39)
        if pcaddr1 == batSameIP:
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            n = 0
            while n < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, n)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    n += 1
                else:
                    print('IP地址已自动获取成功', n)
                    break
            else:
                raise Exception('未获取到地址2')

    def tearDown(self):
        print('initTestPC over')

if __name__=='__main__':
    unittest.main()