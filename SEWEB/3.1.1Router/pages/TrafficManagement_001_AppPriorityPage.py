#! -*-conding:utf-8 -*-
#@Time: 2019/1/22 0022 15:55
#@swzhou
'''
流量管理-应用优先
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'AppPriorityPage').getlog()
from common.ReadConfig import getMenu

class AppPriorityPage(BasePage):
    AppPriorityM = getMenu('AppPriorityM')

    TrafficManagement = (By.XPATH, '//span[@data-local="{TrafficManagement}"]') #流量管理菜单
    AppPriority = (By.LINK_TEXT, AppPriorityM)  # 应用优先
    #应用优先
    appType = ('appType')
    changeAppType = (By.ID,'changeAppType')
    list_name1 = ('//*[@id="1"]/div/div[1]/div[1]/table/tbody/tr[1]/td[3]/span')
    checkOpen = (By.ID,'checkOpen')
    checkOpens = ('checkOpen')
    add = (By.ID,'add')
    delete = (By.ID,'delete')
    import1 = (By.ID,'import')
    export = (By.ID,'export')
    listnodata = ('//*[@id="1"]/div/div[1]/div[1]/table/tbody/tr[1]/td/div')


    def click_TrafficManagement(self):
        self.find_element(*self.TrafficManagement).click()
        logger.info('点击流量管理')

    def click_AppPriority(self):
        self.find_element(*self.AppPriority).click()
        logger.info('点击应用优先')

    def click_changeAppType(self):
        self.find_element(*self.changeAppType).click()

    def click_checkOpen(self):
        self.find_element(*self.checkOpen).click()

    def find_add(self):
        self.exist_element(*self.add)

    def find_delete(self):
        self.exist_element(*self.delete)

    def find_import1(self):
        self.exist_element(*self.import1)

    def find_export(self):
        self.exist_element(*self.export)



