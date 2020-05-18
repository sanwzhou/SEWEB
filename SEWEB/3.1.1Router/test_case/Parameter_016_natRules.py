#! -*-conding:utf-8 -*-
#@Time: 2019/2/15 0015 14:38
#@swzhou
'''
转发规则：
端口映射
NAT规则
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from pages.PortMapping_002_staticMappingPage import staticMappingPage
from pages.PortMapping_003_natRulePage import natRulePage
from pages.PortMapping_004_DMZpage import DMZPage
from pages.PortMapping_001_UPNPpage import UPNPpage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_016_natRules').getlog()

class natRules(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        ststicmap = staticMappingPage(self.driver,self.url)
        ststicmap.click_NetworkConfig()
        time.sleep(0.5)
        ststicmap.click_portMapping()
        time.sleep(1)
        # pass

    def test_001_staticMapping(self):
        u'''端口映射'''
        ststicmap = staticMappingPage(self.driver, self.url)
        ststicmap.click_add()
        time.sleep(1)
        ststicmap.input_IDs('test')
        ststicmap.input_IPs('1.2.3.4')
        Selprotocols = ststicmap.selelement_byName(ststicmap.Protocols)
        Select(Selprotocols).select_by_value('1')  # 1:tcp 2:udp 3:tcp/udp
        time.sleep(0.5)
        Select(Selprotocols).select_by_value('2')
        time.sleep(0.5)
        Select(Selprotocols).select_by_value('3')
        time.sleep(0.5)
        ststicmap.input_inS('80')
        ststicmap.input_inE('80')
        ststicmap.input_outS('80')
        ststicmap.input_outE('80')
        self.driver.quit()
        logger.info('test_001_staticMapping passed')

    def test_002_easyIP_one2one(self):
        u'''NAT规则'''
        natRule = natRulePage(self.driver, self.url)
        natRule.click_natRule()
        time.sleep(1)
        natRule.click_add()
        time.sleep(1)
        natRule.input_RuleIDs('easyIPtest')
        natRule.click_typeOne2one()
        time.sleep(0.5)
        natRule.click_typeeasyIp()
        time.sleep(0.5)
        natRule.input_InFromIPs('192.168.1.200')
        natRule.input_InEndIPs('192.168.1.202')
        natRule.input_OutIPs('192.169.122.250')
        self.driver.quit()
        logger.info('test_002_easyIP_one2one passed')

    def test_003_DMZ_UPNP(self):
        u'''DMZ_UPNP'''
        dmz = DMZPage(self.driver, self.url)
        dmz.click_DMZ()
        time.sleep(1)
        dmz.click_DMZEn()
        dmz.input_GlobalDMZ('0.0.0.0')
        dmz.input_WAN1DMZ('0.0.0.0')

        upnp = UPNPpage(self.driver, self.url)
        upnp.click_UPnP()
        time.sleep(1)
        switch = upnp.getAttribute_byId(upnp.checkOn, 'checktype')  # checktype 0未开启，1开启
        self.assertEqual(switch,'0',msg='UPNP默认未关闭')

        self.driver.quit()
        logger.info('test_003_DMZ_UPNP passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

