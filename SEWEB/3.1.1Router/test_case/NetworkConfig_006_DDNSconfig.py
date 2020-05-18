#! -*-conding:utf-8 -*-
#@Time: 2019/1/18 0018 10:58
#@swzhou
'''
ddns 配置
'''

import time
import unittest
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_006_DDNSpage import DDNSpage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'NetworkConfig_006_DDNSconfig').getlog()

class DDNS(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        ddnsconfig = DDNSpage(self.driver,self.url)
        # 打开网络配置 - 动态域名
        ddnsconfig.click_netConfig()
        time.sleep(0.5)
        ddnsconfig.click_DDNSconfig()
        time.sleep(1)

        # pass

    def test_001_SupportFiveDDNS(self):
        u'''支持五种域名服务商'''
        #尝试分别选择5种 服务商
        ddnsconfig = DDNSpage(self.driver, self.url)
        ddnsconfig.click_add()
        time.sleep(1)
        selDDNSProvider = ddnsconfig.selelement_byName(ddnsconfig.selDDNSProvider)
        try:
            self.driver.implicitly_wait(2)
            Select(selDDNSProvider).select_by_value('3322.org')
            time.sleep(0.5)
            ddnsconfig.click_Interface()
        except NoSuchElementException:
            raise Exception('3323.org 不存在')

        try:
            self.driver.implicitly_wait(2)
            Select(selDDNSProvider).select_by_value('www.oray.net')
            time.sleep(0.5)
            ddnsconfig.click_Interface()
        except NoSuchElementException:
            raise Exception('www.oray.net 不存在')

        try:
            self.driver.implicitly_wait(2)
            Select(selDDNSProvider).select_by_value('dyndns.org')
            time.sleep(0.5)
            ddnsconfig.click_Interface()
        except NoSuchElementException:
            raise Exception('dyndns.org 不存在')

        try:
            self.driver.implicitly_wait(2)
            Select(selDDNSProvider).select_by_value('no-ip.com')
            time.sleep(0.5)
            ddnsconfig.click_Interface()
        except NoSuchElementException:
            raise Exception('no-ip.com 不存在')

        try:
            self.driver.implicitly_wait(2)
            Select(selDDNSProvider).select_by_value('uttcare.com')
            time.sleep(0.5)
            ddnsconfig.click_Interface()
        except NoSuchElementException:
            raise Exception('uttcare.com 不存在')

        self.driver.quit()
        logger.info('test_001_SupportFiveDDNS passed')

    def test_002_uttcare(self):
        u'''uttcare 解析地址为WAN口IP地址'''
        ConnectState = getAssertText('ConnectState')
        nodata = getAssertText('nodata')

        ddnsconfig = DDNSpage(self.driver, self.url)
        ddnsconfig.click_add()
        time.sleep(1)
        selDDNSProvider = ddnsconfig.selelement_byName(ddnsconfig.selDDNSProvider)
        Select(selDDNSProvider).select_by_value('uttcare.com')
        time.sleep(0.5)
        ddnsconfig.click_save()
        time.sleep(5)

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 ip变量赋值，页面读取
        # 判断联网状态
        i = 0
        while i < 21:
            wanpage.click_refresh()
            time.sleep(1)
            list_conState = wanpage.getText_byXpath(wanpage.connectState1)
            print(str(list_conState), i)
            if str(list_conState) != ConnectState:
                time.sleep(3)
                i += 1
            else:
                break
        else:
            CapPic(self.driver)
            logger.info(u"WAN口未连接")
            raise Exception('WAN1 未连接')
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)

        ddnsconfig = DDNSpage(self.driver, self.url)
        # 打开网络配置 - 动态域名
        ddnsconfig.click_DDNSconfig()
        time.sleep(1)
        n = 0
        while n < 20:
            ddnsconfig.click_fresh()
            time.sleep(1)
            list_status = ddnsconfig.getText_byXpath(ddnsconfig.list_status)
            if list_status == ConnectState:
                list_ServiceProvider = ddnsconfig.getText_byXpath(ddnsconfig.list_ServiceProvider)
                self.assertEqual(list_ServiceProvider, 'uttcare.com', msg='服务商不为 uttcare.com')
                list_ip = ddnsconfig.getText_byXpath(ddnsconfig.list_ip)
                self.assertEqual(list_ip, WAN1_ip, msg='解析的IP与wan1口IP不一致')
                break
            else:
                time.sleep(3)
                n += 1
        else:
            raise Exception('uttcare域名未更新成功')
        # 删除已配置的域名
        ddnsconfig.click_delete()
        time.sleep(1)
        ddnsconfig.click_ok()
        time.sleep(1)
        list_nodata = str(ddnsconfig.getText_byXpath(ddnsconfig.list_nodata))
        self.assertEqual(list_nodata,nodata,msg='uttcare域名删除失败')
        self.driver.quit()
        logger.info('test_002_uttcare passed')

    def test_003_3322_oray(self):
        u'''3322.org&花生壳,解析地址为公司外网IP地址'''
        ConnectState = getAssertText('ConnectState')
        nodata = getAssertText('nodata')

        ddnsconfig = DDNSpage(self.driver, self.url)
        # 操作删除 以访已有规则
        ddnsconfig.click_selall()
        time.sleep(0.2)
        ddnsconfig.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            ddnsconfig.find_ok()
        except NoSuchElementException:
            try:
                ddnsconfig.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            print('ddns列表为空')

        # 3322.org
        ddnsconfig.click_add()
        time.sleep(1)
        selDDNSProvider = ddnsconfig.selelement_byName(ddnsconfig.selDDNSProvider)
        Select(selDDNSProvider).select_by_value('3322.org')
        time.sleep(0.5)
        ddnsconfig.input_DDNS3322('lixiaojiao01.3322.org')
        ddnsconfig.input_Account3322('lixiaojiao2009')
        ddnsconfig.input_Password3322('tjq888928')
        ddnsconfig.click_save()
        time.sleep(2)
        # 获取上网的出口地址
        try:
            self.driver.get('https://ip.cn/')
            time.sleep(1)
            Extranet_ip=str(ddnsconfig.getText_byXpath(ddnsconfig.Extranet_ip1))
            # print(Extranet_ip)
        except NoSuchElementException:
            try:
                self.driver.get('http://ip.tool.chinaz.com/siteip')
                time.sleep(2)
                Extranet_ip = str(ddnsconfig.getText_byXpath(ddnsconfig.Extranet_ip2))
                # print(Extranet_ip)
            except NoSuchElementException:
                raise Exception('未获取到wan口地址')
            self.driver.back()
            time.sleep(1)
        # 断言 解析地址是否和外网地址匹配 ip
        self.driver.back()
        time.sleep(1)
        n = 0
        while n < 20:
            ddnsconfig.click_fresh()
            time.sleep(1)
            list_status = ddnsconfig.getText_byXpath(ddnsconfig.list_status)
            if list_status == ConnectState:
                list_ServiceProvider = ddnsconfig.getText_byXpath(ddnsconfig.list_ServiceProvider)
                self.assertEqual(list_ServiceProvider, '3322.org', msg='服务商不为 3322.org')
                list_ip = ddnsconfig.getText_byXpath(ddnsconfig.list_ip)
                self.assertEqual(list_ip, Extranet_ip, msg='解析的IP与上网外网地址不一致')
                break
            else:
                time.sleep(3)
                n += 1
        else:
            raise Exception('3322.org 域名没有更新成功')
        # 删除已配置的域名
        ddnsconfig.click_delete()
        time.sleep(1)
        ddnsconfig.click_ok()
        time.sleep(3)
        list_nodata = str(ddnsconfig.getText_byXpath(ddnsconfig.list_nodata))
        self.assertEqual(list_nodata, nodata, msg='3322.org域名删除失败')

        # 花生壳
        ddnsconfig = DDNSpage(self.driver, self.url)
        ddnsconfig.click_add()
        time.sleep(1)
        selDDNSProvider = ddnsconfig.selelement_byName(ddnsconfig.selDDNSProvider)
        Select(selDDNSProvider).select_by_value('www.oray.net')
        time.sleep(1)
        ddnsconfig.input_AccountNut('wxl0556')
        ddnsconfig.input_PasswordNut('wxl123456')
        ddnsconfig.click_save()
        # 断言 解析地址是否出口路由器IP
        time.sleep(3)
        n = 0
        while n < 20:
            ddnsconfig.click_fresh()
            time.sleep(0.5)
            list_status = ddnsconfig.getText_byXpath(ddnsconfig.list_status)
            if list_status == ConnectState:
                list_ServiceProvider = ddnsconfig.getText_byXpath(ddnsconfig.list_ServiceProvider)
                self.assertEqual(list_ServiceProvider, 'www.oray.net', msg='服务商不为 www.oray.net')
                list_ip = ddnsconfig.getText_byXpath(ddnsconfig.list_ip)
                self.assertEqual(list_ip, Extranet_ip, msg='解析的IP与上网外网地址不一致')
                break
            else:
                time.sleep(3)
                n += 1
        else:
            raise Exception('花生壳 域名没有更新成功')

        # 删除已配置的域名
        ddnsconfig.click_delete()
        time.sleep(1)
        ddnsconfig.click_ok()
        time.sleep(3)
        list_nodata = str(ddnsconfig.getText_byXpath(ddnsconfig.list_nodata))
        self.assertEqual(list_nodata, nodata, msg='花生壳 域名删除失败')
        self.driver.quit()
        logger.info('test_003_3322_oray passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()