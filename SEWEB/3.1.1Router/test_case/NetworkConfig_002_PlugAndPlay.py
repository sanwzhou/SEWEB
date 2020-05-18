#! -*-conding:utf-8 -*-
#@Time: 2019/1/10 0010 18:06
#@swzhou
'''
即插即用：开启错误IP可以上网，关闭 错误IP不能上网
'''


import os
import time
import unittest
import os.path
import socket
import subprocess
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,gettelnet
from common.loginRoute import login
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
logger = LogGen(Logger = 'NetworkConfig_002_PlugAndPlay').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
host = gettelnet('host')

class plug_and_play(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        plug = NetworkConfig_LANpage(self.driver, self.url)
        # 打开网络配置 - 内网配置
        plug.click_NetworkConfig()
        time.sleep(0.5)
        plug.click_LANconfig()
        time.sleep(1)
        plug.click_globalconfig()
        time.sleep(1)
        # pass

    def test_001_open(self):
        u'''开启即插即用 错误的IP，依旧上网'''
        plug = NetworkConfig_LANpage(self.driver, self.url)
        saveSucess = getAssertText('saveSucess')
        #开启UPNP
        plug.click_upnpEN()
        time.sleep(0.5)
        plug.click_save()
        time.sleep(1)

        # 断言 开启提示信息是否有误
        tips = str(plug.getText_byClass(plug.tips))
        time.sleep(1)
        self.assertEqual(tips, saveSucess, msg='即插即用 开启出错')
        print('即插即用 已开启')

        # 判断联网 ，不能上网则报错
        pingTestIP('www.163.com')  # 避免失误
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('connect failed.')

        # 调用bat脚本 地址修改为 192.168.189.39 网关192.168.189.1
        os.system('%s' % (batpath + 'changeStaticIP.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr, n)
            if str(pcaddr) != '192.168.198.39':
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为地址 192.168.198.39', n)
                break
        else:
            raise Exception('地址修改为192.168.198.39 失败')

        # 判断联网 ，不能上网则报错
        pingTestIP('www.163.com')  # 避免失误
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('connect failed.')

        self.driver.quit()
        logger.info('test_001_open passed')

    def test_002_close(self):
        u'''关闭即插即用 错误的IP，无法上网'''
        plug = NetworkConfig_LANpage(self.driver, self.url)
        saveSucess = getAssertText('saveSucess')

        # 关闭UPNP
        plug.click_upnpClose()
        time.sleep(0.5)
        plug.click_save()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        tips = str(plug.getText_byClass(plug.tips))
        time.sleep(1)
        self.assertEqual(tips, saveSucess, msg='即插即用 开启出错')
        print('即插即用 已关闭')

        #判断联网 ,关闭即插即用后 错误IP用户应该不能上网
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        if pcaddr != '192.168.189.39':
            # 调用bat脚本 地址修改为 192.168.189.39 网关192.168.198.1
            os.system('%s' % (batpath + 'changeStaticIP.bat'))
            time.sleep(5)
            n = 0
            while n < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr, n)
                if str(pcaddr) != '192.168.198.39':
                    time.sleep(2)
                    n += 1
                else:
                    print('地址已修改为地址 192.168.198.39', n)
                    break
            else:
                raise Exception('地址修改为192.168.198.39 失败')
        time.sleep(3)
        pingTestIP('114.114.114.114') #避免失误
        pingTestIP() #避免失误

        p = pingTestIP('114.114.114.114')
        if p == 'Y':
            raise Exception('错误IP用户依旧可以上网')
        p = pingTestIP()
        if p == 'Y':
            raise Exception('错误IP用户依旧可以访问路由器')
        time.sleep(1)

        #将IP改回自动获取
        os.system('%s' % batpath + 'changeDhcpIp.bat')
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

        # 判断联网 ，不能上网则报错
        pingTestIP('www.163.com')  # 避免失误
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('connect failed.')

        self.driver.quit()
        logger.info('test_002_close passed')


    def tearDown(self):

        pingTestIP()
        p = pingTestIP()
        if p == 'N':
            # 将IP改回自动获取
            os.system('%s' % batpath + 'changeDhcpIp.bat')
            time.sleep(5)
            n = 0
            while n < 30:
                pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                # print(pcaddr1, n)
                if '192.168.' not in str(pcaddr1):
                    time.sleep(2)
                    n += 1
                else:
                    print('IP地址已自动获取成功', n)
                    break
            else:
                raise Exception('未获取到地址')


        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

