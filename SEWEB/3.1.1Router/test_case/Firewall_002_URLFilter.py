#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 17:03
#@swzhou
'''
防火墙：开启URL过滤，过滤内容为www.163.com，适用用户为IP段，在生效时间内PC能访问官网，不能访问www.163.com
'''

import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.select import Select
import time
import unittest
import socket

from common.LogGen import LogGen
logger = LogGen(Logger = 'Firewall_002_URLFilter').getlog()
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Firewall_001_ACLPage import AccessControlPage
from pages.sysObj_timePlanPage import timePlanPage

class URLFilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_URLFilter(self):
        u'''URL过滤 www.163.com，控制IP段，生效时间内无法访问163,可以访问百度'''
        baidutitle = getAssertText('baidutitle')
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

        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

        #配置防火墙
        firewall = AccessControlPage(self.driver,self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        firewall.click_add()
        time.sleep(1)
        firewall.input_PolicyNames('URLfilter')
        firewall.click_sourceIP()
        time.sleep(1)
        firewall.click_usergroup()
        time.sleep(1)
        # 选择IP段 用自身IP
        firewall.click_userip()
        time.sleep(1)
        firewall.input_starip(pcaddr)
        firewall.input_endip(pcaddr)
        firewall.click_saveW1()
        time.sleep(1)
        seltime=firewall.selelement_byName('timeGrpName')
        time.sleep(1)
        Select(seltime).select_by_value('TimePlan')
        selFilterTypes = firewall.selelement_byName(firewall.selFilterTypes)
        time.sleep(1)
        Select(selFilterTypes).select_by_value('2') #URL过滤
        firewall.input_glnrUrl('www.163.com')
        firewall.click_save()
        time.sleep(1)
        # 开启访问控制
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS,'checktype')  # checktype 0未开启，1开启
        if checkTrafficS == '0':
            firewall.click_checkTraffic()
        time.sleep(2)
        print('访问控制策略 已添加')
        #断言
        list_content = str(firewall.getText_byXpath(firewall.list_Content))
        self.assertEqual(list_content , 'www.163.com', msg='过滤内容不为"www.163.com"')
        checkTrafficS=firewall.getAttribute_byId(firewall.checkTrafficS,'checktype') #checktype 0未开启，1开启
        self.assertEqual(checkTrafficS,'1',msg='访问控制 未开启')
        self.driver.quit()

        # 访问官网，使用打不开网页的 title做断言
        time.sleep(5)
        self.dr = webdriver.Chrome()
        # self.dr.maximize_window()
        self.dr.implicitly_wait(10)
        self.dr.set_page_load_timeout(10)  # selenium超时设置/等待时间过长自动停止
        # 清除浏览器cookies
        cookies = self.dr.get_cookies()
        print(f"main: cookies = {cookies}")
        self.dr.delete_all_cookies()
        # 因为被过滤，会打不开网站，，命令执行后会一直处于命令执行中，最后报超时错误，默认超时300s
        # selenium.common.exceptions.TimeoutException: Message: timeout
        # 配合上文 set_page_load_timeout(10)设置等待超时时间，这里等待10s，判断报超时错误则正常，否则失败
        time.sleep(3)
        # 尝试访问百度 应可以
        time.sleep(1)
        self.dr.get('http://www.baidu.com')
        title2 = self.dr.title
        print(title2)
        self.assertEqual(title2, baidutitle, msg='URL过滤开启后 不能打开其他网页')
        print('百度正常打开 验证成功')
        # 尝试访问163 应不可以
        try:
            self.dr.get('http://www.163.com/')
        except TimeoutException:
            print('163禁止 验证成功')
        else:
            raise Exception('163禁止失败')

        self.dr.close()
        logger.info('test_URLFilter passed')

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

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()
