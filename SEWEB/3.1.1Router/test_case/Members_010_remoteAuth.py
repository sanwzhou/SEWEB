#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 17:38
#@swzhou
'''
功能说明
'''


import time
import unittest
import os.path
from selenium import webdriver
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_010_remoteAuth').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
remoteAuthP = getParameter('remoteAuthP')
Support = getExcelValue(remoteAuthP)

class remoteAuth(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_openRemoteAuth(self):
        u'''开启远程认证'''
        if Support == '√':
            logger.info(u'参数支持远程认证')
            organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空

            # 打开用户管理 - 用户认证
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            remoteauth = Organization_userAuthPage(self.driver,self.url)
            remoteauth.click_UserManage()
            time.sleep(0.3)
            remoteauth.click_userAuth()
            time.sleep(1)
            # 开启远程认证
            remoteauth.click_remoteAuthEn()
            time.sleep(0.5)
            # 断言 提示信息是否有误
            status = str(remoteauth.getAttribute_byXpath(remoteauth.remoteAuthEs,'checked'))
            self.assertEqual(status, 'true', msg='远程认证开启出错')
            time.sleep(1)
            self.driver.quit()
            print('远程认证 开启成功')

            # 新增用户组及PC的组织架构
            organization_group.add_user(self)
            time.sleep(1)
        elif Support == '×':
            logger.info(u'参数不支持远程认证')
        logger.info('test_001_openRemoteAuth passed')

    def test_002_remoteAuth_FreeAuth(self):
        u'''认证弹窗测试&&免认证测试'''
        if Support == '√':
            logger.info(u'参数支持远程认证')
            saveSucess = getAssertText('saveSucess')

            self.driver = webdriver.Chrome()
            # self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            #打开网页测试
            self.driver.get('http://www.utt.com.cn')
            time.sleep(2)
            title1=self.driver.title
            now_url = self.driver.current_url
            print(title1,now_url)
            # self.assertEqual(title1, '艾泰科技', msg='认证页面跳转不正常') 如
            self.assertIn('http://auth.greenwifi.com.cn',now_url, msg='认证页面跳转不正常')
            self.driver.quit()
            print('远程认证 弹窗验证成功')

            #打开组织架构的免认证
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            remoteauth = Organization_userAuthPage(self.driver, self.url)
            remoteauth.click_UserManage()
            time.sleep(0.3)
            remoteauth.click_userAuth()
            time.sleep(1)
            # 免认证选择组织架构
            remoteauth.click_noConfig()
            time.sleep(1)
            remoteauth.click_usergroup()
            time.sleep(1)
            # 组织架构,这里选择的是ROOT 所有
            remoteauth.click_Root()
            time.sleep(0.5)
            remoteauth.click_save()
            time.sleep(1)
            # 开启免认证
            remoteauth.click_FreeAuthEn()
            time.sleep(2)
            # 断言 提示信息是否有误
            pageTip = str(remoteauth.getText_byClass(remoteauth.pageTip))
            time.sleep(1)
            self.assertEqual(pageTip, saveSucess, msg='免认证开启出错')
            self.driver.quit()
            print('免认证开启')

            # 打开网页测试
            time.sleep(5)
            self.driver = webdriver.Chrome()
            # self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get('http://www.baidu.com')
            time.sleep(2)
            title3 = self.driver.title
            print(title3)
            self.assertEqual(title3, '百度一下，你就知道', msg='开启免认证后 不能直接打开网页')
            self.driver.quit()
        elif Support == '×':
            logger.info(u'参数不支持远程认证')
        logger.info('test_002_remoteAuth_FreeAuth passed')

    def test_003_closeRemoteAuth(self):
        u'''关闭远程认证'''
        if Support == '√':
            logger.info(u'参数支持远程认证')
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            remoteauth = Organization_userAuthPage(self.driver, self.url)
            remoteauth.click_UserManage()
            time.sleep(0.3)
            remoteauth.click_userAuth()
            time.sleep(1)
            # 关闭web认证
            remoteauth.click_remoteAuthC()
            time.sleep(1)
            # 断言 提示信息是否有误
            status = str(remoteauth.getAttribute_byXpath(remoteauth.remoteAuthCs,'checked'))
            self.assertEqual(status, 'true', msg='远程认证关闭出错')
            print('远程认证关闭')
            # 免认证选择 全部用户，然后关闭免认证
            remoteauth.click_noConfig()
            time.sleep(1)
            remoteauth.click_alluser()
            time.sleep(0.5)
            remoteauth.click_save()
            time.sleep(1)
            remoteauth.click_FreeAuthC()
            time.sleep(2)
            # 断言 提示信息是否有误
            status2 = str(remoteauth.getAttribute_byXpath(remoteauth.FreeAuthCs,'checked'))
            self.assertEqual(status2, 'true', msg='免认证关闭出错')
            print('免认证关闭')
            self.driver.quit()

            # 清空组织架构组
            organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空
            print('删除组织架构组 完成')
        elif Support == '×':
            logger.info(u'参数不支持远程认证')
        logger.info('test_003_closeRemoteAuth passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()