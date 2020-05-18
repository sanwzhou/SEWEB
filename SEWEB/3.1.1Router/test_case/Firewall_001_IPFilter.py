#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 17:03
#@swzhou
'''
防火墙：开启IP地址过滤，过滤TCP80端口，适用用户为组织架构成员，生效时间内无法访问http网页
'''


from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Firewall_001_ACLPage import AccessControlPage
from pages.sysObj_timePlanPage import timePlanPage
logger = LogGen(Logger = 'Firewall_001_IPFilter').getlog()
httpWebUrl = getAssertText('httpWebUrl')

class IPfilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_IPfilter(self):
        u'''IP地址过滤tcp80 控制组织架构成员，生效时间内无法访问http网页'''
        organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空
        organization_group.add_user(self) #将自身IP增加到组织架构中

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        timePlan = timePlanPage(self.driver,self.url)
        # 创建时间计划 为当天
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        # 操作删除 以访已有规则
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
        # 断言 开启提示信息是否有误
        list_name = str(timePlan.getText_byXpath(timePlan.listName))
        time.sleep(1)
        self.assertEqual(list_name, 'TimePlan', msg='时间段名 与配置的不一致')
        print('时间计划已添加')

        #配置防火墙
        firewall = AccessControlPage(self.driver,self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        firewall.click_add()
        time.sleep(1)
        firewall.input_PolicyNames('IPfilter')
        firewall.click_sourceIP()
        time.sleep(1)
        firewall.click_usergroup()
        time.sleep(1)
        # 组织架构,这里选择的是ROOT 所有
        firewall.click_Root()
        firewall.click_saveW1()
        time.sleep(1)
        seltime=firewall.selelement_byName('timeGrpName')
        time.sleep(1)
        Select(seltime).select_by_value('TimePlan')
        # #默认就是IP过滤、TCP 可省略
        # FilterTypessel = self.driver.find_element_by_name('FilterTypes')
        # time.sleep(1)
        # Select(FilterTypessel).select_by_value('1') #IP过滤
        # Protocol = self.driver.find_element_by_name('Protocol')
        # time.sleep(1)
        # Select(Protocol).select_by_value('2') #TCP
        selservice = firewall.selelement_byName('cyfw')
        time.sleep(1)
        Select(selservice).select_by_value('80')  #80(web)
        firewall.click_save()
        time.sleep(1)
        firewall.click_checkTraffic()
        time.sleep(2)
        print('访问控制策略 已添加')
        #断言
        list_dstport = str(firewall.getText_byXpath(firewall.list_dstport))
        self.assertEqual(list_dstport , '80-80', msg='策略目的端口不为"80-80"')
        checkTrafficS=firewall.getAttribute_byId(firewall.checkTrafficS,'checktype') #checktype 0未开启，1开启
        self.assertEqual(checkTrafficS,'1',msg='访问控制 未开启')
        self.driver.quit()

        #访问官网，使用打不开网页的 title做断言
        time.sleep(8)
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://' + httpWebUrl + '/')
        title = str(self.driver.title)
        # print(title)
        self.assertEqual(title,httpWebUrl,msg='TCP80 禁止失败')
        self.driver.quit()
        logger.info('test_IPfilter passed')

    def tearDown(self):
        nodata = getAssertText('nodata')
        # 关闭防火墙，删除禁止策略
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        firewall = AccessControlPage(self.driver, self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        firewall.click_checkTraffic()
        time.sleep(1)
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS,'checktype')  # checktype 0未开启，1开启
        self.assertEqual(checkTrafficS, '0', msg='访问控制 未关闭')
        print('访问控制策略 已关闭')
        firewall.click_delete()
        time.sleep(1)
        firewall.click_ok()
        time.sleep(1)
        # 断言
        listnodata = str(firewall.getText_byXpath(firewall.listnodata))
        self.assertEqual(listnodata, nodata, msg='策略删除失败')
        print('策略已删除')
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
        self.assertEqual(listtips2,nodata, msg='时间计划删除失败')
        print('时间计划已删除')
        self.driver.quit()
        # 删除组织架构
        organization_group.group_delete(self)
        print('组织架构 已删除')

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()
