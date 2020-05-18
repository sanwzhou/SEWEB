#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 13:07
#@swzhou
'''
网络配置 - 端口映射
'''

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'PortMapping_002_staticMappingPage').getlog()
from common.ReadConfig import getMenu

class staticMappingPage(BasePage):
    portMappingM = getMenu('portMappingM')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    portMapping = (By.LINK_TEXT,portMappingM) #端口映射菜单

    add = (By.ID,'add')
    IDs = (By.NAME,'IDs')
    IPs = (By.NAME,'IPs')
    Protocols = ('Protocols')
    inS = (By.NAME,'inS')
    inE = (By.NAME,'inE')
    outS = (By.NAME,'outS')
    outE = (By.NAME,'outE')
    save =(By.ID,'save')
    list_port = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span')
    edit1 = (By.XPATH,'//*[@data-primarykey="1"and@data-event="edit"]')
    delete1 = (By.XPATH,'//*[@data-primarykey="1"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    list_tips = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td')
    list1_Ens = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/input')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 静态映射界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 静态映射跳转最后页

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_portMapping(self):
        self.find_element(*self.portMapping).click()
        logger.info('点击端口映射')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_IDs(self,IDs):
        self.find_element(*self.IDs).clear()
        self.find_element(*self.IDs).send_keys(IDs)

    def input_IPs(self,IPs):
        self.find_element(*self.IPs).clear()
        self.find_element(*self.IPs).send_keys(IPs)

    def input_inS(self,inS):
        self.find_element(*self.inS).clear()
        self.find_element(*self.inS).send_keys(inS)

    def input_inE(self,inE):
        self.find_element(*self.inE).click()
        time.sleep(0.5)
        self.find_element(*self.inE).clear()
        self.find_element(*self.inE).send_keys(inE)

    def input_outS(self,outS):
        self.find_element(*self.outS).clear()
        self.find_element(*self.outS).send_keys(outS)

    def input_outE(self,outE):
        self.find_element(*self.outE).click()
        time.sleep(0.5)
        self.find_element(*self.outE).clear()
        self.find_element(*self.outE).send_keys(outE)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_edit1(self):
        self.find_element(*self.edit1).click()

    def click_delete1(self):
        self.find_element(*self.delete1).click()

    def find_delete1(self):
        self.exist_element(*self.delete1).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()
