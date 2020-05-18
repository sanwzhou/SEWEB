#! -*-conding:utf-8 -*-
#@Time: 2019/4/3 0003 16:07
#@swzhou
'''
无线配置 - 无线基本配置 页面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'BasicConfigPage').getlog()
from common.ReadConfig import getMenu

class BasicConfigPage(BasePage):
    BasicConfigM = getMenu('BasicConfigM') #无线基本配置
    securitySetM = getMenu('securitySetM')#安全设置
    BandwidthsetM = getMenu('BandwidthsetM') #带宽设置

    wifiConfig = (By.XPATH, '//span[@data-local="{wifiConfig}"]')
    BasicConfig = (By.LINK_TEXT, BasicConfigM )
    securitySet = (By.LINK_TEXT,securitySetM)
    Bandwidthset = (By.LINK_TEXT,BandwidthsetM)

    add = (By.ID,'addWBConfig')
    ssid1 = (By.NAME, 'ssid1')
    encodeType1 = ('encodeType1')
    encodeType2 = ('encodeType2')
    fre2 = (By.XPATH,'//input[@name="spjk"and@value="fre2"]') #射频接口
    fre5 = (By.XPATH, '//input[@name="spjk"and@value="fre5"]')
    ifName = ('ifName') #接口名称
    gjxx = (By.ID,'gjxx') #高级选项
    broadcastEnablewEn = (By.XPATH,'//input[@name="broadcastEnablew1"and@value="0"]') #隐藏ssid 开启
    broadcastEnablewEns = ('//input[@name="broadcastEnablew1"and@value="0"]')
    broadcastEnablewC = (By.XPATH, '//input[@name="broadcastEnablew1"and@value="1"]')
    broadcastEnablewcs = ('//input[@name="broadcastEnablew1"and@value="1"]')
    wlanClientIsolationEn = (By.XPATH,'//input[@name="wlanClientIsolation"and@value="1"]') #无线客户端隔离开启
    wlanClientIsolationC = (By.XPATH, '//input[@name="wlanClientIsolation"and@value="0"]')
    LanWlanSep1En = (By.XPATH,'//input[@name="LanWlanSep1"and@value="1"]') #无线有线隔离开启
    LanWlanSep1C = (By.XPATH, '//input[@name="LanWlanSep1"and@value="0"]')

    list_ssid1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/a')
    list_ssid2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[3]/a')
    list_Mode1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span')
    list_Mode2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[8]/span')
    list_wifiInter1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    list_wifiInter2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span')
    list_wifipwd1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/a')
    list_wifipwd2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[9]/a')
    list_speed1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[10]/span')
    list_speed2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[10]/span')
    list_edit1 = (By.XPATH,'//span[@data-primarykey="0"and@data-event="edit"]')
    list_edit2 = (By.XPATH, '//span[@data-primarykey="1"and@data-event="edit"]')
    # 安全设置
    secMode1 = ('secMode1') #加密方式

    wepAuthMode1 = ('wepAuthMode1') #WEP 认证类型
    keyFormat = ('keyFormat')
    wpaAuthMode1 = ('wpaAuthMode1') #WPA/WPA2 WPA版本
    wpaCipher1 = ('wpaCipher1')
    radiusIP = (By.NAME,'radiusIP')
    radiusPort = (By.NAME,'radiusPort')
    radiusPsswd = (By.NAME,'radiusPsswd')
    keyUpdateCyc1 = (By.NAME,'keyUpdateCyc1')
    wpapskAuthMode1 = ('wpapskAuthMode1') #WPA-PSK/WPA2-PSK WPA版本
    wpapskCipher1 = ('wpapskCipher1')
    pskPsswd1 = (By.NAME,'pskPsswd1')
    pskkeyUpdateCyc1 = (By.NAME,'pskkeyUpdateCyc1')

    # 带宽设置
    share_sel1 = (By.XPATH, '//input[@name="share_select1"and@value="1"]') #共享
    share_sel2 = (By.XPATH, '//input[@name="share_select1"and@value="2"]') #独享
    txBand1 = (By.NAME, 'txBand1')
    rxBand1 = (By.NAME, 'rxBand1')
    save = (By.ID,'save')

    def click_wifiConfig(self):
        self.find_element(*self.wifiConfig).click()
        logger.info('点击无线配置')

    def click_BasicConfig(self):
        self.find_element(*self.BasicConfig).click()
        logger.info('点击无线基本配置')

    def click_securitySet(self):
        self.find_element(*self.securitySet).click()
        logger.info('点击安全配置')

    def click_Bandwidthset(self):
        self.find_element(*self.Bandwidthset).click()
        logger.info('点击带宽配置')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_ssid1(self, ssid1):
        self.find_element(*self.ssid1).clear()
        self.find_element(*self.ssid1).send_keys(ssid1)

    def click_fre2(self):
        self.find_element(*self.fre2).click()

    def click_fre5(self):
        self.find_element(*self.fre5).click()

    def click_gjxx(self):
        self.find_element(*self.gjxx).click()

    def click_broadcastEnablewEn(self):
        self.find_element(*self.broadcastEnablewEn).click()

    def click_broadcastEnablewC(self):
        self.find_element(*self.broadcastEnablewC).click()

    def click_wlanClientIsolationEn(self):
        self.find_element(*self.wlanClientIsolationEn).click()

    def click_wlanClientIsolationC(self):
        self.find_element(*self.wlanClientIsolationC).click()

    def click_LanWlanSep1En(self):
        self.find_element(*self.LanWlanSep1En).click()

    def click_LanWlanSep1C(self):
        self.find_element(*self.LanWlanSep1C).click()

    def input_radiusIP(self,radiusIP):
        self.find_element(*self.radiusIP).clear()
        self.find_element(*self.radiusIP).send_keys(radiusIP)

    def input_radiusPort(self,radiusPort):
        self.find_element(*self.radiusPort).clear()
        self.find_element(*self.radiusPort).send_keys(radiusPort)

    def input_radiusPsswd(self,radiusPsswd):
        self.find_element(*self.radiusPsswd).clear()
        self.find_element(*self.radiusPsswd).send_keys(radiusPsswd)

    def input_keyUpdateCyc1(self,keyUpdateCyc1):
        self.find_element(*self.keyUpdateCyc1).clear()
        self.find_element(*self.keyUpdateCyc1).send_keys(keyUpdateCyc1)

    def input_pskPsswd1(self, pskPsswd1):
        self.find_element(*self.pskPsswd1).clear()
        self.find_element(*self.pskPsswd1).send_keys(pskPsswd1)

    def input_pskkeyUpdateCyc1(self, pskkeyUpdateCyc1):
        self.find_element(*self.pskkeyUpdateCyc1).clear()
        self.find_element(*self.pskkeyUpdateCyc1).send_keys(pskkeyUpdateCyc1)

    def click_share_sel1(self):
        self.find_element(*self.share_sel1).click()

    def click_share_sel2(self):
        self.find_element(*self.share_sel2).click()

    def input_txBand1(self, txBand1):
        self.find_element(*self.txBand1).clear()
        self.find_element(*self.txBand1).send_keys(txBand1)

    def input_rxBand1(self, rxBand1):
        self.find_element(*self.rxBand1).clear()
        self.find_element(*self.rxBand1).send_keys(rxBand1)

    def click_list_edit1(self):
        self.find_element(*self.list_edit1).click()

    def click_list_edit2(self):
        self.find_element(*self.list_edit2).click()

    def click_save(self):
        self.find_element(*self.save).click()
