#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 17:43
#@swzhou
'''
行为管理 - 电子通告
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ElectronicsNoticePage').getlog()
from common.ReadConfig import getMenu

class ElectronicsNoticePage(BasePage):
    ElectronicsNoticeM = getMenu('ElectronicsNoticeM')

    BehaviorManagement = (By.XPATH, '//span[@data-local="{BehaviorManagement}"]') #行为管理菜单
    ElectronicsNotice = (By.LINK_TEXT, ElectronicsNoticeM)  # 电子通告菜单

    rulename = (By.NAME,'rulename')
    swEn = (By.XPATH,'//input[@name="status"and@value="on"]')
    swEs = ('//input[@name="status"and@value="on"]')
    save = (By.ID,'save')
    swC = (By.XPATH, '//input[@name="status"and@value="off"]')
    swCs = ('//input[@name="status"and@value="off"]')
    remarks = (By.NAME,'remarks') #备注
    edipage = (By.ID,'edipage') #通告页面编辑
    NoticePageName = (By.NAME, 'NoticePageName')
    NoticePageNote = (By.NAME, 'NoticePageNote')
    NoticePageTitle = (By.NAME, 'NoticePageTitle')
    SkipUrl = (By.NAME, 'SkipUrl')
    SkipTime = (By.NAME, 'SkipTime')
    NoticeBody = (By.NAME, 'NoticeBody')
    modalhide = (By.ID, 'modal-hide')
    applyUser = (By.NAME,'applyUser')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    saveW1 = (By.XPATH, '//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]')  # 弹窗中的保存
    seltime = ('effecttime')  # 生效时间

    def click_BehaviorManagement(self):
        self.find_element(*self.BehaviorManagement).click()
        logger.info('点击行为管理')

    def click_ElectronicsNotice(self):
        self.find_element(*self.ElectronicsNotice).click()
        logger.info('点击电子通告')

    def input_rulename(self,rulename):
        self.find_element(*self.rulename).clear()
        self.find_element(*self.rulename).send_keys(rulename)

    def click_swEn(self):
        self.find_element(*self.swEn).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_swC(self):
        self.find_element(*self.swC).click()

    def input_remarks(self, remarks):
        self.find_element(*self.remarks).clear()
        self.find_element(*self.remarks).send_keys(remarks)

    def click_edipage(self):
        self.find_element(*self.edipage).click()

    def click_NoticePageName(self):
        self.find_element(*self.NoticePageName).click()

    def input_NoticePageNote(self, NoticePageNote):
        self.find_element(*self.NoticePageNote).clear()
        self.find_element(*self.NoticePageNote).send_keys(NoticePageNote)

    def input_NoticePageTitle(self, NoticePageTitle):
        self.find_element(*self.NoticePageTitle).clear()
        self.find_element(*self.NoticePageTitle).send_keys(NoticePageTitle)

    def input_SkipUrl(self, SkipUrl):
        self.find_element(*self.SkipUrl).clear()
        self.find_element(*self.SkipUrl).send_keys(SkipUrl)

    def input_SkipTime(self, SkipTime):
        self.find_element(*self.SkipTime).clear()
        self.find_element(*self.SkipTime).send_keys(SkipTime)

    def input_NoticeBody(self, NoticeBody):
        self.find_element(*self.NoticeBody).clear()
        self.find_element(*self.NoticeBody).send_keys(NoticeBody)

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def click_applyUser(self):
        self.find_element(*self.applyUser).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_userall(self):
        self.find_element(*self.userall).click()

    def click_saveW1(self):
        self.find_element(*self.saveW1).click()