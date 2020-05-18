#! -*-conding:utf-8 -*-
#@Time: 2019/2/18 0018 10:30
#@swzhou
'''
系统对象 - 地址组
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'sysObj_AddressGroupPage').getlog()
from common.ReadConfig import getMenu

class AddressGroupPage(BasePage):
    AddressGroupM = getMenu('AddressGroupM')

    sysObj = (By.XPATH, '//span[@data-local="{sysObj}"]') #系统对象菜单
    AddressGroup = (By.LINK_TEXT, AddressGroupM)  # 地址组菜单

    add = (By.ID,'add')
    name = (By.NAME,'name')
    addressTypeold = (By.XPATH,'//input[@name="addressType"and@value="old"]')
    btn_tor = (By.ID,'btn_tor')
    btn_tol = (By.ID,'btn_tol')
    btn_delet = (By.ID,'btn_delet')
    addressTypenew = (By.XPATH, '//input[@name="addressType"and@value="new"]')
    startAddress = (By.NAME,'startAddress')
    endAddress = (By.NAME,'endAddress')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_sysObj(self):
        self.find_element(*self.sysObj).click()
        logger.info('点击系统对象菜单')

    def click_AddressGroup(self):
        self.find_element(*self.AddressGroup).click()
        logger.info('点击地址组菜单')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_name(self, name):
        self.find_element(*self.name).clear()
        self.find_element(*self.name).send_keys(name)

    def click_addressTypeold(self):
        self.find_element(*self.addressTypeold).click()

    def click_btn_tor(self):
        self.find_element(*self.btn_tor).click()

    def click_btn_tol(self):
        self.find_element(*self.btn_tol).click()

    def click_btn_delet(self):
        self.find_element(*self.btn_delet).click()

    def click_addressTypenew(self):
        self.find_element(*self.addressTypenew).click()

    def input_startAddress(self,startAddress):
        self.find_element(*self.startAddress).click()
        self.find_element(*self.startAddress).send_keys(startAddress)

    def input_endAddress(self,endAddress):
        self.find_element(*self.endAddress).click()
        self.find_element(*self.endAddress).send_keys(endAddress)

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()