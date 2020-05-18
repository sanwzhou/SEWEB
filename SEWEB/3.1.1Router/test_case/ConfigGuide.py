#! -*-conding:utf-8 -*-
#@Time: 2018/12/10 0010 9:25
#@swzhou
'''
配置向导：配置三种上网方式，上网业务均正常
'''

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import time
import unittest
import os.path
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from common.pingTest import pingTestIP
from common.loginRoute import login
from pages.ConfigGuidepage import ConfigGuidepage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'ConfigGuide').getlog()
wifiload2Gp = getParameter('wifiload2Gp')
support2 = getExcelValue(wifiload2Gp)
wifiload5Gp = getParameter('wifiload5Gp')
support5 = getExcelValue(wifiload5Gp)
# print('support2:',support2)
# print('support5:',support5)


class guide(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_dhcp(self):
        u'''配置向导 - 动态接入'''
        guide = ConfigGuidepage(self.driver, self.url)
        linetype = getAssertText('DHCPline')
        ConnectState = getAssertText('ConnectState')
        # 进入配置向导
        guide.click_configGuide()
        time.sleep(0.5)
        guide.click_next()
        time.sleep(1)
        connectionTypew=guide.selelement_byName(guide.connectionTypew)
        Select(connectionTypew).select_by_value('DHCP')
        try:
            self.driver.implicitly_wait(2)
            guide.find_okey()
        except NoSuchElementException:
            print('设备支持无线')
            if support2 != '--':
                logger.info(u'参数支持2.4G')
                logger.info(u'支持2.4G，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持2.4G，与参数表不相符')
                raise Exception('支持2.4G，与参数表不相符')
            guide.click_next()
            time.sleep(1)
            guide.input_ssid('ssid_2.4G')
            try:
                guide.find_ssid_5g()
            except NoSuchElementException:
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'不支持5G，与参数表不相符')
                    raise Exception('不支持5G，与参数表不相符')
                else:
                    logger.info(u'不支持5G，与参数表相符')
            else:
                print('设备支持5G')
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表不相符')
                    raise Exception('支持5G，与参数表不相符')
                guide.input_ssid_5g('ssid_5G')
            guide.click_okey()
            time.sleep(8)
        else:
            print('设备不支持无线')
            if support2 != '--':
                CapPic(self.driver)
                logger.info(u'不支持2.4G，与参数表不相符')
                raise Exception('不支持2.4G，与参数表不相符')
            else:
                logger.info(u'不支持2.4G，与参数表相符')
        time.sleep(15)
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 断言
        list_lineType = wan_config.getText_byXpath(wan_config.line1Type)
        print('list_lineType:', list_lineType)
        self.assertEqual(str(list_lineType), linetype, msg='连接类型 不为 动态接入')
        # 判断联网状态
        i = 0
        while i < 21:
            wan_config.click_refresh()
            time.sleep(1)
            list_conState = wan_config.getText_byXpath(wan_config.connectState1)
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
        i = 0
        while i < 21:
            # 判断联网 ，不能上网则报错
            # pingTestIP('114.114.114.114')
            p = pingTestIP('www.baidu.com')
            print(p, i)
            if p == 'N':
                time.sleep(3)
                i += 1
            else:
                break
        else:
            logger.info(u"connect failed")
            raise Exception('connect failed.')

        self.driver.quit()
        logger.info('test_001_dhcp passed')

    def test_002_static(self):
        u'''配置向导 - 固定接入'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        Staticline = getAssertText('Staticline')
        ConnectState = getAssertText('ConnectState')
        # 从外网配置页面获取WAN1口地址
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 判断联网状态
        i = 0
        while i < 21:
            wan_config.click_refresh()
            time.sleep(1)
            list_conState = wan_config.getText_byXpath(wan_config.connectState1)
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
        WAN1_ip = wan_config.getText_byXpath(wan_config.line1IP)
        WAN1_gw = wan_config.getText_byXpath(wan_config.line1gw)
        WAN1_dns = wan_config.getText_byXpath(wan_config.line1Dns)
        time.sleep(1)
        # 进入配置向导 将wan1口的IP/网关/dns 拿来输入
        guide = ConfigGuidepage(self.driver,self.url)
        guide.click_configGuide()
        time.sleep(1)
        guide.click_next()
        time.sleep(1)
        connectionTypew=guide.selelement_byName(guide.connectionTypew)
        Select(connectionTypew).select_by_value('STATIC')
        time.sleep(1)
        guide.input_staticIp(WAN1_ip)
        guide.input_staticGateway(WAN1_gw)
        guide.input_staticPriDns(WAN1_dns)
        try:
            self.driver.implicitly_wait(2)
            guide.find_okey()
        except NoSuchElementException:
            print('设备支持无线')
            if support2 != '--':
                logger.info(u'参数支持2.4G')
                logger.info(u'支持2.4G，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持2.4G，与参数表不相符')
                raise Exception('支持2.4G，与参数表不相符')
            guide.click_next()
            time.sleep(1)
            guide.input_ssid('ssid_2.4G')
            try:
                guide.find_ssid_5g()
            except NoSuchElementException:
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'不支持5G，与参数表不相符')
                    raise Exception('不支持5G，与参数表不相符')
                else:
                    logger.info(u'不支持5G，与参数表相符')
            else:
                print('设备支持5G')
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表不相符')
                    raise Exception('支持5G，与参数表不相符')
                guide.input_ssid_5g('ssid_5G')
            guide.click_okey()
            time.sleep(8)
        else:
            print('设备不支持无线')
            if support2 != '--':
                CapPic(self.driver)
                logger.info(u'不支持2.4G，与参数表不相符')
                raise Exception('不支持2.4G，与参数表不相符')
            else:
                logger.info(u'不支持2.4G，与参数表相符')
        self.driver.implicitly_wait(10)
        time.sleep(15)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 断言
        list_lineType = wan_config.getText_byXpath(wan_config.line1Type)
        print('list_lineType', list_lineType)
        self.assertEqual(str(list_lineType), Staticline, msg='连接类型 不为 固定接入')
        # 判断联网状态
        i = 0
        while i < 21:
            wan_config.click_refresh_s()
            time.sleep(1)
            list_conState = wan_config.getText_byXpath(wan_config.connectState1)
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
        i = 0
        while i < 21:
            # 判断联网 ，不能上网则报错
            # pingTestIP('114.114.114.114')
            p = pingTestIP('www.baidu.com')
            print(p, i)
            if p == 'N':
                i += 1
                time.sleep(3)
            else:
                break
        else:
            logger.info(u"connect failed")
            raise Exception('connect failed.')

        self.driver.quit()
        logger.info('test_002_static passed')

    def test_003_pppoe(self):
        u'''配置向导 - PPPoE接入'''
        guide = ConfigGuidepage(self.driver, self.url)
        PPPoEline = getAssertText('PPPoEline')
        ConnectState = getAssertText('ConnectState')
        # 进入配置向导
        guide.click_configGuide()
        time.sleep(0.5)
        guide.click_next()
        time.sleep(1)
        connectionTypew = guide.selelement_byName(guide.connectionTypew)
        Select(connectionTypew).select_by_value('PPPOE')
        time.sleep(1)
        guide.input_pppoeUser('111')#输入上层网关配置的PPPoE账号密码
        guide.input_pppoePass('111')
        self.driver.implicitly_wait(2)  # 无线设备会定位不到okey,这里让等待时间缩短一些
        try:
            guide.find_okey()
        except NoSuchElementException:
            print('设备支持无线')
            if support2 != '--':
                logger.info(u'参数支持2.4G')
                logger.info(u'支持2.4G，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持2.4G，与参数表不相符')
                raise Exception('支持2.4G，与参数表不相符')
            guide.click_next()
            time.sleep(1)
            guide.input_ssid('ssid_2.4G')
            try:
                guide.find_ssid_5g()
            except NoSuchElementException:
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'不支持5G，与参数表不相符')
                    raise Exception('不支持5G，与参数表不相符')
                else:
                    logger.info(u'不支持5G，与参数表相符')
            else:
                print('设备支持5G')
                if support5 != '--':
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'支持5G，与参数表不相符')
                    raise Exception('支持5G，与参数表不相符')
                guide.input_ssid_5g('ssid_5G')
            guide.click_okey()
            time.sleep(8)
        else:
            print('设备不支持无线')
            if support2 != '--':
                CapPic(self.driver)
                logger.info(u'不支持2.4G，与参数表不相符')
                raise Exception('不支持2.4G，与参数表不相符')
            else:
                logger.info(u'不支持2.4G，与参数表相符')
        time.sleep(15)
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 断言
        list_lineType = wan_config.getText_byXpath(wan_config.line1Type)
        # print('list_lineType:',list_lineType)
        self.assertEqual(str(list_lineType), PPPoEline, msg='连接类型 不为 PPPoE接入')
        # PPPoE接入 拨号成功才会显示已连接
        i = 0
        while i < 21:
            wan_config.click_refresh()
            time.sleep(1)
            list_conState = wan_config.getText_byXpath(wan_config.connectState1)
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
        i = 0
        while i < 21:
            # 判断联网 ，不能上网则报错
            # pingTestIP('114.114.114.114')
            p = pingTestIP('www.baidu.com')
            print(p, i)
            if p == 'N':
                i += 1
                time.sleep(3)
            else:
                break
        else:
            logger.info(u"connect failed")
            raise Exception('connect failed.')
        #
        # list_conState = guide.getText_byXpath(guide.list_connState)
        # print('list_connection_state:',str(list_conState))
        # if str(list_conState) != ConnectState:  # PPPoE接入 拨号成功才会显示已连接
        #     time.sleep(5)
        #     guide.click_refresh()
        #     time.sleep(0.5)
        #     list_conState = guide.getText_byXpath(guide.list_connState)
        #     if str(list_conState) != ConnectState:  # PPPoE接入 拨号成功才会显示已连接
        #         guide.click_list_connState()
        #         guide.click_dial()
        #         time.sleep(10)
        #         guide.click_refresh()
        #         time.sleep(0.5)
        #         list_conState = guide.getText_byXpath(guide.list_connState)
        #         if str(list_conState) != ConnectState:
        #             raise Exception('WAN1 未连接')
        #         else:  # 已连接
        #             time.sleep(3)
        #             pingTestIP('114.114.114.114')
        #             pingTestIP('www.baidu.com')
        #             p = pingTestIP('www.baidu.com')
        #             if p == 'N':
        #                 raise Exception('connect failed.')
        #     else:  # 已连接
        #         time.sleep(3)
        #         pingTestIP('114.114.114.114')
        #         pingTestIP('www.baidu.com')
        #         p = pingTestIP('www.baidu.com')
        #         if p == 'N':
        #             raise Exception('connect failed.')
        # else:  # 已连接
        #     time.sleep(3)
            # pingTestIP('114.114.114.114')
            # pingTestIP('www.baidu.com')
            # p = pingTestIP('www.baidu.com')
            # if p == 'N':
            #     raise Exception('connect failed.')

        self.driver.quit()
        logger.info('test_003_pppoe passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()



