#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 14:56
#@swzhou
'''
开启域名过滤，仅允许/仅禁止www.163.com及域名过滤通告
'''


from selenium import webdriver
import time
import unittest
import os.path
import subprocess
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.pingTest import pingTestIP
from common.loginRoute import login
from pages.actionManage_002_DomainFilterPage import DomainFilterPage
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
DomainFilterNotice = getAssertText('DomainFilterNotice')
logger = LogGen(Logger = 'actionManage_007_DomainFilter').getlog()

class DomainFilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        domainfilter = DomainFilterPage(self.driver,self.url)
        # 行为管理-域名过滤
        domainfilter.click_BehaviorManagement()
        time.sleep(0.5)
        domainfilter.click_DomainFilter()
        time.sleep(1)
        # pass

    def test_001_Forbidfilter_Notice(self):
        u'''开启域名过滤，禁止163&&域名过滤通告'''
        #未开启时候可以ping通163和百度
        p = pingTestIP('114.114.114.114')
        if p == 'N':
            raise Exception('114.114.114.114 无法ping通')
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('www.163.com 无法ping通')
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('www.baidu.com 无法ping通')

        #开启域名过滤
        domainfilter = DomainFilterPage(self.driver, self.url)
        time.sleep(1)
        domainfilter.click_DomainFilterEn()
        time.sleep(1)
        domainfilter.input_DnsFilterName('filter')
        # 仅禁止
        domainfilter.click_onlyBlockEn()
        domainfilter.click_cleanDns()
        time.sleep(1)
        domainfilter.click_ok()
        time.sleep(1)
        domainfilter.input_addHostFilter('www.163.com')
        domainfilter.click_addDns()
        time.sleep(1)
        domainfilter.click_save()
        time.sleep(1)
        #断言
        DomainFilterEns=domainfilter.getAttribute_byXpath(domainfilter.DomainFilterEs,'checked')
        self.assertEqual(str(DomainFilterEns),'true',msg='域名过滤未开启')
        onlyBlockEns = domainfilter.getAttribute_byXpath(domainfilter.onlyBlockEs,'checked')
        self.assertEqual(str(onlyBlockEns), 'true', msg='动作不是禁止')

        # 调用脚本修改dns为114.114.114.114,清空dns缓存
        os.system('%s' % (batpath + 'changeStaticDns_flushdns.bat'))
        time.sleep(5)
        os.system('%s' % (batpath + 'changeStaticDns_flushdns.bat'))
        time.sleep(5)

        # 判断联网 ,应该无法解析ping通www.163.com,能解析ping通访问www.baidu.com
        pingTestIP('114.114.114.114')
        time.sleep(5)
        p = pingTestIP('www.163.com')
        if p == 'Y':
            raise Exception('163 依旧可以ping通')
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('www.baidu.com 无法ping通')
        print('DNS过滤仅禁止 验证通过')

        # 打开通告
        domainfilter.click_terminalEn()
        domainfilter.click_save()
        time.sleep(1)
        #断言
        noticeStatus = domainfilter.getAttribute_byXpath(domainfilter.terminalEs,'checked')
        self.assertEqual(str(noticeStatus), 'true', msg='通告未开启')
        self.driver.quit()
        #测试通告
        time.sleep(3)
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        # 尝试访问163 应不可以
        self.driver.get('http://www.163.com')
        title1 = str(self.driver.title)
        print('title1:',title1)
        self.assertEqual(title1, DomainFilterNotice, msg='通告未弹出')
        self.driver.quit()
        #注意通告打开情况下，可以ping通，在setdown中关闭
        logger.info('test_001_Forbidfilter_Notice passed')

    def test_002_allowfilter_Notice(self):
        u'''开启域名过滤，仅允许163&&域名过滤通告'''

        #开启域名过滤
        domainfilter = DomainFilterPage(self.driver, self.url)
        domainfilter.click_DomainFilterEn()
        time.sleep(1)
        #仅允许
        domainfilter.click_onlyAllowEn()
        domainfilter.click_save()
        time.sleep(1)
        #断言
        DomainFilterEns = domainfilter.getAttribute_byXpath(domainfilter.DomainFilterEs, 'checked')
        self.assertEqual(str(DomainFilterEns),'true',msg='域名过滤未开启')
        actionStatus = domainfilter.getAttribute_byXpath(domainfilter.onlyAllowEs,'checked')
        self.assertEqual(str(actionStatus), 'true', msg='动作不是允许')

        time.sleep(1)
        # 调用脚本修改dns为114.114.114.114,清空dns缓存
        os.system('%s' % (batpath + 'changeStaticDns_flushdns.bat'))
        time.sleep(3)
        os.system('%s' % (batpath + 'changeStaticDns_flushdns.bat'))
        time.sleep(5)

        # 判断联网 ,应该能解析ping通www.163.com,无法解析ping通访问www.baidu.com
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('163 无法ping通')
        p = pingTestIP('www.baidu.com')
        if p == 'Y':
            raise Exception('百度 依旧可以ping通')

        print('DNS过滤仅允许 验证通过')

        # 打开通告
        domainfilter.click_terminalEn()
        domainfilter.click_save()
        time.sleep(1)
        # 断言
        noticeStatus =domainfilter.getAttribute_byXpath(domainfilter.terminalEs,'checked')
        self.assertEqual(str(noticeStatus), 'true', msg='通告未开启')
        self.driver.quit()
        # 测试通告
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get('http://www.utt.com.cn')
        title1 = str(self.driver.title)
        # print(title1)
        self.assertEqual(title1, DomainFilterNotice, msg='通告未弹出')
        self.driver.quit()
        logger.info('test_002_allowfilter_Notice passed')

    def tearDown(self):
        # 关闭域名过滤
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        domainfilter = DomainFilterPage(self.driver, self.url)
        # 行为管理-域名过滤
        domainfilter.click_BehaviorManagement()
        time.sleep(0.5)
        domainfilter.click_DomainFilter()
        time.sleep(1)
        domainfilter.click_DomainFilterC()
        time.sleep(1)
        # 关闭通告，打开通告情况下ping是可以通的
        domainfilter.click_terminalC()
        domainfilter.click_save()
        time.sleep(1)
        # 断言
        DomainFilterEns = domainfilter.getAttribute_byXpath(domainfilter.DomainFilterCs,'checked')
        self.assertEqual(str(DomainFilterEns), 'true', msg='域名过滤未关闭')
        print('域名过滤已关闭')
        noticeStatus = domainfilter.getAttribute_byXpath(domainfilter.terminalCs,'checked')
        self.assertEqual(str(noticeStatus), 'true', msg='通告未关闭')
        self.driver.quit()
        print('通告已关闭')

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
