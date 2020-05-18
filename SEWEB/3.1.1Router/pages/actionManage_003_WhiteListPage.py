#! -*-conding:utf-8 -*-
#@Time: 2019/2/18 0018 11:32
#@swzhou
'''
行为管理 - 白名单
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'WhiteListPage').getlog()
from common.ReadConfig import getMenu

class WhiteListPage(BasePage):
    WhitelistM = getMenu('WhitelistM')
    globalconfigM = getMenu('globalconfigM')

    BehaviorManagement = (By.XPATH, '//span[@data-local="{BehaviorManagement}"]') #行为管理菜单
    Whitelist = (By.LINK_TEXT, WhitelistM)  # 白名单菜单
    globalconfig = (By.LINK_TEXT,globalconfigM) #全局配置

    add = (By.ID,'add')
    ALI = (By.XPATH,'//input[@name="type"and@value="{ALI}"]')
    QQ = (By.XPATH,'//input[@name="type"and@value="QQ"]')
    acount = (By.NAME,'acount')
    modalhide = (By.ID,'modal-hide')
    QQEn = (By.XPATH,'//input[@name="ExceptQQEnable"and@value="on"]')
    QQC = (By.XPATH, '//input[@name="ExceptQQEnable"and@value="off"]')
    AliEn = (By.XPATH, '//input[@name="ExceptAliEnable"and@value="on"]')
    AliC = (By.XPATH, '//input[@name="ExceptAliEnable"and@value="off"]')

    maxpagenums = (By.XPATH,'//*[@id="1"]/div/div/div[2]/div/input')
    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页
    next = (By.ID,'next') # 界面页数框下一页

    def click_BehaviorManagement(self):
        self.find_element(*self.BehaviorManagement).click()
        logger.info('点击行为管理')

    def click_Whitelist(self):
        self.find_element(*self.Whitelist).click()
        logger.info('点击白名单')

    def click_globalconfig(self):
        self.find_element(*self.globalconfig).click()
        logger.info('点击全局配置')

    def click_add(self):
        self.find_element(*self.add).click()

    def click_ALI(self):
        self.find_element(*self.ALI).click()

    def click_QQ(self):
        self.find_element(*self.QQ).click()

    def input_acount(self,acount):
        self.find_element(*self.acount).clear()
        self.find_element(*self.acount).send_keys(acount)

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def click_QQEn(self):
        self.find_element(*self.QQEn).click()

    def click_QQC(self):
        self.find_element(*self.QQC).click()

    def click_AliEn(self):
        self.find_element(*self.AliEn).click()

    def click_AliC(self):
        self.find_element(*self.AliC).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()

    def input_maxpagenums(self,maxpagenums):
        self.find_element(*self.maxpagenums).clear()
        self.find_element(*self.maxpagenums).send_keys(maxpagenums)

    def click_next(self):
        self.find_element(*self.next).click()