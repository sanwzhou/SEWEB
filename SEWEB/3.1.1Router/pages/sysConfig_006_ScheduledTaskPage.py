#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 13:15
#@swzhou
'''
系统管理 - 计划任务界面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger = 'ScheduledTaskPage').getlog()

class ScheduledTaskPage(BasePage):
    ScheduledTaskM = getMenu('ScheduledTaskM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    ScheduledTask = (By.LINK_TEXT, ScheduledTaskM)  # 计划任务菜单

    add = (By.ID,'add')
    obj = ('obj') #生效对象
    selContent = ('selContent') #任务内容
    ID = (By.NAME,'ID') #任务名称
    selDay = ('selDay') #运行时间
    txtHour1 = (By.NAME,'txtHour1') #时
    txtMin1 = (By.NAME,'txtMin1') #分
    save = (By.ID,'save')
    list_obj = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span') #生效对象
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID,'delete')
    ok = (By.ID,'u-cfm-ok')
    tipsshowin = (By.CLASS_NAME, 'tips-show-in')

    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_ScheduledTask(self):
        self.find_element(*self.ScheduledTask).click()
        logger.info('点击计划任务菜单')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_ID(self, ID):
        self.find_element(*self.ID).clear()
        self.find_element(*self.ID).send_keys(ID)

    def input_txtHour1(self, txtHour1):
        self.find_element(*self.txtHour1).clear()
        self.find_element(*self.txtHour1).send_keys(txtHour1)

    def input_txtMin1(self, txtMin1):
        self.find_element(*self.txtMin1).clear()
        self.find_element(*self.txtMin1).send_keys(txtMin1)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)