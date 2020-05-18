#! -*-conding:utf-8 -*-
#@Time: 2019/2/21 0021 17:30
#@swzhou
'''
系统监控 - 流量监控
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger='flowWatchpage').getlog()


class flowWatchpage(BasePage):
    flowWatchM = getMenu('flowWatchM')

    systemWatch = (By.XPATH, '//span[@data-local="{systemWatch}"]') #系统监控
    flowWatch = (By.LINK_TEXT,flowWatchM)  #流量监控

    checkOpen = (By.ID,'checkOpen')
    checkOpens = ('checkOpen')
    export = (By.ID,'export')
    selrefresh = ('//*[@id="btns"]/ul/li[1]/select')
    list_apply1 = ('//*[@id="table"]/div/div[1]/table/tbody/tr[1]/td[2]/span')
    list_apply2 = ('//*[@id="table"]/div/div[1]/table/tbody/tr[2]/td[2]/span')
    list_apply3 = ('//*[@id="table"]/div/div[1]/table/tbody/tr[3]/td[2]/span')
    list_apply4 = ('//*[@id="table"]/div/div[1]/table/tbody/tr[4]/td[2]/span')
    list_apply5 = ('//*[@id="table"]/div/div[1]/table/tbody/tr[5]/td[2]/span')
    fresh = (By.ID,'fresh')

    def click_systemWatch(self):
        self.find_element(*self.systemWatch).click()
        logger.info('点击系统监控')

    def click_flowWatch(self):
        self.find_element(*self.flowWatch).click()
        logger.info('点击流量监控')

    def click_checkOpen(self):
        self.find_element(*self.checkOpen).click()

    def click_export(self):
        self.find_element(*self.export).click()

    def click_fresh(self):
        self.find_element(*self.fresh).click()





