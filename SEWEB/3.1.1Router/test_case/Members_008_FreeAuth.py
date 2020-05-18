#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 13:44
#@swzhou
'''
免认证 验证测试
'''


import time
import unittest
import os.path
import socket
from selenium import webdriver
from common.LogGen import LogGen
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_008_FreeAuth').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'

class FreeAuth(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        #开启web 认证
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        freeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        freeauth.click_UserManage()
        time.sleep(0.5)
        freeauth.click_userAuth()
        time.sleep(1)
        # 开启web认证
        freeauth.click_WebAuthEn()
        time.sleep(0.5)
        # 断言 提示信息是否有误
        status1 = str(freeauth.getAttribute_byXpath(freeauth.WebAuthEs,'checked'))
        self.assertEqual(status1, 'true', msg='web认证开启出错')
        print('web认证开启')
        time.sleep(1)
        #开启免认证
        freeauth.click_FreeAuthEn()
        time.sleep(0.5)
        # 断言 提示信息是否有误
        status2 = str(freeauth.getAttribute_byXpath(freeauth.FreeAuthEs,'checked'))
        self.assertEqual(status2, 'true', msg='免认证开启出错')
        print('免认证开启')
        # pass

    def test_001_FreeAuthgroup(self):
        u'''免认证 - 组织成员'''
        self.driver.quit()

        organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        freeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        freeauth.click_UserManage()
        time.sleep(0.5)
        freeauth.click_userAuth()
        time.sleep(1)
        #免认证选择组织架构
        freeauth.click_noConfig()
        time.sleep(1)
        freeauth.click_usergroup()
        time.sleep(1)
        # 组织架构,这里选择的是ROOT 所有
        freeauth.click_Root()
        time.sleep(0.5)
        freeauth.click_save()
        time.sleep(1)
        self.driver.quit()

        # 新增用户组及普通IP用户
        organization_group.add_user(self)


        #打开网页验证 断言
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title1 = self.driver.title
        # print(title1)
        self.assertEqual(title1, '百度一下，你就知道', msg='免认证-组织架构 出错')
        self.driver.quit()
        print('免认证 - 组织成员 验证成功')

        #导入空组织架构 以 清空
        organization_group.import_empty_template(self)
        logger.info('test_001_FreeAuthgroup passed')

    def test_002_FreeAuthIP(self):
        u'''免认证 - IP地址'''
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))  # 获取本机ip 默认有线地址
        # 免认证选择IP地址
        time.sleep(2)
        freeauth = Organization_userAuthPage(self.driver, self.url)
        freeauth.click_noConfig()
        time.sleep(1)
        freeauth.click_userip()
        time.sleep(1)
        freeauth.input_starip(pcaddr)
        freeauth.input_endip(pcaddr)
        freeauth.click_save()
        time.sleep(5)
        self.driver.quit()

        # 打开网页验证 断言
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title1 = self.driver.title
        # print(title1)
        self.assertEqual(title1, '百度一下，你就知道', msg='免认证-IP地址 出错')
        self.driver.quit()
        logger.info('test_002_FreeAuthIP passed')

    def test_003_FreeAuthAll(self):
        u'''免认证 - 所有用户'''
        time.sleep(2)
        freeauth = Organization_userAuthPage(self.driver, self.url)
        freeauth.click_noConfig()
        time.sleep(1)
        freeauth.click_alluser()
        time.sleep(0.5)
        freeauth.click_save()
        time.sleep(5)

        # 打开网页验证 断言
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title1 = self.driver.title
        # print(title1)
        self.assertEqual(title1, '百度一下，你就知道', msg='免认证 组织架构 出错')
        self.driver.quit()
        logger.info('test_003_FreeAuthAll passed')

    def tearDown(self):
        # 关闭web 认证
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        freeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        freeauth.click_UserManage()
        time.sleep(0.5)
        freeauth.click_userAuth()
        time.sleep(1)
        # 开启web认证
        freeauth.click_WebAuthC()
        time.sleep(1)
        # 断言 提示信息是否有误
        status3 = str(freeauth.getAttribute_byXpath(freeauth.WebAuthCs,'checked'))
        self.assertEqual(status3, 'true', msg='web认证关闭出错')
        print('web认证关闭')
        time.sleep(2)
        # 关闭免认证
        freeauth.click_FreeAuthC()
        time.sleep(1)
        # 断言 提示信息是否有误
        status4 = str(freeauth.getAttribute_byXpath(freeauth.FreeAuthCs,'checked'))
        self.assertEqual(status4, 'true', msg='免认证关闭出错')
        print('免认证关闭')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

