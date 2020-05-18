#! -*-conding:utf-8 -*-
#@Time: 2019/2/15 0015 15:10
#@swzhou
'''
线路备份、负载均衡、带宽比、电信/联通/移动双线路接入策略路由
策略路由
静态路由绑定vpn接口
'''

import time
import unittest
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_005_RouteConfigPage import RouteConfigPage
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_017_PolicyRoute').getlog()

class PolicyRoute(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        # pass

    def test_001_line(self):
        u'''线路备份、负载均衡、带宽比、电信/联通/移动双线路接入策略路由'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line1edit()
        time.sleep(1)
        #主备
        # 注意这里下拉框select_by_value('0')有问题，使用xpath选择
        wan_config.click_backline1()
        time.sleep(0.5)
        wan_config.click_mainline1()
        time.sleep(0.5)
        #上下行及带宽比
        wan_config.input_txBands2('1000')
        wan_config.input_rxBands2('2000')
        wan_config.input_rMin2('70')
        wan_config.input_rMax2('90')
        wan_config.input_limitRatio2('50')
        #线路模板
        wan_config.click_ISPType()
        time.sleep(0.5)
        wan_config.click_ISPType1()
        time.sleep(0.5)
        wan_config.click_ISPType2()
        time.sleep(0.5)

        self.driver.quit()
        logger.info('test_001_line passed')

    def test_002_PolicyRoute(self):
        u'''策略路由'''
        policyP = getParameter('policyP')
        Support = getExcelValue(policyP)
        if Support != '×':
            logger.info(u'参数支持策略路由')
            routeconfig = RouteConfigPage(self.driver,self.url)
            try:
                self.driver.implicitly_wait(2)
                routeconfig.click_Routeconfig()
                time.sleep(1)
                routeconfig.click_PolicyRoute()
                time.sleep(0.5)
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持策略路由，与参数表不符')
                raise Exception(u'软件不支持策略路由，与参数表不符')
            self.driver.implicitly_wait(10)
            # 新增
            routeconfig.click_addPolicy()
            time.sleep(1)
            routeconfig.click_sourceIP()
            time.sleep(1)
            routeconfig.click_userall()
            time.sleep(0.5)
            routeconfig.click_usergroup()
            time.sleep(0.5)
            routeconfig.click_userip()
            time.sleep(0.5)
            routeconfig.click_saveW()
            time.sleep(0.5)
            routeconfig.click_dstAddr()
            time.sleep(1)
            routeconfig.click_dstgroup()
            time.sleep(0.5)
            routeconfig.click_destIP()
            time.sleep(0.5)

        self.driver.quit()
        logger.info('test_002_PolicyRoute passed')

    def test_003_bandingInter(self):
        u'''静态路由绑定vpn接口（L2TP/PPTP）'''
        bandingVPNp = getParameter('bandingVPNp')
        nodata = getAssertText('nodata')
        Support = getExcelValue(bandingVPNp)
        if Support == '√':
            logger.info(u'参数支持静态路由可绑定PPTP/L2TP接口')
            vpn = pptpL2tpPage(self.driver,self.url)
            vpn.click_VPNConfig()
            time.sleep(0.5)
            try:
                self.driver.implicitly_wait(2)
                vpn.click_pptpL2tp()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持L2TP/PPTP 静态路由无法绑定vpn接口，与参数表不符')
                raise Exception(u'软件不支持L2TP/PPTP 静态路由无法绑定vpn接口，与参数表不符')
            else:
                self.driver.implicitly_wait(10)
                time.sleep(1)
                #配置 VPN
                # 操作删除 以访已有规则
                vpn.click_selall()
                time.sleep(0.2)
                vpn.click_delall()
                time.sleep(2)
                try:
                    self.driver.implicitly_wait(2)
                    vpn.find_ok()
                except NoSuchElementException:
                    try:
                        vpn.find_tipsshowin()
                        time.sleep(1)
                    except NoSuchElementException:
                        pass
                else:
                    time.sleep(1)
                    print('VPN隧道列表为空')
                vpn.click_add()
                time.sleep(1)
                vpn.input_TunNames('staticRoute')
                vpn.input_userNames('staticRoute')
                vpn.input_password('staticRoute')
                vpn.input_remoteInIp('1.2.3.4')
                vpn.input_remoteInIPMask('255.255.255.0')
                vpn.click_save()
                time.sleep(3)
                listtips1 = str(vpn.getText_byXpath(vpn.listtips1))
                self.assertEqual(listtips1, 'staticRoute', msg='VPN名称不为staticRoute')
                print('PPTP已添加')
                vpn.click_add()
                time.sleep(1)
                vpn.click_l2tpB()
                vpn.input_TunNames('staticRoute2')
                vpn.input_userNames('staticRoute2')
                vpn.input_password('staticRoute2')
                vpn.input_remoteInIp('4.3.2.1')
                vpn.input_remoteInIPMask('255.255.255.0')
                vpn.click_save()
                time.sleep(3)
                listtips2 = str(vpn.getText_byXpath(vpn.listtips2))
                self.assertEqual(listtips2, 'staticRoute2', msg='VPN2名称不为staticRoute2')
                print('L2TP已添加')
                # 修改静态路由 绑定PPTP接口
                routeconfig = RouteConfigPage(self.driver, self.url)
                routeconfig.click_NetworkConfig()
                time.sleep(0.5)
                routeconfig.click_Routeconfig()
                time.sleep(1)
                routeconfig.click_add()
                time.sleep(1)
                selProfiles = routeconfig.selelement_byName(routeconfig.selProfiles)
                time.sleep(1)
                try:
                    self.driver.implicitly_wait(2)
                    Select(selProfiles).select_by_value('(PPTPS)staticRoute')
                    time.sleep(0.5)
                    Select(selProfiles).select_by_value('(L2TPS)staticRoute2')
                except NoSuchElementException:
                    CapPic(self.driver)
                    logger.info(u'静态路由无法绑定vpn接口（L2TP/PPTP）')
                    raise Exception(u'静态路由无法绑定vpn接口（L2TP/PPTP）')
                else:
                    self.driver.implicitly_wait(10)
                    time.sleep(1)
                    routeconfig.click_modalhide()
                    time.sleep(0.5)
                    # 删除两条VPN
                    vpn = pptpL2tpPage(self.driver, self.url)
                    vpn.click_VPNConfig()
                    time.sleep(0.5)
                    vpn.click_pptpL2tp()
                    time.sleep(1)
                    vpn.click_delete1()
                    time.sleep(1)
                    vpn.click_ok()
                    time.sleep(2)
                    vpn.click_delete1()
                    time.sleep(1)
                    vpn.click_ok()
                    time.sleep(3)
                    # 断言
                    list_nodata = str(vpn.getText_byXpath(vpn.list_nodata))
                    self.assertEqual(list_nodata, nodata, msg='静态路由删除失败')
                    print('VPN已删除')
        elif Support == '×':
            logger.info(u'参数不支持静态路由可绑定PPTP/L2TP接口')
            vpn = pptpL2tpPage(self.driver, self.url)
            try:
                self.driver.implicitly_wait(2)
                vpn.click_pptpL2tp()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持L2TP/PPTP 静态路由无法绑定vpn接口，与参数表相符')
            else:
                self.driver.implicitly_wait(10)
                time.sleep(1)
                # 配置 VPN
                # 操作删除 以访已有规则
                vpn.click_selall()
                time.sleep(0.2)
                vpn.click_delall()
                time.sleep(2)
                try:
                    self.driver.implicitly_wait(2)
                    vpn.find_ok()
                except NoSuchElementException:
                    try:
                        vpn.find_tipsshowin()
                        time.sleep(1)
                    except NoSuchElementException:
                        pass
                else:
                    time.sleep(1)
                    print('VPN隧道列表为空')
                vpn.click_add()
                time.sleep(1)
                vpn.input_TunNames('staticRoute')
                vpn.input_userNames('staticRoute')
                vpn.input_password('staticRoute')
                vpn.input_remoteInIp('1.2.3.4')
                vpn.input_remoteInIPMask('255.255.255.0')
                vpn.click_save()
                time.sleep(3)
                listtips1 = str(vpn.getText_byXpath(vpn.listtips1))
                self.assertEqual(listtips1, 'staticRoute', msg='VPN名称不为staticRoute')
                print('PPTP已添加')
                vpn.click_add()
                time.sleep(1)
                vpn.click_l2tpB()
                vpn.input_TunNames('staticRoute2')
                vpn.input_userNames('staticRoute2')
                vpn.input_password('staticRoute2')
                vpn.input_remoteInIp('4.3.2.1')
                vpn.input_remoteInIPMask('255.255.255.0')
                vpn.click_save()
                time.sleep(3)
                listtips2 = str(vpn.getText_byXpath(vpn.listtips2))
                self.assertEqual(listtips2, 'staticRoute2', msg='VPN2名称不为staticRoute2')
                print('L2TP已添加')
                # 修改静态路由 绑定PPTP接口
                routeconfig = RouteConfigPage(self.driver, self.url)
                routeconfig.click_NetworkConfig()
                time.sleep(0.5)
                routeconfig.click_Routeconfig()
                time.sleep(1)
                routeconfig.click_add()
                time.sleep(1)
                selProfiles = routeconfig.selelement_byName(routeconfig.selProfiles)
                time.sleep(1)
                try:
                    self.driver.implicitly_wait(2)
                    Select(selProfiles).select_by_value('(PPTPS)staticRoute')
                    time.sleep(0.5)
                    Select(selProfiles).select_by_value('(L2TPS)staticRoute2')
                except NoSuchElementException:
                    logger.info(u'静态路由无法绑定vpn接口（L2TP/PPTP），与参数表相符')
                    self.driver.implicitly_wait(10)
                    time.sleep(1)
                    routeconfig.click_modalhide()
                    time.sleep(0.5)
                    # 删除两条VPN
                    vpn = pptpL2tpPage(self.driver, self.url)
                    vpn.click_VPNConfig()
                    time.sleep(0.5)
                    vpn.click_pptpL2tp()
                    time.sleep(1)
                    vpn.click_delete1()
                    time.sleep(1)
                    vpn.click_ok()
                    time.sleep(2)
                    vpn.click_delete1()
                    time.sleep(1)
                    vpn.click_ok()
                    time.sleep(3)
                    # 断言
                    list_nodata = str(vpn.getText_byXpath(vpn.list_nodata))
                    self.assertEqual(list_nodata, nodata, msg='静态路由删除失败')
                    print('VPN已删除')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持L2TP/PPTP 静态路由绑定vpn接口，与参数表不符')
                    raise Exception(u'软件支持L2TP/PPTP 静态路由绑定vpn接口，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()

        logger.info('test_003_bandingInter passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

