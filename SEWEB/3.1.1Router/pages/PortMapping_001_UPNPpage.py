#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 11:08
#@swzhou
'''
网络配置 - UPNP
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'PortMapping_001_UPNPpage').getlog()
from common.ReadConfig import getMenu

class UPNPpage(BasePage):
    portMappingM = getMenu('portMappingM')
    UPnPm = getMenu('UPnPm')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    portMapping = (By.LINK_TEXT,portMappingM) #端口映射菜单
    UPnP = (By.LINK_TEXT,UPnPm) #UPnP菜单

    checkOnc = (By.ID,'checkOn')
    checkOn = ('checkOn')
    refreshTable = (By.ID,'refreshTable')
    list_tips1 = ('//*[@id="4"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_portMapping(self):
        self.find_element(*self.portMapping).click()
        logger.info('点击端口映射')

    def click_UPnP(self):
        self.find_element(*self.UPnP).click()
        logger.info('点击UPnP')

    def click_checkOnc(self):
        self.find_element(*self.checkOnc).click()

    def click_refreshTable(self):
        self.find_element(*self.refreshTable).click()