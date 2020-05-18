#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 14:40
#@swzhou
'''
网络配置 - 端口映射 - DMZ
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'PortMapping_004_DMZPage').getlog()
from common.ReadConfig import getMenu

class DMZPage(BasePage):
    portMappingM = getMenu('portMappingM')
    DMZm = getMenu('DMZm')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    portMapping = (By.LINK_TEXT, portMappingM)  # 端口映射菜单
    DMZ = (By.LINK_TEXT,DMZm) #DMZ菜单

    DMZEn = (By.XPATH,'//input[@name="DMZEnable"and@value="on"]')
    DMZEs = ('//input[@name="DMZEnable"and@value="on"]')
    GlobalDMZ = (By.NAME,'GlobalDMZ')
    WAN1DMZ = (By.NAME,'WAN1DMZ')
    save = (By.ID,'save')
    DMZC = (By.XPATH,'//input[@name="DMZEnable"and@value="off"]')
    DMZCs = ('//input[@name="DMZEnable"and@value="off"]')

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_portMapping(self):
        self.find_element(*self.portMapping).click()
        logger.info('点击端口映射')

    def click_DMZ(self):
        self.find_element(*self.DMZ).click()
        logger.info('点击DMZ')

    def click_DMZEn(self):
        self.find_element(*self.DMZEn).click()

    def input_GlobalDMZ(self,GlobalDMZ):
        self.find_element(*self.GlobalDMZ).clear()
        self.find_element(*self.GlobalDMZ).send_keys(GlobalDMZ)

    def input_WAN1DMZ(self,WAN1DMZ):
        self.find_element(*self.WAN1DMZ).clear()
        self.find_element(*self.WAN1DMZ).send_keys(WAN1DMZ)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_DMZC(self):
        self.find_element(*self.DMZC).click()