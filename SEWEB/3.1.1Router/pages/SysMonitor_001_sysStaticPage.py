#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 18:03
#@swzhou
'''
系统监控 - 系统状态
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger='sysStaticPage').getlog()


class sysStaticPage(BasePage):
    sysStaticM = getMenu('sysStaticM')

    systemWatch = (By.XPATH, '//span[@data-local="{systemWatch}"]') #系统监控
    sysStatic = (By.LINK_TEXT,sysStaticM)  #系统状态
    Model = ('//*[@id="msg"]/table/tbody/tr[1]/td[2]/span')  #设备型号
    hdmodel = ('//*[@id="msg"]/table/tbody/tr[5]/td[2]/span') #硬件版本
    software = ('//*[@id="msg"]/table/tbody/tr[3]/td[2]/span') #软件版本
    SN = ('//*[@id="msg"]/table/tbody/tr[4]/td[2]/span') #序列号


    tips1 = ('//*[@id="content"]/div[2]/div[1]/div/div/div/div/nav/ul/li[1]/a')
    tips2 = ('//*[@id="content"]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div/nav/ul/li/a')
    tips3 = ('//*[@id="content"]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/nav/ul/li/a')
    tips4 = ('//*[@id="content"]/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div/nav/ul/li/a')
    tips5 = ('//*[@id="content"]/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/nav/ul/li/a')

    more1 = (By.XPATH,'//*[@id="content"]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/nav/ul/div/a') #今日应用流量排名更多
    more2 = (By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div/nav/ul/div/a')  # 今日用户网络流量排名更多
    more3 = (By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/nav/ul/div/a')  # VPN状态更多

    list_num = ('//*[@id="todayAppFlowRanking"]/div/div[1]/table/tbody/tr[1]/td[1]/span') #今日应用流量排名
    list_user = ('//*[@id="todayUserNetworkFlowRanking"]/div/div[1]/table/tbody/tr[1]/td[1]/span') #今日用户网络流量排名
    list_name = ('//*[@id="VPNStatus"]/div/div[1]/table/tbody/tr[1]/td[2]/span') # VPN状态

    def click_systemWatch(self):
        self.find_element(*self.systemWatch).click()
        logger.info('点击系统监控')

    def click_sysStatic(self):
        self.find_element(*self.sysStatic).click()
        logger.info('点击系统状态')

    def click_more1(self):
        self.find_element(*self.more1).click()

    def click_more2(self):
        self.find_element(*self.more2).click()

    def click_more3(self):
        self.find_element(*self.more3).click()

