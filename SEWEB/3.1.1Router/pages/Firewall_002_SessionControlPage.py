#! -*-conding:utf-8 -*-
#@Time: 2019/2/15 0015 17:32
#@swzhou
'''
防火墙 - 连接数限制
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'SessionControlPage').getlog()
from common.ReadConfig import getMenu

class SessionControlPage(BasePage):
    SessionControlM = getMenu('SessionControlM')

    FireWall = (By.XPATH, '//span[@data-local="{fireWall}"]') #防火墙菜单
    SessionControl = (By.LINK_TEXT, SessionControlM)  # 连接数限制菜单

    swENs = ('//input[@name="enable"and@value="off"]')

    totalCnt = ('totalCnt')
    tcp = ('tcp')
    udp = ('udp')
    icmp = ('icmp')

    def click_FireWall(self):
        self.find_element(*self.FireWall).click()
        logger.info('点击防火墙')

    def click_SessionControl(self):
        self.find_element(*self.SessionControl).click()
        logger.info('点击连接数限制菜单')