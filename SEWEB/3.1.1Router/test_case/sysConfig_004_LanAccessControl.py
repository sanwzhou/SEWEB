#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 13:49
#@swzhou
'''
系统配置-网管策略-内网访问控制,修改测试 全部用户、组织架构和IP段用户
'''


import time
import unittest
import os.path
import telnetlib
import socket
from selenium import webdriver
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getweb,gettelnet
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
logger = LogGen(Logger = 'sysConfig_004_LANAccessControl').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
batSameIP = getweb('batSameIP')
host = gettelnet('host')

class LanAccessControl(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        accesscontrol = ManagementPolicyPage(self.driver,self.url)
        #进入系统配置-网管策略-内网访问控制
        accesscontrol.click_sysConfig()
        time.sleep(0.5)
        accesscontrol.click_ManagementPolicy()
        time.sleep(1)
        accesscontrol.click_lanAccessControl()
        time.sleep(1)
        # pass

    def test_001_userall(self):
        u'''内网访问控制 - 全部用户'''
        # 适用用户 选择 全部用户
        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        accesscontrol.click_choosePeople()
        time.sleep(1)
        accesscontrol.click_userall()
        accesscontrol.click_saveW1()
        time.sleep(1)
        accesscontrol.click_innerAccessControlEn()
        accesscontrol.click_save()
        time.sleep(1)
        self.driver.quit()

        #验证是否可以登录
        login.loginWeb(self) #admin账号登录
        self.driver.quit()
        logger.info('test_001_userall passed')

    def test_002_usergroup(self):
        u'''内网访问控制 - 组织架构'''
        self.driver.quit()
        RouteUrl = getweb('RouteUrl')
        #增加组织架构用户
        organization_group.import_empty_template(self)
        organization_group.add_user(self)

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-内网访问控制
        accesscontrol.click_sysConfig()
        time.sleep(0.5)
        accesscontrol.click_ManagementPolicy()
        time.sleep(1)
        accesscontrol.click_lanAccessControl()
        time.sleep(1)
        accesscontrol.click_choosePeople()
        time.sleep(1)
        accesscontrol.click_usergroup()
        #组织架构,这里选择的是ROOT 所有
        time.sleep(1)
        accesscontrol.click_Root()
        #弹窗中的保存
        accesscontrol.click_saveW1()
        time.sleep(1)
        accesscontrol.click_innerAccessControlEn()
        accesscontrol.click_save()
        time.sleep(1)
        self.driver.quit()

        # 调用bat脚本 地址修改为非组织架构IP 192.168.1.39 网关192.168.1.1
        if '192.168.1.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_1duan.bat'))
        elif '192.168.16.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_16duan.bat'))
        else:
            raise Exception('lan口非 1网段、16网段')
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if str(pcaddr1) != batSameIP:
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为非绑定地址 192.168.1.39', n)
                break
        else:
            raise Exception('地址修改为非绑定地址 192.168.1.39失败')

        # 判断登录 切换IP后应该不能登录设备
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(RouteUrl)
        title=self.driver.title
        if 'Error: Forbidden' in title:
            print('非组织架构用户无法登录设备 验证通过')
        else:
            CapPic(self.driver)
            logger.info('非组织架构用户依旧可以登录设备')
            raise Exception('非组织架构用户依旧可以登录设备')
        self.driver.quit()

        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr, n)
            if '192.168.' not in str(pcaddr):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址')

        # 验证是否可以登录 并删除添加的组织架构
        #先关闭访问控制 否则删除组织架构后 无法登录
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-内网访问控制
        accesscontrol.click_sysConfig()
        time.sleep(0.5)
        accesscontrol.click_ManagementPolicy()
        time.sleep(1)
        accesscontrol.click_lanAccessControl()
        time.sleep(1)
        accesscontrol.click_innerAccessControlC()
        accesscontrol.click_save()
        time.sleep(1)
        self.driver.quit()
        #删除添加的组织架构
        organization_group.group_delete(self)
        print('访问控制 选择组织架构  验证通过')
        logger.info('test_002_usergroup passed')

    def test_003_userip(self):
        u'''内网访问控制 - IP地址'''
        RouteUrl = getweb('RouteUrl')
        # 使用用户 选择 IP地址
        #获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-内网访问控制
        accesscontrol.click_choosePeople()
        time.sleep(1)
        accesscontrol.click_userip()
        time.sleep(1)
        accesscontrol.input_starip(pcaddr)
        accesscontrol.input_endip(pcaddr)
        accesscontrol.click_saveW1()
        time.sleep(1)
        accesscontrol.click_innerAccessControlEn()
        accesscontrol.click_save()
        time.sleep(1)
        self.driver.quit()

        # 调用bat脚本 地址修改为非组织架构IP 192.168.1.39 网关192.168.1.1
        if '192.168.1.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_1duan.bat'))
        elif '192.168.16.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_16duan.bat'))
        else:
            raise Exception('lan口非 1网段、16网段')
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if str(pcaddr1) != batSameIP:
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为非绑定地址 192.168.1.39', n)
                break
        else:
            raise Exception('地址修改为非绑定地址 192.168.1.39失败')

        # 判断登录 切换IP后应该不能登录设备
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(RouteUrl)
        title = self.driver.title
        if 'Error: Forbidden' in title:
            print('非组织架构用户无法登录设备 验证通过')
        else:
            raise Exception('非组织架构用户依旧可以登录设备')
        self.driver.quit()

        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr, n)
            if '192.168.' not in str(pcaddr):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址')

        #验证是否可以登录
        login.loginWeb(self) #admin账号登录
        self.driver.quit()
        logger.info('test_003_userip passed')

    def tearDown(self):
        host = gettelnet('host')
        port = gettelnet('port')
        try:
            telnetlib.Telnet(host, port= port, timeout=10)
        except socket.timeout:
            # 将IP改回自动获取（设置dns为自动获取）
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
            time.sleep(5)
            n = 0
            while n < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr, n)
                if '192.168.' not in str(pcaddr):
                    time.sleep(2)
                    n += 1
                else:
                    print('IP地址已自动获取成功', n)
                    break
            else:
                raise Exception('未获取到地址')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-内网访问控制
        accesscontrol.click_sysConfig()
        time.sleep(0.5)
        accesscontrol.click_ManagementPolicy()
        time.sleep(1)
        accesscontrol.click_lanAccessControl()
        time.sleep(1)
        accesscontrol.click_innerAccessControlC()
        accesscontrol.click_save()
        time.sleep(1)
        self.driver.quit()
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
