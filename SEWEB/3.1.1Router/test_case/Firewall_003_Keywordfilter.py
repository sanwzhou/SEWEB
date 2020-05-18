#! -*-conding:utf-8 -*-
#@Time: 2019/1/17 0017 17:21
#@swzhou
'''
开启关键字过滤，过滤内容为“通知”，在200.200.200.134搜索通知文档不成功
'''


from selenium import webdriver
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from selenium.webdriver.support.select import Select
import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.Firewall_001_ACLPage import AccessControlPage
logger = LogGen(Logger = 'Firewall_003_Keywordfilter').getlog()


class Keywordfilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_Keywordfilter(self):
        u'''关键字过滤 “通知”，在200.200.200.134搜索通知文档不成功'''
        OAurl = getAssertText('OAurl')
        OAadmin = getAssertText('OAadmin')
        OApasswd = getAssertText('OApasswd')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        #配置防火墙
        firewall = AccessControlPage(self.driver,self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        firewall.click_add()
        time.sleep(1)
        firewall.input_PolicyNames('Keywordfilter')
        selFilterTypes = firewall.selelement_byName(firewall.selFilterTypes)
        time.sleep(1)
        Select(selFilterTypes).select_by_value('3') #关键字过滤
        firewall.input_glnrKeyword('通知')
        firewall.click_save()
        time.sleep(20)
        # 开启访问控制
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS,'checktype')  # checktype 0未开启，1开启
        if checkTrafficS == '0':
            firewall.click_checkTraffic()
        time.sleep(2)
        print('访问控制策略 已添加')
        #断言
        list_content = str(firewall.getText_byXpath(firewall.list_Content))
        self.assertEqual(list_content , '通知', msg='过滤内容不为"www.163.com"')
        checkTrafficS=firewall.getAttribute_byId(firewall.checkTrafficS,'checktype') #checktype 0未开启，1开启
        self.assertEqual(checkTrafficS,'1',msg='访问控制 未开启')
        self.driver.quit()
        #
        # # 访问OA
        time.sleep(5)
        self.driver = webdriver.Chrome()
        self.driver.set_page_load_timeout(10)  # selenium超时设置/等待时间过长自动停止 配合去情形1
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(OAurl)
        firewall = AccessControlPage(self.driver, self.url)
        firewall.input_OAloginid(OAadmin)
        firewall.input_OApassword(OApasswd)
        firewall.click_OAlogin()
        time.sleep(2)
        # 切换成文档搜索 输入关键字

        #
        # try:
        #     self.driver.implicitly_wait(2)
        #     firewall.click_notice()
        #     time.sleep(2)
        # except NoSuchElementException:
        #     pass

        firewall.click_OAsearcn()
        time.sleep(1)
        firewall.click_OAsearcnWD()
        time.sleep(1)
        firewall.input_OAsearchvalue('通知')
        time.sleep(1)
        #不同chrome 点击确定后的情况不同
        # 情况1：
        # 因为被过滤，在点击后不会有返回结果，命令执行后会一直处于命令执行中，最后报超时错误，默认超时300s
        # selenium.common.exceptions.TimeoutException: Message: timeout
        # 配合上文 set_page_load_timeout(10)设置等待超时时间，这里等待10s，判断报超时错误则正常，否则失败
        # 情况2
        # 点击的命令有返回，这时候就通过 不能定位到HeaderForXtalbe状态栏确定

        firewall.find_OAsearchbt()
        time.sleep(5)
        try:
            firewall.find_OAsearchbt()
            # self.driver.find_element_by_id('searchbt').click()
        except TimeoutException:
            print('关键字过滤 验证通过')
        else:
            try:
                firewall.find_HeaderForXtalbe()
            except NoSuchElementException:
                print('关键字过滤 验证通过2')
            else:
                raise Exception('关键字过滤失败')

        # 退出OA
        firewall.click_OAlogout()
        time.sleep(1)
        firewall.click_OAsubmit()
        self.driver.quit()

        logger.info('test_Keywordfilter passed')

    def tearDown(self):
        nodata = getAssertText('nodata')
        # 关闭防火墙，删除禁止策略
        # login.loginWeb(self)  # admin账号登录
        # self.driver.implicitly_wait(10)
        # firewall = AccessControlPage(self.driver, self.url)
        # firewall.click_FireWall()
        # time.sleep(0.5)
        # firewall.click_AccessControl()
        # time.sleep(1)
        # firewall.click_checkTraffic()
        # time.sleep(1)
        # checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS,'checktype')  # checktype 0未开启，1开启
        # self.assertEqual(checkTrafficS, '0', msg='访问控制 未关闭')
        # print('访问控制策略 已关闭')
        # firewall.click_delete()
        # time.sleep(1)
        # firewall.click_ok()
        # time.sleep(1)
        # # 断言
        # listnodata = str(firewall.getText_byXpath(firewall.listnodata))
        # self.assertEqual(listnodata, nodata, msg='策略删除失败')
        # print('策略已删除')
        # self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
