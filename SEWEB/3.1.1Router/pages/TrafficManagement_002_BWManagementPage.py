#! -*-conding:utf-8 -*-
#@Time: 2019/2/18 0018 18:11
#@swzhou
'''
流量管理 - 流量管理
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'BWManagementPage').getlog()
from common.ReadConfig import getMenu

class BWManagementPage(BasePage):
    TrafficManagementM = getMenu('TrafficManagementM')

    Qos = (By.XPATH, '//span[@data-local="{TrafficManagement}"]') #流量管理菜单
    TrafficManagement = (By.LINK_TEXT, TrafficManagementM)  # 流量管理二级菜单

    add = (By.ID,'add')
    GroupNames = (By.NAME,'GroupNames')
    notes = (By.NAME,'notes')
    order = (By.NAME,'order')
    orgShow = (By.NAME, 'orgShow')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    saveW1 = (By.XPATH, '//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]')  # 弹窗中的保存
    lkcl1 = (By.XPATH,'//input[@name="lkcl"and@value="1"]') #应用保障
    lkcl0 = (By.XPATH, '//input[@name="lkcl"and@value="0"]')  # 应用限制
    policy2 = (By.XPATH, '//input[@name="policy"and@value="2"]')  # 共享限速
    policy1 = (By.XPATH, '//input[@name="policy"and@value="1"]')  # 独享限速
    uRate = (By.NAME,'uRate') #上传
    dRate = (By.NAME,'dRate') #下载
    effecttime = ('effecttime')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_Qos(self):
        self.find_element(*self.Qos).click()
        logger.info('点击流量管理')

    def click_TrafficManagement(self):
        self.find_element(*self.TrafficManagement).click()
        logger.info('点击流量管理二级菜单')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_GroupNames(self, GroupNames):
        self.find_element(*self.GroupNames).clear()
        self.find_element(*self.GroupNames).send_keys(GroupNames)

    def input_notes(self, notes):
        self.find_element(*self.notes).clear()
        self.find_element(*self.notes).send_keys(notes)

    def input_order(self, order):
        self.find_element(*self.order).clear()
        self.find_element(*self.order).send_keys(order)

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

    def click_lkcl1(self):
        self.find_element(*self.lkcl1).click()

    def click_lkcl0(self):
        self.find_element(*self.lkcl0).click()

    def click_policy2(self):
        self.find_element(*self.policy2).click()

    def click_policy1(self):
        self.find_element(*self.policy1).click()

    def input_uRate(self, uRate):
        self.find_element(*self.uRate).clear()
        self.find_element(*self.uRate).send_keys(uRate)

    def input_dRate(self, dRate):
        self.find_element(*self.dRate).clear()
        self.find_element(*self.dRate).send_keys(dRate)

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()