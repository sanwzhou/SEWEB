#! -*-conding:utf-8 -*-
#@Time: 2019/4/11 0011 12:01
#@swzhou
'''
修改无线信道、模式、带宽
'''
import time
import unittest
import telnetlib
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.GetRouteCPU import getCPUmodel
from common.ReadConfig import gettelnet,getweb
from common.loginRoute import login
from pages.wifiConfig_002_RFConfigPage import RFConfigPage
logger = LogGen(Logger = 'WIFIconfig_003_RFConfig').getlog()
host = gettelnet('host')
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")
cpumodel = getCPUmodel()

class RFConfig(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_RFConfig2(self):
        u'''修改2.4G修改无线信道、模式、带宽'''
        rfConfig = RFConfigPage(self.driver, self.url)
        rfConfig.click_wifiConfig()
        time.sleep(0.5)
        rfConfig.click_RFConfig()
        time.sleep(1)
        channel_2 = rfConfig.selelement_byName(rfConfig.channel2)
        Select(channel_2).select_by_value('5')
        mode_2 = rfConfig.selelement_byName(rfConfig.wrlessMode2)
        chanWidth_2 = rfConfig.selelement_byName(rfConfig.chanWidth2)
        if cpumodel == 'MTK':
            Select(mode_2).select_by_value('4')  # 仅11g
            Select(chanWidth_2).select_by_value('0')  # 20M
        elif cpumodel == 'Qualcomm':
            Select(mode_2).select_by_value('2')  # 仅11g
            Select(chanWidth_2).select_by_value('1')  # 20M
        rfConfig.click_save()
        time.sleep(8)
        tn = telnetlib.Telnet(host=host, port=port)  # telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(
            b'cat /etc/Wireless/RT2860/RT2860.dat | grep -E "WirelessMode|Channel|HT_BW|HT_BSSCoexistence"' + b'\n')
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
            if "WirelessMode=4" in result:  # 11g
                print('2.4G模式配置正常')
            else:
                raise Exception('2.4G模式配置异常')
            if "Channel=5" in result:
                print('2.4G信道配置正常')
            else:
                raise Exception('2.4G信道配置异常')
            if "HT_BW=0" and "HT_BSSCoexistence=0" in result:  # 20M
                print('2.4G频宽配置正常')
            else:
                raise Exception('2.4G信道配置异常')
        elif cpumodel == "Qualcomm":
            if "hwmode=11g" in result:  # 11g
                print('2.4G模式配置正常')
            else:
                raise Exception('2.4G模式配置异常')
            if "channel=5" in result:
                print('2.4G信道配置正常')
            else:
                raise Exception('2.4G信道配置异常')
            if "htmode=HT20" in result:  # 20M
                print('2.4G频宽配置正常')
            else:
                raise Exception('2.4G频宽配置异常')
        tn.close()  # tn.write('exit\n')
        channel_2 = rfConfig.selelement_byName(rfConfig.channel2) #信道自动
        Select(channel_2).select_by_value('0') #mtk、高通默认自动均为0
        rfConfig.click_save()
        time.sleep(15)
        tn = telnetlib.Telnet(host=host, port=port)  # telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(
                b'cat /etc/Wireless/RT2860/RT2860.dat | grep Channel' + b'\n')
        elif cpumodel == "Qualcomm":
            tn.write(b'cat /etc/Wireless/wifi0/qca_ath0.dat | grep channel' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if cpumodel == "MTK":
            if ("Channel=0" in result) and ("AutoChannelSelect=0" not in result) :
                print('2.4G信道自动配置正常')
            else:
                raise Exception('2.4G信道自动配置异常')
        if cpumodel == "Qualcomm":
            if "channel=auto" in result:
                print('2.4G信道自动配置正常')
            else:
                raise Exception('2.4G信道自动配置异常')
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_001_RFConfig2 passed')

    def test_002_RFConfig5(self):
        u'''修改5G修改无线信道、模式、带宽'''

        rfConfig = RFConfigPage(self.driver, self.url)
        rfConfig.click_wifiConfig()
        time.sleep(0.5)
        rfConfig.click_RFConfig()
        time.sleep(1)
        channel_5 = rfConfig.selelement_byName(rfConfig.channel5)
        Select(channel_5).select_by_value('40')
        mode_5 = rfConfig.selelement_byName(rfConfig.wrlessMode5)
        chanWidth_5 = rfConfig.selelement_byName(rfConfig.chanWidth5)
        if cpumodel == 'MTK':
            Select(mode_5).select_by_value('14') #11vht AC/AN/A
            Select(chanWidth_5).select_by_value('0')  # 20M
        elif cpumodel == 'Qualcomm':
            Select(mode_5).select_by_value('4')  # 11a/n混合
            Select(chanWidth_5).select_by_value('1')  # 20M
        rfConfig.click_save()
        time.sleep(15)
        tn = telnetlib.Telnet(host=host, port=port)  # telnet验证
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
            if "WirelessMode=14" in result:  #11vht AC/AN/A
                print('5G模式配置正常')
            else:
                raise Exception('5G模式配置异常')
            if "Channel=40" in result:
                print('5G信道配置正常')
            else:
                raise Exception('5G信道配置异常')
            if "HT_BW=0" and "HT_BSSCoexistence=0" in result:  # 20M
                print('5G频宽配置正常')
            else:
                raise Exception('5G信道配置异常')
        elif cpumodel == "Qualcomm":
            if "hwmode=11na" in result:  # 11a/n混合
                print('5G模式配置正常')
            else:
                raise Exception('5G模式配置异常')
            if "channel=40" in result:
                print('5G信道配置正常')
            else:
                raise Exception('5G信道配置异常')
            if "htmode=HT20" in result:  # 40M
                print('5G频宽配置正常')
            else:
                raise Exception('5G频宽配置异常')
        tn.close()  # tn.write('exit\n')
        channel_5 = rfConfig.selelement_byName(rfConfig.channel5)
        Select(channel_5).select_by_value('0')  # 信道自动
        rfConfig.click_save()
        time.sleep(10)
        tn = telnetlib.Telnet(host=host, port=port)  # telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat | grep Channel' + b'\n')
        elif cpumodel == "Qualcomm":
            tn.write(b'cat /etc/Wireless/wifi1/qca_ath1.dat | grep channel' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if cpumodel == "MTK":
            if ("Channel=0" in result) and ("AutoChannelSelect=0" not in result):
                print('5G信道自动配置正常')
            else:
                raise Exception('5G信道自动配置异常')
        if cpumodel == "Qualcomm":
            if "channel=auto" in result:
                print('5G信道自动配置正常')
            else:
                raise Exception('5G信道自动配置异常')
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_002_RFConfig5 passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()




