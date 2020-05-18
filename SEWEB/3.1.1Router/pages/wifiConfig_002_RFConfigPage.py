#! -*-conding:utf-8 -*-
#@Time: 2019/4/3 0003 17:16
#@swzhou
'''
无线配置 - 射频配置 页面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'RFConfigPage').getlog()
from common.ReadConfig import getMenu

class RFConfigPage(BasePage):
    RFConfigM = getMenu('RFConfigM')

    wifiConfig = (By.XPATH, '//span[@data-local="{wifiConfig}"]') #无线配置
    RFConfig = (By.LINK_TEXT,RFConfigM)

    WrlessEn2 = (By.XPATH,'//input[@name="WrlessEnable"and@value="on"]')
    WrlessEn2s = ('//input[@name="WrlessEnable"and@value="on"]')
    wrlessMode2 = ('wrlessMode')
    wrlessMode2_11nM = ('//*[@id="divleft"]/table/tbody/tr[3]/td[2]/select/option[2]') #mtk2.4G 模式11n
    wrlessMode2_11nM1 = ('//*[@id="1"]/div/table/tbody/tr[3]/td[2]/select/option[2]')  # mtk2.4G 模式11n 不支持5G的
    wrlessMode2_11nQ = ('//*[@id="divleft"]/table/tbody/tr[3]/td[2]/select/option[1]')  #高通 2.4G 模式11n
    channel2 = ('channel')
    channel2_71 = ('//*[@id="1"]/div/table/tbody/tr[4]/td[2]/select/option[8]') #不支持5G的2.4G 信道7
    channel2_7 = ('//*[@id="divleft"]/table/tbody/tr[4]/td[2]/select/option[8]') #2.4G 信道7 支持5G的
    chanWidth2 = ('chanWidth')
    chanWidth2_40M = ('//*[@id="divleft"]/table/tbody/tr[5]/td[2]/select/option[3]') #mtk2.4G 频宽40M
    chanWidth2_40M1 = ('//*[@id="1"]/div/table/tbody/tr[5]/td[2]/select/option[3]')  # mtk2.4G 频宽40M 不支持5G的
    chanWidth2_40Q = ('//*[@id="divleft"]/table/tbody/tr[5]/td[2]/select/option[4]')  # 高通2.4G 频宽40M
    gjxxa = (By.ID,'gjxxa')
    beacon2 = (By.NAME,'beacon') #信标间隔
    rts2 = (By.NAME,'rts') #RTS阈值
    fragment2 = (By.NAME,'fragment') #分段阈值
    dtim2 = (By.NAME,'dtim') #DTIM间隔
    wmmEn2 = (By.XPATH, '//input[@name="wmm_capable"and@value="1"]')#wmm
    wmmC2 = (By.XPATH, '//input[@name="wmm_capable"and@value="0"]')
    shortEn2 = (By.XPATH, '//input[@name="short_preamble"and@value="1"]')# 短前导码
    shortC2 = (By.XPATH, '//input[@name="short_preamble"and@value="0"]')
    WrlessEn5 = (By.XPATH, '//input[@name="WrlessEnable_5"and@value="on"]')
    WrlessEn5s = ('//input[@name="WrlessEnable_5"and@value="on"]')
    wrlessMode5 = ('wrlessMode_5')
    wrlessMode5_15M = ('//*[@id="divright"]/table/tbody/tr[3]/td[2]/select/option[4]') #mtk5G模式 11vht AC/AN
    wrlessMode5_15Q = ('//*[@id="divright"]/table/tbody/tr[3]/td[2]/select/option[4]')  #高通 5G模式 11ac
    channel5 = ('channel_5')
    channel5_36 = ('//*[@id="divright"]/table/tbody/tr[5]/td[2]/select/option[2]') #5G模式 信道36
    channel5_36_2 = ('//*[@id="divright"]/table/tbody/tr[6]/td[2]/select/option[2]')  # 5G模式 信道36 美国版本多一个country
    chanWidth5 = ('chanWidth_5')
    chanWidth5_40M = ('//*[@id="divright"]/table/tbody/tr[6]/td[2]/select/option[3]') #mtk5G模式 频宽40
    chanWidth5_40M_2 = ('//*[@id="divright"]/table/tbody/tr[7]/td[2]/select/option[3]')  # mtk5G模式 频宽40 美国版本
    chanWidth5_40Q = ('//*[@id="divright"]/table/tbody/tr[6]/td[2]/select/option[4]')  # 高通 5G模式 频宽40
    chanWidth5_40Q_2 = ('//*[@id="divright"]/table/tbody/tr[7]/td[2]/select/option[4]')  #高通 5G模式 频宽40 美国版本
    beacon5 = (By.NAME,'beacon_5')  # 信标间隔
    rts5 = (By.NAME,'rts_5')  # RTS阈值
    fragment5 = (By.NAME,'fragment_5')  # 分段阈值
    dtim5 = (By.NAME,'dtim_5')  # DTIM间隔
    wmmEn5 = (By.XPATH, '//input[@name="wmm_capable_5"and@value="1"]')#wmm
    wmmC5 = (By.XPATH, '//input[@name="wmm_capable_5"and@value="0"]')
    shortEn5 = (By.XPATH, '//input[@name="short_preamble_5"and@value="1"]')# 短前导码
    shortC5 = (By.XPATH, '//input[@name="short_preamble_5"and@value="0"]')
    vhtChanWidth_5 = ('vhtChanWidth_5') #VHT频道带宽
    save = (By.ID,'save')

    def click_wifiConfig(self):
        self.find_element(*self.wifiConfig).click()
        logger.info('点击无线配置')

    def click_RFConfig(self):
        self.find_element(*self.RFConfig).click()
        logger.info('点击射频配置')

    def click_WrlessEn2 (self):
        self.find_element(*self.WrlessEn2 ).click()

    def click_gjxxa(self):
        self.find_element(*self.gjxxa).click()

    def click_WrlessEn5(self):
        self.find_element(*self.WrlessEn5).click()

    def input_beacon2(self,beacon2):
        self.find_element(*self.beacon2).clear()
        self.find_element(*self.beacon2).send_keys(beacon2)

    def input_rts2(self,rts2):
        self.find_element(*self.rts2).clear()
        self.find_element(*self.rts2).send_keys(rts2)

    def input_fragment2(self, fragment2):
        self.find_element(*self.fragment2).clear()
        self.find_element(*self.fragment2).send_keys(fragment2)

    def input_dtim2(self, dtim2):
        self.find_element(*self.dtim2).clear()
        self.find_element(*self.dtim2).send_keys(dtim2)

    def input_beacon5(self,beacon5):
        self.find_element(*self.beacon5).clear()
        self.find_element(*self.beacon5).send_keys(beacon5)

    def input_rts5(self,rts5):
        self.find_element(*self.rts5).clear()
        self.find_element(*self.rts5).send_keys(rts5)

    def input_fragment5(self, fragment5):
        self.find_element(*self.fragment5).clear()
        self.find_element(*self.fragment5).send_keys(fragment5)

    def input_dtim5(self, dtim5):
        self.find_element(*self.dtim5).clear()
        self.find_element(*self.dtim5).send_keys(dtim5)

    def click_wmmEn2 (self):
        self.find_element(*self.wmmEn2).click()

    def click_wmmC2(self):
        self.find_element(*self.wmmC2).click()

    def click_shortEn2(self):
        self.find_element(*self.shortEn2).click()

    def click_shortC2 (self):
        self.find_element(*self.shortC2).click()

    def click_wmmEn5(self):
        self.find_element(*self.wmmEn5).click()

    def click_wmmC5(self):
        self.find_element(*self.wmmC5).click()

    def click_shortEn5(self):
        self.find_element(*self.shortEn5).click()

    def click_shortC5(self):
        self.find_element(*self.shortC5).click()

    def click_save(self):
        self.find_element(*self.save).click()