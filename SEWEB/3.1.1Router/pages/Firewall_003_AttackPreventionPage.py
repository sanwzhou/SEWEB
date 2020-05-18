#! -*-conding:utf-8 -*-
#@Time: 2019/2/15 0015 16:00
#@swzhou
'''
防火墙 - 攻击防御
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'AttackPreventionPage').getlog()
from common.ReadConfig import getMenu

class AttackPreventionPage(BasePage):
    AttackPreventionM = getMenu('AttackPreventionM')

    FireWall = (By.XPATH, '//span[@data-local="{fireWall}"]') #防火墙菜单
    AttackPrevention = (By.LINK_TEXT, AttackPreventionM)  # 攻击防护菜单

    # ARP欺骗主动防御
    ArpBroadcastIntervalVal = ('ArpBroadcastIntervalVal')
    ArpBroadcastIntervalVals = ('ArpBroadcastEnable')
    ArpBroadcastIntervalValEn = (By.NAME,'ArpBroadcastEnable')
    # FLOOD攻击防御 UDP
    UDPFlood = ('max_udp_rxpps')
    UDPFloods = ('UDPFlood')
    UDPFloodEn = (By.NAME,'UDPFlood')
    # FLOOD攻击防御 ICMP
    ICMPFlood = ('max_icmp_rxpps')
    ICMPFloods = ('ICMPFlood')
    ICMPFloodEn=(By.NAME,'ICMPFlood')
    # FLOOD攻击防御 SYN
    SYNFlood = ('max_syn_rxpps')
    SYNFloods = ('max_syn_rxpps')
    SYNFloodEn = (By.NAME,'SYNFlood')
    # IP欺骗防御
    IPCheats = ('IPCheat')
    IPCheateEn = (By.NAME,'IPCheat')
    # DDoS攻击防御
    DDOSEnables = ('DDOSEnable')
    DDOSEnableEn = (By.NAME,'DDOSEnable')
    # 外网PING防御
    PingDisables = ('PingDisable')
    PingDisableEn = (By.NAME,'PingDisable')

    def click_FireWall(self):
        self.find_element(*self.FireWall).click()
        logger.info('点击防火墙')

    def click_AttackPrevention(self):
        self.find_element(*self.AttackPrevention).click()
        logger.info('点击攻击防护菜单')

    def click_ArpBroadcastIntervalValEn(self):
        self.find_element(*self.ArpBroadcastIntervalValEn).click()

    def click_UDPFloodEn(self):
        self.find_element(*self.UDPFloodEn).click()

    def click_ICMPFloodEn(self):
        self.find_element(*self.ICMPFloodEn).click()

    def click_SYNFloodEn(self):
        self.find_element(*self.SYNFloodEn).click()

    def click_IPCheateEn(self):
        self.find_element(*self.IPCheateEn).click()

    def click_DDOSEnableEn(self):
        self.find_element(*self.DDOSEnableEn).click()

    def click_PingDisableEn(self):
        self.find_element(*self.PingDisableEn).click()
