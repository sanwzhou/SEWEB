#! -*-conding:utf-8 -*-
#@Time: 2019/9/6 0006 15:43
#@swzhou
'''
系统配置 - 云服务
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger = 'CloudServePage').getlog()

class CloudServePage(BasePage):
    CloudServeM = getMenu('CloudServeM')
    bindingM = getMenu('bindingM') #云页面几个超链接
    registerM = getMenu('registerM')
    loginM = getMenu('loginM')
    helpM = getMenu('helpM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    CloudServe = (By.LINK_TEXT, CloudServeM)  # 云服务 菜单

    cloudEn = (By.XPATH, '//input[@name="cloudEn"and@value="on"]')
    cloudEns = ('//input[@name="cloudEn"and@value="on"]')
    cloudC = (By.XPATH, '//input[@name="cloudEn"and@value="off"]')
    cloudCs = ('//input[@name="cloudEn"and@value="off"]')

    webSN = ('//*[@id="2"]/table/tbody/tr[2]/td[2]/span')
    code = ('//*[@id="2"]/table/tbody/tr[3]/td[2]') #激活码
    save = (By.ID,'save')
    binding = (By.LINK_TEXT,'bindingM')
    register = (By.LINK_TEXT, 'registerM')
    login = (By.LINK_TEXT, 'loginM ')
    help = (By.LINK_TEXT, 'helpM')


    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_CloudServe(self):
        self.find_element(*self.CloudServe).click()
        logger.info('点击云服务菜单')

    def click_cloudEn(self):
        self.find_element(*self.cloudEn).click()

    def click_cloudC(self):
        self.find_element(*self.cloudC).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_binding(self):
        self.find_element(*self.binding).click()

    def click_register(self):
        self.find_element(*self.register).click()

    def click_login(self):
        self.find_element(*self.login).click()

    def find_help(self):
        self.exist_element(*self.help).click()
