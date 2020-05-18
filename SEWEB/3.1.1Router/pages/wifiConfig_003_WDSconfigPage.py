#! -*-conding:utf-8 -*-
#@Time: 2019/4/4 0004 14:04
#@swzhou
'''
无线配置 - 射频配置 页面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'wifiConfig_003_WDSconfigPage').getlog()
from common.ReadConfig import getMenu

class WDSconfigPage(BasePage):
    wsdconfigM = getMenu('wdsconfigM')
    wdsconfig5M = getMenu('wdsconfig5M')

    wifiConfig = (By.XPATH, '//span[@data-local="{wifiConfig}"]') #无线配置
    wsdconfig = (By.LINK_TEXT,wsdconfigM)
    wsdconfig5 = (By.LINK_TEXT,wdsconfig5M)

    wdsEn2 = (By.XPATH, '//input[@name="wdsEnable"and@value="1"]')
    wdsC2 = (By.XPATH,'//input[@name="wdsEnable"and@value="0"]')
    bridgessid2 = (By.NAME,'bridgessid')
    briggebssid2 = (By.NAME,'briggebssid')
    wdsscan2 = (By.ID,'wdsscan')
    apclisecmode2 = ('apclisecmode') #加密方式
    apclikeyFormat2 = ('apclikeyFormat') #WEP 密钥格式
    apcliwepkey12 = (By.NAME,'apcliwepkey1') #密钥1
    apcliwpapskAuthMode2 = ('apcliwpapskAuthMode') #WPAPSK WPA版本
    apcliwpapskCipher2 = ('apcliwpapskCipher') #加密算法
    apclipskPsswd2 = (By.NAME,'apclipskPsswd') #预共享密钥

    wdsEn5 = (By.XPATH, '//*[@id="2"]/table/tbody/tr[1]/td[2]/input[1]')
    wdsC5 = (By.XPATH, '//*[@id="2"]/table/tbody/tr[1]/td[2]/input[2]')
    bridgessid5 = (By.XPATH,'//*[@id="2"]/table/tbody/tr[2]/td[2]/input')
    briggebssid5 = (By.XPATH,'//*[@id="2"]/table/tbody/tr[3]/td[2]/input')
    wdsscan5 = (By.XPATH,'//*[@id="2"]/table/tbody/tr[3]/td[3]/a')
    apclisecmode5 = ('//*[@id="2"]/table/tbody/tr[5]/td[2]/select')  # 加密方式
    apclikeyFormat5 = ('//*[@id="2"]/table/tbody/tr[6]/td[2]/select')  # WEP 密钥格式
    apcliwepkey15 = (By.XPATH,'//*[@id="2"]/table/tbody/tr[9]/td[2]/input[2]')  # 密钥1
    apcliwpapskAuthMode5 = ('//*[@id="2"]/table/tbody/tr[13]/td[2]/select')  # WPAPSK WPA版本
    apcliwpapskCipher5 = ('//*[@id="2"]/table/tbody/tr[14]/td[2]/select')  # 加密算法
    apclipskPsswd5 = (By.XPATH,'//*[@id="2"]/table/tbody/tr[15]/td[2]/input')  # 预共享密钥


    def click_wifiConfig(self):
        self.find_element(*self.wifiConfig).click()
        logger.info('点击无线配置')

    def click_wsdconfig(self):
        self.find_element(*self.wsdconfig).click()
        logger.info('点击WDS配置')

    def click_wsdconfig5(self):
        self.find_element(*self.wsdconfig5).click()
        logger.info('点击5G WDS配置')

    def click_wdsEn2(self):
        self.find_element(*self.wdsEn2).click()

    def click_wdsC2(self):
        self.find_element(*self.wdsC2).click()

    def input_apclipskPsswd2(self,apclipskPsswd2):
        self.find_element(*self.apclipskPsswd2).clear()
        self.find_element(*self.apclipskPsswd2).send_keys(apclipskPsswd2)

    def click_wdsEn5(self):
        self.find_element(*self.wdsEn5).click()

    def click_wdsC5(self):
        self.find_element(*self.wdsC5).click()

    def input_apclipskPsswd5(self,apclipskPsswd5):
        self.find_element(*self.apclipskPsswd5).clear()
        self.find_element(*self.apclipskPsswd5).send_keys(apclipskPsswd5)

    def input_bridgessid2(self, bridgessid2):
        self.find_element(*self.bridgessid2).clear()
        self.find_element(*self.bridgessid2).send_keys(bridgessid2)

    def input_briggebssid2(self, briggebssid2):
        self.find_element(*self.briggebssid2).clear()
        self.find_element(*self.briggebssid2).send_keys(briggebssid2)

    def find_wdsscan2(self):
        self.exist_element(*self.wdsscan2)

    def input_bridgessid5(self, bridgessid5):
        self.find_element(*self.bridgessid5).clear()
        self.find_element(*self.bridgessid5).send_keys(bridgessid5)

    def input_briggebssid5(self, briggebssid5):
        self.find_element(*self.briggebssid5).clear()
        self.find_element(*self.briggebssid5).send_keys(briggebssid5)

    def find_wdsscan5(self):
        self.exist_element(*self.wdsscan5)

    def find_apcliwepkey12(self):
        self.exist_element(*self.apcliwepkey12)

    def find_apcliwepkey15(self):
        self.exist_element(*self.apcliwepkey15)

