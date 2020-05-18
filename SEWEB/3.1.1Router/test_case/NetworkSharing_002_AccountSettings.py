#! -*-conding:utf-8 -*-
#@Time: 2019/1/24 0024 14:45
#@swzhou
'''
网络共享账号设置
'''

import time
import unittest
from common.LogGen import LogGen
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.NetConfig_008_NetworkSharingPage import NetworkSharingPage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import InvalidElementStateException, NoSuchElementException
logger = LogGen(Logger = 'NetworkSharing_002_AccountSettings').getlog()


class AccountSettings(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        account = NetworkSharingPage(self.driver,self.url)
        # 打开网络配置-网络共享
        account.click_netConfig()
        time.sleep(0.5)
        account.click_NetworkSharing()
        time.sleep(1)
        account.click_AccountSettings()
        time.sleep(1)
        # pass

    def test_001_AccountSettings(self):
        u'''账号设置：新建、删除、修改'''

        reachMaxA = getAssertText('reachMaxA')
        roleA = getAssertText('roleA')
        account = NetworkSharingPage(self.driver, self.url)
        #新建
        n = 2
        while n < 6:
            n += 1
            if n < 6 :
                account.click_add()
                time.sleep(1)
                account.input_username(n)
                account.input_passwd1(n)
                account.input_passwd2(n)
                authority = account.selelement_byName(account.authority)
                Select(authority).select_by_value('1') #0 读 1 读写
                account.click_save()
                time.sleep(1)
            else:
                account.click_add()
                time.sleep(1)
                account.input_username(n)
                account.input_passwd1(n)
                account.input_passwd2(n)
                authority = account.selelement_byName(account.authority)
                Select(authority).select_by_value('0')  # 0 读 1 读写
                account.click_save()
                time.sleep(1)
                tips = str(account.getText_byClass(account.tips_show_in))
                self.assertEqual(tips,reachMaxA,msg='最大账号为5个 验证失败')
                account.click_modal_hide()
                time.sleep(1)
        Acc3 = str(account.getText_byXpath(account.Acc3))
        auth3 = str(account.getText_byXpath(account.auth3))
        self.assertEqual(Acc3, '3', msg='新增账号失败')
        self.assertEqual(auth3, roleA, msg='新增账号权限失败')
        Acc4 = str(account.getText_byXpath(account.Acc4))
        auth4 = str(account.getText_byXpath(account.auth4))
        self.assertEqual(Acc4, '4', msg='新增账号名失败')
        self.assertEqual(auth4, roleA, msg='新增账号权限失败')
        Acc5 = str(account.getText_byXpath(account.Acc5))
        auth5 = str(account.getText_byXpath(account.auth5))
        self.assertEqual(Acc5, '5', msg='新增账号名失败')
        self.assertEqual(auth5, roleA, msg='新增账号权限失败')

        self.driver.quit()
        logger.info('test_001_AccountSettings passed')

    def test_002_systemAccount(self):
        u'''系统账号不能删除/不能修改账号名'''

        CannotdeleteA = getAssertText('CannotdeleteA')
        Cannotdelete2A = getAssertText('Cannotdelete2A')
        UnableChangeA = getAssertText('UnableChangeA')
        account = NetworkSharingPage(self.driver, self.url)
        #系统账号不能删除
        account.click_listdel1()
        time.sleep(1)
        tips = str(account.getText_byClass(account.tips_show_in))
        self.assertEqual(tips,CannotdeleteA,msg='admin账号不能删除 异常')
        account.click_listdel2()
        time.sleep(1)
        tips = str(account.getText_byClass(account.tips_show_in))
        self.assertEqual(tips, Cannotdelete2A, msg='guest账号不能删除 异常')
        #系统账号名不能修改
        account.click_listedit1()
        time.sleep(1)
        try:
            account.input_username('1')
        except InvalidElementStateException:
            print('admin账号不可修改 验证通过')
            account.click_modal_hide()
            time.sleep(1)
        else:
            raise Exception('admin账号可修改')
        account.click_listedit2()
        time.sleep(1)
        account.input_username('guest1')
        account.click_save()
        time.sleep(1)
        try:
            tips = str(account.getText_byClass(account.tips_show_in))
            self.assertEqual(tips, UnableChangeA, msg='guest账号修改提示信息 异常')
        except NoSuchElementException:
            raise Exception('guest账号可修改')
        account.click_modal_hide()
        time.sleep(1)

        self.driver.quit()
        logger.info('test_002_systemAccount passed')

    def test_003_otherAccount(self):
        u'''修改其他新增账号名及密码'''

        role2A = getAssertText('role2A')
        account = NetworkSharingPage(self.driver, self.url)
        account.click_listedit3()
        time.sleep(1)
        account.input_username('33')
        account.input_passwd1('33')
        account.input_passwd2('33')
        authority = account.selelement_byName(account.authority)
        Select(authority).select_by_value('0')  # 0 读 1 读写
        account.click_save()
        time.sleep(1)
        Acc3 = str(account.getText_byXpath(account.Acc3))
        auth3 = str(account.getText_byXpath(account.auth3))
        self.assertEqual(Acc3, '33', msg='新增账号失败')
        self.assertEqual(auth3, role2A, msg='新增账号权限失败')

        self.driver.quit()
        logger.info('test_003_otherAccount passed')

    def test_004_delAccount(self):
        u'''账号删除：单个/批量'''

        account = NetworkSharingPage(self.driver, self.url)
        #单个账号删除
        account.click_listdel5()
        time.sleep(1)
        account.click_ok()
        time.sleep(1)
        list5_nodata = account.getText_byXpath(account.list5_nodata)
        self.assertEqual(list5_nodata,' ',msg='第5行账号删除失败')
        #批量删除 全选
        account.click_allsel()
        time.sleep(0.2)
        account.click_delete()
        time.sleep(2)
        account.click_ok()
        time.sleep(1)
        list3_nodata = account.getText_byXpath(account.list3_nodata)
        self.assertEqual(list3_nodata, ' ', msg='第3行账号删除失败')

        self.driver.quit()
        logger.info('test_004_delAccount passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()
