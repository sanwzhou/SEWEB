#! -*-conding:utf-8 -*-
#@Time: 2019/1/10 0010 18:47
#@swzhou
'''
DHCP 服务器
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'DHCP_server').getlog()
from common.ReadConfig import getMenu

class DHCPserverpage(BasePage):
    DHCPserverM = getMenu('DHCPserver')
    StaticDHCPM = getMenu('StaticDHCP')
    DHCPClientListM = getMenu('DHCPClientList')
    globalconfigM = getMenu('globalconfigM')
    save = (By.ID, 'save')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]')
    DHCPserver = (By.LINK_TEXT, DHCPserverM)
    # DHCP服务器配置
    dhcpEn = ('//input[@data-primarykey="0"and@type="checkbox"]')
    addpool = (By.ID, 'add')
    poolName = (By.NAME,'poolName')
    poolVid = ('poolVid')
    list_name2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[3]/span')
    list_name3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[3]/span')
    list_int2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[5]/span')
    list_int3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[5]/span')
    seloption43Type = ('option43Type')
    list_delpool2 = (By.XPATH,'//span[@data-primarykey="1"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    #静态DHCP
    StaticDHCP = (By.LINK_TEXT, StaticDHCPM)
    addStatic = (By.XPATH,'//*[@id="2"]/div/div/header/ul[2]/ul/li[1]/button')
    UserName = (By.NAME,'UserName')
    IP = (By.NAME,'IP')
    MAC = (By.NAME,'Mac')
    list_username = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    list_poolname = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    list_IP = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    list_MAC = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')

    #客户端列表
    DHCPClientList = (By.LINK_TEXT,DHCPClientListM)
    search = (By.XPATH,'//*[@id="3"]/div/div/header/ul[1]/div[2]/input') #搜索框
    searchb = (By.XPATH, '//*[@id="3"]/div/div/header/ul[1]/div[2]/i')  # 搜索按钮
    list_tips = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    selrefreshtime = ('//*[@id="btns"]/ul/li[1]/select')
    Refresh = (By.XPATH,'//*[@id="3"]/div/div/header/ul[2]/ul/li[2]')
    listIP = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td[1]/span')
    listmask = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    listmac = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    listLeaseTime = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')

    #全局配置
    GlobalConfig = (By.LINK_TEXT, globalconfigM)
    dnspEn = (By.XPATH, '//input[@name="dnspEnblw"and@value="on"]')
    dnspEns = ('//input[@name="dnspEnblw"and@value="on"]')
    tips = ('pageTip-success')

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_DHCPserver(self):
        self.find_element(*self.DHCPserver).click()
        logger.info('点击DHCP服务')

    def click_StaticDHCP(self):
        self.find_element(*self.StaticDHCP).click()
        logger.info('点击静态DHCP')

    def click_add(self):
        self.find_element(*self.addStatic).click()

    def input_UserName(self,UserName):
        self.find_element(*self.UserName).clear()
        self.find_element(*self.UserName).send_keys(UserName)

    def input_IP(self,IP):
        self.find_element(*self.IP).clear()
        self.find_element(*self.IP).send_keys(IP)

    def input_MAC(self,MAC):
        self.find_element(*self.MAC).clear()
        self.find_element(*self.MAC).send_keys(MAC)

    def click_save(self):
        self.find_element(*self.save).click()

    def clicl_DHCPClientList(self):
        self.find_element(*self.DHCPClientList).click()

    def input_search(self, Mac):
        self.find_element(*self.search).clear()
        self.find_element(*self.search).send_keys(Mac)

    def click_searchb(self):
        self.find_element(*self.searchb).click()

    def click_GlobalConfig(self):
        self.find_element(*self.GlobalConfig).click()

    def click_dnspEn(self):
        self.find_element(*self.dnspEn).click()

    def click_addpool(self):
        self.find_element(*self.addpool).click()

    def input_poolName(self,poolName):
        self.find_element(*self.poolName).clear()
        self.find_element(*self.poolName).send_keys(poolName)

    def click_Refresh(self):
        self.find_element(*self.Refresh).click()

    def click_list_delpool2(self):
        self.find_element(*self.list_delpool2).click()

    def click_ok(self):
        self.find_element(*self.ok).click()