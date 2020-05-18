#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 17:00
#@swzhou
'''
认证账号	:新增、查看、编辑认证账号
'''


from selenium.webdriver.support.select import Select
import time
import unittest
import os.path
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_009_AuthNumber').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'

class AuthNumber(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_addWebAccNumber(self):
        u'''认证账号 - web账号'''
        AccountingType = getAssertText('AccountingType')
        organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空
        # 调用新增组 “SelfComputerTest”
        organization_group.group_add(self)

        # 新增web认证账号
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
        print('认证账号 - 新增web账号 验证成功')

        # 修改web账号的计费方式为日期计费
        time.sleep(1)
        webauth.click_listedit1()
        time.sleep(1)
        webauth.click_accountBillEn()
        time.sleep(0.5)
        webauth.click_save()
        time.sleep(1)
        # 断言 编辑的账号 计费方式是否已开启
        list_AccountingType = str(webauth.getText_byXpath(webauth.list_AccountingType))
        self.assertEqual(list_AccountingType, AccountingType, msg='web认证账号 修改成功')
        self.driver.quit()
        logger.info('test_001_addWebAccNumber passed')

    def test_002_addpppoeAccNumber(self):
        u'''认证账号 - PPPoE账号(部分型号不支持PPPoE server)'''
        bindingMode = getAssertText('bindingMode')
        # 开启PPPoE认证
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        pppoeauth = Organization_userAuthPage(self.driver, self.url)
        # 打开用户管理 - 用户认证
        pppoeauth.click_UserManage()
        time.sleep(0.5)
        pppoeauth.click_userAuth()
        time.sleep(1)
        # 新增pppoe认证账号
        pppoeauth.click_account()
        time.sleep(1)
        pppoeauth.click_addUser()
        time.sleep(1)
        pppoeauth.input_name('pppoetest1')
        # 仅有一个用户组，这里省略
        select = pppoeauth.selelement_byName(pppoeauth.authType)
        Select(select).select_by_value('PPPoE')
        time.sleep(1)
        pppoeauth.input_authAccount('pppoetest1')
        pppoeauth.input_authPassword('pppoetest1')
        pppoeauth.click_save()
        time.sleep(2)
        # 断言 添加的账号 认证方式和认证账号 是否正常
        list_authtype = pppoeauth.getText_byXpath(pppoeauth.list_authtype)
        list_authAcc = pppoeauth.getText_byXpath(pppoeauth.list_authAcc)
        self.assertEqual(str(list_authtype), 'PPPoE', msg='认证方式显示不为“PPPoE”')
        self.assertEqual(str(list_authAcc), 'pppoetest1', msg='认证账号不为“pppoetest1”')
        print('认证账号 - 新增PPPoE用户 验证成功')

        # 修改pppoe账号的绑定模式为自动绑定
        time.sleep(1)
        pppoeauth.click_listedit1()
        time.sleep(1)
        pppoeauth.click_autoBind()
        time.sleep(0.5)
        pppoeauth.click_save()
        time.sleep(2)
        # 断言 编辑的账号 绑定模式是否为自动绑定
        binding_mode = pppoeauth.getText_byXpath(pppoeauth.list_bindingMode)
        self.assertEqual(str(binding_mode), bindingMode, msg='pppoe账号 修改成功')
        self.driver.quit()
        logger.info('test_002_addpppoeAccNumber passed')

    def test_003_delAccNumber(self):
        u'''认证账号 - 删除'''
        nodata = getAssertText('nodata')
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
        pppoeauth.click_selAll()
        time.sleep(0.5)
        pppoeauth.click_deleteAll()
        time.sleep(1)
        pppoeauth.click_ok()
        time.sleep(1)
        list_tips=pppoeauth.getText_byXpath(pppoeauth.list_tips)
        self.assertEqual(str(list_tips),nodata,msg='账号删除失败')
        print('认证账号 - 账号删除 验证通过')
        self.driver.quit()
        organization_group.group_delete(self)  # 删除组
        logger.info('test_003_delAccNumber passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
