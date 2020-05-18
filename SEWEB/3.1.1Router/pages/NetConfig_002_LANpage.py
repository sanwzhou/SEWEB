#! -*-conding:utf-8 -*-
#@Time: 2019/1/10 0010 17:50
#@swzhou
'''
网络配置 内网配置页面 元素定位
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'NetworkConfig_lan').getlog()
from common.ReadConfig import getMenu,getAssertText

class NetworkConfig_LANpage(BasePage):
    lanconfigM = getMenu('lanconfigM')

    NetworkConfig = (By.XPATH, '//span[@data-local="{netConfig}"]')
    save = (By.ID,'save')
    tips = ('pageTip-success')
    LANconfig = (By.LINK_TEXT, lanconfigM)
    #lan口配置
    add = (By.ID,'add')
    lanIpName = (By.NAME,'lanIpName')
    lanIp = (By.NAME,'lanIp')
    lanNetmask = (By.NAME,'lanNetmask')
    selsxjk = ('sxjk')
    dhcpVid = (By.NAME,'dhcpVid')
    list_name2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[2]/span')
    list_name3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[2]/span')
    list_ip2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[3]/span')
    list_ip3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[3]/span')
    list_vlanid2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[5]/span')
    list_vlanid3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[5]/span')
    tipsshowin = ('tips-show-in')
    modalhide = (By.ID,'modal-hide')
    allsel = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delete = (By.ID,'delete')
    ok = (By.ID,'u-cfm-ok')
    wifiInter1 = (By.XPATH,'//*[@id="modal-add"]/div/div/div[2]/table/tbody/tr[6]/td[2]/input')#wifi接口1
    wifiInter2 = (By.XPATH, '//*[@id="modal-add"]/div/div/div[2]/table/tbody/tr[7]/td[2]/input')  # wifi接口2

    # 全局配置
    globalconfigM = getMenu('globalconfigM')
    GlobalConfig = (By.LINK_TEXT, globalconfigM)
    upnpEN = (By.XPATH,'//*[@name="isOpen"and@value="on"]')
    upnpClose = (By.XPATH, '//*[@name="isOpen"and@value="off"]')
    upnpCloseS = ('//*[@name="isOpen"and@value="off"]')
    lanRateseled = ('//*[@id="2"]/table/tbody/tr[2]/td[2]/select/option[1]')  # 默认协商速率
    sellanRate = ('//*[@id="2"]/table/tbody/tr[2]/td[2]/select')  # 协商速率
    lanmodenow = ('//*[@id="2"]/table/tbody/tr[2]/td[2]/select/option[1]')  # 当前协商速率
    mac = (By.NAME,'mac')
    lan_tips = ('//*[@id="2"]/table/tbody/tr[1]/td[2]/span/span[2]')  # lan口mac地址清空保存提示



    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_LANconfig(self):
        self.find_element(*self.LANconfig).click()
        logger.info('点击内网配置')

    def click_globalconfig(self):
        self.find_element(*self.GlobalConfig).click()

    def click_upnpEN(self):
        self.find_element(*self.upnpEN).click()

    def click_upnpClose(self):
        self.find_element(*self.upnpClose).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_add(self):
        self.find_element(*self.add).click()

    def input_lanIpName(self, lanIpName):
        self.find_element(*self.lanIpName).clear()
        self.find_element(*self.lanIpName).send_keys(lanIpName)

    def input_lanIp(self, lanIp):
        self.find_element(*self.lanIp).clear()
        self.find_element(*self.lanIp).send_keys(lanIp)

    def input_lanNetmask(self, lanNetmask):
        self.find_element(*self.lanNetmask).clear()
        self.find_element(*self.lanNetmask).send_keys(lanNetmask)

    def input_dhcpVid(self, dhcpVid):
        self.find_element(*self.dhcpVid).clear()
        self.find_element(*self.dhcpVid).send_keys(dhcpVid)

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_allsel(self):
        self.find_element(*self.allsel).click()

    def clear_mac(self):
        self.find_element(*self.mac).clear()

    def click_wifiInter1(self):
        self.find_element(*self.wifiInter1).click()

    def click_wifiInter2(self):
        self.find_element(*self.wifiInter2).click()
