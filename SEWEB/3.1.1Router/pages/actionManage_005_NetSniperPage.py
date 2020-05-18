#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 17:21
#@swzhou
'''
行为管理 - 内网网络尖兵
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'NetSniperPage').getlog()
from common.ReadConfig import getMenu

class NetSniperPage(BasePage):
    NetSniperM = getMenu('NetSniperM')
    NetSniperconfigM = getMenu('NetSniperconfigM')

    BehaviorManagement = (By.XPATH, '//span[@data-local="{BehaviorManagement}"]') #行为管理菜单
    NetSniper = (By.LINK_TEXT,NetSniperM)  # 内网网络尖兵菜单
    NetSniperconfig = (By.LINK_TEXT,NetSniperconfigM) # 网络尖兵配置菜单

    listnodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    enable = ('enable')

    def click_BehaviorManagement(self):
        self.find_element(*self.BehaviorManagement).click()
        logger.info('点击行为管理')

    def click_NetSniper(self):
        self.find_element(*self.NetSniper).click()
        logger.info('点击内网网络尖兵')

    def click_NetSniperconfig(self):
        self.find_element(*self.NetSniperconfig).click()
        logger.info('点击网络尖兵配置')


