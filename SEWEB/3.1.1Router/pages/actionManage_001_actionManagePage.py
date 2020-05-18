#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 15:55
#@swzhou
'''
行为管理页面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'actionManagePage').getlog()
from common.ReadConfig import getMenu

class actionManagePage(BasePage):
    BehaviorManagementM = getMenu('BehaviorManagementM')

    BehaviorManagement = (By.XPATH, '//span[@data-local="{BehaviorManagement}"]') #行为管理菜单
    BehaviorManagement2 = (By.LINK_TEXT, BehaviorManagementM)  # 电子通告菜单

    add = (By.ID,'add')
    ruleName = (By.NAME,'ruleName')
    users = (By.NAME,'users')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    starip = (By.NAME,'starip')
    endip = (By.NAME,'endip')
    saveW1 = (By.XPATH,'//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]') #弹窗中的保存
    servers = (By.NAME,'servers')
    searchText = (By.ID,'search-text-box')
    search = (By.ID,'search')
    appSearchRes = (By.XPATH,'//*[@id="appSearchRes"]/ul/li') #选中搜索到的
    saveW2 = (By.XPATH, '//*[@id="appServer"]/div/div/div[3]/ul/li[1]')  # 弹窗中的保存
    save = (By.ID,'save')
    checkOpen = (By.ID,'checkOpen')
    checkOpens = ('checkOpen')
    list_server = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    delete = (By.XPATH,'//*[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    listnodata = ('//*[@id="1"]/div[1]/div/div[1]/table/tbody/tr[1]/td/div')

    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    seltime = ('time')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_BehaviorManagement(self):
        self.find_element(*self.BehaviorManagement).click()
        logger.info('点击行为管理')

    def click_BehaviorManagement2(self):
        self.find_element(*self.BehaviorManagement2).click()
        logger.info('点击行为管理 二级菜单')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_ruleName(self,ruleName):
        self.find_element(*self.ruleName).clear()
        self.find_element(*self.ruleName).send_keys(ruleName)

    def click_users(self):
        self.find_element(*self.users).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_userall(self):
        self.find_element(*self.userall).click()

    def input_starip(self,starip):
        self.find_element(*self.starip).clear()
        self.find_element(*self.starip).send_keys(starip)

    def input_endip(self,endip):
        self.find_element(*self.endip).clear()
        self.find_element(*self.endip).send_keys(endip)

    def click_saveW1(self):
        self.find_element(*self.saveW1).click()

    def click_servers(self):
        self.find_element(*self.servers).click()

    def input_searchText(self,searchText):
        self.find_element(*self.searchText).clear()
        self.find_element(*self.searchText).send_keys(searchText)

    def click_search(self):
        self.find_element(*self.search).click()

    def click_appSearchRes(self):
        self.find_element(*self.appSearchRes).click()

    def click_saveW2(self):
        self.find_element(*self.saveW2).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_checkOpen(self):
        self.find_element(*self.checkOpen).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()