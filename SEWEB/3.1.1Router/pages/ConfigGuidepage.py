#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 17:34
#@swzhou
'''
配置向导 页面 元素定位
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ConfigGuidepage').getlog()
from common.ReadConfig import getMenu

class ConfigGuidepage(BasePage):
    wanconfigM = getMenu('wanconfigM') #菜单外网配置
    configGuide = (By.XPATH,'//span[@data-local="{configWizard}"]')
    next = (By.ID,'next')
    #配置向导 接入方式
    # connectionTypew = (By.NAME,'connectionTypew')
    connectionTypew = ('connectionTypew')
    okey = (By.ID,'okey')
    #无线设备
    ssid = (By.NAME,'ssid')
    ssid_5g = (By.NAME,'ssid_5g')
    passwd = (By.NAME,'passwd')
    passwd_5g = (By.NAME,'passwd_5g')
    wrlessMode = ('wrlessMode')
    wrlessMode_5g = ('wrlessMode_5g')
    channel = ('channel')
    channel_5g = ('channel_5g')
    chanWidth = ('chanWidth')
    chanWidth_5g = ('chanWidth_5g')
    # # 网络配置
    # netConfig = (By.XPATH, '//span[@data-local="{netConfig}"]')
    # wanConfig = (By.LINK_TEXT,wanconfigM)
    # #wan1口连接类型
    # # list_lineType = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    # list_lineType = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    # #刷新
    # refresh = (By.XPATH,'//*[@id="otherBtns"]/button')
    # #wan1口连接状态
    # list_connState = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/a')
    #
    # #固定002
    # # 从外网配置页面获取WAN1口地址
    # WAN1_ip = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    # WAN1_gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    # WAN1_dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/span')
    #配置向导固定
    staticIp = (By.NAME, 'staticIp')
    staticGateway = (By.NAME, 'staticGateway')
    staticPriDns = (By.NAME, 'staticPriDns')
    #003 pppoe
    pppoeUser = (By.NAME, 'pppoeUser')
    pppoePass = (By.NAME, 'pppoePass')
    dial = (By.XPATH,'//*[@id="otherBtns"]/button[2]') #拨号


    def click_configGuide(self):
        self.find_element(*self.configGuide).click()
        logger.info('点击配置向导')

    def click_next(self):
        self.find_element(*self.next).click()

    # def sel_connectionTypew(self):
    #     self.find_element(*self.connectionTypew)

    def find_okey(self):
        self.exist_element(*self.okey).click()

    def click_okey(self):
        self.find_element(*self.okey).click()

    def input_staticIp(self,staticIp):
        self.find_element(*self.staticIp).clear()
        self.find_element(*self.staticIp).send_keys(staticIp)

    def input_staticGateway(self,staticGateway):
        self.find_element(*self.staticGateway).clear()
        self.find_element(*self.staticGateway).send_keys(staticGateway)

    def input_staticPriDns(self,staticPriDns):
        self.find_element(*self.staticPriDns).clear()
        self.find_element(*self.staticPriDns).send_keys(staticPriDns)


    def input_pppoeUser(self,pppoeUser):
        self.find_element(*self.pppoeUser).clear()
        self.find_element(*self.pppoeUser).send_keys(pppoeUser)

    def input_pppoePass(self,pppoePass):
        self.find_element(*self.pppoePass).clear()
        self.find_element(*self.pppoePass).send_keys(pppoePass)

    def input_ssid(self,ssid):
        self.find_element(*self.ssid).clear()
        self.find_element(*self.ssid).send_keys(ssid)

    def input_passwd(self,passwd):
        self.find_element(*self.passwd).clear()
        self.find_element(*self.passwd).send_keys(passwd)

    def input_ssid_5g(self,ssid_5g):
        self.find_element(*self.ssid_5g).clear()
        self.find_element(*self.ssid_5g).send_keys(ssid_5g)

    def input_passwd_5g(self,passwd_5g):
        self.find_element(*self.passwd_5g).clear()
        self.find_element(*self.passwd_5g).send_keys(passwd_5g)

    def find_ssid_5g(self):
        self.exist_element(*self.ssid_5g).click()

    # def click_netConfig(self):
    #     self.find_element(*self.netConfig).click()
    #     logger.info('点击网络配置')
    #
    # def click_wanConfig(self):
    #     self.find_element(*self.wanConfig).click()
    #     logger.info('点击外网配置')
    #
    # #刷新
    # def click_refresh(self):
    #     self.find_element(*self.refresh).click()
    #
    # def click_list_connState(self):
    #     self.find_element(*self.list_connState).click()

    def click_dial(self):
        self.find_element(*self.dial).click()