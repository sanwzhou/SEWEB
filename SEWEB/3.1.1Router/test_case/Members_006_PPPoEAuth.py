#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 10:31
#@swzhou
'''
PPPoE拨号认证
'''


from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import unittest
import os.path
import socket
import subprocess
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,gettelnet,getweb
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_002_userStatuspage import Organization_userStatusPage
from pages.Organization_004_userBlackpage import Organization_userBlackPage
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_006_pppoeAuth').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
host = gettelnet('host')
RouteUrl = getweb('RouteUrl')
baidutitle = getAssertText('baidutitle')

class Adsl():
    # connect 宽带拨号
    def connect(self,name='adsl',username='pppoeauth',password='pppoeauth'):
        cmd_str = "rasdial %s %s %s" % (name,username,password)
        os.system(cmd_str)
        time.sleep(5)

    # disconnect 宽带断开
    def disconnect(self,name='adsl'): #pc上宽带拨号的名称改为adsl，建议不用中文 编码会有问题
        cmd_str ="rasdial %s /disconnect"  %  name
        os.system(cmd_str)
        time.sleep(5)

class pppoeAuth(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_openPPPoEAuth_addAcc(self):
        u'''开启PPPoE认证 - 创建PPPoE账号'''

        # 005中设置了黑名单上网，这里增加一个判断联网
        nodata = getAssertText('nodata')
        # 判断联网 ，不能则改回mac
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            # 将mac改回
            # 调用bat脚本
            os.system('%s' % (batpath + 'changeMacToBack.bat'))
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
                # raise Exception('未获取到地址1')
                # 开启绑定情况下 仅更改mac 可能会获取不到地址
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
            # 删除黑名单绑定
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            blacklist = Organization_userBlackPage(self.driver, self.url)
            # 打开用户管理 - 组织成员
            blacklist.click_UserManage()
            time.sleep(0.5)
            blacklist.click_blacklist()
            time.sleep(1)
            blacklist.click_delete()
            time.sleep(1)
            blacklist.click_ok()
            time.sleep(1)
            # 断言 开启提示信息是否有误
            listtips = str(blacklist.getText_byXpath(blacklist.list_tips))
            time.sleep(1)
            self.assertEqual(listtips, nodata, msg='黑名单用户删除失败')
            print('黑名单用户已删除')
            self.driver.quit()

        organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空

        #调用新增组 “SelfComputerTest”
        organization_group.group_add(self)
        time.sleep(1)
        #开启PPPoE认证
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        pppoeauth = Organization_userAuthPage(self.driver,self.url)
        # 打开用户管理 - 用户认证
        pppoeauth.click_UserManage()
        time.sleep(0.5)
        pppoeauth.click_userAuth()
        time.sleep(1)
        #修改PPPoE服务器配置
        pppoeauth.click_PPPoEConfig()
        time.sleep(2)
        pppoeauth.input_pppoeStart('10.10.10.1')
        pppoeauth.input_pppoePriDns('114.114.114.114')
        pppoeauth.click_PppoeNoticeEn()
        pppoeauth.input_remainDays('50')#账号到期提前通告时间50天 配合账号将要过期的通告
        pppoeauth.click_save()
        time.sleep(2)
        #启用pppoe server
        pppoeauth.click_pppoeAuthEn()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        status = str(pppoeauth.getAttribute_byXpath(pppoeauth.pppoeAuthEns,'checked'))
        time.sleep(1)
        print(status)
        self.assertEqual(status, 'true', msg='PPPoE认证开启出错')
        print('PPPoE认证开启 验证成功')

        #配置一个不计费的PPPoE账号
        pppoeauth.click_account()
        time.sleep(1)
        pppoeauth.click_addUser()
        time.sleep(1)
        pppoeauth.input_name('pppoeauth')
        #仅有一个用户组，这里省略
        select=pppoeauth.selelement_byName(pppoeauth.authType)
        Select(select).select_by_value('PPPoE')
        time.sleep(1)
        pppoeauth.input_authAccount('pppoeauth')
        pppoeauth.input_authPassword('pppoeauth')
        pppoeauth.click_save()
        time.sleep(2)
        #断言 添加的账号 认证方式和认证账号 是否正常
        list_authtype=pppoeauth.getText_byXpath(pppoeauth.list_authtype)
        list_authAcc=pppoeauth.getText_byXpath(pppoeauth.list_authAcc)
        self.assertEqual(str(list_authtype), 'PPPoE', msg='认证方式显示不为“PPPoE”')
        self.assertEqual(str(list_authAcc), 'pppoeauth', msg='认证账号不为“pppoeauth”')

        self.driver.quit()
        logger.info('test_001_openPPPoEAuth_addAcc passed')

    def test_002_userstatus(self):
        u'''PPPoE拨号挂断&&查看拨号信息&&同网段通信'''


        #将有线地址改为不同网段的地址，以验证同网段通信
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

        # 开始拨号
        Adsl.connect(self)
        # 通过断言IP地址网段，判断是否可以拨号成功
        pcaddr_connectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        # print(pcaddr_connectAdsl)
        self.assertIn('10.10.10.', str(pcaddr_connectAdsl), msg='PPPoE拨号失败')
        # 打开网页测试，测试上网
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title1 = self.driver.title
        print(title1)
        self.assertEqual(title1, baidutitle, msg='网页打开异常')
        time.sleep(1)
        #打开路由器页面测试同网段访问
        self.driver.get(RouteUrl)
        time.sleep(2)
        url = self.driver.current_url
        print(url)
        self.assertIn('login.html', url, msg='无法访问路由器')
        self.driver.quit()

        #查看拨号信息显示
        # 打开用户管理 - 用户状态
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        #通过过滤IP地址验证是否显示拨号用户信息
        status.input_search(str(pcaddr_connectAdsl))
        status.click_searchb()
        list_IP1 = str(status.getText_byXpath(status.list_IP1))
        self.assertIsNotNone(list_IP1,msg='pppoe列表 未显示拨号用户信息')
        self.driver.quit()

        #拨号挂断，通过断言IP地址网段，判断是否挂断
        Adsl.disconnect(self)
        pcaddr_disconnectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        print(pcaddr_disconnectAdsl)
        self.assertIn('192.168.', str(pcaddr_disconnectAdsl), msg='PPPoE挂断失败')

        # 将IP改回自动获取
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
            raise Exception('未获取到地址')

        logger.info('test_002_userstatus passed')

    def test_003_AuthNotice(self):
        u'''账号到期通告'''
        messages = getAssertText('PPPoENotice')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        pppoeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        pppoeauth.click_UserManage()
        time.sleep(0.5)
        pppoeauth.click_userAuth()
        time.sleep(1)
        pppoeauth.click_account()
        time.sleep(1)
        # 新增已过期账号
        pppoeauth.click_addUser()
        time.sleep(1)
        pppoeauth.input_name('BeOverdue')
        selauthType = pppoeauth.selelement_byName('authType')
        Select(selauthType).select_by_value('PPPoE')
        time.sleep(1)
        pppoeauth.input_authAccount('BeOverdue')
        pppoeauth.input_authPassword('BeOverdue')
        pppoeauth.click_accountBillEn()
        time.sleep(1)
        #设置账号日期
        pppoeauth.click_accountOpenDater()
        pppoeauth.click_bnpreMonth() #向前一个月
        pppoeauth.click_day1()#任意选择
        pppoeauth.click_accountStopDate()
        pppoeauth.click_bnpreMonth() # 向前一个月
        pppoeauth.click_day2()
        pppoeauth.click_save()
        time.sleep(2)
        # 断言 添加的账号 认证方式和认证账号 是否正常（第二行）
        list_authtype2 = pppoeauth.getText_byXpath(pppoeauth.list_authtype2)
        list_authAcc2 = pppoeauth.getText_byXpath(pppoeauth.list_authAcc2)
        self.assertEqual(str(list_authtype2), 'PPPoE', msg='认证方式显示不为“PPPoE”')
        self.assertEqual(str(list_authAcc2), 'BeOverdue', msg='认证账号不为“BeOverdue”')
        print('认证账号 - 新增已过期账号 成功')

        # 新增将过期账号
        pppoeauth.click_addUser()
        time.sleep(1)
        pppoeauth.input_name('Overdue')
        selauthType = pppoeauth.selelement_byName('authType')
        Select(selauthType).select_by_value('PPPoE')
        time.sleep(1)
        pppoeauth.input_authAccount('Overdue')
        pppoeauth.input_authPassword('Overdue')
        pppoeauth.click_accountBillEn()
        time.sleep(1)
        # 设置账号日期
        pppoeauth.click_accountOpenDater()
        pppoeauth.click_bnpreMonth()  # 向前一个月
        pppoeauth.click_day1()  # 任意选择
        pppoeauth.click_accountStopDate()
        pppoeauth.click_bnpostMonth()  # 向后一个月
        pppoeauth.click_day3()
        pppoeauth.click_save()
        time.sleep(2)
        # 断言 添加的账号 认证方式和认证账号 是否正常(第三行)
        list_authtype3 = pppoeauth.getText_byXpath(pppoeauth.list_authtype3)
        list_authAcc3 = pppoeauth.getText_byXpath(pppoeauth.list_authAcc3)
        self.assertEqual(str(list_authtype3), 'PPPoE', msg='认证方式显示不为“PPPoE”')
        self.assertEqual(str(list_authAcc3), 'Overdue', msg='认证账号不为“BeOverdue”')
        print('认证账号 - 新增将过期账号 成功')
        self.driver.quit()

        #开始验证账号到期通告
        # 已过期账号验证
        #开始拨号
        Adsl.connect(self,name='adsl',username='BeOverdue',password='BeOverdue')
        # 通过断言IP地址网段，判断是否可以拨号成功
        pcaddr_connectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        # print(pcaddr_connectAdsl)
        self.assertIn('10.10.10.', str(pcaddr_connectAdsl), msg='PPPoE拨号失败')
        time.sleep(2)
        # 打开网页测试，测试上网
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.utt.com.cn')
        time.sleep(2)
        title1 = self.driver.title
        print(title1)
        self.assertEqual(title1, messages, msg='通告未显示')
        time.sleep(1)
        # 拨号挂断，通过断言IP地址网段，判断是否挂断
        Adsl.disconnect(self)
        pcaddr_disconnectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        print(pcaddr_disconnectAdsl)
        self.assertIn('192.168.', str(pcaddr_disconnectAdsl), msg='PPPoE挂断失败')
        self.driver.quit()
        print('已过期账号 到期通告 - 验证成功')

        # 将期账号验证
        # 开始拨号
        Adsl.connect(self, name='adsl', username='Overdue', password='Overdue')
        # 通过断言IP地址网段，判断是否可以拨号成功
        pcaddr_connectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        # print(pcaddr_connectAdsl)
        self.assertIn('10.10.10.', str(pcaddr_connectAdsl), msg='PPPoE拨号失败')
        # 打开网页测试，测试上网
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.utt.com.cn')
        time.sleep(2)
        title1 = self.driver.title
        print(title1)
        self.assertEqual(title1, messages, msg='通告未显示')
        time.sleep(1)
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title1 = self.driver.title
        print(title1)
        self.assertEqual(title1, baidutitle, msg='第二次打开网页异常')
        time.sleep(1)
        # 拨号挂断，通过断言IP地址网段，判断是否挂断
        Adsl.disconnect(self)
        pcaddr_disconnectAdsl = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        print(pcaddr_disconnectAdsl)
        self.assertIn('192.168.', str(pcaddr_disconnectAdsl), msg='PPPoE挂断失败')
        self.driver.quit()
        print('将过期账号 到期通告 - 验证成功')

        print('账号到期通告 - 验证成功')
        #删除组织架构组（组内的pppoe账号也会一并删掉）
        organization_group.group_delete(self)

        # 关闭pppoe server
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        pppoeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        pppoeauth.click_UserManage()
        time.sleep(0.5)
        pppoeauth.click_userAuth()
        time.sleep(1)
        pppoeauth.click_pppoeAuthC()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        status = str(pppoeauth.getAttribute_byXpath(pppoeauth.pppoeAuthCs,'checked'))
        time.sleep(1)
        self.assertEqual(status, 'true', msg='PPPoE认证关闭出错')
        print('PPPoE认证关闭 验证成功')

        self.driver.quit()
        logger.info('test_003_AuthNotice passed')

    def tearDown(self):
        # 设置了指定IP，这里增加一个判断联网
        host = gettelnet('host').split(r'.')
        host1 = host[0] + '.' + host[1] + '.' + host[2] + '.'
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        print(pcaddr)
        pingTestIP()# 避免判断失误
        p = pingTestIP()
        if p == 'N' or host1 not in pcaddr:  # 如果不通 or 地址不为lan口网段
            # 1、改回DHCP， 调用bat脚本
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
                raise Exception('未获取到地址')

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()





