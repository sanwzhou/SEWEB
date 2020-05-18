#! -*-conding:utf-8 -*-
#@Time: 2019/1/30 0030 13:47
#@swzhou
'''
无线扩展 - 软件管理
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'APSoftwarePage').getlog()
from common.ReadConfig import getMenu

class APSoftwarePage(BasePage):
    APsoftwareM = getMenu('APsoftwareM') #软件管理

    wirelessExtension = (By.XPATH, '//span[@data-local="{wirelessExtension}"]')
    #AP软件升级页面 2.6.3
    updatesoftware = (By.NAME,'updatesoftware')
    uttupdate = (By.ID,'uttupdate')
    #AC软件管理页面
    APsoftware = (By.LINK_TEXT, APsoftwareM)
    serach = (By.XPATH,'//input[@data-local="{enterSearchContent}"]')
    serachB = (By.CLASS_NAME,'icon-search')
    list_version1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    list_sel1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input')
    list_sel3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[1]/input')
    upDataLocal = (By.ID,'upDataLocal') #手动更新
    chooseFile = (By.ID,'chooseFile')
    demo_upgrade = (By.ID,'demo_upgrade')
    ok = (By.ID,'u-cfm-ok')
    oks = ('u-cfm-ok')
    #002
    list_selall = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    checkUpdata = (By.ID,'checkUpdata') #检测更新
    list_updata1 = (By.XPATH,'//a[@data-primarykey="0"and@id="upData"]')
    tipsshowin = ('tips-show-in')
    upData = (By.ID,'upData') #自动更新
    list_status1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]')

    def click_wirelessExtension(self):
        self.find_element(*self.wirelessExtension).click()
        logger.info('点击无线扩展')

    def click_APsoftware(self):
        self.find_element(*self.APsoftware).click()
        logger.info('点击软件管理')

    def input_updatesoftware(self,updatesoftware):
        self.find_element(*self.updatesoftware).clear()
        self.find_element(*self.updatesoftware).send_keys(updatesoftware)

    def click_uttupdate(self):
        self.find_element(*self.uttupdate).click()

    def input_serach(self,serach):
        self.find_element(*self.serach).clear()
        self.find_element(*self.serach).send_keys(serach)

    def click_serachB(self):
        self.find_element(*self.serachB).click()

    def click_list_sel1(self):
        self.find_element(*self.list_sel1).click()

    def click_list_sel3(self):
        self.find_element(*self.list_sel3).click()

    def click_upDataLocal(self):
            self.find_element(*self.upDataLocal).click()

    def find_upDataLocal(self):
            self.exist_element(*self.upDataLocal)

    def click_chooseFile(self):
        self.find_element(*self.chooseFile).click()

    def click_demo_upgrade(self):
        self.find_element(*self.demo_upgrade).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def click_list_selall(self):
        self.find_element(*self.list_selall).click()

    def click_checkUpdata(self):
        self.find_element(*self.checkUpdata).click()

    def find_checkUpdata(self):
        self.exist_element(*self.checkUpdata)

    def click_list_updata1(self):
        self.find_element(*self.list_updata1).click()

    def click_upData(self):
        self.find_element(*self.upData).click()

    def find_upData(self):
        self.exist_element(*self.upData)