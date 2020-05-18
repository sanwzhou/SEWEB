#! -*-conding:utf-8 -*-
#@Time: 2019/3/5 0005 14:44
#@swzhou
'''
负载均衡 页面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger = 'loadBalancingPage').getlog()

class loadBalancingPage(BasePage):
    loadBalancingM = getMenu('loadBalancingM') #负载均衡

    wirelessExtension = (By.XPATH, '//span[@data-local="{wirelessExtension}"]')
    loadBalancing = (By.LINK_TEXT,loadBalancingM)

    add = (By.ID,'addModal')
    loadBalanceNames = (By.NAME,'loadBalanceNames')
    selAP1 = (By.XPATH, '//*[@id="left_AP"]/option[1]')
    toright = (By.ID, 'toright')
    save = (By.ID,'save')
    list_state = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    checkOpen = (By.ID,'checkOpen')
    checkOpens = ('checkOpen')
    list_del1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span[2]')
    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 组1页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_wirelessExtension(self):
        self.find_element(*self.wirelessExtension).click()
        logger.info('点击无线扩展')

    def click_loadBalancing(self):
        self.find_element(*self.loadBalancing).click()
        logger.info('点击负载均衡')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_loadBalanceNames(self, loadBalanceNames):
        self.find_element(*self.loadBalanceNames).clear()
        self.find_element(*self.loadBalanceNames).send_keys(loadBalanceNames)

    def click_selAP1(self):
        self.find_element(*self.selAP1).click()

    def click_selAP2(self):
        self.find_element(*self.selAP2).click()

    def click_selAP3(self):
        self.find_element(*self.selAP3).click()

    def click_selAP4(self):
        self.find_element(*self.selAP4).click()

    def click_toright(self):
        self.find_element(*self.toright).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_checkOpen(self):
        self.find_element(*self.checkOpen).click()

    def click_list_del1(self):
        self.find_element(*self.list_del1).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()