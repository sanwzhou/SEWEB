#! -*-conding:utf-8 -*-
#@Time: 2019/1/17 0017 19:34
#@swzhou
'''
开启DNS过滤，过滤内容为www.baidu.com，无法解析ping通www.baidu.com
能解析ping通访问news.baidu.com和www.utt.com.cn
'''

import os
import time
import unittest
import subprocess
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.pingTest import pingTestIP
from common.loginRoute import login
from pages.Firewall_001_ACLPage import AccessControlPage
logger = LogGen(Logger = 'Firewall_004_DNSfilter').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'

class DNSfilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_DNSfilter(self):
        u'''DNS过滤 www.baidu.com，无法ping通百度,可以ping news.baidu.com和官网'''
        # 调用脚本修改dns为114.114.114.114,清空dns缓存
        os.system('%s' % (batpath + 'changeStaticDns_flushdns.bat'))
        time.sleep(5)

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
        firewall.input_PolicyNames('DNSfilter')
        selFilterTypes = firewall.selelement_byName(firewall.selFilterTypes)
        time.sleep(1)
        Select(selFilterTypes).select_by_value('4') #DNS过滤
        firewall.input_glnrdns('www.baidu.com')
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
        self.assertEqual(list_content , 'www.baidu.com', msg='过滤内容不为"www.baidu.com"')
        checkTrafficS=firewall.getAttribute_byId(firewall.checkTrafficS,'checktype') #checktype 0未开启，1开启
        self.assertEqual(checkTrafficS,'1',msg='访问控制 未开启')
        self.driver.quit()

        # 判断联网 ,应该无法解析ping通www.baidu.com,能解析ping通访问news.baidu.com和www.utt.com.cn
        time.sleep(5)
        p = pingTestIP('www.baidu.com')
        if p == 'Y':
            raise Exception('百度 依旧可以ping通')
        p = pingTestIP('news.baidu.com')
        if p == 'N':
            raise Exception('news.baidu.com 无法ping通')
        p = pingTestIP('www.utt.com.cn')
        if p == 'N':
            raise Exception('www.utt.com.cn 无法ping通')
        time.sleep(1)

        logger.info('test_DNSfilter passed')

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
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
