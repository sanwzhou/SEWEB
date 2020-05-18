#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 17:29
#@swzhou
'''
附加测试
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ManagementPolicyPage').getlog()
from common.ReadConfig import getweb

class AdditionalTestPage(BasePage):
    RouteUrl = getweb('RouteUrl')
    aspUrl = RouteUrl + '/uttCli.asp'

    deleteall = (By.ID,'delete all')
    addCommand = (By.NAME,'addCommand')
    add = (By.ID,'add')

    def click_deleteall(self):
        self.find_element(*self.deleteall).click()

    def input_addCommand(self, addCommand):
        self.find_element(*self.addCommand).clear()
        self.find_element(*self.addCommand).send_keys(addCommand)

    def click_add(self):
        self.find_element(*self.add).click()