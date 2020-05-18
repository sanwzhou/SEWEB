#! -*-conding:utf-8 -*-
#@Time: 2019/3/12 0012 13:24
#@swzhou
'''
PPTP & L2TP VPN
'''

import time
import unittest
from common.LogGen import LogGen
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb,gettelnet
from common.loginRoute import login
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'VPNconfig_002_PPTP&L2TP').getlog()
vpnRouteWan = getweb('vpnRouteWan')
vpnRouteLan = getweb('vpnRouteLan')
host = gettelnet('host')
vpnRouteUrl = 'http://' + vpnRouteWan + ':8081'
ConnectState = getAssertText('ConnectState')

class PPTPL2TP(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_PPTPserver(self):
        u'''PPTPserver'''

        vpnRouteLan = getweb('vpnRouteLan')
        host = gettelnet('host')
        StateVPN2 = getAssertText('StateVPN2')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        pptpl2tp = pptpL2tpPage(self.driver,self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_PPTPGlobalSet()
        time.sleep(0.5)
        pptpl2tp.click_pptpserverEn()
        pptpl2tp.input_priDns('114.114.114.114')
        pptpl2tp.click_save()
        time.sleep(1)
        pptpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.pptpserverEs,'checked')
        if pptpSs == 'true':
            logger.info(u'pptpserver已开启')
        else:
            CapPic(self.driver)
            logger.info(u'pptpserver未开启')
            return Exception(u'pptpserver未开启')

        pptpl2tp.click_add()
        time.sleep(1)
        pptpl2tp.click_workMode1()
        pptpl2tp.click_workModepptp()
        pptpl2tp.input_TunNames('testS')
        seluserType = pptpl2tp.selelement_byName(pptpl2tp.seluserType)
        Select(seluserType).select_by_value('lantolan')
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(vpnRouteLan)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_saveS()
        time.sleep(2)

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
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
        # print('WAN1_ip=',WAN1_ip)
        time.sleep(1)
        self.driver.quit()

        # 另外一台路由器 配置pptp Client
        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_add()
        time.sleep(2)
        pptpl2tp.click_workMode2()
        pptpl2tp.click_workModepptp()
        pptpl2tp.input_TunNames('testS')
        pptpl2tp.input_TunNamesIP(WAN1_ip)
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(host)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_save()
        time.sleep(2)

        i = 0
        while i < 100:
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            list_status = pptpl2tp.getText_byXpath(pptpl2tp.list_status)
            print(list_status)
            if list_status == StateVPN2 :
                logger.info(u'PPTP 已建立')
                break
            else:
                time.sleep(3)
                i += 1
        else:
            logger.info(u'pptp 未建立成功')
            CapPic(self.driver)
            raise Exception(u'pptp未建立成功')
        self.driver.quit()

        logger.info('test_001_PPTPserver passed')

    def test_002_PPTPclient(self):
        u'''PPTPclient'''

        vpnRouteLan = getweb('vpnRouteLan')
        host = gettelnet('host')
        StateVPN2 = getAssertText('StateVPN2')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        pptpl2tp = pptpL2tpPage(self.driver,self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')
        pptpl2tp.click_add()
        time.sleep(2)
        pptpl2tp.click_workMode2()
        pptpl2tp.click_workModepptp()
        pptpl2tp.input_TunNames('testC')
        pptpl2tp.input_TunNamesIP(vpnRouteWan)
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(vpnRouteLan)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_save()
        time.sleep(2)
        self.driver.quit()

        # 另外一台路由器 配置pptp Server
        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        pptpl2tp.click_PPTPGlobalSet() #语言问题 待修改成xpath
        time.sleep(0.5)
        pptpl2tp.click_pptpserverEn()
        pptpl2tp.input_priDns('114.114.114.114')
        pptpl2tp.click_save()
        time.sleep(1)
        pptpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.pptpserverEs, 'checked')
        if pptpSs == 'true':
            logger.info(u'pptpserver已开启')
        else:
            CapPic(self.driver)
            logger.info(u'pptpserver未开启')
            return Exception(u'pptpserver未开启')

        pptpl2tp.click_add()
        time.sleep(1)
        pptpl2tp.click_workMode1()
        pptpl2tp.click_workModepptp()
        pptpl2tp.input_TunNames('testC')
        seluserType = pptpl2tp.selelement_byName(pptpl2tp.seluserType)
        Select(seluserType).select_by_value('lantolan')
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(host)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_saveS()
        time.sleep(2)

        i = 0
        while i < 100:
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            list_status = pptpl2tp.getText_byXpath(pptpl2tp.list_status)
            print(list_status)
            if list_status == StateVPN2 :
                logger.info(u'PPTP 已建立')
                break
            else:
                time.sleep(3)
                i += 1
        else:
            logger.info(u'pptp 未建立成功')
            CapPic(self.driver)
            raise Exception(u'pptp未建立成功')
        self.driver.quit()

        logger.info('test_002_PPTPclient passed')

    def test_003_L2tpserver(self):
        u'''L2tpserver'''

        vpnRouteLan = getweb('vpnRouteLan')
        host = gettelnet('host')
        StateVPN2 = getAssertText('StateVPN2')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        pptpl2tp = pptpL2tpPage(self.driver,self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_l2tpGlobalSet()
        time.sleep(0.5)
        pptpl2tp.click_L2tpserverEn()
        pptpl2tp.input_priDns('114.114.114.114')
        pptpl2tp.click_save()
        time.sleep(1)
        pptpl2tp.click_l2tpGlobalSet()
        time.sleep(0.5)
        l2tpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.L2tpserverEs,'checked')
        if l2tpSs == 'true':
            logger.info(u'L2tpserver已开启')
        else:
            CapPic(self.driver)
            logger.info(u'L2tpserver未开启')
            return Exception(u'L2tpserver未开启')

        pptpl2tp.click_Tunnellist()
        time.sleep(0.5)
        pptpl2tp.click_add()
        time.sleep(1)
        pptpl2tp.click_workMode1()
        pptpl2tp.click_workModel2tp()
        pptpl2tp.input_TunNames('testS')
        seluserType = pptpl2tp.selelement_byName(pptpl2tp.seluserType)
        Select(seluserType).select_by_value('lantolan')
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(vpnRouteLan)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_saveS()
        time.sleep(2)

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
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
        # print('WAN1_ip=',WAN1_ip)
        time.sleep(1)
        self.driver.quit()

        # 另外一台路由器 配置pptp Client
        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_add()
        time.sleep(2)
        pptpl2tp.click_workMode2()
        pptpl2tp.click_workModel2tp()
        pptpl2tp.input_TunNames('testS')
        pptpl2tp.input_TunNamesIP(WAN1_ip)
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(host)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_save()
        time.sleep(5)

        i = 0
        while i < 100:
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            list_status = pptpl2tp.getText_byXpath(pptpl2tp.list_status)
            print(list_status)
            if list_status == StateVPN2 :
                logger.info(u'L2tp 已建立')
                break
            else:
                time.sleep(3)
                i += 1
        else:
            logger.info(u'L2tp 未建立成功')
            CapPic(self.driver)
            raise Exception(u'L2tp未建立成功')
        self.driver.quit()

        logger.info('test_003_L2tpserver passed')

    def test_004_L2tpclient(self):
        u'''L2tpclient'''

        vpnRouteLan = getweb('vpnRouteLan')
        host = gettelnet('host')
        StateVPN2 = getAssertText('StateVPN2')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        pptpl2tp = pptpL2tpPage(self.driver,self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_add()
        time.sleep(2)
        pptpl2tp.click_workMode2()
        pptpl2tp.click_workModel2tp()
        pptpl2tp.input_TunNames('testC')
        pptpl2tp.input_TunNamesIP(vpnRouteWan)
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(vpnRouteLan)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_save()
        time.sleep(2)
        self.driver.quit()

        # 另外一台路由器 配置pptp Server
        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        # 操作删除 以访已有规则
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            pptpl2tp.find_ok()
        except NoSuchElementException:
            try:
                pptpl2tp.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('VPN隧道列表为空')

        pptpl2tp.click_l2tpGlobalSet() #语言问题待修改成xpath
        time.sleep(0.5)
        pptpl2tp.click_L2tpserverEn()
        pptpl2tp.input_priDns('114.114.114.114')
        pptpl2tp.click_save()
        time.sleep(1)
        pptpl2tp.click_l2tpGlobalSet()
        time.sleep(0.5)
        l2tpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.L2tpserverEs, 'checked')
        if l2tpSs == 'true':
            logger.info(u'L2tpserver已开启')
        else:
            CapPic(self.driver)
            logger.info(u'L2tpserver未开启')
            return Exception(u'L2tpserver未开启')

        pptpl2tp.click_Tunnellist()
        time.sleep(0.5)
        pptpl2tp.click_add()
        time.sleep(1)
        pptpl2tp.click_workMode1()
        pptpl2tp.click_workModel2tp()
        pptpl2tp.input_TunNames('testC')
        seluserType = pptpl2tp.selelement_byName(pptpl2tp.seluserType)
        Select(seluserType).select_by_value('lantolan')
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp(host)
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_saveS()
        time.sleep(2)

        i = 0
        while i < 100:
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            list_status = pptpl2tp.getText_byXpath(pptpl2tp.list_status)
            print(list_status)
            if list_status == StateVPN2 :
                logger.info(u'L2tp 已建立')
                break
            else:
                time.sleep(3)
                i += 1
        else:
            logger.info(u'L2tp 未建立成功')
            CapPic(self.driver)
            raise Exception(u'L2tp未建立成功')
        self.driver.quit()

        logger.info('test_004_L2tpclient passed')

    def tearDown(self):
        nodata = getAssertText('nodata')

        #删除VPN
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(1)
        pptpl2tp.click_ok()
        time.sleep(2)
        list_nodata = pptpl2tp.getText_byXpath(pptpl2tp.list_nodata)
        if list_nodata == nodata:
            logger.info(u'R1 VPN 已删除')
        else:
            CapPic(self.driver)
            logger.info(u'R1 VPN删除失败')
            raise Exception(u'R1 VPN删除失败')

        pptpl2tp.click_PPTPGlobalSet()
        time.sleep(0.5)
        pptpl2tp.click_pptpserverC()
        pptpl2tp.click_save()
        time.sleep(1)
        pptpl2tp.click_PPTPGlobalSet()
        time.sleep(0.5)
        pptpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.pptpserverCs, 'checked')
        if pptpSs == 'true':
            logger.info(u'pptpserver已关闭')
        else:
            CapPic(self.driver)
            logger.info(u'pptpserver未关闭')
            return Exception(u'pptpserver未关闭')
        pptpl2tp.click_l2tpGlobalSet()
        time.sleep(0.5)
        pptpl2tp.click_L2tpserverC()
        pptpl2tp.click_saveSl2tp()
        time.sleep(1)
        pptpl2tp.click_l2tpGlobalSet()
        time.sleep(0.5)
        l2tpSs = pptpl2tp.getAttribute_byXpath(pptpl2tp.L2tpserverCs, 'checked')
        if l2tpSs == 'true':
            logger.info(u'L2tpserver已关闭')
        else:
            CapPic(self.driver)
            logger.info(u'L2tpserver未关闭')
            return Exception(u'L2tpserver未关闭')
        self.driver.quit()

        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_VPNConfig()
        time.sleep(0.5)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(1)
        pptpl2tp.click_ok()
        time.sleep(2)
        try: #VPN 路由器是中文简体，在测试其他语言版本时，删除后的nodata会不一致
            pptpl2tp.find_list_nodataX()
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'R2 ipsec删除失败')
            raise Exception(u'R2 ipsec删除失败')
        else:
            logger.info(u'R2 ipsec 已删除')
        # list_nodata = pptpl2tp.getText_byXpath(pptpl2tp.list_nodata)
        # if list_nodata == nodata:
        #     logger.info(u'R2 VPN 已删除')
        # else:
        #     CapPic(self.driver)
        #     logger.info(u'R2 VPN删除失败')
        #     raise Exception(u'R2 VPN删除失败')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()


