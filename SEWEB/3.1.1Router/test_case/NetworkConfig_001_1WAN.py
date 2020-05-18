#! -*-conding:utf-8 -*-
#@Time: 2018/12/29 0029 16:17
#@swzhou
'''
单线路接入：动态、固定、pppoe接入
'''

import os
import time
import unittest
import os.path
import subprocess
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import ElementNotVisibleException,NoSuchElementException,ElementNotInteractableException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.swconfig import swconfig
from common.pingTest import pingTestIP
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'NetworkConfig_001_1WAN').getlog()

class Config_WAN(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # 进入网络配置-外网配置
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # pass

    def test_000_getReady(self):
        u'''更改wan口数量/初始化交换机vlan'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 动态wan口，调整wan口数量
        self.driver.implicitly_wait(2)
        try:
            wan_config.find_GlobalConfig()
            time.sleep(1)
        except AttributeError:
            logger.info(u'wan口页面没有全局配置，则不支持动态WAN口')
        except NoSuchElementException:
            logger.info(u'wan口页面没有全局配置，则不支持动态WAN口')
        else:
            try:
                wan_config.find_PortNumber()
            except ElementNotVisibleException:
                logger.info(u'页面没有wan口数量调整，不支持动态WAN口')
            except ElementNotInteractableException:
                logger.info(u'页面没有wan口数量调整，不支持动态WAN口')
            else:
                selPortNumber = wan_config.selelement_byName(wan_config.selPortNumber)
                Select(selPortNumber).select_by_value('1')
                time.sleep(2)
                try:
                    wan_config.find_cfm_ok()
                except NoSuchElementException:
                    logger.info(u'WAN口数量已为1')
                else:
                    time.sleep(30)
                    i = 0
                    while i < 20:
                        now_url = str(self.driver.current_url)
                        # print(now_url,i)
                        if '/noAuth/login.html' not in now_url:  # 如果不同
                            time.sleep(5)
                        else:
                            break
                        i += 1
                    else:
                        raise Exception('更改设备wan口数量后未正常启动')
        self.driver.quit()
        # 2 初始化初始化交换机vlan
        swconfig.test_initSwPort(self)
        logger.info('test_000_getReady passed')

    def test_001_dhcp(self):
        u'''外网配置 - 动态接入'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        #先判断几条外线接入，删除其他几条外线
        wan_config.click_line1edit()
        time.sleep(1)
        value_list = []
        wan_num = wan_config.selelement_byName(wan_config.PortName)
        options_list = wan_num.find_elements_by_tag_name(wan_config.PortNameOptions)
        for option in options_list:
            print("Value is:%s  Text is:%s" % (option.get_attribute("value"), option.text))
            value_list.append(option.get_attribute("value"))
        print(value_list)
        wan_config.click_back()
        time.sleep(1)
        if 'WAN2' in value_list:
            wan_config.click_line2delete()
            time.sleep(1)
            wan_config.click_cfm_ok()
            time.sleep(10)
        if 'WAN3' in value_list:
            wan_config.click_line3delete()
            time.sleep(1)
            wan_config.click_cfm_ok()
            time.sleep(10)
        if 'WAN4' in value_list:
            wan_config.click_line4delete()
            time.sleep(1)
            wan_config.click_cfm_ok()
            time.sleep(10)
        if 'WAN5' in value_list:
            wan_config.click_line5delete()
            time.sleep(1)
            wan_config.click_cfm_ok()
            time.sleep(10)

        # 获取外线的链接类型
        line1_type = wan_config.getText_byXpath(wan_config.line1Type)
        linetype = getAssertText('DHCPline')
        ConnectState = getAssertText('ConnectState')
        # 先改为动态接入，得到正确的IP地址及网关地址
        # WAN1
        if str(line1_type) != linetype:
            wan_config.click_line1edit()
            time.sleep(1)
            access_mode = wan_config.selelement_byName(wan_config.connectionType)
            Select(access_mode).select_by_value('DHCP')
            wan_config.click_save()
            time.sleep(10)  # 修改接口后 可能会回到登录页面 所以关闭，再打开
            self.driver.quit()
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            wan_config = NetworkConfig_wanpage(self.driver, self.url)
            wan_config.click_NetworkConfig()
            time.sleep(0.5)
            wan_config.click_WANconfig()
            time.sleep(1)
        else:
            print('wan1 动态接入')
        #断言
        list_lineType = wan_config.getText_byXpath(wan_config.line1Type)
        print('list_lineType:', list_lineType)
        self.assertEqual(str(list_lineType),linetype ,msg='连接类型 不为 动态接入')
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
        u'''外网配置 - 固定接入'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        Staticline = getAssertText('Staticline')
        ConnectState = getAssertText('ConnectState')
        # 从外网配置页面获取WAN1口地址
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
        # WAN1 ip变量赋值，页面读取
        WAN1_ip = wan_config.getText_byXpath(wan_config.line1IP)
        # print('WAN1_ip=',WAN1_ip)
        WAN1_gw = wan_config.getText_byXpath(wan_config.line1gw)
        # print('WAN1_gw=',WAN1_gw)
        WAN1_dns = wan_config.getText_byXpath(wan_config.line1Dns)
        # print('WAN1_dns=',WAN1_dns)
        time.sleep(1)
        # 将wan1口的IP/网关/dns 拿来输入
        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('STATIC')
        time.sleep(1)
        wan_config.input_staticIp(WAN1_ip)
        wan_config.input_staticGateway(WAN1_gw)
        wan_config.input_staticPriDns(WAN1_dns)
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        #断言
        list_lineType = wan_config.getText_byXpath(wan_config.line1Type)
        print('list_lineType',list_lineType)
        self.assertEqual(str(list_lineType),Staticline,msg='连接类型 不为 固定接入')
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
        u'''外网配置 - PPPoE接入'''
        wan_config = NetworkConfig_wanpage(self.driver,self.url)
        PPPoEline = getAssertText('PPPoEline')
        ConnectState = getAssertText('ConnectState')

        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('111')
        wan_config.input_pppoePass('111')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        #断言
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

        # list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
        # print('list_connection_state:',str(list_connectState1))
        # if str(list_connectState1) != ConnectState:  # PPPoE接入 拨号成功才会显示已连接
        #     time.sleep(5)
        #     wan_config.click_refresh()
        #     time.sleep(0.5)
        #     list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
        #     if str(list_connectState1) != ConnectState:
        #         wan_config.click_connectState1()
        #         wan_config.click_dial()
        #         time.sleep(10)
        #         wan_config.click_refresh()
        #         time.sleep(0.5)
        #         list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
        #         if str(list_connectState1) != ConnectState:
        #             raise Exception('WAN1 未连接')
        #         else:  # 已连接
        #             time.sleep(3)
        #             pingTestIP('114.114.114.114') #避免失误
        #             pingTestIP('www.baidu.com') #避免失误
        #             p = pingTestIP('www.baidu.com')
        #             if p == 'N':
        #                 raise Exception('connect failed.')
        #     else:  # 已连接
        #         time.sleep(3)
        #         pingTestIP('114.114.114.114') #避免失误
        #         pingTestIP('www.baidu.com') #避免失误
        #         p = pingTestIP('www.baidu.com')
        #         if p == 'N':
        #             raise Exception('connect failed.')
        # else:  # 已连接
        #     time.sleep(3)
        #     pingTestIP('114.114.114.114')
        #     pingTestIP('www.baidu.com')
        #     p = pingTestIP('www.baidu.com')
        #     if p == 'N':
        #         raise Exception('connect failed.')

        self.driver.quit()
        print(u'外网配置 - PPPoE接入 验证通过')

        #改回动态接入
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('DHCP')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()
        logger.info('test_003_pppoe passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
