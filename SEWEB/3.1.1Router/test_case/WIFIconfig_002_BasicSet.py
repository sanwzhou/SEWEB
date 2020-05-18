#! -*-conding:utf-8 -*-
#@Time: 2019/4/11 0011 10:21
#@swzhou
'''
无线加密、限速、无线vlan
'''

import time
import unittest
import telnetlib
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb
from common.GetRouteCPU import getCPUmodel
from common.loginRoute import login
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
from pages.wifiConfig_001_BasicConfigPage import BasicConfigPage
logger = LogGen(Logger = 'WIFIconfig_002_BasicSet').getlog()
host = gettelnet('host')
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")
cpumodel = getCPUmodel()


class BasicSet(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_wifi2(self):
        u'''2.4G无线加密、限速、无线vlan'''

        #lan
        lanpage = NetworkConfig_LANpage(self.driver,self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_add()
        lanpage.input_lanIpName('wifi1')
        lanpage.input_lanIp('213.1.10.1')
        selsxjk = lanpage.selelement_byName(lanpage.selsxjk)
        Select(selsxjk).select_by_value('wifi')
        lanpage.click_wifiInter1()
        lanpage.click_save()
        time.sleep(2)
        list_name2 = (lanpage.getText_byXpath(lanpage.list_name2))
        list_ip2 = (lanpage.getText_byXpath(lanpage.list_ip2))
        self.assertEqual(list_name2, 'wifi1', msg='wifi1名称与设置的不一致')
        self.assertEqual(list_ip2, '213.1.10.1', msg='wifi1 IP与设置的不一致')
        # dhcp
        dhcpserver = DHCPserverpage(self.driver, self.url)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        dhcpserver.click_addpool()
        time.sleep(1)
        dhcpserver.input_poolName('wifi1')
        selpoolVid = dhcpserver.selelement_byName(dhcpserver.poolVid)
        Select(selpoolVid).select_by_value('wifi1')
        time.sleep(1)
        dhcpserver.click_save()
        time.sleep(2)
        list_name2 = dhcpserver.getText_byXpath(dhcpserver.list_name2)
        list_int2 = dhcpserver.getText_byXpath(dhcpserver.list_int2)
        self.assertEqual(list_name2, 'wifi1', msg='wifi1名称与设置的不一致')
        self.assertEqual(list_int2, 'wifi1', msg='wifi1 IP与设置的不一致')

        wifi = BasicConfigPage(self.driver, self.url)
        wifi.click_wifiConfig()
        time.sleep(0.5)
        wifi.click_BasicConfig()
        time.sleep(1)
        wifi.click_list_edit1()
        time.sleep(1)
        wifi.input_ssid1('test3_2.41')
        ifName = wifi.selelement_byName(wifi.ifName)
        Select(ifName).select_by_value('wifi1')
        wifi.click_securitySet()
        time.sleep(1)
        secMode1 = wifi.selelement_byName(wifi.secMode1)
        Select(secMode1).select_by_value('WPAPSK')
        time.sleep(0.5)
        wifi.input_pskPsswd1('123456789')
        wifi.click_Bandwidthset()
        time.sleep(1)
        wifi.input_txBand1('1000')
        wifi.input_rxBand1('1000')
        wifi.click_save()
        time.sleep(1)
        lsit_ssid1 = wifi.getText_byXpath(wifi.list_ssid1)
        self.assertEqual(lsit_ssid1, 'test3_2.41', msg='2.4G SSID保存异常')
        list_wifiInter1 = wifi.getText_byXpath(wifi.list_wifiInter1)
        self.assertEqual(list_wifiInter1, 'wifi1', msg='2.4G wifi接口保存异常')
        list_speed1 = wifi.getText_byXpath(wifi.list_speed1)
        self.assertEqual(list_speed1, '1000/1000', msg='2.4G SSID保存异常')
        list_wifipwd1 = wifi.getAttribute_byXpath(wifi.list_wifipwd1, 'data-local')
        self.assertEqual(list_wifipwd1, '123456789', msg='2.4G密码保存异常')
        time.sleep(13)
        tn = telnetlib.Telnet(host=host, port=port) #telnet验证
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
            if "SSID1=test3_2.41" in result:
                print('2.4G SSID配置正常')
            else:
                raise Exception('2.4G SSID配置异常')
            if "WPAPSK1=123456789" in result:
                print('2.4G 密码配置正常')
            else:
                raise Exception('2.4G 密码配置异常')
        elif cpumodel == "Qualcomm":
            if "ssid=test3_2.41" in result:
                print('2.4G SSID配置正常')
            else:
                raise Exception('2.4G SSID配置异常')
            if "key=123456789" in result:
                print('2.4G 密码配置正常')
            else:
                raise Exception('2.4G 密码配置异常')
        tn.close()  # tn.write('exit\n')

        logger.info('test_001_wifi2 passed')

    def test_002_wifi5(self):
        u'''5G无线加密、限速、无线vlan'''

        #lan
        lanpage = NetworkConfig_LANpage(self.driver,self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_add()
        lanpage.input_lanIpName('wifi2')
        lanpage.input_lanIp('213.1.20.1')
        selsxjk = lanpage.selelement_byName(lanpage.selsxjk)
        Select(selsxjk).select_by_value('wifi')
        lanpage.click_wifiInter2()
        lanpage.click_save()
        time.sleep(2)
        list_name2 = (lanpage.getText_byXpath(lanpage.list_name2))
        list_ip2 = (lanpage.getText_byXpath(lanpage.list_ip2))
        self.assertEqual(list_name2, 'wifi2', msg='wifi2名称与设置的不一致')
        self.assertEqual(list_ip2, '213.1.20.1', msg='wifi3 IP与设置的不一致')
        # dhcp
        dhcpserver = DHCPserverpage(self.driver, self.url)
        dhcpserver.click_DHCPserver()
        time.sleep(2)
        dhcpserver.click_addpool()
        time.sleep(1)
        dhcpserver.input_poolName('wifi2')
        selpoolVid = dhcpserver.selelement_byName(dhcpserver.poolVid)
        Select(selpoolVid).select_by_value('wifi2')
        time.sleep(1)
        dhcpserver.click_save()
        time.sleep(2)
        list_name2 = dhcpserver.getText_byXpath(dhcpserver.list_name2)
        list_int2 = dhcpserver.getText_byXpath(dhcpserver.list_int2)
        self.assertEqual(list_name2, 'wifi2', msg='wifi2名称与设置的不一致')
        self.assertEqual(list_int2, 'wifi2', msg='wifi2 IP与设置的不一致')

        wifi = BasicConfigPage(self.driver, self.url)
        wifi.click_wifiConfig()
        time.sleep(0.5)
        wifi.click_BasicConfig()
        time.sleep(1)
        wifi.click_list_edit2()
        time.sleep(1)
        wifi.input_ssid1('test3_51')
        ifName = wifi.selelement_byName(wifi.ifName)
        Select(ifName).select_by_value('wifi2')
        wifi.click_securitySet()
        time.sleep(1)
        secMode1 = wifi.selelement_byName(wifi.secMode1)
        Select(secMode1).select_by_value('WPAPSK')
        time.sleep(0.5)
        wifi.input_pskPsswd1('123456789')
        wifi.click_Bandwidthset()
        time.sleep(1)
        wifi.click_share_sel1() #共享
        wifi.input_txBand1('1000')
        wifi.input_rxBand1('1000')
        wifi.click_save()
        time.sleep(1)
        lsit_ssid2 = wifi.getText_byXpath(wifi.list_ssid2)
        self.assertEqual(lsit_ssid2, 'test3_51', msg='5G SSID保存异常')
        list_wifiInter2 = wifi.getText_byXpath(wifi.list_wifiInter2)
        self.assertEqual(list_wifiInter2, 'wifi2', msg='5G wifi接口保存异常')
        list_speed2 = wifi.getText_byXpath(wifi.list_speed2)
        self.assertEqual(list_speed2, '1000/1000', msg='5G SSID保存异常')
        list_wifipwd2 = wifi.getAttribute_byXpath(wifi.list_wifipwd2, 'data-local')
        self.assertEqual(list_wifipwd2, '123456789', msg='5G密码保存异常')
        time.sleep(13)
        tn = telnetlib.Telnet(host=host, port=port) #telnet验证
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        if cpumodel == "MTK":
            tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat | grep -E "SSID1|WPAPSK1"' + b'\n')
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
            if "SSID1=test3_51" in result:
                print('5G SSID配置正常')
            else:
                raise Exception('5G SSID配置异常')
            if "WPAPSK1=123456789" in result:
                print('5G 密码配置正常')
            else:
                raise Exception('5G 密码配置异常')
        elif cpumodel == "Qualcomm":
            if "ssid=test3_51" in result:
                print('5G SSID配置正常')
            else:
                raise Exception('5G SSID配置异常')
            if "key=123456789" in result:
                print('5G 密码配置正常')
            else:
                raise Exception('5G 密码配置异常')
        tn.close()  # tn.write('exit\n')

        logger.info('test_002_wifi5 passed')

    def tearDown(self):
        #删除
        dhcpserver = DHCPserverpage(self.driver, self.url)
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        dhcpserver.click_list_delpool2()
        time.sleep(1)
        dhcpserver.click_ok()
        time.sleep(1)
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_allsel()
        time.sleep(1)
        lanpage.click_delete()
        time.sleep(1)
        lanpage.click_ok()
        time.sleep(1)
        self.driver.quit()
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()


