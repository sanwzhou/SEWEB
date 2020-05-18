#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 13:49
#@swzhou
'''
系统管理 - 网络工具界面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ToolsPage').getlog()
from common.ReadConfig import getMenu

class ToolsPage(BasePage):
    ToolsM = getMenu('ToolsM')
    TraceRouteM = getMenu('TraceRouteM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    Tools = (By.LINK_TEXT, ToolsM)  # 网络工具菜单
    #ping
    ping = ('//*[@id="1"]/table/tbody/tr[3]/td[1]/label') #ping次数
    # TraceRoute
    TraceRoute = (By.LINK_TEXT,TraceRouteM)  # TraceRoute菜单
    maxTTL1 = ('//*[@id="2"]/table/tbody/tr[3]/td[1]/label')  #最大TTL

    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_Tools(self):
        self.find_element(*self.Tools).click()
        logger.info('点击网络工具菜单')

    def click_TraceRoute(self):
        self.find_element(*self.TraceRoute).click()
        logger.info('点击TraceRoute菜单')
