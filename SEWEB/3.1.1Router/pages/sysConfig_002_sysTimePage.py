#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 11:51
#@swzhou
'''
系统管理 - 系统时间界面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'sysTimePage').getlog()
from common.ReadConfig import getMenu

class sysTimePage(BasePage):
    SystemTimeM = getMenu('SystemTimeM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    SystemTime = (By.LINK_TEXT, SystemTimeM)  # 时钟管理菜单

    SntpEns = ('//input[@name="SntpEnable"and@value="on"]')
    withInternet1 = ('//*[@id="1"]/table/tbody/tr[3]/td[2]/span[2]') #网络时间同步

    dates = ('dates')
    NTPServerIP = (By.NAME,'NTPServerIP')
    save = (By.ID,'save')

    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_SystemTime(self):
        self.find_element(*self.SystemTime).click()
        logger.info('点击时钟管理菜单')

    def input_NTPServerIP(self, NTPServerIP):
        self.find_element(*self.NTPServerIP).clear()
        self.find_element(*self.NTPServerIP).send_keys(NTPServerIP)

    def click_save(self):
        self.find_element(*self.save).click()
