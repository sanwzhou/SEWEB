#! -*-conding:utf-8 -*-
#@Time: 2019/4/8 0008 16:21
#@swzhou
'''
配置向导配置无线SSID、加密、模式、信道、带宽，生效
'''


import time
import unittest
import telnetlib
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getParameter,gettelnet,getweb,getAssertText
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from common.GetRouteCPU import getCPUmodel
from pages.ConfigGuidepage import ConfigGuidepage
from pages.wifiConfig_001_BasicConfigPage import BasicConfigPage
from pages.wifiConfig_002_RFConfigPage import RFConfigPage
logger = LogGen(Logger = 'WIFIconfig_001_configGuide').getlog()
wifiload2Gp = getParameter('wifiload2Gp')
support2 = getExcelValue(wifiload2Gp)
wifiload5Gp = getParameter('wifiload5Gp')
support5 = getExcelValue(wifiload5Gp)
# print('support2:',support2)
# print('support5:',support5)
host = gettelnet('host')
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")
languageA = getAssertText('languageA')

class guide(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_ConfigGuide(self):
        u'''配置向导配置无线'''
        cpumodel = getCPUmodel()
        guide = ConfigGuidepage(self.driver, self.url)
        guide.click_configGuide()
        time.sleep(0.5)
        guide.click_next()
        time.sleep(1)
        # guide.click_next() #不修改接入方式
        # time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            guide.click_next()
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'配置向导中，不支持wifi参数配置')
            raise Exception('配置向导中，不支持wifi参数配置')
        else:
            time.sleep(1)
        guide.input_ssid('test3_2.4')
        guide.input_passwd('12345678')
        channel = guide.selelement_byName(guide.channel)
        Select(channel).select_by_value('7')
        wrlessMode = guide.selelement_byName(guide.wrlessMode)
        chanWidth = guide.selelement_byName(guide.chanWidth)
        if cpumodel == 'MTK':
            Select(wrlessMode).select_by_value('6') #mtk 11n
            Select(chanWidth).select_by_value('2') #mtk为40M
        elif cpumodel == 'Qualcomm':
            Select(wrlessMode).select_by_value('1') #高通 11n
            Select(chanWidth).select_by_value('3') #高通 40M
        if support5 != '--':
            try:
                guide.find_ssid_5g()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持5G，与参数表不相符')
                raise Exception('不支持5G，与参数表不相符')
            guide.input_ssid_5g('test3_5')
            guide.input_passwd_5g('12345678')
            channel_5g = guide.selelement_byName(guide.channel_5g)
            Select(channel_5g).select_by_value('36')
            wrlessMode_5g = guide.selelement_byName(guide.wrlessMode_5g)
            chanWidth_5g = guide.selelement_byName(guide.chanWidth_5g)
            if cpumodel == 'MTK':
                Select(wrlessMode_5g).select_by_value('15')  # mtk 11vht AC/AN
                Select(chanWidth_5g).select_by_value('2')  # mtk为40M
            elif cpumodel == 'Qualcomm':
                Select(wrlessMode_5g).select_by_value('5')  # 高通 11ac
                Select(chanWidth_5g).select_by_value('3')  # 高通 HT40
        guide.click_okey()
        time.sleep(35)

        self.driver.implicitly_wait(10)
        basicConfig = BasicConfigPage(self.driver,self.url)
        basicConfig.click_wifiConfig()
        time.sleep(0.5)
        basicConfig.click_BasicConfig()
        time.sleep(1)
        lsit_ssid1 = basicConfig.getText_byXpath(basicConfig.list_ssid1)
        self.assertEqual(lsit_ssid1,'test3_2.4',msg='2.4G SSID保存异常')
        lsit_Mode1 = basicConfig.getText_byXpath(basicConfig.list_Mode1)
        self.assertEqual(lsit_Mode1, 'WPA-PSK/WPA2-PSK', msg='2.4G密码加密模式异常')
        list_wifipwd1 = basicConfig.getAttribute_byXpath(basicConfig.list_wifipwd1,'data-local')
        self.assertEqual(list_wifipwd1, '12345678', msg='2.4G密码保存异常')
        tn = telnetlib.Telnet(host=host, port=port,timeout=10) #telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep -E "SSID1|WPAPSK1"' + b'\n')
        elif cpumodel == "Qualcomm":
            tn.write(b'cat /etc/Wireless/wifi0/qca_ath0.dat | grep -E "ssid|key"' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if cpumodel == "MTK":
            if "SSID1=test3_2.4" in result:
                print('2.4G SSID配置正常')
            else:
                raise Exception('2.4G SSID配置异常')
            if "WPAPSK1=12345678" in result:
                print('2.4G 密码配置正常')
            else:
                raise Exception('2.4G 密码配置异常')
        elif cpumodel == "Qualcomm":
            if "ssid=test3_2.4" in result:
                print('2.4G SSID配置正常')
            else:
                raise Exception('2.4G SSID配置异常')
            if "key=12345678" in result:
                print('2.4G 密码配置正常')
            else:
                raise Exception('2.4G 密码配置异常')
        tn.close()  # tn.write('exit\n')
        if support5 != '--':
            time.sleep(5)
            try:
                lsit_ssid2 = basicConfig.getText_byXpath(basicConfig.list_ssid2)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持5G，与参数表不相符')
                raise Exception('不支持5G，与参数表不相符')
            self.assertEqual(lsit_ssid2, 'test3_5', msg='5G SSID保存异常')
            lsit_Mode2 = basicConfig.getText_byXpath(basicConfig.list_Mode2)
            self.assertEqual(lsit_Mode2, 'WPA-PSK/WPA2-PSK', msg='5G密码加密模式异常')
            list_wifipwd2 = basicConfig.getAttribute_byXpath(basicConfig.list_wifipwd2, 'data-local')
            self.assertEqual(list_wifipwd2, '12345678', msg='5G密码保存异常')
            tn = telnetlib.Telnet(host=host, port=port,timeout=10)  # telnet验证
            tn.set_debuglevel(5)
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            if cpumodel == "MTK":
                tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat  | grep -E "SSID1|WPAPSK1"' + b'\n')
            elif cpumodel == "Qualcomm":
                tn.write(b'cat /etc/Wireless/wifi1/qca_ath1.dat | grep -E "ssid|key"' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 判断
            if cpumodel == "MTK":
                if "SSID1=test3_5" in result:
                    print('5G SSID配置正常')
                else:
                    raise Exception('5G SSID配置异常')
                if "WPAPSK1=12345678" in result:
                    print('5G 密码配置正常')
                else:
                    raise Exception('5G 密码配置异常')
            elif cpumodel == "Qualcomm":
                if "ssid=test3_5" in result:
                    print('5G SSID配置正常')
                else:
                    raise Exception('5G SSID配置异常')
                if "key=12345678" in result:
                    print('5G 密码配置正常')
                else:
                    raise Exception('5G 密码配置异常')
            tn.close()  # tn.write('exit\n')

        rfConfig = RFConfigPage(self.driver, self.url)
        rfConfig.click_RFConfig()
        time.sleep(1)
        if support5 != '--':
            channel2_7 = rfConfig.getAttribute_byXpath(rfConfig.channel2_7, 'selected')
            if cpumodel == "MTK":
                wrlessMode2_11n = rfConfig.getAttribute_byXpath(rfConfig.wrlessMode2_11nM, 'selected')
                chanWidth2_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth2_40M, 'selected')
            elif cpumodel == "Qualcomm":
                wrlessMode2_11n = rfConfig.getAttribute_byXpath(rfConfig.wrlessMode2_11nQ, 'selected')
                chanWidth2_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth2_40Q, 'selected')
        else:
            channel2_7 = rfConfig.getAttribute_byXpath(rfConfig.channel2_71, 'selected')
            if cpumodel == "MTK":
                wrlessMode2_11n = rfConfig.getAttribute_byXpath(rfConfig.wrlessMode2_11nM1, 'selected')
                chanWidth2_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth2_40M1, 'selected')
        self.assertEqual(channel2_7, 'true', msg='2.4G信道不为7')

        self.assertEqual(wrlessMode2_11n, 'true', msg='2.4G模式不为11n')
        self.assertEqual(chanWidth2_40, 'true', msg='2.4G频宽不为40M')
        tn = telnetlib.Telnet(host=host, port=port,timeout=10)  # telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep -E "WirelessMode|Channel|HT_BW|HT_BSSCoexistence"' + b'\n')
        elif cpumodel == "Qualcomm":
            tn.write(b'cat /etc/Wireless/wifi0/qca_ath0.dat | grep -E "hwmode|channel|htmode"' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if cpumodel == "MTK":
            if "WirelessMode=6" in result: #11n
                print('2.4G模式配置正常')
            else:
                raise Exception('2.4G模式配置异常')
            if "Channel=7" in result:
                print('2.4G信道配置正常')
            else:
                raise Exception('2.4G信道配置异常')
            if "HT_BW=1" and "HT_BSSCoexistence=0" in result:#40M
                print('2.4G频宽配置正常')
            else:
                raise Exception('2.4G频宽配置异常')
        elif cpumodel == "Qualcomm":
            if "hwmode=11n" in result: #11n
                print('2.4G模式配置正常')
            else:
                raise Exception('2.4G模式配置异常')
            if "channel=7" in result:
                print('2.4G信道配置正常')
            else:
                raise Exception('2.4G信道配置异常')
            if "htmode=HT40" in result:#40M
                print('2.4G频宽配置正常')
            else:
                raise Exception('2.4G频宽配置异常')
        tn.close()  # tn.write('exit\n')
        if support5 != '--':
            try:
                if cpumodel == "MTK":
                    wrlessMode5_15 = rfConfig.getAttribute_byXpath(rfConfig.wrlessMode5_15M,'selected')
                elif cpumodel == "Qualcomm":
                    wrlessMode5_15 = rfConfig.getAttribute_byXpath(rfConfig.wrlessMode5_15Q, 'selected')
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持5G，与参数表不相符')
                raise Exception('不支持5G，与参数表不相符')
            self.assertEqual(wrlessMode5_15, 'true', msg='5G模式不为 11vht AC/AN')
            if languageA == 'English':
                channel5_36 = rfConfig.getAttribute_byXpath(rfConfig.channel5_36_2, 'selected')#英文版本多一个国家码
            else:
                channel5_36 = rfConfig.getAttribute_byXpath(rfConfig.channel5_36, 'selected')
            self.assertEqual(channel5_36, 'true', msg='5G信道不为36')
            if cpumodel == "MTK":
                if languageA == 'English':
                    chanWidth5_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth5_40M_2, 'selected')
                else:
                    chanWidth5_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth5_40M, 'selected')
            elif cpumodel == "Qualcomm":
                if languageA == 'English':
                    chanWidth5_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth5_40Q_2, 'selected')
                else:
                    chanWidth5_40 = rfConfig.getAttribute_byXpath(rfConfig.chanWidth5_40Q, 'selected')
            self.assertEqual(chanWidth5_40, 'true', msg='5G频宽不为40M')
            tn = telnetlib.Telnet(host=host, port=port,timeout=10)  # telnet验证
            tn.set_debuglevel(5)
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            if cpumodel == "MTK":
                tn.write(
                    b'cat /etc/Wireless/iNIC/iNIC_ap.dat | grep -E "WirelessMode|Channel|HT_BW|HT_BSSCoexistence"' + b'\n')  # 无线隔离
            elif cpumodel == "Qualcomm":
                tn.write(b'cat /etc/Wireless/wifi1/qca_ath1.dat | grep -E "hwmode|channel|htmode"' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 判断
            if cpumodel == "MTK":
                if "WirelessMode=15" in result:  # mtk 11vht AC/AN
                    print('5G模式配置正常')
                else:
                    raise Exception('5G模式配置异常')
                if "Channel=36" in result:
                    print('5G信道配置正常')
                else:
                    raise Exception('5G信道配置异常')
                if "HT_BW=1" and "HT_BSSCoexistence=0" in result:  # 40M
                    print('5G频宽配置正常')
                else:
                    raise Exception('5G频宽配置异常')
            elif cpumodel == "Qualcomm":
                if "hwmode=11ac" in result:  # mtk 11vht AC/AN
                    print('5G模式配置正常')
                else:
                    raise Exception('5G模式配置异常')
                if "channel=36" in result:
                    print('5G信道配置正常')
                else:
                    raise Exception('5G信道配置异常')
                if "htmode=HT40" in result:  # 40M
                    print('5G频宽配置正常')
                else:
                    raise Exception('5G频宽配置异常')
            tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_ConfigGuide passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()



