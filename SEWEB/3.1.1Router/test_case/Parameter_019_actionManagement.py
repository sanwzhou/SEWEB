#! -*-conding:utf-8 -*-
#@Time: 2019/2/18 0018 10:54
#@swzhou
'''
上网行为管理:
系统对象：时间计划、地址组
上网行为管理
域名过滤&DNS重定向
电子通告
'''

import time
import unittest
from common.LogGen import LogGen
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText
from pages.sysObj_timePlanPage import timePlanPage
from pages.sysObj_AddressGroupPage import AddressGroupPage
from pages.actionManage_001_actionManagePage import actionManagePage
from pages.actionManage_002_DomainFilterPage import DomainFilterPage
from pages.actionManage_003_WhiteListPage import WhiteListPage
from pages.actionManage_004_ElectronicsNoticePage import ElectronicsNoticePage
logger = LogGen(Logger = 'Parameter_019_actionManagement').getlog()

class actionManagement(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # pass

    def test_001_SystemObject(self):
        u'''系统对象：时间计划、地址组'''
        # 创建时间计划 为当天
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        #操作删除 以访已有规则
        timePlan.click_selall()
        time.sleep(0.2)
        timePlan.click_delall()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            timePlan.find_ok()
        except NoSuchElementException:
            try:
                timePlan.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('时间计划列表已删除')
        timePlan.click_add()
        time.sleep(1)
        timePlan.input_TimeRangeName('TimePlan')
        timePlan.click_save()
        time.sleep(1)
        list_name = str(timePlan.getText_byXpath(timePlan.listName))
        time.sleep(1)
        self.assertEqual(list_name, 'TimePlan', msg='时间段名 与配置的不一致')
        print('时间计划已添加')

        addressgroup = AddressGroupPage(self.driver,self.url)
        addressgroup.click_AddressGroup()
        time.sleep(1)
        addressgroup.click_add()
        time.sleep(1)
        addressgroup.input_name('test')
        time.sleep(1)
        addressgroup.click_addressTypeold()
        time.sleep(0.5)
        addressgroup.click_btn_tor()
        time.sleep(0.3)
        addressgroup.click_btn_tol()
        time.sleep(0.3)
        addressgroup.click_btn_delet()
        time.sleep(0.3)
        addressgroup.click_addressTypenew()
        time.sleep(0.5)
        addressgroup.input_startAddress('1.2.3.4')
        addressgroup.input_endAddress('1.2.3.5')
        addressgroup.click_btn_tol()
        time.sleep(0.3)
        addressgroup.click_btn_delet()
        time.sleep(0.3)
        addressgroup.click_btn_tor()
        time.sleep(0.3)
        print('地址组 验证通过')

        self.driver.quit()
        logger.info('test_001_SystemObject passed')

    def test_002_actionManage(self):
        u'''上网行为管理'''
        actionManage = actionManagePage(self.driver, self.url)
        # 配置行为管理
        actionManage.click_BehaviorManagement()
        time.sleep(0.5)
        actionManage.click_BehaviorManagement2()
        time.sleep(1)
        # 开/关
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens, 'checktype')  # checktype 0未开启，1开启
        self.assertEqual(checkOpenS, '0', msg='行为管理 默认未关闭')
        actionManage.click_checkOpen()
        time.sleep(2)
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens, 'checktype')
        self.assertEqual(checkOpenS, '1', msg='行为管理 开启失败')
        actionManage.click_checkOpen()
        time.sleep(2)
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens, 'checktype')
        self.assertEqual(checkOpenS, '0', msg='行为管理 关闭失败')

        actionManage.click_add()
        time.sleep(1)
        actionManage.input_ruleName('test')
        actionManage.click_users()
        time.sleep(2)
        actionManage.click_usergroup()
        time.sleep(0.5)
        actionManage.click_userip()
        time.sleep(0.5)
        actionManage.click_userall()
        time.sleep(0.5)
        actionManage.click_saveW1()
        time.sleep(1)
        actionManage.click_servers()
        time.sleep(1)
        actionManage.input_searchText('http')
        actionManage.click_search()
        time.sleep(1)
        actionManage.click_appSearchRes()
        actionManage.click_saveW2()
        time.sleep(1)
        seltime = actionManage.selelement_byName(actionManage.seltime)
        Select(seltime).select_by_value('TimePlan')
        time.sleep(0.5)

        whitelist = WhiteListPage(self.driver,self.url)
        whitelist.click_Whitelist()
        time.sleep(1)
        whitelist.click_add()
        time.sleep(1)
        whitelist.click_ALI()
        time.sleep(0.5)
        whitelist.click_QQ()
        time.sleep(0.5)
        whitelist.input_acount('123456')
        whitelist.click_modalhide()
        time.sleep(0.5)
        whitelist.click_globalconfig()
        time.sleep(1)
        whitelist.click_QQEn()
        time.sleep(0.3)
        whitelist.click_QQC()
        time.sleep(0.3)
        whitelist.click_AliEn()
        time.sleep(0.3)
        whitelist.click_AliC()
        time.sleep(0.3)

        self.driver.quit()
        logger.info('test_002_actionManage passed')

    def test_003_DomainFiltering(self):
        u'''域名过滤&DNS重定向'''
        domainfilter = DomainFilterPage(self.driver, self.url)
        domainfilter.click_BehaviorManagement()
        time.sleep(0.5)
        domainfilter.click_DomainFilter()
        time.sleep(1)
        noticeStatus = domainfilter.getAttribute_byXpath(domainfilter.DomainFilterCs, 'checked')
        self.assertEqual(str(noticeStatus), 'true', msg='域名过滤 默认未关闭')

        domainfilter.input_DnsFilterName('test')
        domainfilter.click_orgShow()
        time.sleep(1)
        domainfilter.click_usergroup()
        time.sleep(0.2)
        domainfilter.click_userip()
        time.sleep(0.2)
        domainfilter.click_userall()
        time.sleep(0.5)
        domainfilter.click_saveW1()
        time.sleep(1)
        seltime = domainfilter.selelement_byName(domainfilter.seltime)
        Select(seltime).select_by_value('TimePlan')
        time.sleep(0.5)
        domainfilter.click_onlyAllowEn()
        time.sleep(0.3)
        domainfilter.click_onlyBlockEn()
        time.sleep(0.3)
        domainfilter.click_terminalEn()#通告
        time.sleep(0.5)
        selterminalRemind = domainfilter.selelement_byName(domainfilter.terminalRemind)
        Select(selterminalRemind).select_by_value('0') #发布通告
        domainfilter.click_editNotePage()
        time.sleep(1)
        domainfilter.click_NoticePageName()
        domainfilter.input_NoticePageNote('test')
        domainfilter.input_NoticePageTitle('test')
        domainfilter.input_SkipUrl('test')
        domainfilter.input_SkipTime('3')
        domainfilter.input_NoticeBody('test')
        domainfilter.click_modalhide()
        time.sleep(0.5)
        Select(selterminalRemind).select_by_value('1')  # 重定向
        time.sleep(0.5)
        domainfilter.click_domainRedirection()
        time.sleep(0.2)

        self.driver.quit()
        logger.info('test_003_DomainFiltering passed')

    def test_004_ElectronicsNotice(self):
        u'''电子通告'''
        nodata = getAssertText('nodata')
        electronicsNotice = ElectronicsNoticePage(self.driver, self.url)
        electronicsNotice.click_BehaviorManagement()
        time.sleep(0.5)
        electronicsNotice.click_ElectronicsNotice()
        time.sleep(1)
        status = str(electronicsNotice.getAttribute_byXpath(electronicsNotice.swCs,'checked'))
        self.assertEqual(status, 'true', msg='电子通告 默认未关闭')

        electronicsNotice.input_rulename('test')
        electronicsNotice.click_swEn()
        electronicsNotice.input_remarks('test')
        electronicsNotice.click_edipage()
        time.sleep(1)
        electronicsNotice.click_NoticePageName()
        electronicsNotice.input_NoticePageNote('test')
        electronicsNotice.input_NoticePageTitle('test')
        electronicsNotice.input_SkipUrl('test')
        electronicsNotice.input_SkipTime('3')
        electronicsNotice.input_NoticeBody('test')
        electronicsNotice.click_modalhide()
        time.sleep(0.5)
        electronicsNotice.click_applyUser()
        time.sleep(1)
        electronicsNotice.click_usergroup()
        time.sleep(0.3)
        electronicsNotice.click_userip()
        time.sleep(0.3)
        electronicsNotice.click_userall()
        time.sleep(0.5)
        electronicsNotice.click_saveW1()
        time.sleep(1)
        seltime = electronicsNotice.selelement_byName(electronicsNotice.seltime)
        Select(seltime).select_by_value('TimePlan')
        time.sleep(0.5)
        print('电子通告 验证通过')
        # 删除时间计划
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        timePlan.click_delete()
        time.sleep(1)
        timePlan.click_ok()
        time.sleep(1)
        # 断言
        listtips2 = str(timePlan.getText_byXpath(timePlan.listnodata))
        self.assertEqual(listtips2, nodata, msg='时间计划删除失败')
        print('时间计划已删除')
        self.driver.quit()
        logger.info('test_004_ElectronicsNotice passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

