#! -*-conding:utf-8 -*-
#@Time: 2019/1/28 0028 11:08
#@swzhou
'''
网络名称
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from pages.AC_001_NetNamePage import netNamePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
from test_case.sysConfig_009_Reboot import Reboot
from test_case.AC_002_APmanagement import APmanagement
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'AC_003_netName').getlog()

class netName(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_ssidNum(self):
        u'''网络名称添加'''
        vlanPortP = getParameter('vlanPortP')
        Support = getExcelValue(vlanPortP)
        if Support == '√': #支持vlan接口
            logger.info(u'参数表支持vlan接口')
            lanpage = NetworkConfig_LANpage(self.driver,self.url)
            # 进入网络配置-外网配置 配置vlan接口
            lanpage.click_NetworkConfig()
            time.sleep(0.5)
            lanpage.click_LANconfig()
            time.sleep(1)
            #vlan 1000
            lanpage.click_add()
            time.sleep(1)
            lanpage.input_lanIpName('1000')
            lanpage.input_lanIp('192.168.10.1')
            lanpage.input_lanNetmask('255.255.255.0')
            selsxjk = lanpage.selelement_byName(lanpage.selsxjk)
            Select(selsxjk).select_by_value('vlanid')
            time.sleep(1)
            lanpage.input_dhcpVid('1000')
            lanpage.click_save()
            time.sleep(1)
            # vlan 1999
            lanpage.click_add()
            time.sleep(1)
            lanpage.input_lanIpName('1999')
            lanpage.input_lanIp('192.168.100.1')
            lanpage.input_lanNetmask('255.255.255.0')
            selsxjk = lanpage.selelement_byName(lanpage.selsxjk)
            Select(selsxjk).select_by_value('vlanid')
            time.sleep(1)
            lanpage.input_dhcpVid('1999')
            lanpage.click_save()
            time.sleep(1)
            #断言
            list_name2 = (lanpage.getText_byXpath(lanpage.list_name2))
            list_name3 = (lanpage.getText_byXpath(lanpage.list_name3))
            list_ip2 = (lanpage.getText_byXpath(lanpage.list_ip2))
            list_ip3 = (lanpage.getText_byXpath(lanpage.list_ip3))
            list_vlanid2 = (lanpage.getText_byXpath(lanpage.list_vlanid2))
            list_vlanid3 = (lanpage.getText_byXpath(lanpage.list_vlanid3))
            self.assertEqual(list_name2, '1000', msg='vlan1000名称与设置的不一致')
            self.assertEqual(list_name3, '1999', msg='vlan1999名称与设置的不一致')
            self.assertEqual(list_ip2, '192.168.10.1', msg='vlan1000IP与设置的不一致')
            self.assertEqual(list_ip3, '192.168.100.1', msg='vlan1000IP与设置的不一致')
            self.assertEqual(list_vlanid2, '1000', msg='vlan1000 ID与设置的不一致')
            self.assertEqual(list_vlanid3, '1999', msg='vlan1000 ID与设置的不一致')
            #配置dhcp
            dhcpserver = DHCPserverpage(self.driver,self.url)
            #1000
            dhcpserver.click_DHCPserver()
            time.sleep(1)
            dhcpserver.click_addpool()
            time.sleep(1)
            dhcpserver.input_poolName('1000')
            selpoolVid = dhcpserver.selelement_byName(dhcpserver.poolVid)
            Select(selpoolVid).select_by_value('VIF1000')
            time.sleep(1)
            dhcpserver.click_save()
            time.sleep(2)
            # 1999
            dhcpserver.click_addpool()
            time.sleep(1)
            dhcpserver.input_poolName('1999')
            selpoolVid = dhcpserver.selelement_byName(dhcpserver.poolVid)
            Select(selpoolVid).select_by_value('VIF1999')
            time.sleep(1)
            dhcpserver.click_save()
            time.sleep(1)
            # 断言
            list_name2 = dhcpserver.getText_byXpath(dhcpserver.list_name2)
            list_name3 = dhcpserver.getText_byXpath(dhcpserver.list_name3)
            list_int2 = dhcpserver.getText_byXpath(dhcpserver.list_int2)
            list_int3 = dhcpserver.getText_byXpath(dhcpserver.list_int3)
            self.assertEqual(list_name2, '1000', msg='pool1000名称与设置的不一致')
            self.assertEqual(list_name3, '1999', msg='pool1999名称与设置的不一致')
            self.assertEqual(list_int2, '1000', msg='pool1000IP与设置的不一致')
            self.assertEqual(list_int3, '1999', msg='pool1000IP与设置的不一致')

        # 配置网络名称
        netname = netNamePage(self.driver,self.url)
        netname.click_wirelessExtension()
        time.sleep(0.5)
        netname.click_netName()
        time.sleep(1)
        checkOpen = str(netname.getAttribute_byId(netname.checkOpens,'checktype'))
        if checkOpen == '0' : # 0为关闭，1打开
            time.sleep(1)
            netname.click_ok() # 点确认开启
            time.sleep(1)
        checkOpen = str(netname.getAttribute_byId(netname.checkOpens, 'checktype'))
        self.assertEqual(checkOpen, '1', msg='无线扩展默认未关闭')  # 0关闭，1打开

        # 编辑默认ssid
        netname.click_list_edit1()
        time.sleep(1)
        netname.input_ssid('ssid_1中')
        netname.click_next_tab()
        time.sleep(1)
        selencryType= netname.selelement_byName(netname.encryType)
        Select(selencryType).select_by_value('3')  # 0不加密 3 WPA-PSK/WPA2-PSK
        time.sleep(1)
        netname.input_pskPsswd('12345678')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.input_txBand('1000')
        netname.input_rxBand('1000')
        netname.click_save()
        time.sleep(1)
        # 断言 开关打开
        list_ssid1 = str(netname.getText_byXpath(netname.list_ssid1))
        self.assertEqual(list_ssid1, 'ssid_1中', msg='ssid1 与设置不一致')

        # 新增2Gssid
        netname.click_add()
        time.sleep(1)
        netname.input_zoneName('2G')
        netname.input_ssid('2.4Gz中')
        netname.click_cli_5g()#默认全选，点5G=勾掉，剩下2.4G
        if Support == '√':  # 支持vlan接口
            selvlanId = netname.selelement_byName(netname.vlanId)# 选vlan接口
            Select(selvlanId).select_by_value('1000')
        time.sleep(1)
        netname.click_gjxx() #点开高级选项
        time.sleep(0.5)
        netname.click_broadcastEn() #隐藏ssid
        netname.click_isolateEn() #无线客户端隔离
        time.sleep(0.5)
        netname.click_next_tab()
        time.sleep(1)
        selencryType = netname.selelement_byName(netname.encryType)
        Select(selencryType).select_by_value('3')  # 0不加密 3 WPA-PSK/WPA2-PSK
        time.sleep(1)
        netname.input_pskPsswd('12345678')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.input_txBand('1000')
        netname.input_rxBand('1000')
        netname.click_save()
        time.sleep(1)
        # 断言 开关打开
        list_ssid2 = str(netname.getText_byXpath(netname.list_ssid2))
        self.assertEqual(list_ssid2, '2.4Gz中', msg='ssid2 与设置不一致')

        # 新增5Gssid
        netname.click_add()
        time.sleep(1)
        netname.input_zoneName('5G')
        netname.input_ssid('5Gz中')
        netname.click_cli_2g()  # 默认全选，点2G=勾掉，剩下5G
        if Support == '√':  # 支持vlan接口
            selvlanId = netname.selelement_byName(netname.vlanId)  # 选vlan接口
            Select(selvlanId).select_by_value('1999')
        time.sleep(1)
        netname.click_gjxx()  # 点开高级选项
        time.sleep(0.5)
        netname.click_broadcastEn()  # 隐藏ssid
        netname.click_isolateEn()  # 无线客户端隔离
        time.sleep(0.5)
        netname.click_next_tab()
        time.sleep(1)
        selencryType = netname.selelement_byName(netname.encryType)
        Select(selencryType).select_by_value('3')  # 0不加密 3 WPA-PSK/WPA2-PSK
        time.sleep(1)
        netname.input_pskPsswd('12345678')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_sharelimit()#共享
        netname.input_txBand('1000')
        netname.input_rxBand('1000')
        netname.click_save()
        time.sleep(1)
        # 断言 开关打开
        list_ssid3 = str(netname.getText_byXpath(netname.list_ssid3))
        self.assertEqual(list_ssid3, '5Gz中', msg='ssid3 与设置不一致')

        # 新增默认接口ssid
        netname.click_add()
        time.sleep(1)
        netname.input_zoneName('all')
        netname.input_ssid('ssid_all中')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_save()
        time.sleep(1)
        # 断言
        list_ssid4 = str(netname.getText_byXpath(netname.list_ssid4))
        self.assertEqual(list_ssid4, 'ssid_all中', msg='ssid4 与设置不一致')

        self.driver.quit()

        logger.info('test_001_ssidNum passed')

    def test_002_editDelSSID(self):
        u'''网络名称修改、删除'''
        netname = netNamePage(self.driver, self.url)
        # 修改网络名称
        netname.click_wirelessExtension()
        time.sleep(0.5)
        netname.click_netName()
        time.sleep(1)
        #编辑第4个ssid
        netname.click_list_edit4()
        time.sleep(1)
        netname.input_ssid('ssid_all中2')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_save()
        time.sleep(1)
        list_ssid4 = str(netname.getText_byXpath(netname.list_ssid4))
        self.assertEqual(list_ssid4, 'ssid_all中2', msg='ssid4 与修改不一致')

        #删除
        netname.click_list_del4()
        time.sleep(1)
        netname.click_ok()
        time.sleep(1)
        list_nodata4 = str(netname.getText_byXpath(netname.list_nodata4))
        if list_nodata4 == '' or ' ':
            print('ssid 删除成功')
        else:
            CapPic(self.driver)
            logger.info(u'ssid 删除失败')
            raise Exception('删除失败')

        # 再新增第四个ssid
        netname.click_add()
        time.sleep(1)
        netname.input_zoneName('all')
        netname.input_ssid('ssid_all中')
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_next_tab()
        time.sleep(0.5)
        netname.click_save()
        time.sleep(1)
        list_ssid4 = str(netname.getText_byXpath(netname.list_ssid4))
        self.assertEqual(list_ssid4, 'ssid_all中', msg='ssid4 与设置不一致')

        self.driver.quit()
        logger.info('test_002_editDelSSID passed')

    def test_003_AutoSend(self):
        u'''网络名称 默认自动下发'''
        netname = netNamePage(self.driver, self.url)
        netname.click_wirelessExtension()
        time.sleep(0.5)
        netname.click_netName()
        time.sleep(1)
        list_autosend1 = str(netname.getAttribute_byXpath(netname.list_autosend1,'checked'))
        self.assertEqual(list_autosend1,'true',msg='默认自动下发 未开启')
        self.driver.quit()
        logger.info('test_003_AutoSend passed')

    def test_004_hairDown(self):
        u'''自动下发功能（重启后也能生效）'''
        OnlineA = getAssertText('OnlineA')

        netname = netNamePage(self.driver, self.url)
        netname.click_wirelessExtension()
        time.sleep(0.5)
        netname.click_netName()
        time.sleep(1)
        #取消掉第1个ssid的自动下发功能
        list_autosend1 = str(netname.getAttribute_byXpath(netname.list_autosend1, 'checked'))
        if list_autosend1 == 'true': #如果ssid1 自动下发打开（性能参数和002中已经核对默认自动下发是否已打开）
            netname.click_list_autosend1c()
            time.sleep(1)
            list_autosend1 = str(netname.getAttribute_byXpath(netname.list_autosend1, 'checked'))
            self.assertEqual(list_autosend1, 'None', msg='ssid1自动下发 未取消')
        #勾选第四个ssid的自动下发
        list_sutosend4 = str(netname.getAttribute_byXpath(netname.list_sutosend4, 'checked'))
        if list_sutosend4 == 'None':
            netname.click_list_sutosend4c()
            time.sleep(1)
            list_sutosend4 = str(netname.getAttribute_byXpath(netname.list_sutosend4, 'checked'))
            self.assertEqual(list_sutosend4, 'true', msg='ssid4自动下发 未开启')
        self.driver.quit()

        #1、先重启路由器
        Reboot.test_reboot1(self)
        time.sleep(40) #刚重启好 操作AP恢复出厂 可能会引起配置未删除的问题，这里等待一下
        print('重启后 稍等一下 。。。')
        #2、确认AP均上线
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(45)
        # 先确认AP均上线
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
                print('channel1=', channel1, 'channel2=', channel2, 'channel3=', channel3, 'channel4=', channel4, x)
                if channel1 != '' and channel2 != '' and channel3 != '' and channel4 != '':
                    print('4台AP2.4G无线接口已同步', x)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            x = x + 1
        else:
            CapPic(self.driver)
            logger.info(u'AP  未能同步2.4G无线接口')
            raise Exception('AP  未能同步2.4G无线接口')

        # 3、设备管理恢复AP验证自动下发功能
        APmanagement.test_006_resertAP(self)

        logger.info('test_004_hairDown passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
