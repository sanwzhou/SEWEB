#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 16:28
#@swzhou
'''
网络配置 -静态路由界面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'RouteConfigPage').getlog()
from common.ReadConfig import getMenu

class RouteConfigPage(BasePage):
    routeconfigM = getMenu('routeconfigM')
    PolicyRouteM = getMenu('PolicyRouteM')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    Routeconfig = (By.LINK_TEXT, routeconfigM)  # 路由配置菜单

    add = (By.ID,'add')
    RouteNames = (By.NAME,'RouteNames')
    DesIPs = (By.NAME,'DesIPs')
    DesMasks = (By.NAME,'DesMasks')
    GateWays = (By.NAME,'GateWays')
    save = (By.ID,'save')
    list_dst = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    edit = (By.XPATH, '//span[@data-primarykey="0"and@data-event="edit"]')
    selProfiles = ('Profiles')
    list_Interface = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span')
    delete = (By.XPATH,'//span[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    modalhide = (By.ID,'modal-hide')

    #策略路由
    PolicyRoute = (By.LINK_TEXT,PolicyRouteM)
    addPolicy = (By.XPATH,'//*[@id="2"]/div[1]/div/header/ul[2]/ul/li')
    sourceIP = (By.NAME,'sourceIP')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    saveW = (By.XPATH,'//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[3]') # 弹窗中的保存
    dstAddr = (By.NAME,'dstAddr')
    dstgroup = (By.XPATH,'//input[@name="dstIP"and@value="groupSel"]')
    destIP = (By.XPATH,'//input[@name="dstIP"and@value="ipRange"and@data-control-src="ip"]')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input') #静态路由界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 静态路由跳转最后页
    maxpagenums2 = ('//*[@id="2"]/div/div/div[2]/div/input')  # 策略路由界面页数框
    # '//*[@id="wannapage"]'
    pageend2 = (By.XPATH, '//*[@id="2"]/div/div/div[2]/div/img[4]')  # 策略路由跳转最后页

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_Routeconfig(self):
        self.find_element(*self.Routeconfig).click()
        logger.info('点击端口映射')

    def click_add(self):
        self.find_element(*self.add).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def input_RouteNames(self,RouteNames):
        self.find_element(*self.RouteNames).clear()
        self.find_element(*self.RouteNames).send_keys(RouteNames)

    def input_DesIPs(self,DesIPs):
        self.find_element(*self.DesIPs).clear()
        self.find_element(*self.DesIPs).send_keys(DesIPs)

    def input_DesMasks(self,DesMasks):
        self.find_element(*self.DesMasks).clear()
        self.find_element(*self.DesMasks).send_keys(DesMasks)

    def input_GateWays(self,GateWays):
        self.find_element(*self.GateWays).clear()
        self.find_element(*self.GateWays).send_keys(GateWays)

    def click_edit(self):
        self.find_element(*self.edit).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def click_PolicyRoute(self):
        self.find_element(*self.PolicyRoute).click()
        logger.info('点击策略路由')

    def click_addPolicy(self):
        self.find_element(*self.addPolicy).click()

    def click_sourceIP(self):
        self.find_element(*self.sourceIP).click()

    def click_userall(self):
        self.find_element(*self.userall).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_saveW(self):
        self.find_element(*self.saveW).click()

    def click_dstAddr(self):
        self.find_element(*self.dstAddr).click()

    def click_dstgroup(self):
        self.find_element(*self.dstgroup).click()

    def click_destIP(self):
        self.find_element(*self.destIP).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()

    def click_pageend2(self):
        self.find_element(*self.pageend2).click()