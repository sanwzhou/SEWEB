#! -*-conding:utf-8 -*-
#@Time: 2019/2/25 0025 17:54
#@swzhou
'''
无线扩展
'''

import time
import unittest
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb,getParameter
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
from pages.AC_001_NetNamePage import netNamePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from pages.AC_003_RftemplatePage import RftemplatePage
from pages.AC_005_APSoftwarePage import APSoftwarePage
logger = LogGen(Logger = 'Parameter_025_AC').getlog()
APnumP = getParameter('APnumP')
Support = getExcelValue(APnumP)

class AC(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')

        # pass

    def test_001_APconfig(self):
        u'''AP配置管理'''
        wirelessTipsA =getAssertText('wirelessTipsA')
        OnlineA = getAssertText('OnlineA')
        Support5GAP = getweb('Support5GAP') #环境中支持5G的AP
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # 先进入网络名称 判断无线扩展是否打开
        netname = netNamePage(self.driver, self.url)
        # print(Support)
        if str(Support).isdigit(): #判断字符串是否为数字
            logger.info(u'参数支持AP管理')
            try:
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持无线扩展/网络名称，与参数表不符')
                raise Exception(u'软件不支持无线扩展/网络名称，与参数表不符')
            else:
                logger.info(u'软件支持无线扩展，与参数表相符')
                self.driver.implicitly_wait(10)
                checkOpen = str(netname.getAttribute_byId(netname.checkOpens, 'checktype'))
                ManageProtocols = str(netname.getAttribute_byId(netname.ManageProtocolss, 'checktype'))

                if checkOpen == '0':  # 0为关闭，1打开
                    tips = netname.getText_byClass(netname.u_cfm_boxT)
                    time.sleep(1)
                    self.assertIn(wirelessTipsA, tips, msg='提示信息有误')
                    netname.click_ok()  # 点确认开启
                    time.sleep(30) #等AP上线 时间久一点
                else:
                    time.sleep(5)  # 002中打开 等待时间稍短一些
                if ManageProtocols == '0':  # 0为关闭，1打开
                    netname.click_ManageProtocols() # 开启
                    time.sleep(10) #等v1AP上线
                # 断言 开关打开
                checkOpen = str(netname.getAttribute_byId(netname.checkOpens, 'checktype'))
                self.assertEqual(checkOpen, '1', msg='无线扩展默认未打开')  # 0关闭，1打开
                ManageProtocols = str(netname.getAttribute_byId(netname.ManageProtocolss, 'checktype'))
                self.assertEqual(ManageProtocols, '1', msg='兼容模式未打开')
                #进入设备管理
                device = deviceMgmtPage(self.driver, self.url)
                device.click_deviceMgmt()
                time.sleep(1)
                #判断AP已正常上线
                x = 0
                while x < 120:
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
                    raise Exception('AP  未能同步2.4G无线接口')

                #需选择一个同时支持2.4G 5G的AP 并搜索
                device.input_search(Support5GAP)
                device.click_searchB()
                time.sleep(1)
                device.click_list_name1()
                time.sleep(0.5)
                device.input_list_namein1('1')
                time.sleep(0.5)
                device.find_list_nameS1()
                #2.4G 信道
                device.click_list_channel1c()
                time.sleep(0.5)
                select_2 = device.selelement_byXpath(device.selchannel2_1)
                Select(select_2).select_by_value('1')
                time.sleep(0.2)
                Select(select_2).select_by_value('2')
                time.sleep(0.2)
                Select(select_2).select_by_value('3')
                time.sleep(0.2)
                Select(select_2).select_by_value('4')
                time.sleep(0.2)
                Select(select_2).select_by_value('5')
                time.sleep(0.2)
                Select(select_2).select_by_value('6')
                time.sleep(0.2)
                Select(select_2).select_by_value('7')
                time.sleep(0.2)
                Select(select_2).select_by_value('8')
                time.sleep(0.2)
                Select(select_2).select_by_value('9')
                time.sleep(0.2)
                Select(select_2).select_by_value('10')
                time.sleep(0.2)
                Select(select_2).select_by_value('11')
                time.sleep(0.2)
                Select(select_2).select_by_value('auto')
                time.sleep(0.2)
                device.find_selchannel2S_1()
                #5G
                device.click_list_channel51c()
                time.sleep(0.5)
                select_5 = device.selelement_byXpath(device.selchannel5_1)
                Select(select_5).select_by_value('36')
                time.sleep(0.2)
                Select(select_5).select_by_value('40')
                time.sleep(0.2)
                Select(select_5).select_by_value('44')
                time.sleep(0.2)
                Select(select_5).select_by_value('48')
                time.sleep(0.2)
                Select(select_5).select_by_value('149')
                time.sleep(0.2)
                Select(select_5).select_by_value('153')
                time.sleep(0.2)
                Select(select_5).select_by_value('157')
                time.sleep(0.2)
                Select(select_5).select_by_value('161')
                time.sleep(0.2)
                Select(select_5).select_by_value('165')
                time.sleep(0.2)
                Select(select_5).select_by_value('auto')
                time.sleep(0.2)
                device.find_selchannel5S_1()
                #漫游阈值
                device.click_deviceMgmt()
                time.sleep(1)
                device.click_list_mangement1()
                time.sleep(2)
                device.click_modifyPw()#修改密码
                time.sleep(0.2)
                device.click_roamingSet()
                time.sleep(0.5)
                # rpaming_en_2G = str(device.getAttribute_byXpath(device.roaming_cs,'checked'))
                # self.assertEqual(rpaming_en_2G,'true',msg='2.4G漫游阈值 默认未关闭')
                device.click_roaming_en()
                time.sleep(0.5)
                device.input_roaming_th('-80')
                time.sleep(0.2)
                # rpaming_en_5G = str(device.getAttribute_byXpath(device.roaming_c5s,'checked'))
                # self.assertEqual(rpaming_en_5G, 'true', msg='5G漫游阈值 默认未关闭')
                device.click_roaming_en5()
                time.sleep(0.5)
                device.input_roaming_th5('-80')
                time.sleep(0.2)
                device.click_modal_hide()
                time.sleep(1)
                #重启
                device.find_list_reboot1()
                #批量管理
                device.click_list_sel1()
                device.click_BatchManagement()
                time.sleep(2)
                #射频模板
                spmb = device.selelement_byName(device.spmb)
                Select(spmb).select_by_value('default2')
                time.sleep(0.2)
                Select(spmb).select_by_value('default1')
                time.sleep(0.2)
                Select(spmb).select_by_value('default3')
                time.sleep(0.2)
                #网络名称
                device.click_ssidM()
                time.sleep(1)
                device.click_list_selwn1()
                device.click_selall_w()
                device.find_sendToApM()
                #系统设置
                device.click_Syssetup()
                time.sleep(1)
                device.click_TaskS_En()#计划任务
                time.sleep(0.2)
                device.click_TaskS_C()
                time.sleep(0.2)
                device.click_sleepMode_En()# 睡眠模式
                time.sleep(0.2)
                device.click_sleepMode_C()
                time.sleep(0.2)
                # 配置重启
                device.click_configreboot()
                time.sleep(0.5)
                device.find_restart()
                device.find_factory_reset()
                device.click_close()
                time.sleep(0.5)
                #备份配置
                device.click_backupconfig()
                time.sleep(1)
                device.find_allDelete()
                device.find_backup()
                device.find_uploadBackup()
                #软件升级
                apsoftware = APSoftwarePage(self.driver, self.url)
                apsoftware.click_APsoftware()
                time.sleep(1)
                apsoftware.find_checkUpdata()
                apsoftware.find_upData()
                apsoftware.find_upDataLocal()
        else:
            logger.info(u'参数不支持AP管理')
            try:
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展，与参数表不符')
                raise Exception(u'软件支持无线扩展，与参数表不符')
        self.driver.quit()
        logger.info('test_001_APconfig passed')

    def test_002_SSIDconfig(self):
        u'''网络名称设置&加密方式'''
        APnumP = getParameter('APnumP')
        Support = getExcelValue(APnumP)
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        if str(Support).isdigit(): #判断字符串是否为数字
            logger.info(u'参数支持AP管理')
            wirelessTipsA = getAssertText('wirelessTipsA')
            vlanPortP = getParameter('vlanPortP')
            Support = getExcelValue(vlanPortP)
            if Support == '√':  # 支持vlan接口
                logger.info(u'参数表支持vlan接口')
                # 进入网络配置-内网配置 配置vlan接口
                lanpage = NetworkConfig_LANpage(self.driver,self.url)
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
                list_name2 = str(lanpage.getText_byXpath(lanpage.list_name2))
                list_name3 = str(lanpage.getText_byXpath(lanpage.list_name3))
                list_ip2 = str(lanpage.getText_byXpath(lanpage.list_ip2))
                list_ip3 = str(lanpage.getText_byXpath(lanpage.list_ip3))
                list_vlanid2 = str(lanpage.getText_byXpath(lanpage.list_vlanid2))
                list_vlanid3 = str(lanpage.getText_byXpath(lanpage.list_vlanid3))
                self.assertEqual(list_name2, '1000', msg='vlan1000名称与设置的不一致')
                self.assertEqual(list_name3, '1999', msg='vlan1999名称与设置的不一致')
                self.assertEqual(list_ip2, '192.168.10.1', msg='vlan1000IP与设置的不一致')
                self.assertEqual(list_ip3, '192.168.100.1', msg='vlan1000IP与设置的不一致')
                self.assertEqual(list_vlanid2, '1000', msg='vlan1000 ID与设置的不一致')
                self.assertEqual(list_vlanid3, '1999', msg='vlan1000 ID与设置的不一致')
                #配置dhcp
                dhcppage = DHCPserverpage(self.driver,self.url)
                #1000
                dhcppage.click_DHCPserver()
                time.sleep(1)
                dhcppage.click_addpool()
                time.sleep(1)
                dhcppage.input_poolName('1000')
                seldhcppool = dhcppage.selelement_byName(dhcppage.poolVid)
                Select(seldhcppool).select_by_value('VIF1000')
                time.sleep(1)
                dhcppage.click_save()
                time.sleep(1)
                # 1999
                dhcppage.click_DHCPserver()
                time.sleep(1)
                dhcppage.click_addpool()
                time.sleep(1)
                dhcppage.input_poolName('1999')
                seldhcppool = dhcppage.selelement_byName(dhcppage.poolVid)
                Select(seldhcppool).select_by_value('VIF1999')
                time.sleep(1)
                dhcppage.click_save()
                time.sleep(1)
                # 断言
                list_name2 = str(dhcppage.getText_byXpath(dhcppage.list_name2))
                list_name3 = str(dhcppage.getText_byXpath(dhcppage.list_name3))
                list_int2 = str(dhcppage.getText_byXpath(dhcppage.list_int2))
                list_int3 = str(dhcppage.getText_byXpath(dhcppage.list_int3))
                self.assertEqual(list_name2, '1000', msg='pool1000名称与设置的不一致')
                self.assertEqual(list_name3, '1999', msg='pool1999名称与设置的不一致')
                self.assertEqual(list_int2, '1000', msg='pool1000IP与设置的不一致')
                self.assertEqual(list_int3, '1999', msg='pool1000IP与设置的不一致')

            # 配置网络名称
            netname = netNamePage(self.driver,self.url)
            try:
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                #网络名称页面的提示
                netname.click_netName()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持无线扩展/网络名称，与参数表不符')
                raise Exception(u'软件不支持无线扩展/网络名称，与参数表不符')
            else:
                self.driver.implicitly_wait(10)
                time.sleep(1)
                checkOpen = str(netname.getAttribute_byId(netname.checkOpens, 'checktype'))
                if checkOpen  == '0' : # 0为关闭，1打开
                    tips = netname.getText_byClass(netname.u_cfm_boxT)
                    time.sleep(1)
                    self.assertIn(wirelessTipsA,tips, msg='提示信息有误')
                    netname.click_ok() # 点确认开启
                    time.sleep(3)
                else:
                    raise Exception('无线扩展默认未关闭')
                # 断言 开关打开
                checkOpen = str(netname.getAttribute_byId(netname.checkOpens, 'checktype'))
                self.assertEqual(checkOpen, '1', msg='无线扩展默认未关闭')  # 0关闭，1打开
                # 确认兼容模式按钮默认关闭
                ManageProtocols = str(netname.getAttribute_byId(netname.ManageProtocolss, 'checktype'))
                self.assertEqual(ManageProtocols, '0', msg='兼容模式默认未关闭')  # 0关闭，1打开
                # 打开兼容模式
                netname.click_ManageProtocols()
                time.sleep(5)
                ManageProtocols = str(netname.getAttribute_byId(netname.ManageProtocolss, 'checktype'))
                self.assertEqual(ManageProtocols, '1', msg='兼容模式未打开')  # 0关闭，1打开

                #判断自动下发是否开启
                Auto = str(netname.getAttribute_byXpath(netname.list_autosend1,'checked'))
                self.assertEqual(str(Auto),'true',msg='默认自动下发未开启')
                # 编辑默认ssid
                netname.click_list_edit1()
                time.sleep(1)
                netname.input_ssid('ssid_1中')
                netname.click_next_tab()
                time.sleep(1)
                selencryType = netname.selelement_byName(netname.encryType)
                Select(selencryType).select_by_value('1')  # 0不加密 3 WPA-PSK/WPA2-PSK
                time.sleep(0.3)
                Select(selencryType).select_by_value('0')
                time.sleep(0.3)
                Select(selencryType).select_by_value('2')
                time.sleep(0.3)
                Select(selencryType).select_by_value('3')
                time.sleep(0.5)
                netname.input_pskPsswd('12345678')
                netname.click_next_tab()
                time.sleep(0.5)
                netname.click_sharelimit()  # 共享
                netname.input_txBand('1000')
                netname.input_rxBand('1000')
                netname.click_save()
                time.sleep(1)
                list_ssid1 = str(netname.getText_byXpath(netname.list_ssid1))
                self.assertEqual(list_ssid1, 'ssid_1中', msg='ssid1 与设置不一致')

                # 新增2Gssid
                netname.click_add()
                time.sleep(1)
                netname.input_zoneName('2G')
                netname.input_ssid('2.4Gz中')
                netname.click_cli_5g()  # 默认全选，点5G=勾掉，剩下2.4G
                if Support == '√':  # 支持vlan接口
                    selvlanId = netname.selelement_byName(netname.vlanId)  # 选vlan接口
                    Select(selvlanId).select_by_value('1000')
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
                netname.input_txBand('1000')
                netname.input_rxBand('1000')
                netname.click_save()
                time.sleep(2)
                # 断言 开关打开
                list_ssid2 = str(netname.getText_byXpath(netname.list_ssid2))
                self.assertEqual(list_ssid2, '2.4Gz中', msg='ssid2 与设置不一致')

                # 新增5Gssid
                netname.click_add()
                time.sleep(1)
                netname.input_zoneName('5G')
                netname.input_ssid('5Gz中')
                selSSIDmode = netname.selelement_byName(netname.encodeType)
                Select(selSSIDmode).select_by_value('0')#0电脑优先 1手机优先
                time.sleep(1)
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
                netname.input_txBand('1000')
                netname.input_rxBand('1000')
                netname.click_save()
                time.sleep(1)
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

                #再新建提示保存成功（ssid数量后续版本做了调整）
                netname.click_add()
                time.sleep(1)
                netname.input_zoneName('5')
                netname.input_ssid('5')
                netname.click_next_tab()
                time.sleep(0.5)
                netname.click_next_tab()
                time.sleep(0.5)
                netname.click_save()
                time.sleep(1)
                # 断言 开关打开
                list_ssid5 = str(netname.getText_byXpath(netname.list_ssid5))
                self.assertEqual(list_ssid5, '5', msg='ssid5 与设置不一致')
                print('网络名称设置 验证通过')

                #删除ssid
                netname.click_selall()
                time.sleep(0.2)
                netname.click_sellist1()
                time.sleep(0.2)
                netname.click_delete()
                time.sleep(2)
                netname.click_ok()
                time.sleep(1)
                if Support == '√':  # 支持vlan接口
                    # 删除dhcp
                    dhcppage = DHCPserverpage(self.driver, self.url)
                    dhcppage.click_NetworkConfig()
                    time.sleep(0.5)
                    dhcppage.click_DHCPserver()
                    time.sleep(0.5)
                    dhcppage.click_DHCPserver()
                    time.sleep(1)
                    dhcppage.click_list_delpool2()
                    time.sleep(1)
                    dhcppage.click_ok()
                    time.sleep(1)
                    dhcppage.click_list_delpool2()
                    time.sleep(1)
                    dhcppage.click_ok()
                    time.sleep(1)
                    # 删除vlan接口
                    lanpage = NetworkConfig_LANpage(self.driver, self.url)
                    lanpage.click_LANconfig()
                    time.sleep(1)
                    lanpage.click_allsel()
                    time.sleep(1)
                    lanpage.click_delete()
                    time.sleep(1)
                    lanpage.click_ok()
                    time.sleep(1)
        else:
            logger.info(u'参数不支持AP管理')
            try:
                netname = netNamePage(self.driver, self.url)
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展，与参数表不符')
                raise Exception(u'软件支持无线扩展，与参数表不符')

        self.driver.quit()
        logger.info('test_002_SSIDconfig passed')

    def test_003_Template(self):
        u'''AP配置模板'''
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        rftemplate = RftemplatePage(self.driver, self.url)
        if str(Support).isdigit(): #判断字符串是否为数字
            logger.info(u'参数支持AP管理')
            try:
                self.driver.implicitly_wait(2)
                # 进入无线拓展_射频模板
                rftemplate.click_wirelessExtension()
                time.sleep(0.5)
                rftemplate.click_rfTemplate()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持无线扩展/网络名称，与参数表不符')
                raise Exception(u'软件不支持无线扩展/网络名称，与参数表不符')
            else:
                logger.info(u'软件支持无线扩展，与参数表相符')
                self.driver.implicitly_wait(10)
                rftemplate.click_list_edit1()
                time.sleep(1)
                #2.4G
                #无线功能开启/关闭
                en_wireless = str(rftemplate.getAttribute_byXpath(rftemplate.en_wirelessS,'checked'))
                self.assertEqual(en_wireless,'true',msg='模板2.4G ssid默认未开启')
                rftemplate.click_C_wireless()
                time.sleep(0.2)
                rftemplate.click_C_wireless1()
                time.sleep(0.2)
                selmode = rftemplate.selelement_byName(rftemplate.mode)
                Select(selmode).select_by_value('1') #1 仅11g
                time.sleep(0.5)
                selrate = rftemplate.selelement_byName(rftemplate.rate)
                Select(selrate).select_by_value('54') #54M
                time.sleep(0.2)
                Select(selrate).select_by_value('0')  # 自动
                time.sleep(0.2)
                Select(selmode).select_by_value('2')  # 2 仅11n
                time.sleep(0.5)
                Select(selrate).select_by_value('150')  # 150M
                time.sleep(0.2)
                Select(selrate).select_by_value('300')  # 300M
                time.sleep(0.2)
                Select(selrate).select_by_value('0')  # 自动
                time.sleep(0.2)
                Select(selmode).select_by_value('3')  # 3 b/g/n
                time.sleep(0.5)
                selpower = rftemplate.selelement_byName(rftemplate.power) #无线传输功率
                Select(selpower).select_by_value('1')  #1 手动
                time.sleep(1)
                selmanual = rftemplate.selelement_byName(rftemplate.manual)
                Select(selmanual).select_by_value('2')  # 中
                time.sleep(0.2)
                Select(selmanual).select_by_value('1')  # 低
                time.sleep(0.2)
                Select(selmanual).select_by_value('3')  # 高
                time.sleep(0.2)
                Select(selpower).select_by_value('0')  # 0 自动
                time.sleep(0.5)
                selchannel = rftemplate.selelement_byName(rftemplate.channel)
                Select(selchannel).select_by_value('1')
                time.sleep(0.2)
                Select(selchannel).select_by_value('2')
                time.sleep(0.2)
                Select(selchannel).select_by_value('3')
                time.sleep(0.2)
                Select(selchannel).select_by_value('4')
                time.sleep(0.2)
                Select(selchannel).select_by_value('5')
                time.sleep(0.2)
                Select(selchannel).select_by_value('6')
                time.sleep(0.2)
                Select(selchannel).select_by_value('7')
                time.sleep(0.2)
                Select(selchannel).select_by_value('8')
                time.sleep(0.2)
                Select(selchannel).select_by_value('9')
                time.sleep(0.2)
                Select(selchannel).select_by_value('10')
                time.sleep(0.2)
                Select(selchannel).select_by_value('11')
                time.sleep(0.2)
                Select(selchannel).select_by_value('0')  # 0 自动
                time.sleep(0.5)
                selBW = rftemplate.selelement_byName(rftemplate.BW)
                Select(selBW).select_by_value('0')  #0 20M
                time.sleep(0.2)
                Select(selBW).select_by_value('1') #自动
                time.sleep(0.2)
                rftemplate.click_gjxxa()  #高级选项
                time.sleep(0.5)
                SGI = str(rftemplate.getAttribute_byXpath(rftemplate.SGIs,'checked'))
                self.assertEqual(SGI,'true',msg='短间隔 默认未开启')
                rftemplate.click_SGIc()
                wmm = str(rftemplate.getAttribute_byXpath(rftemplate.wmms,'checked'))
                self.assertEqual(wmm, 'true', msg='wmm 默认未开启')
                rftemplate.click_wmmc()
                preamble = str(rftemplate.getAttribute_byXpath(rftemplate.preambles,'checked'))
                self.assertEqual(preamble, 'true', msg='短前导码	 默认未开启')
                rftemplate.click_preamblesc()
                rftemplate.input_BeaconPeriod('200') #信标间隔
                #5G
                # 无线功能开启/关闭
                en_wireless_5 = str(rftemplate.getAttribute_byXpath(rftemplate.en_wireless5S,'checked'))
                self.assertEqual(en_wireless_5, 'true', msg='模板2.4G ssid默认未开启')
                rftemplate.click_C_wireless5()
                time.sleep(0.2)
                rftemplate.click_C_wireless51()
                time.sleep(0.2)
                selmode_5 = rftemplate.selelement_byName(rftemplate.mode_5)  # 无线模式
                Select(selmode_5).select_by_value('4')  # 仅11a
                time.sleep(0.2)
                BW_5 = rftemplate.selelement_byName(rftemplate.BW_5)  # 频道带宽
                Select(BW_5).select_by_value('0')  # 0 20M
                time.sleep(0.2)
                Select(BW_5).select_by_value('1')  # 自动
                time.sleep(0.2)
                Select(selmode_5).select_by_value('5')  # 11a/n混合
                time.sleep(0.2)
                Select(BW_5).select_by_value('0')  # 0 20M
                time.sleep(0.2)
                Select(BW_5).select_by_value('1')  # 自动
                time.sleep(0.2)
                Select(selmode_5).select_by_value('6')  # 11vht AC/AN/A
                time.sleep(0.2)
                VHTBW = rftemplate.selelement_byName(rftemplate.VHTBW)  # 频道带宽
                Select(VHTBW).select_by_value('0')  # 0 20M/40
                time.sleep(0.2)
                Select(VHTBW).select_by_value('1')  # 80M
                time.sleep(0.2)
                Select(BW_5).select_by_value('0')  # 0 20M
                time.sleep(0.2)
                Select(BW_5).select_by_value('1')  # 自动
                time.sleep(0.2)
                Select(selmode_5).select_by_value('7')  # 11vht AC/AN
                time.sleep(0.2)
                Select(VHTBW).select_by_value('0')  # 0 20M/40
                time.sleep(0.2)
                Select(VHTBW).select_by_value('1')  # 80M
                time.sleep(0.2)
                Select(BW_5).select_by_value('0')  # 0 20M
                time.sleep(0.2)
                Select(BW_5).select_by_value('1')  # 自动
                time.sleep(0.2)
                power_5 = rftemplate.selelement_byName(rftemplate.power_5)  # 无线传输功率
                Select(power_5).select_by_value('1')  # 1 手动
                time.sleep(1)
                manual_5 = rftemplate.selelement_byName(rftemplate.manual_5)
                CapPic(self.driver)
                Select(manual_5).select_by_value('2')  # 中
                time.sleep(0.2)
                Select(manual_5).select_by_value('1')  # 低
                time.sleep(0.2)
                Select(manual_5).select_by_value('3')  # 高
                time.sleep(0.2)
                Select(power_5).select_by_value('0')  # 0 自动
                time.sleep(0.5)
                channel_5 = rftemplate.selelement_byName(rftemplate.channel_5)
                Select(channel_5).select_by_value('36')
                time.sleep(0.2)
                Select(channel_5).select_by_value('40')
                time.sleep(0.2)
                Select(channel_5).select_by_value('44')
                time.sleep(0.2)
                Select(channel_5).select_by_value('48')
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
                Select(channel_5).select_by_value('0') # 0 自动
                time.sleep(0.2)
                #高级选项
                SGI_5 = str(rftemplate.getAttribute_byXpath(rftemplate.SGI5s,'checked'))
                self.assertEqual(SGI_5, 'true', msg='5G短间隔 默认未开启')
                rftemplate.click_SGI5c()
                wmm_5 = str(rftemplate.getAttribute_byXpath(rftemplate.wmm5s,'checked'))
                self.assertEqual(wmm_5, 'true', msg='5G wmm 默认未开启')
                rftemplate.click_wmm5c()
                preamble_5 = str(rftemplate.getAttribute_byXpath(rftemplate.preamble5s,'checked'))
                self.assertEqual(preamble_5, 'true', msg='5G 短前导码 默认未开启')
                rftemplate.click_preambles5c()
                rftemplate.input_BeaconPeriod5('200')  # 信标间隔
                time.sleep(0.2)
        else:
            logger.info(u'参数不支持AP管理')
            try:
                self.driver.implicitly_wait(2)
                rftemplate.click_wirelessExtension()
                time.sleep(0.5)
                rftemplate.click_rfTemplate()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展/射频模板，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展/射频模板，与参数表不符')
                raise Exception(u'软件支持无线扩展/射频模板，与参数表不符')
        self.driver.quit()
        logger.info('test_003_Template passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
