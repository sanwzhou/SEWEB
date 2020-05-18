#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 16:44
#@swzhou
'''
系统对象 - 时间计划
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'sysObj_timePlanPage').getlog()
from common.ReadConfig import getMenu

class timePlanPage(BasePage):
    timePlanM = getMenu('timePlanM')

    sysObj = (By.XPATH, '//span[@data-local="{sysObj}"]') #系统对象菜单
    timePlan = (By.LINK_TEXT, timePlanM)  # 时间计划菜单

    add = (By.ID,'add')
    TimeRangeName = (By.NAME,'TimeRangeName')
    save = (By.ID,'save')
    listName = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    delete = (By.XPATH,'//*[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    listnodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID,'delete')
    tipsshowin = (By.CLASS_NAME,'tips-show-in')
    list_name5 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[2]/span')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_sysObj(self):
        self.find_element(*self.sysObj).click()
        logger.info('点击系统对象')

    def click_timePlan(self):
        self.find_element(*self.timePlan).click()
        logger.info('点击时间计划')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_TimeRangeName(self, TimeRangeName):
        self.find_element(*self.TimeRangeName).clear()
        self.find_element(*self.TimeRangeName).send_keys(TimeRangeName)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()