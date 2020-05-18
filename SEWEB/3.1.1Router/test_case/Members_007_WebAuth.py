#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 12:44
#@swzhou
'''
web认证 ：弹出认证页面、认证后正常访问网络
'''



import time
import unittest
import os.path
import socket
import subprocess
from selenium import webdriver
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,getParameter,gettelnet
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_007_WebAuth').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
webAutnp = getParameter('webAutnp')
Support = getExcelValue(webAutnp)

class webAuth(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_openWebAuth(self):
        u'''web认证开启'''
        host = gettelnet('host').split(r'.')
        host1 = host[0] + '.' + host[1] + '.' + host[2] +'.'
        # 006中设置了指定IP，这里增加一个判断联网
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        print(pcaddr)
        pingTestIP()  # 避免判断失误

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

        if Support == '√':
            logger.info(u'参数支持本地认证')
            organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空

            # 打开用户管理 - 用户认证
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            webauth = Organization_userAuthPage(self.driver, self.url)
            # 打开用户管理 - 用户认证
            webauth.click_UserManage()
            time.sleep(0.5)
            webauth.click_userAuth()
            time.sleep(1)
            #开启web认证
            webauth.click_WebAuthEn()
            time.sleep(1)
            # 断言 提示信息是否有误
            status = str(webauth.getAttribute_byXpath(webauth.WebAuthEs,'checked'))
            time.sleep(1)
            self.assertEqual(status,'true',msg='web认证开启出错')
            self.driver.quit()
        elif Support == '×':
            logger.info(u'参数不支持本地认证')
        logger.info('test_001_openWebAuth passed')

    def test_002_webAuthTest(self):
        u'''web认证测试'''
        if Support == '√':
            logger.info(u'参数支持本地认证')
            webauthpage = getAssertText('webauthpage')
            webauthsucess = getAssertText('webauthsucess')
            # 新增用户组及认证账号
            # 调用新增组 “SelfComputerTest”
            organization_group.group_add(self)
            time.sleep(1)
            #
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            webauth = Organization_userAuthPage(self.driver, self.url)
            # 打开用户管理 - 用户认证
            webauth.click_UserManage()
            time.sleep(0.5)
            webauth.click_userAuth()
            time.sleep(1)
            webauth.click_account()
            time.sleep(1)
            webauth.click_addUser()
            time.sleep(1)
            webauth.input_name('webtest1')
            # 仅有一个用户组，这里省略
            select = webauth.selelement_byName(webauth.authType)
            Select(select).select_by_value('Web')
            time.sleep(1)
            webauth.input_authAccount('webtest1')
            webauth.input_authPassword('webtest1')
            webauth.click_save()
            time.sleep(2)
            # 断言 添加的账号 认证方式和认证账号 是否正常
            list_authtype = webauth.getText_byXpath(webauth.list_authtype)
            list_authAcc = webauth.getText_byXpath(webauth.list_authAcc)
            self.assertEqual(str(list_authtype), 'Web', msg='认证方式显示不为“Web”')
            self.assertEqual(str(list_authAcc), 'webtest1', msg='认证账号不为“webtest1”')
            self.driver.quit()

            self.driver = webdriver.Chrome()
            # self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            #打开网页测试
            self.driver.get('http://www.utt.com.cn')
            time.sleep(2)
            title1=self.driver.title
            print(title1)
            self.assertEqual(title1, webauthpage, msg='认证页面跳转不正常')

            webauth = Organization_userAuthPage(self.driver, self.url)
            webauth.input_userName('webtest1')
            webauth.input_userPasswd('webtest1')
            webauth.click_loginbtn()
            time.sleep(2)
            title2 = self.driver.title
            print(title2)
            self.assertEqual(title2, webauthsucess, msg='不能认证成功')

            self.driver.get('http://www.baidu.com')
            time.sleep(2)
            title3 = self.driver.title
            print(title3)
            self.assertEqual(title3, '百度一下，你就知道', msg='认证后 不能打开网页')
            self.driver.quit()
        elif Support == '×':
            logger.info(u'参数不支持本地认证')
        logger.info('test_002_webAuthTest passed')

    def test_003_closeWebAuth(self):
        u'''关闭web认证'''
        if Support == '√':
            logger.info(u'参数支持本地认证')
            # 打开用户管理 - 用户认证
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            webauth = Organization_userAuthPage(self.driver, self.url)
            # 打开用户管理 - 用户认证
            webauth.click_UserManage()
            time.sleep(0.5)
            webauth.click_userAuth()
            time.sleep(1)
             # 开启web认证
            webauth.click_WebAuthC()
            time.sleep(1)
            # 断言 提示信息是否有误
            status = str(webauth.getAttribute_byXpath(webauth.WebAuthCs,'checked'))
            time.sleep(1)
            self.assertEqual(status, 'true', msg='web认证关闭出错')
            self.driver.quit()
            print('web认证关闭 验证成功')

            # 清空组织架构组
            organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空
            print('删除组织架构组 完成')
        elif Support == '×':
            logger.info(u'参数不支持本地认证')
        logger.info('test_003_closeWebAuth passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

