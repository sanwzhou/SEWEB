#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 16:47
#@swzhou
'''
基本功能
'''

import time
import unittest
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter
from common.loginRoute import login
from common.GetExcelValue import getExcelValue
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from pages.NetConfig_005_RouteConfigPage import RouteConfigPage
from pages.actionManage_005_NetSniperPage import NetSniperPage
from pages.NetConfig_006_DDNSpage import DDNSpage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_015_basicFunction').getlog()

class basicFunction(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # pass

    def test_001_wanParameters(self):
        u'''WAN口相关 工作模式、连接类型、拨号类型、拨号模式'''
        wanpage = NetworkConfig_wanpage(self.driver,self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        #工作模式
        workMode = wanpage.selelement_byName(wanpage.workMode)
        Select(workMode).select_by_value('0') #0 路由模式 1 NAT模式
        time.sleep(0.5)
        Select(workMode).select_by_value('1')
        time.sleep(0.5)
        # 连接类型
        connectionType = wanpage.selelement_byName(wanpage.connectionType)
        Select(connectionType).select_by_value('DHCP')
        time.sleep(0.5)
        Select(connectionType).select_by_value('STATIC')
        time.sleep(0.5)
        Select(connectionType).select_by_value('PPPOE')
        time.sleep(0.5)
        # 拨号类型
        pppoeOPMode = wanpage.selelement_byName(wanpage.pppoeOPMode)
        Select(pppoeOPMode).select_by_value('DEMAND') #按需拨号
        time.sleep(0.5)
        Select(pppoeOPMode).select_by_value('MANUAL') #手动拨号
        time.sleep(0.5)
        Select(pppoeOPMode).select_by_value('KEEPALIVE') #自动拨号
        time.sleep(0.5)
        # 拨号模式
        pppoeDailMode = wanpage.selelement_byName(wanpage.pppoeDailMode)
        Select(pppoeDailMode).select_by_value('SP1')  # 特殊模式1
        time.sleep(0.5)
        Select(pppoeDailMode).select_by_value('SP2')  # 特殊模式2
        time.sleep(0.5)
        Select(pppoeDailMode).select_by_value('SP3')  # 特殊模式3
        time.sleep(0.5)
        Select(pppoeDailMode).select_by_value('NORMAL')  # 普通模式
        time.sleep(0.5)
        self.driver.quit()
        logger.info('test_001_wanParameters passed')

    def test_002_DNSProxy(self):
        u'''DNS Proxy代理、酒店即插即用'''
        dhcpserver = DHCPserverpage(self.driver,self.url)
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        dhcpserver.click_GlobalConfig()
        time.sleep(1)
        switch = str(dhcpserver.getAttribute_byXpath(dhcpserver.dnspEns,'checked'))
        self.assertEqual(switch,'true',msg='dns代理 默认未开启')
        # 酒店即插即用
        lanpage = NetworkConfig_LANpage(self.driver,self.url)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        switch2 = str(lanpage.getAttribute_byXpath(lanpage.upnpCloseS,'checked'))
        self.assertEqual(switch2, 'true', msg='UPNP 默认开启')
        print('DNS Proxy代理、酒店即插即用 验证通过')
        # 静态路由
        routeconfig = RouteConfigPage(self.driver, self.url)
        routeconfig.click_Routeconfig()
        time.sleep(1)
        routeconfig.click_add()
        time.sleep(1)
        routeconfig.click_modalhide()
        time.sleep(0.5)
        # #策略路由
        # routeconfig.click_PolicyRoute()
        # time.sleep(1)
        # routeconfig.click_addPolicy()
        # time.sleep(1)
        # routeconfig.click_modalhide()
        # time.sleep(0.5)
        self.driver.quit()
        logger.info('test_002_DNSProxy passed')

    def test_003_NetSniper(self):
        u'''内网网络尖兵（某些型号不支持）'''
        nodata = getAssertText('nodata')
        NetSniperP = getParameter('NetSniperP')
        Support = getExcelValue(NetSniperP)
        print(Support)
        netSniper = NetSniperPage(self.driver, self.url)
        netSniper.click_BehaviorManagement()
        time.sleep(0.5)
        if Support == '√':
            try:
                self.driver.implicitly_wait(2)
                netSniper.click_NetSniper()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持内网网络尖兵，与参数表不符')
                raise Exception(u'软件不支持内网网络尖兵，与参数表不符')
            else:
                logger.info(u'软件支持内网网络尖兵，与参数表相符')
                self.driver.implicitly_wait(10)
                time.sleep(1)
                listtips = str(netSniper.getText_byXpath(netSniper.listnodata))
                self.assertEqual(listtips, nodata, msg='管制IP列表 默认不为空')

                netSniper.click_NetSniperconfig()
                time.sleep(0.5)
                switch = str(netSniper.getAttribute_byName(netSniper.enable, 'checked'))
                self.assertEqual(switch, 'None', msg='网络尖兵 默认开启')
        elif Support == '×':
            try:
                self.driver.implicitly_wait(2)
                netSniper.click_NetSniper()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持内网网络尖兵，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持内网网络尖兵，与参数表不符')
                raise Exception(u'软件支持内网网络尖兵，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_003_NetSniper passed')

    def test_004_FiveDDNS(self):
        u'''支持五种域名服务商'''
        ddnsconfig = DDNSpage(self.driver, self.url)
        # 打开网络配置 - 动态域名
        ddnsconfig.click_netConfig()
        time.sleep(0.5)
        ddnsconfig.click_DDNSconfig()
        time.sleep(1)
        ddnsconfig.click_add()
        time.sleep(1)
        #尝试分别选择5种 服务商
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
        logger.info('test_004_FiveDDNS passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
