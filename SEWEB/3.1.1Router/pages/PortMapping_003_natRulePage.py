#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 14:15
#@swzhou
'''
网络配置 - 端口映射 - NAT规则
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'PortMapping_003_natRulePage').getlog()
from common.ReadConfig import getMenu

class natRulePage(BasePage):
    portMappingM = getMenu('portMappingM')
    natRuleM = getMenu('natRuleM')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    portMapping = (By.LINK_TEXT, portMappingM)  # 端口映射菜单
    natRule = (By.LINK_TEXT,natRuleM) #端口映射菜单

    add = (By.XPATH,'//*[@id="content"]/div/div[2]/div/div/header/ul[2]/ul/li[1]')
    RuleIDs = (By.NAME,'RuleIDs')
    InFromIPs = (By.NAME,'InFromIPs')
    InEndIPs = (By.NAME,'InEndIPs')
    OutIPs =(By.NAME,'OutIPs')
    save = (By.ID,'save')
    list_InFromIPs = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    list_InEndIPs = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')
    list_OutIPs = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    edit = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span[1]')
    type_one2one = (By.XPATH,'//input[@name="NatTypes"and@value="2"]')
    delete = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span[2]')
    ok = (By.ID,'u-cfm-ok')
    listtips = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    type_easyIp = (By.XPATH, '//input[@name="NatTypes"and@value="1"]')

    maxpagenums1 = ('//*[@id="2"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="2"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_portMapping(self):
        self.find_element(*self.portMapping).click()
        logger.info('点击端口映射')

    def click_natRule(self):
        self.find_element(*self.natRule).click()
        logger.info('点击nat规则')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_RuleIDs(self,RuleIDs):
        self.find_element(*self.RuleIDs).clear()
        self.find_element(*self.RuleIDs).send_keys(RuleIDs)

    def input_InFromIPs(self,InFromIPs):
        self.find_element(*self.InFromIPs).clear()
        self.find_element(*self.InFromIPs).send_keys(InFromIPs)

    def input_InEndIPs (self,InEndIPs ):
        self.find_element(*self.InEndIPs ).clear()
        self.find_element(*self.InEndIPs ).send_keys(InEndIPs )

    def input_OutIPs(self,OutIPs):
        self.find_element(*self.OutIPs).clear()
        self.find_element(*self.OutIPs).send_keys(OutIPs)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_edit(self):
        self.find_element(*self.edit).click()

    def click_typeOne2one(self):
        self.find_element(*self.type_one2one).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_typeeasyIp(self):
        self.find_element(*self.type_easyIp).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()