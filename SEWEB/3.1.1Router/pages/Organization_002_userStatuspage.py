#! -*-conding:utf-8 -*-
#@Time: 2019/1/12 0012 16:44
#@swzhou
'''
用户管理 - 用户状态页面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'Organization_userStatusPage').getlog()
from common.ReadConfig import getMenu,getAssertText


class Organization_userStatusPage(BasePage):
    userstatusM = getMenu('userstatusM') #用户状态

    UserManage = (By.XPATH,'//span[@data-local="{UserManage}"]')
    userstatus = (By.LINK_TEXT,userstatusM)
    #001
    selmanual = ('//*[@id="btns"]/ul/li[1]/select')
    refreshtable = (By.ID,'refreshtable')
    ID = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    username = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    group = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    VlanID = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')
    IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    authmode = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span')
    online_time_length = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[10]/span')
    Uploading_data = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[11]/span')
    Downing_data = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[12]/span')
    Uploading_speed = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[13]/span')
    Downing_speed = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[14]/span')
    edit = ('//*[@data-primarykey="0"and@id="calldown"]')
    #002
    list_IP1 =('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    checkbox1 =(By.XPATH,'//input[@type="checkbox"and@data-primarykey="0"]')
    move = (By.ID,'move')
    save = (By.ID,'save')
    #003
    list_IP2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span')
    search = (By.XPATH,'//*[@class="u-searchbox"]/input')
    searchb = (By.CLASS_NAME,'icon-search')
    list_checkbox1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input')
    Selected_MAC = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    addToBlackList = (By.ID,'add-to-black-list')
    ok = (By.ID,'u-cfm-ok')
    calldown = (By.XPATH,'//*[@id="calldown"]')

    def click_UserManage(self):
        self.find_element(*self.UserManage).click()
        logger.info('点击用户管理')

    def click_userstatus(self):
        self.find_element(*self.userstatus).click()
        logger.info('点击用户状态')

    def click_refreshtable(self):
        self.find_element(*self.refreshtable).click()

    def click_checkbox1(self):
        self.find_element(*self.checkbox1).click()

    def click_move(self):
        self.find_element(*self.move).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def input_search(self, search):
        self.find_element(*self.search).clear()
        self.find_element(*self.search).send_keys(search)

    def click_searchb(self):
        self.find_element(*self.searchb).click()

    def click_addToBlackList(self):
        self.find_element(*self.addToBlackList).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_listCheckbox1(self):
        self.find_element(*self.list_checkbox1).click()

    def click_calldown(self):
        self.find_element(*self.calldown).click()

    def find_move(self):
        self.exist_element(*self.move)

    def find_addToBlackList(self):
        self.exist_element(*self.addToBlackList)
