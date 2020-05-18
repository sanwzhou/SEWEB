#! -*-conding:utf-8 -*-
#@Time: 2019/1/22 0022 17:24
#@swzhou
'''
系统配置-网管策略-系统管理员配置
'''


import time
import unittest

from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
logger = LogGen(Logger = 'administrator').getlog()
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb
from common.loginRoute import login
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
RouteUrl = getweb('RouteUrl')

class administrator(unittest.TestCase):

    def setUp(self):
        print('sysConfig_001_administrator start')


    def test_001_test1(self):
        u'''添加管理员账号'''
        roleA = getAssertText('roleA')
        # 添加管理员账号test/test，读写权限
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        administrator = ManagementPolicyPage(self.driver,self.url)
        #进入系统配置-网管策略-系统管理员
        administrator.click_sysConfig()
        time.sleep(0.5)
        administrator.click_ManagementPolicy()
        time.sleep(1)
        # 添加管理员账号test/test
        administrator.click_add()
        time.sleep(1)
        administrator.input_username('test')
        administrator.input_passwd1('test')
        administrator.input_passwd2('test')
        #设置权限变量，选择 读写 权限
        selrole = administrator.selelement_byName(administrator.role)
        Select(selrole).select_by_value('adm')
        administrator.click_save()
        time.sleep(1)
        # 断言 再点击编辑 确认元素不为空（账号确实是test）：代表账号确实是test
        list_name1 = administrator.getText_byXpath(administrator.list_name1)
        list_role1 = administrator.getText_byXpath(administrator.list_role1)
        self.assertEqual(list_name1,'test',msg='新建账号不为test')
        self.assertEqual(list_role1, roleA, msg='新建账号权限不为读写')
        #注销当前登录
        login.logoutWeb(self)
        time.sleep(1)
        self.driver.quit()

    def test_002_test2(self):
        u'''新增账号登录 修改权限'''
        RouteUrl = getweb('RouteUrl')
        self.url = RouteUrl
        #能使用test该账号登陆管理DUT
        login.test_enableLoginWeb(self, username='test', password='test')
        # self.url = RouteUrl
        self.driver.implicitly_wait(10)
        administrator = ManagementPolicyPage(self.driver, self.url)
        administrator.click_sysConfig()
        time.sleep(0.5)
        administrator.click_ManagementPolicy()
        time.sleep(1)
        #修改test/test为test1/test1，(测试：账号权限一起改 提交时候权限未改成功，这里分两步完成)
        administrator.click_listEdit1()
        time.sleep(1)
        administrator.input_username('test1')
        administrator.input_passwd1('test1')
        administrator.input_passwd2('test1')
        administrator.click_save()
        time.sleep(1)
        self.driver.quit()
        #重新登录--只为修改test1的权限(可以使用test1登录也验证了上一步修改成功)
        login.test_enableLoginWeb(self, username='test1', password='test1')
        self.driver.implicitly_wait(10)
        administrator = ManagementPolicyPage(self.driver, self.url)
        administrator.click_sysConfig()
        time.sleep(0.5)
        administrator.click_ManagementPolicy()
        time.sleep(1)
        #修改test1/test1，为只读权限。
        administrator.click_listEdit1()
        time.sleep(1)
        selrole = administrator.selelement_byName(administrator.role)
        Select(selrole).select_by_value('viewer')       #改为只读权限
        time.sleep(1)
        administrator.click_input_group()#修改后点击下其他元素，避免没有保存成功
        time.sleep(1)
        administrator.click_save()
        time.sleep(1)
        self.driver.quit()

    def test_003_test3(self):
        u'''已删除账号验证 只读权限验证'''
        pageTipWarnA = getAssertText('pageTipWarnA')
        #使用test账号不能登陆管理DUT
        login.test_unableLoginWeb(self, username='test', password='test')
        self.driver.implicitly_wait(10)
        self.driver.quit()

        #使用test1账号可以登陆管理DUT
        login.test_enableLoginWeb(self, username='test1', password='test1')
        self.driver.implicitly_wait(10)
        # 只读权限test1 尝试删除test1/test1账号，应该不成功
        administrator = ManagementPolicyPage(self.driver, self.url)
        administrator.click_sysConfig()
        time.sleep(0.5)
        administrator.click_ManagementPolicy()
        time.sleep(1)
        #尝试删除test1/test1账号，应该不成功
        administrator.click_listDelete1()
        time.sleep(1)
        administrator.click_ok()
        time.sleep(1)
        # 断言删除时候提示信息（logout_span）元素不为空：代表无法删除
        pageTip_warn = administrator.getText_byClass(administrator.pageTip_warn)
        if pageTip_warn != pageTipWarnA:
            CapPic(self.driver)
            logger.info(u'只读权限删除提示有误')
            raise Exception('只读权限删除提示有误')
        else:
            print('已删除账号验证、只读权限验证 通过')
        self.driver.quit()

    def test_004_test4(self):
        u'''删除新增账号 admin登录验证'''
        #删除test1/test1，会退出当前登陆（test1已经修改了权限 用admin删除）
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        administrator = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-系统管理员
        administrator.click_sysConfig()
        time.sleep(0.5)
        administrator.click_ManagementPolicy()
        time.sleep(1)
        #删除test1/test1
        administrator.click_listDelete1()
        time.sleep(1)
        administrator.click_ok()
        time.sleep(1)
        # 断言列表框里第二行没有值、元素为空：代表删除成功
        list2_nodata = administrator.getText_byXpath(administrator.list2_nodata)
        if list2_nodata != ' ':
            CapPic(self.driver)
            logger.info(u'删除test1/test1 有误')
            raise Exception('删除test1/test1 有误')
        else:
            print('删除test1/test1 通过')
        self.driver.quit()

        #删除后使用test1不可以登录
        login.test_unableLoginWeb(self,username='test1',password='test1')
        time.sleep(1)
        self.driver.quit()
        #使用admin/admin可以登陆
        login.test_enableLoginWeb(self,username='admin',password='admin')
        time.sleep(1)
        self.driver.quit()
        print('管理员账号测试 验证通过')

    def tearDown(self):
        print('sysConfig_001_administrator over')

if __name__=='__main__':
    unittest.main()


