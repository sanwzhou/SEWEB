#! -*-conding:utf-8 -*-
#@Time: 2019/4/3 0003 16:47
#@swzhou
'''
功能说明
'''


import time
import unittest

from selenium.common.exceptions import NoSuchElementException

from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getParameter
from common.loginRoute import login
from common.GetExcelValue import getExcelValue
from common.GetRouteCPU import getCPUmodel
from pages.wifiConfig_001_BasicConfigPage import BasicConfigPage
from pages.wifiConfig_002_RFConfigPage import RFConfigPage
from pages.wifiConfig_003_WDSconfigPage import WDSconfigPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_009_wifiConfig').getlog()
wifiload2Gp = getParameter('wifiload2Gp')
support2 = getExcelValue(wifiload2Gp)
if '/' in support2:
    support2 = support2.strip(r'/')[0]
wifiload5Gp = getParameter('wifiload5Gp')
support5 = getExcelValue(wifiload5Gp)
if '/' in support5:
    support5 = support5.strip(r'/')[0]
# print(support2)

class WirelessParameters(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_wirelessMode(self):
        u'''射频信息&&无线模式'''
        wificonfig = RFConfigPage(self.driver, self.url)
        if str(support2).isdigit(): #判断字符串是否为数字
            logger.info('support:',support2)
            logger.info(u'参数支持2.4G无线')
            cpumodel = getCPUmodel()
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
                time.sleep(0.5)
            except AttributeError:
                CapPic(self.driver)
                logger.info(u'软件不支持无线配置，与参数表不符')
                raise Exception('软件不支持无线配置，与参数表不符')
            else:
                logger.info(u'软件支持无线配，与参数表相符')
                self.driver.implicitly_wait(10)
            wificonfig.click_RFConfig()
            time.sleep(1)
            #2.4G
            WrlessEn2 = wificonfig.getAttribute_byXpath(wificonfig.WrlessEn2s,'checked')
            self.assertEqual( WrlessEn2,'true',msg='2.4G默认未开启')
            mode_2 = wificonfig.selelement_byName(wificonfig.wrlessMode2)
            if cpumodel == 'MTK':
                Select(mode_2).select_by_value('6') #仅11n
                time.sleep(0.3)
                Select(mode_2).select_by_value('4')  # 仅11g
                time.sleep(0.3)
                Select(mode_2).select_by_value('9')  # 11b/g/n混合
                time.sleep(0.3)
            elif cpumodel == 'Qualcomm':
                Select(mode_2).select_by_value('1')  # 仅11n
                time.sleep(0.3)
                Select(mode_2).select_by_value('2')  # 仅11g
                time.sleep(0.3)
                Select(mode_2).select_by_value('6')  # 11b/g/n混合
                time.sleep(0.3)
            channel_2 = wificonfig.selelement_byName(wificonfig.channel2)
            Select(channel_2).select_by_value('1')
            time.sleep(0.2)
            Select(channel_2).select_by_value('2')
            time.sleep(0.2)
            Select(channel_2).select_by_value('3')
            time.sleep(0.2)
            Select(channel_2).select_by_value('4')
            time.sleep(0.2)
            Select(channel_2).select_by_value('5')
            time.sleep(0.2)
            Select(channel_2).select_by_value('6')
            time.sleep(0.2)
            Select(channel_2).select_by_value('7')
            time.sleep(0.2)
            Select(channel_2).select_by_value('8')
            time.sleep(0.2)
            Select(channel_2).select_by_value('9')
            time.sleep(0.2)
            Select(channel_2).select_by_value('10')
            time.sleep(0.2)
            Select(channel_2).select_by_value('11')
            time.sleep(0.2)
            Select(channel_2).select_by_value('0') #自动
            time.sleep(0.2)
            chanWidth_2 = wificonfig.selelement_byName(wificonfig.chanWidth2)
            if cpumodel == 'MTK':
                Select(chanWidth_2).select_by_value('1') #自动
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('0')  # 20M
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('2')  # 40M
                time.sleep(0.2)
            elif cpumodel == 'Qualcomm':
                Select(chanWidth_2).select_by_value('0')  # 自动
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('1')  # HT20
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('2')  # HT40-
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('3')  # HT40
                time.sleep(0.2)
                Select(chanWidth_2).select_by_value('4')  # HT40+
                time.sleep(0.2)
            wificonfig.click_gjxxa()
            time.sleep(0.5)
            wificonfig.input_beacon2('100')
            wificonfig.input_rts2('1')
            wificonfig.input_fragment2('256')
            wificonfig.input_dtim2('255')
            wificonfig.click_wmmC2()
            wificonfig.click_wmmEn2()
            wificonfig.click_shortC2()
            wificonfig.click_shortEn2()
            #5G
            if support5 != '--':
                try:
                    self.driver.implicitly_wait(2)
                    WrlessEn5 = wificonfig.getAttribute_byXpath(wificonfig.WrlessEn5s, 'checked')
                    self.assertEqual(WrlessEn5, 'true', msg='5G默认未开启')
                except AttributeError:
                    CapPic(self.driver)
                    logger.info(u'软件不支持5G，与参数表不符')
                    raise Exception('软件不支持5G，与参数表不符')
                else:
                    logger.info(u'软件支持5G，与参数表相符')
                    self.driver.implicitly_wait(10)
                WrlessEn5 = wificonfig.getAttribute_byXpath(wificonfig.WrlessEn5s,'checked')
                self.assertEqual(WrlessEn5, 'true', msg='5G默认未开启')
                mode_5 = wificonfig.selelement_byName(wificonfig.wrlessMode5)
                if cpumodel == 'MTK':
                    Select(mode_5).select_by_value('2')
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('8')
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('14')
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('15')
                    time.sleep(0.3)
                elif cpumodel == 'Qualcomm':
                    Select(mode_5).select_by_value('1') #仅11n
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('3') #仅11a
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('4') #11a/n混合
                    time.sleep(0.3)
                    Select(mode_5).select_by_value('5') #11ac
                    time.sleep(0.3)
                channel_5 = wificonfig.selelement_byName(wificonfig.channel5)
                Select(channel_5).select_by_value('36')
                time.sleep(0.2)
                Select(channel_5).select_by_value('40')
                time.sleep(0.2)
                Select(channel_5).select_by_value('44')
                time.sleep(0.2)
                Select(channel_5).select_by_value('48')
                time.sleep(0.2)
                Select(channel_5).select_by_value('52')
                time.sleep(0.2)
                Select(channel_5).select_by_value('56')
                time.sleep(0.2)
                Select(channel_5).select_by_value('60')
                time.sleep(0.2)
                Select(channel_5).select_by_value('64')
                time.sleep(0.2)
                Select(channel_5).select_by_value('149')
                time.sleep(0.2)
                Select(channel_5).select_by_value('153')
                time.sleep(0.2)
                Select(channel_5).select_by_value('157')
                time.sleep(0.2)
                Select(channel_5).select_by_value('161')
                time.sleep(0.2)
                Select(channel_5).select_by_value('165')
                time.sleep(0.2)
                Select(channel_5).select_by_value('0')  # 自动
                time.sleep(0.2)
                chanWidth_5 = wificonfig.selelement_byName(wificonfig.chanWidth5)
                if cpumodel == 'MTK':
                    Select(chanWidth_5).select_by_value('1')  # 自动
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('2')  # 20M
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('0')  # 40M
                    time.sleep(0.2)
                    vhtChanWidth_5 = wificonfig.selelement_byName(wificonfig.vhtChanWidth_5)
                    time.sleep(0.3)
                    Select(vhtChanWidth_5).select_by_value('1')  # HT80
                    time.sleep(0.2)
                    Select(vhtChanWidth_5).select_by_value('0')  # 20/40
                    time.sleep(0.2)
                elif cpumodel == 'Qualcomm':
                    Select(chanWidth_5).select_by_value('0')  # 自动
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('1')  # HT20
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('2')  # HT40-
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('3')  # HT40
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('4')  # HT40+
                    time.sleep(0.2)
                    Select(chanWidth_5).select_by_value('5')  # HT80
                    time.sleep(0.2)
                wificonfig.input_beacon5('100')
                wificonfig.input_rts5('1')
                wificonfig.input_fragment5('256')
                wificonfig.input_dtim5('255')
                wificonfig.click_wmmC5()
                wificonfig.click_wmmEn5()
                wificonfig.click_shortC5()
                wificonfig.click_shortEn5()
            elif support5 == '--':
                logger.info(u'参数不支持5G无线')
                try:
                    self.driver.implicitly_wait(2)
                    wificonfig.getAttribute_byXpath(wificonfig.WrlessEn5s, 'checked')
                except AttributeError :
                    logger.info(u'软件不支持5G无线，与参数表相符')
                except NoSuchElementException:
                    logger.info(u'软件不支持5G无线，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持5G无线，与参数表不符')
                    raise Exception(u'软件支持5G无线，与参数表不符')
            else:
                logger.info(u'参数表读取异常')
                logger.info(u'参数表读取值为：', support5)
                raise Exception(u'参数表读取异常')
        else:
            logger.info(u'参数不支持2.4G无线')
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
            except AttributeError:
                logger.info(u'软件不支持2.4G无线，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持2.4G无线，与参数表不符')
                raise Exception(u'软件支持2.4G无线，与参数表不符')
        self.driver.quit()
        logger.info('test_001_wirelessMode passed')

    def test_002_WDSconfig(self):
        u'''2.4G/5G工作模式：WDS'''
        wificonfig = WDSconfigPage(self.driver, self.url)
        if str(support2).isdigit():
            logger.info(u'参数支持2.4G无线')
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
                time.sleep(0.5)
            except AttributeError:
                CapPic(self.driver)
                logger.info(u'软件不支持无线配置，与参数表不符')
                raise Exception('软件不支持无线配置，与参数表不符')
            else:
                logger.info(u'软件支持无线配，与参数表相符')
                self.driver.implicitly_wait(10)
            wificonfig.click_wsdconfig()
            time.sleep(1)
            #2.4G WDS
            wificonfig.click_wdsEn2()
            wificonfig.click_wdsC2()
            wificonfig.input_bridgessid2('test')
            wificonfig.input_briggebssid2('11:22:33:44:55:66')
            wificonfig.find_wdsscan2()
            apclisecmode_2 = wificonfig.selelement_byName(wificonfig.apclisecmode2)
            Select(apclisecmode_2).select_by_value('WEP')
            time.sleep(0.5)
            apclikeyFormat_2 = wificonfig.selelement_byName(wificonfig.apclikeyFormat2)
            Select(apclikeyFormat_2).select_by_value('1') #ASCII码
            time.sleep(0.2)
            Select(apclikeyFormat_2).select_by_value('0')  # 16进制
            time.sleep(0.2)
            wificonfig.find_apcliwepkey12()
            Select(apclisecmode_2).select_by_value('WPAPSK')
            time.sleep(0.5)
            apcliwpapskAuthMode_2 = wificonfig.selelement_byName(wificonfig.apcliwpapskAuthMode2)
            Select(apcliwpapskAuthMode_2).select_by_value('WPAPSK')
            time.sleep(0.2)
            Select(apcliwpapskAuthMode_2).select_by_value('WPA2PSK')
            time.sleep(0.2)
            apcliwpapskCipher_2 = wificonfig.selelement_byName(wificonfig.apcliwpapskCipher2)
            Select(apcliwpapskCipher_2).select_by_value('TKIP')
            time.sleep(0.2)
            Select(apcliwpapskCipher_2).select_by_value('AES')
            time.sleep(0.2)
            wificonfig.input_apclipskPsswd2('123')
            # 5G WDS
            if support5 != '--':
                try:
                    self.driver.implicitly_wait(2)
                    wificonfig.click_wsdconfig5()
                    time.sleep(1)
                except AttributeError:
                    CapPic(self.driver)
                    logger.info(u'软件不支持5G，与参数表不符')
                    raise Exception('软件不支持5G，与参数表不符')
                else:
                    logger.info(u'软件支持5G，与参数表相符')
                    self.driver.implicitly_wait(10)
                wificonfig.click_wdsC5()
                wificonfig.click_wdsEn5()
                wificonfig.input_bridgessid5('test')
                wificonfig.input_briggebssid5('22:33:44:55:66:77')
                wificonfig.find_wdsscan5()
                apclisecmode_5 = wificonfig.selelement_byXpath(wificonfig.apclisecmode5)
                Select(apclisecmode_5).select_by_value('WEP')
                time.sleep(0.5)
                apclikeyFormat_5 = wificonfig.selelement_byXpath(wificonfig.apclikeyFormat5)
                Select(apclikeyFormat_5).select_by_value('1')  # ASCII码
                time.sleep(0.2)
                Select(apclikeyFormat_5).select_by_value('0')  # 16进制
                time.sleep(0.2)
                wificonfig.find_apcliwepkey15()
                Select(apclisecmode_5).select_by_value('WPAPSK')
                time.sleep(0.5)
                apcliwpapskAuthMode_5 = wificonfig.selelement_byXpath(wificonfig.apcliwpapskAuthMode5)
                Select(apcliwpapskAuthMode_5).select_by_value('WPAPSK')
                time.sleep(0.2)
                Select(apcliwpapskAuthMode_5).select_by_value('WPA2PSK')
                time.sleep(0.2)
                apcliwpapskCipher_5 = wificonfig.selelement_byXpath(wificonfig.apcliwpapskCipher5)
                Select(apcliwpapskCipher_5).select_by_value('TKIP')
                time.sleep(0.2)
                Select(apcliwpapskCipher_5).select_by_value('AES')
                time.sleep(0.2)
                wificonfig.input_apclipskPsswd5('234')
            elif support5 == '--':
                logger.info(u'参数不支持5G无线')
                try:
                    self.driver.implicitly_wait(2)
                    wificonfig.click_wsdconfig5()
                except AttributeError:
                    logger.info(u'软件不支持5G无线，与参数表相符')
                except NoSuchElementException:
                    logger.info(u'软件不支持5G无线，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持5G无线，与参数表不符')
                    raise Exception(u'软件支持5G无线，与参数表不符')
            else:
                logger.info(u'参数表读取异常')
                logger.info(u'参数表读取值为：', support5)
                raise Exception(u'参数表读取异常')
        else:
            logger.info(u'参数不支持2.4G无线')
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
            except AttributeError:
                logger.info(u'软件不支持2.4G无线，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持2.4G无线，与参数表不符')
                raise Exception(u'软件支持2.4G无线，与参数表不符')
        self.driver.quit()
        print('test_002_WDSconfig passed')

    def test_003_WirelessSecurity(self):
        u'''无线安全'''
        wificonfig = BasicConfigPage(self.driver,self.url)
        if str(support2).isdigit():
            logger.info(u'参数2.4G无线')
            cpumodel = getCPUmodel()
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
                time.sleep(0.5)
            except AttributeError:
                CapPic(self.driver)
                logger.info(u'软件不支持无线配置，与参数表不符')
                raise Exception('软件不支持无线配置，与参数表不符')
            else:
                logger.info(u'软件支持无线配，与参数表相符')
                self.driver.implicitly_wait(10)
            wificonfig.click_BasicConfig()
            time.sleep(1)
            wificonfig.click_add()
            time.sleep(1)
            #主编码
            wificonfig.input_ssid1('test')
            encodeType1 = wificonfig.selelement_byName(wificonfig.encodeType1)
            Select(encodeType1).select_by_value('GBK')
            time.sleep(0.2)
            Select(encodeType1).select_by_value('UTF-8')
            time.sleep(0.2)
            Select(encodeType1).select_by_value('BIG5')
            time.sleep(0.2)
            #备用编码
            encodeType2 = wificonfig.selelement_byName(wificonfig.encodeType2)
            Select(encodeType2).select_by_value('GBK')
            time.sleep(0.2)
            Select(encodeType2).select_by_value('UTF-8')
            time.sleep(0.2)
            Select(encodeType2).select_by_value('BIG5')
            time.sleep(0.2)
            Select(encodeType2).select_by_value('NONE')
            time.sleep(0.2)
            #射频接口
            wificonfig.click_fre2()
            if support5 != '--':
                try:
                    self.driver.implicitly_wait(2)
                    wificonfig.click_fre5()
                    time.sleep(1)
                except AttributeError:
                    CapPic(self.driver)
                    logger.info(u'软件不支持5G，与参数表不符')
                    raise Exception('软件不支持5G，与参数表不符')
                else:
                    logger.info(u'软件支持5G，与参数表相符')
            else:
                logger.info(u'参数不支持5G无线')
                try:
                    self.driver.implicitly_wait(2)
                    wificonfig.click_fre5()
                except AttributeError:
                    logger.info(u'软件不支持5G无线，与参数表相符')
                except NoSuchElementException:
                    logger.info(u'软件不支持5G无线，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持5G无线，与参数表不符')
                    raise Exception(u'软件支持5G无线，与参数表不符')
            self.driver.implicitly_wait(10)
            #接口名称
            ifName = wificonfig.selelement_byName(wificonfig.ifName)
            Select(ifName).select_by_value('default')
            #高级选项
            wificonfig.click_gjxx()
            time.sleep(0.5)
            #隐藏ssid
            wificonfig.click_broadcastEnablewEn()
            wificonfig.click_broadcastEnablewC()
            #无线客户端隔离
            wificonfig.click_wlanClientIsolationEn()
            wificonfig.click_wlanClientIsolationC()
            #无线有线隔离
            wificonfig.click_LanWlanSep1En()
            wificonfig.click_LanWlanSep1C()
            #安全设置
            wificonfig.click_securitySet()
            time.sleep(1)
            secMode1 = wificonfig.selelement_byName(wificonfig.secMode1)
            Select(secMode1).select_by_value('NONE')
            time.sleep(0.2)
            if cpumodel == 'MTK': #高通暂不支持WEP
                Select(secMode1).select_by_value('WEP')
                time.sleep(0.2)
                wepAuthMode1 = wificonfig.selelement_byName(wificonfig.wepAuthMode1)
                Select(wepAuthMode1).select_by_value('OPEN')
                time.sleep(0.2)
                Select(wepAuthMode1).select_by_value('SHARED')
                time.sleep(0.2)
                Select(wepAuthMode1).select_by_value('WEPAUTO')
                time.sleep(0.2)
            Select(secMode1).select_by_value('WPA')
            time.sleep(0.5)
            wpaAuthMode1 = wificonfig.selelement_byName(wificonfig.wpaAuthMode1)
            Select(wpaAuthMode1).select_by_value('WPA')
            time.sleep(0.2)
            Select(wpaAuthMode1).select_by_value('WPA2')
            time.sleep(0.2)
            Select(wpaAuthMode1).select_by_value('WPA1WPA2')
            time.sleep(0.2)
            wpaCipher1 = wificonfig.selelement_byName(wificonfig.wpaCipher1)
            Select(wpaCipher1).select_by_value('TKIP')
            time.sleep(0.2)
            Select(wpaCipher1).select_by_value('AES')
            time.sleep(0.2)
            Select(wpaCipher1).select_by_value('TKIPAES')
            time.sleep(0.2)
            wificonfig.input_radiusIP('1.2.3.4')
            wificonfig.input_radiusPort('1814')
            wificonfig.input_radiusPsswd('12345678')
            wificonfig.input_keyUpdateCyc1('3000')
            Select(secMode1).select_by_value('WPAPSK')
            time.sleep(0.5)
            wpapskAuthMode1 = wificonfig.selelement_byName(wificonfig.wpapskAuthMode1)
            Select(wpapskAuthMode1).select_by_value('WPAPSKWPA2PSK')
            time.sleep(0.2)
            Select(wpapskAuthMode1).select_by_value('WPAPSK')
            time.sleep(0.2)
            Select(wpapskAuthMode1).select_by_value('WPA2PSK')
            time.sleep(0.2)
            wpapskCipher1 = wificonfig.selelement_byName(wificonfig.wpapskCipher1)
            Select(wpapskCipher1).select_by_value('TKIP')
            time.sleep(0.2)
            Select(wpapskCipher1).select_by_value('AES')
            time.sleep(0.2)
            Select(wpapskCipher1).select_by_value('TKIPAES')
            time.sleep(0.2)
            wificonfig.input_pskPsswd1('12345678')
            wificonfig.input_pskkeyUpdateCyc1('3000')
            # 带宽设置
            wificonfig.click_Bandwidthset()
            time.sleep(0.5)
            wificonfig.click_share_sel1()
            wificonfig.click_share_sel2()
            wificonfig.input_rxBand1('1000')
            wificonfig.input_txBand1('2000')
        else:
            logger.info(u'参数不支持2.4G无线')
            try:
                self.driver.implicitly_wait(2)
                wificonfig.click_wifiConfig()
            except AttributeError:
                logger.info(u'软件不支持2.4G无线，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持2.4G无线，与参数表不符')
                raise Exception(u'软件支持2.4G无线，与参数表不符')
        self.driver.quit()

        logger.info('test_003_WirelessSecurity passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

