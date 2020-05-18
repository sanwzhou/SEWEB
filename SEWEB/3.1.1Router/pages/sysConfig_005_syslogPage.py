#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 11:38
#@swzhou
'''
系统管理 - 系统日志界面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'syslogPage').getlog()
from common.ReadConfig import getMenu

class syslogPage(BasePage):
    SyslogM = getMenu('SyslogM')
    SyslogServerM = getMenu('SyslogServerM')
    LogtypeM = getMenu('LogtypeM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    Syslog = (By.LINK_TEXT, SyslogM)  # 系统日志菜单
    #系统日志
    export1 = ('export')

    # 日志服务器
    SyslogServer = (By.LINK_TEXT, SyslogServerM)  #日志服务器菜单
    SyslogCs = ('//input[@name="SyslogEnable"and@value="off"]')
    syslogEn = (By.XPATH,'//input[@name="SyslogEnable"and@value="on"]')
    syslogEs = ('//input[@name="SyslogEnable"and@value="on"]')
    syslogC = (By.XPATH, '//input[@name="SyslogEnable"and@value="off"]')
    ServerIp = (By.NAME,'ServerIp')
    ServerPort = (By.NAME,'ServerPort')
    save = (By.ID,'save')

    # 日志类型
    Logtype = (By.LINK_TEXT, LogtypeM)  # 日志类型菜单

    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_Syslog(self):
        self.find_element(*self.Syslog).click()
        logger.info('点击系统日志菜单')

    def click_SyslogServer(self):
        self.find_element(*self.SyslogServer).click()
        logger.info('点击日志服务器菜单')

    def click_Logtype(self):
        self.find_element(*self.Logtype).click()
        logger.info('点击日志类型菜单')

    def click_syslogEn(self):
        self.find_element(*self.syslogEn).click()

    def click_syslogC(self):
        self.find_element(*self.syslogC).click()

    def input_ServerIp(self, ServerIp):
        self.find_element(*self.ServerIp).clear()
        self.find_element(*self.ServerIp).send_keys(ServerIp)

    def input_ServerPort(self, ServerPort):
        self.find_element(*self.ServerPort).clear()
        self.find_element(*self.ServerPort).send_keys(ServerPort)

    def click_save(self):
        self.find_element(*self.save).click()
