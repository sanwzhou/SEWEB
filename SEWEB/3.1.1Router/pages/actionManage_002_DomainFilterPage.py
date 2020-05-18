#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 14:30
#@swzhou
'''
行为管理 - 域名过滤
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'DomainFilterPage').getlog()
from common.ReadConfig import getMenu

class DomainFilterPage(BasePage):
    DomainFilterM = getMenu('DomainFilterM')

    BehaviorManagement = (By.XPATH, '//span[@data-local="{BehaviorManagement}"]') #行为管理菜单
    DomainFilter = (By.LINK_TEXT, DomainFilterM)  # 域名过滤菜单

    DomainFilterEn = (By.XPATH,'//input[@name="DnsFilterEnable"and@value="on"]') #开启域名过滤
    onlyBlockEn = (By.XPATH,'//input[@name="enableType"and@value="0"]') #仅禁止
    onlyBlockEs = ('//input[@name="enableType"and@value="0"]')
    DomainFilterEs = ('//input[@name="DnsFilterEnable"and@value="on"]')
    DnsFilterName = (By.NAME,'DnsFilterName')
    cleanDns = (By.ID,'cleanDns') #清空列表
    ok = (By.ID,'u-cfm-ok')
    addHostFilter = (By.NAME,'addHostFilter')
    addDns = (By.ID,'addDns')
    save = (By.ID,'save')
    terminalEn = (By.XPATH,'//input[@name="terminalEnable"and@value="on"]') #通告
    terminalEs = ('//input[@name="terminalEnable"and@value="on"]')

    onlyAllowEn = (By.XPATH, '//input[@name="enableType"and@value="1"]')
    onlyAllowEs = ('//input[@name="enableType"and@value="1"]')
    DomainFilterC = (By.XPATH, '//input[@name="DnsFilterEnable"and@value="off"]')
    DomainFilterCs = ('//input[@name="DnsFilterEnable"and@value="off"]')
    terminalC = (By.XPATH, '//input[@name="terminalEnable"and@value="off"]')  # 通告
    terminalCs = ('//input[@name="terminalEnable"and@value="off"]')
    orgShow = (By.NAME,'orgShow')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    saveW1 = (By.XPATH, '//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]')  # 弹窗中的保存
    seltime = ('effecttime') #生效时间
    terminalRemind = ('terminalRemind') #通告
    editNotePage = (By.ID,'editNotePage') #通告页面编辑
    NoticePageName = (By.NAME,'NoticePageName')
    NoticePageNote = (By.NAME,'NoticePageNote')
    NoticePageTitle = (By.NAME,'NoticePageTitle')
    SkipUrl = (By.NAME,'SkipUrl')
    SkipTime = (By.NAME,'SkipTime')
    NoticeBody = (By.NAME,'NoticeBody')
    modalhide = (By.ID,'modal-hide')
    domainRedirection = (By.NAME,'domainRedirection')


    def click_BehaviorManagement(self):
        self.find_element(*self.BehaviorManagement).click()
        logger.info('点击行为管理')

    def click_DomainFilter(self):
        self.find_element(*self.DomainFilter).click()
        logger.info('点击域名过滤')

    def click_DomainFilterEn(self):
        self.find_element(*self.DomainFilterEn).click()

    def click_onlyBlockEn(self):
        self.find_element(*self.onlyBlockEn).click()

    def input_DnsFilterName(self,DnsFilterName):
        self.find_element(*self.DnsFilterName).clear()
        self.find_element(*self.DnsFilterName).send_keys(DnsFilterName)

    def click_cleanDns(self):
        self.find_element(*self.cleanDns).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def input_addHostFilter(self,addHostFilter):
        self.find_element(*self.addHostFilter).clear()
        self.find_element(*self.addHostFilter).send_keys(addHostFilter)

    def click_addDns(self):
        self.find_element(*self.addDns).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_terminalEn(self):
        self.find_element(*self.terminalEn).click()

    def click_onlyAllowEn(self):
        self.find_element(*self.onlyAllowEn).click()

    def click_DomainFilterC(self):
        self.find_element(*self.DomainFilterC).click()

    def click_terminalC(self):
        self.find_element(*self.terminalC).click()

    def click_orgShow(self):
        self.find_element(*self.orgShow).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_userall(self):
        self.find_element(*self.userall).click()

    def click_saveW1(self):
        self.find_element(*self.saveW1).click()

    def click_editNotePage(self):
        self.find_element(*self.editNotePage).click()

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

    def click_domainRedirection(self):
        self.find_element(*self.domainRedirection).click()
