#! -*-conding:utf-8 -*-
#@Time: 2019/1/29 0029 15:20
#@swzhou
'''
AP设备管理
'''

import os
import time
import socket
import unittest
import telnetlib
import win32process
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet,getweb,getParameter
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from common.swconfig import swconfig
from common.GetRouteCPU import getCPUmodel
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from pages.sysConfig_006_ScheduledTaskPage import ScheduledTaskPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'AC_002_APmanagement').getlog()
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")
vlanPortP = getParameter('vlanPortP')
Support = getExcelValue(vlanPortP)
v1APname = getweb('v1APname')
v2APname = getweb('v2APname')
class APmanagement(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        os.system('taskkill /im "tftpd32.exe" /F')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        device = deviceMgmtPage(self.driver,self.url)
        #进入网络配置-外网配置
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        # 点击管理通讯协议，v2在上
        device.click_Priorityv2()
        time.sleep(1)
        # pass

    def test_001_APlist(self):
        u'''AP列表显示、修改名称、信道、密码、漫游阈值'''
        OnlineA = getAssertText('OnlineA')
        device = deviceMgmtPage(self.driver, self.url)
        #先确认AP均上线
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

        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        # # 确定第一、四行设备序列号 以防排序变化
        # v2_seq1 = str(device.getText_byXpath(device.list_seq1))
        # print(v2_seq1)
        # v1_seq2 = str(device.getText_byXpath(device.list_seq4))
        # print(v1_seq2)

        # v2协议列表中的操作（搜定位第一排的序列号）
        device.input_search(v2APname)
        device.click_searchB()
        time.sleep(1)
        v2_ip1=str(device.getText_byXpath(device.list_IP1))
        print(v2_ip1)
        #修改设备名称
        device.click_list_name1()
        time.sleep(0.5)
        device.input_list_namein1('1')
        time.sleep(0.5)
        device.click_list_nameS1()
        time.sleep(8)
        name_save1 = str(device.getAttribute_byXpath(device.list_name1s,'data-local'))
        print(name_save1)
        self.assertEqual(name_save1,'1',msg='AP名称修改出错')
        # 2.4G 信道
        device.click_list_channel1c()
        time.sleep(0.5)
        selchannel2_1 = device.selelement_byXpath(device.selchannel2_1)
        Select(selchannel2_1).select_by_value('2')
        time.sleep(0.2)
        device.click_selchannel2S_1()
        time.sleep(6)
        channel2_save1 = str(device.getAttribute_byXpath(device.list_channel1,'data-local'))
        self.assertEqual(channel2_save1, '2', msg='2.4G 信道修改出错')
        # 5G
        device.click_list_channel51c()
        time.sleep(0.5)
        selchannel5_1 = device.selelement_byXpath(device.selchannel5_1)
        Select(selchannel5_1).select_by_value('36')
        time.sleep(0.2)
        device.click_selchannel5S_1()
        time.sleep(6)
        channel5_save = str(device.getAttribute_byXpath(device.list_channel51,'data-local'))
        self.assertEqual(channel5_save, '36', msg='5G 信道修改出错')
        # 单台管理
        device.click_list_mangement1()
        time.sleep(2)
        device.click_modifyPw()
        time.sleep(0.5)
        device.input_pw1('1')
        device.input_pw2('1')
        time.sleep(0.2)
        device.click_save()
        time.sleep(5)
        passurl_v2 = 'http://admin:1@' + v2_ip1 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        try:
            self.driver.get(passurl_v2)
            time.sleep(2)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            raise Exception('v2 AP1密码修改失败')
        self.driver.back()
        #密码改回admin
        device.input_search(v2APname)
        device.click_searchB()
        time.sleep(1)
        device.click_list_mangement1()
        time.sleep(2)
        device.click_modifyPw()
        time.sleep(0.5)
        device.input_pw1('admin')
        device.input_pw2('admin')
        time.sleep(0.2)
        device.click_save()
        time.sleep(5)
        passurl_v2 = 'http://admin:admin@' + v2_ip1 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        try:
            self.driver.get(passurl_v2)
            time.sleep(2)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            raise Exception('v2 AP1密码改回admin失败')
        self.driver.back()
        time.sleep(1)
        device.click_deviceMgmt()
        time.sleep(1)
        #搜序列号
        device.input_search(v2APname)
        device.click_searchB()
        time.sleep(1)
        device.click_list_mangement1()
        time.sleep(2)
        device.click_roamingSet() #漫游阈值
        time.sleep(0.5)
        device.click_roaming_en()
        time.sleep(0.5)
        device.input_roaming_th('-70')
        time.sleep(0.5)
        device.click_roaming_en5()
        time.sleep(0.5)
        device.input_roaming_th5('-100')
        time.sleep(0.2)
        device.click_save()
        time.sleep(8)
        #判断生效
        device.click_list_mangement1()
        time.sleep(2)
        device.click_roamingSet()  # 漫游阈值
        time.sleep(0.5)
        rpaming_en_2G = str(device.getAttribute_byXpath(device.roaming_ens,'checked'))
        self.assertEqual(rpaming_en_2G, 'true', msg='2.4G漫游阈值 开启失败')
        rpaming_en_5G = str(device.getAttribute_byXpath(device.roaming_en5s, 'checked'))
        self.assertEqual(rpaming_en_5G, 'true', msg='漫游阈值 开启失败')
        roaming_th=str(device.getAttribute_byName(device.roaming_ths,'value'))
        self.assertEqual(roaming_th,'-70',msg='2.4G漫游阈值 保存失败')
        roaming_th5G=str(device.getAttribute_byName(device.roaming_ths5,'value'))
        self.assertEqual(roaming_th5G, '-100', msg='5G漫游阈值 保存失败')
        device.click_modal_hide()
        time.sleep(0.5)
        tn = telnetlib.Telnet(host = v2_ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "AssocReqRssiThres:  -70" and 'KickStaRssiLow:     -70' in result:
            print('2.4G 漫游阈值下发正常')
        else:
            raise Exception('2.4G 漫游阈值下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host = v2_ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv rai0 get Config' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "AssocReqRssiThres:  -100" and 'KickStaRssiLow:     -100'  in result:
            print('5G 漫游阈值下发正常')
        else:
            raise Exception('5G 漫游阈值下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        # v1协议列表中的操作（搜定位第4排的序列号）
        device.input_search(v1APname)
        device.click_searchB()
        time.sleep(1)
        v1_ip1 = str(device.getText_byXpath(device.list_IP1))
        print(v1_ip1)
        # 修改设备名称
        device.click_list_name1()
        time.sleep(0.5)
        device.input_list_namein1('1')
        time.sleep(0.5)
        device.click_list_nameS1()
        time.sleep(8)
        name_save1 = str(device.getAttribute_byXpath(device.list_name1s, 'data-local'))
        print(name_save1)
        self.assertEqual(name_save1, '1', msg='AP名称修改出错')
        # 2.4G 信道
        device.click_list_channel1c()
        time.sleep(0.5)
        selchannel2_1 = device.selelement_byXpath(device.selchannel2_1)
        Select(selchannel2_1).select_by_value('2')
        time.sleep(0.2)
        device.click_selchannel2S_1()
        time.sleep(6)
        channel2_save1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
        self.assertEqual(channel2_save1, '2', msg='2.4G 信道修改出错')
        # 5G（环境中v1AP没有5G先隐去）
        # device.click_list_channel51c()
        # time.sleep(0.5)
        # selchannel5_1 = device.selelement_byXpath(device.selchannel5_1)
        # Select(selchannel5_1).select_by_value('36')
        # time.sleep(0.2)
        # device.click_selchannel5S_1()
        # time.sleep(6)
        # channel5_save = str(device.getAttribute_byXpath(device.list_channel51, 'data-local'))
        # self.assertEqual(channel5_save, '36', msg='5G 信道修改出错')
        # 单台管理
        device.click_list_mangement1()
        time.sleep(2)
        device.click_modifyPw()
        time.sleep(0.5)
        device.input_pw1('1')
        device.input_pw2('1')
        time.sleep(0.2)
        device.click_save()
        time.sleep(5)
        passurl_v1 = 'http://admin:1@' + v1_ip1 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        try:
            self.driver.get(passurl_v1)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            raise Exception('v2 AP2密码修改失败')
        self.driver.back()
        #密码改回admin
        device.input_search(v1APname)
        device.click_searchB()
        time.sleep(1)
        device.click_list_mangement1()
        time.sleep(2)
        device.click_modifyPw()
        time.sleep(0.5)
        device.input_pw1('admin')
        device.input_pw2('admin')
        time.sleep(0.2)
        device.click_save()
        time.sleep(5)
        passurl_v1 = 'http://admin:admin@' + v1_ip1 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        try:
            self.driver.get(passurl_v1)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            raise Exception('v2 AP2密码修改失败')
        self.driver.back()
        time.sleep(1)
        device.click_deviceMgmt()
        time.sleep(1)
        # 搜序列号
        device.input_search(v1APname)
        device.click_searchB()
        time.sleep(1)
        device.click_list_mangement1()
        time.sleep(2)
        device.click_roamingSet()  # 漫游阈值
        time.sleep(0.5)
        device.click_roaming_en()
        time.sleep(0.5)
        device.input_roaming_th('-70')
        time.sleep(0.2)
        # # 5G（环境中v1AP没有5G先隐去）
        # device.click_roaming_en5()
        # time.sleep(0.5)
        # device.input_roaming_th5('-100')
        # time.sleep(0.2)
        device.click_save()
        time.sleep(5)
        # 判断生效
        device.click_list_mangement1()
        time.sleep(2)
        device.click_roamingSet()  # 漫游阈值
        time.sleep(0.5)
        rpaming_en_2G = str(device.getAttribute_byXpath(device.roaming_ens, 'checked'))
        self.assertEqual(rpaming_en_2G, 'true', msg='2.4G漫游阈值 开启失败')
        roaming_th = str(device.getAttribute_byName(device.roaming_ths, 'value'))
        self.assertEqual(roaming_th, '-70', msg='2.4G漫游阈值 保存失败')
        # rpaming_en_5G = str(device.getAttribute_byXpath(device.roaming_en5s, 'checked'))
        # self.assertEqual(rpaming_en_5G, 'true', msg='漫游阈值 开启失败')
        # roaming_th5G = str(device.getAttribute_byName(device.roaming_ths5, 'value'))
        # self.assertEqual(roaming_th5G, '-100', msg='5G漫游阈值 保存失败')
        device.click_modal_hide()
        time.sleep(0.5)
        tn = telnetlib.Telnet(host=v1_ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "AssocReqRssiThres:  -70" and 'KickStaRssiLow:     -70' in result:
            print('2.4G 漫游阈值下发正常')
        else:
            raise Exception('2.4G 漫游阈值下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        # tn = telnetlib.Telnet(host=v1_ip1, port=port,timeout=10)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'iwpriv rai0 get Config' + b'\n')  # 无线隔离
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 判断
        # if "AssocReqRssiThres:  -100" and 'KickStaRssiLow:     -100' in result:
        #     print('5G 漫游阈值下发正常')
        # else:
        #     raise Exception('5G 漫游阈值下发异常')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_001_APlist passed')

    def test_002_sendTemplateSSID(self):
        u'''批量-下发射频模板/网络名称'''

        device = deviceMgmtPage(self.driver, self.url)
        # v2协议列表中的操作
        # 批量下发射频模板/网络名称(批量)（排序后第一&第二行）
        device.click_list_sel1()
        device.click_list_sel2()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        Select(spmb).select_by_value('default2')
        time.sleep(0.5)
        device.click_save()
        time.sleep(17)
        device.click_ssidM() # 网络名称
        time.sleep(1)
        device.click_selall_w() # 全选
        time.sleep(0.5)
        device.click_sendToApM()
        time.sleep(1)
        device.click_ok()
        time.sleep(27)
        device.click_tab_modal()
        time.sleep(5)
        #加个循环 判断批量下发的模板
        i = 0
        while i < 40:
            device.click_refreshtable()
            time.sleep(1)
            channel1 = str(device.getAttribute_byXpath(device.list_channel1,'data-local'))
            channel2 = str(device.getAttribute_byXpath(device.list_channel2,'data-local'))
            channel51 = str(device.getAttribute_byXpath(device.list_channel51,'data-local'))
            channel52 = str(device.getAttribute_byXpath(device.list_channel52,'data-local'))
            print(channel1, channel2, channel51, channel52, i)
            if channel1 == '6' and channel2 == '6' and ('auto' in channel51) and ('auto' in channel52):
                print('v2 批量模板下发正常', i)
                break
            else:
                time.sleep(3)
            i = i + 1
        else:
            CapPic(self.driver)
            logger.info(u'v2 批量模板下发不生效')
            raise Exception('v2 批量模板下发不生效')
        # 下发的AP ssid需要和003中配置的ssid 一致
        device.click_refreshtable()
        time.sleep(1)
        device.click_list_ssid1()
        time.sleep(1)
        APModel1 = device.getText_byXpath(device.list_modes1)
        ssid2_1 = device.getAttribute_byXpath(device.list_ssids1,"data-hover-title")
        print('APModel1:',APModel1,'ssid2_1:', ssid2_1)
        self.assertEqual(ssid2_1, 'ssid_1中,2.4Gz中,ssid_all中/ssid_1中,5Gz中,ssid_all中', msg='v2AP ssid下发不一致')
        device.click_refreshtable()
        time.sleep(1)
        device.click_list_ssid2()
        time.sleep(1)
        APModel2 = device.getText_byXpath(device.list_modes2)
        ssid2_2 = device.getAttribute_byXpath(device.list_ssids2, "data-hover-title")
        print('APModel2:', APModel2, 'ssid2_2:', ssid2_2)
        self.assertEqual(ssid2_2, 'ssid_1中,2.4Gz中,ssid_all中/ssid_1中,5Gz中,ssid_all中', msg='v2AP ssid下发不一致')
        print('V2 批量-下发射频模板/网络名称 验证通过')
        #防止页面超时跳转到登录页
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        # 批量下发射频模板/网络名称(单独)（排序后第一行）
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        spmb = device.selelement_byName(device.spmb)
        Select(spmb).select_by_value('default3')
        time.sleep(0.5)
        device.click_save()
        time.sleep(15)
        device.click_ssidM() # 网络名称
        time.sleep(1)
        device.click_list_selwn2() # 第二行
        device.click_list_selwn3() # 第3行
        time.sleep(0.5)
        device.click_sendToApM()
        time.sleep(2)
        device.click_ok()
        time.sleep(27)
        device.click_tab_modal()
        time.sleep(2)
        # 加个循环 判断批量下发的模板
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        i = 0
        while i < 40:
            device.click_refreshtable()
            time.sleep(1)
            channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
            channel51 = str(device.getAttribute_byXpath(device.list_channel51, 'data-local'))
            if channel1 != '11' or ('auto' not in channel51):
                time.sleep(3)
                i += 1
            else:
                device.click_refreshtable()
                time.sleep(1)
                device.click_list_ssid1()
                time.sleep(1)
                APModel1 = device.getText_byXpath(device.list_modes1)
                ssid2_1 = device.getAttribute_byXpath(device.list_ssids1, "data-hover-title")
                print('APModel1',APModel1,channel1, channel51, i)
                if ssid2_1 == '2.4Gz中/5Gz中' :
                    print('v2 单独下发模板ssid正常', i)
                    break
                else:
                    time.sleep(3)
                i = i + 1
        else:
            CapPic(self.driver)
            logger.info(u'v2 单独下发模板ssid出错')
            raise Exception('v2 单独下发模板ssid出错')
        print('V2 批量下发射频模板/网络名称(单独) 验证通过')
        #确认V2 AP1的 无线隔离、无线隐藏、加密、限速、无线vlan（这里查的AP版本为WA2540Nset）
        V2ip1=str(device.getText_byXpath(device.list_IP1))
        print(V2ip1)
        # 连接Telnet服务器
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat |grep isolate' + b'\n') #无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "isolate=1" in result:
            print('2.4G 无线隔离下发正常')
        else:
            raise Exception('2.4G 无线隔离下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat  |grep isolate' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "isolate=1" in result:
            print('2.4G 无线隔离下发正常')
        else:
            raise Exception('5G 无线隔离下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat |grep HideSSID' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "HideSSID=1;0;0;0" in result:  #HideSSID=1;1;0;0 代表 第1个第2个ssid隐藏
            print('2.4G/5G 无线隐藏下发正常')
        else:
            raise Exception('2.4G/5G 无线隐藏下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        #（这里查的AP版本为WA2540Nset v2.6.4-171110）
        # tn.write(b'cat /sbin/rate_limit2.sh | grep WPAPSK=12345678' + b'\n') #SSID是否加密
        #（这里查的AP版本为WA2540Nset v2.6.4-190815）
        tn.write(b'cat /sbin/ConfigWifi.sh | grep WPAPSK=12345678' + b'\n')  # SSID是否加密
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "iwpriv ra0 set WPAPSK=12345678" and "iwpriv rai0 set WPAPSK=12345678" in result:
            print('2.4G/5G SSID加密下发正常')
        else:
            raise Exception('2.4G/5G SSID加密下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config | grep alone' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "0   alone              1000      250            1000      250" in result:  # 限速
            print('2.4G 独享限速下发正常')
        else:
            raise Exception('2.4G 独享限速下发正常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv rai0 get Config | grep share' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "0   share              1000      250            1000      250" in result:  # H限速
            print('5G 共享限速下发正常')
        else:
            raise Exception('5G 共享限速下发正常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        if Support == '√':#如果支持vlan接口
            tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep vlanid' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 判断
            if "vlanid=1000" in result:  # 限速
                print('2.4G vlanID下发正常')
            else:
                raise Exception('2.4G vlanID下发正常')  # 如果没有则报错
            tn.close()  # tn.write('exit\n')
            tn = telnetlib.Telnet(host=V2ip1, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat | grep vlanid' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 判断
            if "vlanid=1999" in result:  # H限速
                print('5G vlanID下发正常')
            else:
                raise Exception('5G vlanID下发正常')  # 如果没有则报错
            tn.close()  # tn.write('exit\n')
            print('V2 AP1下发无线vlan 验证通过')
        print('V2 AP1下发无线隔离、无线隐藏、加密、限速 验证通过')

        # v1协议列表中的操作
        # 防止页面超时跳转到登录页
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        # v1协议列表中的操作
        # 批量下发射频模板/网络名称(批量)（排序后第三&第四行）
        device.click_list_sel3()
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        spmb = device.selelement_byName(device.spmb) # 射频设置
        Select(spmb).select_by_value('default2')
        time.sleep(0.5)
        device.click_save()
        time.sleep(25)
        device.click_ssidM()
        time.sleep(1)
        device.click_selall_w()
        time.sleep(0.5)
        device.click_sendToApM()
        time.sleep(1)
        device.click_ok()
        time.sleep(27)
        device.click_tab_modal()
        time.sleep(2)
        # 加个循环 判断批量下发的模板
        i = 0
        while i < 40:
            device.click_refreshtable()
            time.sleep(1)
            channel3 = str(device.getAttribute_byXpath(device.list_channel3,'data-local'))
            channel4 = str(device.getAttribute_byXpath(device.list_channel4,'data-local'))
            # channel53 = str(device.getAttribute_byXpath(device.list_channel53,'data-local'))
            # channel54 = str((device.getAttribute_byXpath(device.list_channel54,'data-local')))
            # self.assertIn('auto', channel53, msg='v1 AP1 5G 模板下发出错')
            # self.assertIn('auto', channel54, msg='v1 AP2 5G 模板下发出错')
            # print(channel3, channel4, i)
            if channel3 == '6' and channel4 == '6':
                print('v1 批量模板下发正常', i)
                break
            else:
                time.sleep(3)
            i = i + 1
        else:
            CapPic(self.driver)
            logger.info(u'v1 批量模板下发不生效')
            raise Exception('v1 批量模板下发不生效')
        # 加个循环 判断批量下发的ssid
        i = 0
        while i < 40:
            device.click_refreshtable()
            time.sleep(1)
            device.click_list_ssid3()
            time.sleep(1)
            APmode1_1 = device.getText_byXpath(device.list_modes3)
            ssid1_1 = device.getAttribute_byXpath(device.list_ssids3,"data-hover-title")
            print('APmode1_1:', APmode1_1,'ssid1_1:', ssid1_1)
            device.click_refreshtable()
            time.sleep(1)
            device.click_list_ssid4()
            time.sleep(1)
            APModel1_2 = device.getText_byXpath(device.list_modes4)
            ssid1_2 = device.getAttribute_byXpath(device.list_ssids4, "data-hover-title")
            print('APModel1_2:', APModel1_2,'ssid1_2:', ssid1_2)
            if ssid1_1 == 'ssid_1中,2.4Gz中,5Gz中,ssid_all中' and ssid1_2 == 'ssid_1中,2.4Gz中,5Gz中,ssid_all中':
                print('v1 批量ssid下发正常', i)
                break
            else:
                time.sleep(3)
                i = i + 1
        else:
            CapPic(self.driver)
            logger.info(u'v1 批量ssid下发不生效')
            raise Exception('v1 批量ssid下发不生效')
        # 批量下发射频模板/网络名称(单独)（排序后第4行）
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        Select(spmb).select_by_value('default3')
        time.sleep(0.5)
        device.click_save()
        time.sleep(30)
        device.click_ssidM() # 网络名称
        time.sleep(1)
        device.click_list_selwn2() # 第二行
        device.click_list_selwn3() # 第三行
        time.sleep(0.5)
        device.click_sendToApM()
        time.sleep(1)
        device.click_ok()
        time.sleep(27)
        device.click_tab_modal()
        time.sleep(1)
        device.click_refreshtable()
        time.sleep(5)
        # 加个循环 判断批量下发的ssid
        i = 0
        while i < 40:
            device.click_refreshtable()
            time.sleep(1)
            channel4 = str(device.getAttribute_byXpath(device.list_channel4,'data-local'))
            # channel54 = str(device.getAttribute_byXpath(device.list_channel54c,'data-local'))
            # self.assertIn('auto', channel54, msg='5G 模板下发出错')
            if channel4 != '11':
                time.sleep(3)
                i = i + 1
            else:
                device.click_list_ssid4()
                time.sleep(1)
                APmodel = device.getText_byXpath(device.list_modes4)
                ssid1_2 = device.getAttribute_byXpath(device.list_ssids4,"data-hover-title")
                print('APname:',APmodel,'channel4:',channel4,'ssid1_2:', ssid1_2)
                # self.assertEqual(ssid1_2, '2.4Gz中,5Gz中', msg='v2AP ssid单独下发不一致')
                if ssid1_2 == '2.4Gz中,5Gz中':
                    print('v1 单独下发模板及ssid下发正常', i)
                    break
                else:
                    time.sleep(3)
                i = i + 1
        else:
            raise Exception('v1 单独下发模板及ssid下发异常')
        print('V1 批量下发射频模板/网络名称(单独) 验证通过')
        # 确认V1 AP2的 无线隐藏、加密、限速（这里查的AP版本为WA3000N v2.6.3-160519）
        V1ip2 = str(device.getText_byXpath(device.list_IP4))
        print(V1ip2)

        #v1 3000N 无线隔离生效但是没有iso参数 先注释掉
        # # 连接Telnet服务器
        # tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat |grep isolate' + b'\n')  # 无线隔离
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 判断
        # if "isolate=1" in result:
        #     print('2.4G 无线隔离下发正常')
        # else:
        #     raise Exception('2.4G 无线隔离下发异常')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')
        # tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat  |grep isolate' + b'\n')  # 无线隔离
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 判断
        # if "isolate=1" in result:
        #     print('5G 无线隔离下发正常')
        # else:
        #     raise Exception('5G 无线隔离下发异常')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat |grep HideSSID' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "HideSSID=1;1;1;0" in result: # WA3000N v2.6.3-160519 显示是3个
            print('ssid 无线隐藏下发正常')
        else:
            raise Exception('ssid 无线隐藏下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep AuthMode=WPAPSKWPA2PSK' + b'\n')  # SSID是否加密
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "AuthMode=WPAPSKWPA2PSK;WPAPSKWPA2PSK;WPAPSKWPA2PSK;OPEN" in result:
            print('2.4G/5G SSID加密下发正常')
        else:
            raise Exception('2.4G/5G SSID加密下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep =12345678' + b'\n')  # SSID加密密码
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "WPAPSK1=12345678" and 'WPAPSK2=12345678' in result:
            print('2.4G/5G SSID加密密码下发正常')
        else:
            raise Exception('2.4G/5G SSID加密密码下发异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config | grep alone' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "alone              1000      250            1000      250" in result:  # 限速
            print('ssid1 独享限速下发正常')
        else:
            raise Exception('ssid1 独享限速下发正常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra1 get Config | grep share' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "share              1000      250            1000      250" in result:  # 限速
            print('ssid2 共享限速下发正常')
        else:
            raise Exception('ssid2 共享限速下发正常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        # if Support == '√':  # 如果支持vlan接口
            # tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
            # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # # 输入登录用户名
            # tn.read_until(b'login:')
            # tn.write(username + b"\n")
            # tn.read_until(b'Password:')
            # tn.write(password + b"\n")
            # # 登录完毕后执行命令
            # tn.read_until(b'#')
            # tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep vlanid' + b'\n')
            # # 输出结果，判断
            # time.sleep(1)
            # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            # print('-------------------输出结果------------------------')
            # # 命令执行结果
            # print('result:', result)
            # # 判断
            # if "vlanid=1000" in result:  # 限速
            #     print('2.4G vlanID下发正常')
            # else:
            #     raise Exception('2.4G vlanID下发正常')  # 如果没有则报错
            # tn.close()  # tn.write('exit\n')
            # tn = telnetlib.Telnet(host=V1ip2, port=port,timeout=10)
            # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # # 输入登录用户名
            # tn.read_until(b'login:')
            # tn.write(username + b"\n")
            # tn.read_until(b'Password:')
            # tn.write(password + b"\n")
            # # 登录完毕后执行命令
            # tn.read_until(b'#')
            # tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat | grep vlanid' + b'\n')
            # # 输出结果，判断
            # time.sleep(1)
            # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            # print('-------------------输出结果------------------------')
            # # 命令执行结果
            # print('result:', result)
            # # 判断
            # if "vlanid=1999" in result:  # H限速
            #     print('5G vlanID下发正常')
            # else:
            #     raise Exception('5G vlanID下发正常')  # 如果没有则报错
            # tn.close()  # tn.write('exit\n')
        print('V1 AP2下发无线隐藏、加密、限速 验证通过')

        self.driver.quit()
        logger.info('test_002_sendTemplateSSID passed')

    def test_003_taskPlan_SleepMode(self):
        u'''AP计划任务、睡眠模式'''
        host = gettelnet('host')
        nodata = getAssertText('nodata')
        CPUmodel = getCPUmodel()
        # 1、配置AP计划任务
        taskPlan = ScheduledTaskPage(self.driver,self.url)
        taskPlan.click_sysConfig()
        time.sleep(0.5)
        taskPlan.click_ScheduledTask()
        time.sleep(1)
        # 操作删除 以访已有规则
        taskPlan.click_selall()
        time.sleep(0.2)
        taskPlan.click_delall()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            taskPlan.find_ok()
        except NoSuchElementException:
            try:
                taskPlan.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('计划任务列表已为空')
        taskPlan.click_add()
        time.sleep(1)
        taskPlan.input_ID('test')
        obj = taskPlan.selelement_byName(taskPlan.obj)
        Select(obj).select_by_value('02') #生效对象AP
        time.sleep(0.2)
        selDay = taskPlan.selelement_byName(taskPlan.selDay)
        Select(selDay).select_by_value('03') #星期三
        time.sleep(0.2)
        taskPlan.input_txtHour1('7')
        taskPlan.input_txtMin1('7')
        selContent = taskPlan.selelement_byName(taskPlan.selContent)
        Select(selContent).select_by_value('rebootS')
        time.sleep(0.2)
        taskPlan.click_save()
        time.sleep(1)
        list_obj = taskPlan.getText_byXpath(taskPlan.list_obj)
        if list_obj == 'AP':
            logger.info(u'AP计划任务添加正常')
        else:
            CapPic(self.driver)
            logger.info(u'AP计划任务添加异常')
            raise Exception(u'AP计划任务添加异常')
        #2、下发计划任务、睡眠模式
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
        time.sleep(1)
        # 确定第一、四行设备序列号 以防排序变化
        v2_seq1 = str(device.getText_byXpath(device.list_seq1))
        print(v2_seq1)
        v1_seq2 = str(device.getText_byXpath(device.list_seq3))
        print(v1_seq2)

        # v2协议列表中的操作（搜定位第一排的序列号）
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        device.input_search(v2_seq1)
        device.click_searchB()
        time.sleep(1)
        # 批量单台管理
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_Syssetup()
        time.sleep(1)
        device.click_TaskS_En() #开启计划任务
        time.sleep(0.5)
        TaskSValue = device.selelement_byName(device.TaskSValue)
        Select(TaskSValue).select_by_value('1') #选择新建的计划任务
        device.click_sleepMode_En() #开启睡眠模式
        device.click_save()
        time.sleep(10)
        device.click_tab_modal()
        time.sleep(2)
        # 打开tftp32.exe,
        handle = win32process.CreateProcess(r"D:\python\SEWEB\3.1.1Router\test_case\tftpd32.exe", '', None,
                                            None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())  # 打开tftp32.exe，获得其句柄

        #v2 需要借助sqlite3工具查看，并且mtk/p1010/x86平台工具链不一致工具不同

        if CPUmodel == "MTK":
            print('mtk平台')
            sqlite3Tool = 'sqlite3-nv518Gv2-190314'
        elif CPUmodel == 'X86':
            print('X86平台')
            sqlite3Tool = 'sqlite3-lv4250G-190314'
        elif CPUmodel == 'P1010':
            print('P1010平台')
            sqlite3Tool = 'sqlite3-qv4240G-190315'
        elif CPUmodel == 'Qualcomm':
            print('高通平台')
            sqlite3Tool = 'sqlite3-qca-190426'
        else:
            logger.info(u'平台判断出错')
            raise Exception('平台判断出错')

        sqlite3cmd = bytes(('tftp -gr ' + sqlite3Tool + ' ' +pcaddr + ' 69'), encoding='utf8')
        tn = telnetlib.Telnet(host=host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(sqlite3cmd + b'\n')
        tn.read_until(b'#')
        sqlite3cmd2 = bytes(('chmod 777 ' + sqlite3Tool), encoding='utf8')
        tn.write(sqlite3cmd2 + b'\n')
        tn.read_until(b'#')
        sqlite3cmd3 = bytes(('./' + sqlite3Tool + ' apData.db'), encoding='utf8')
        tn.write(sqlite3cmd3 + b'\n')
        tn.read_until(b'sqlite> ')
        sqlite3cmd4 = bytes(("select * from apCfg where sn = '" + v2_seq1 +"' ;"), encoding='utf8')
        tn.write(sqlite3cmd4 + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if '"scheTask":[{"pHour":"07","pCmd":"rebootS","pWeek":"03","pMin":"07","pType":"01"}]' and '"SleepMode":"on"'in result:
            print('v2 计划任务下发正常')
        else:
            logger.info(u'v2 计划任务下发正常异常')
            logger.info('v2 计划任务result:', result)
            raise Exception('v2 计划任务下发正常异常')
        tn.close()  # tn.write('exit\n')

        # v1协议列表中的操作（搜定位第4排的序列号）
        device.click_deviceMgmt()
        time.sleep(1)
        device.input_search(v1_seq2)
        device.click_searchB()
        time.sleep(1)
        # 批量单台管理
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_Syssetup()
        time.sleep(1)
        device.click_TaskS_En()  # 开启计划任务
        time.sleep(0.5)
        TaskSValue = device.selelement_byName(device.TaskSValue)
        Select(TaskSValue).select_by_value('1')  # 选择新建的计划任务
        device.click_sleepMode_En()  # 开启睡眠模式
        device.click_save()
        time.sleep(15)
        device.click_tab_modal()
        time.sleep(5)
        tn = telnetlib.Telnet(host = host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cd /tmp/urcp/ap_configs/' + b'\n')
        tn.read_until(b'#')
        TaskScom = bytes(('cat ' + v1_seq2 +'.xml | grep reboot'),encoding='utf8')
        tn.write(TaskScom + b'\n')  # 计划任务
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if "<active>Yes</active><pMin>07</pMin><pHour>07</pHour><pWeek>03</pWeek>" in result:
            print('v1 计划任务下发正常')
        else:
            logger.info(u'v1 计划任务下发正常异常')
            logger.info('v1 计划任务result:', result)
            raise Exception('v1 计划任务下发正常异常')
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host = host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cd /tmp/urcp/ap_configs/' + b'\n')
        tn.read_until(b'#')
        sleepcom = bytes(('cat ' + v1_seq2 + '.xml | grep wled'), encoding='utf8')
        tn.write(sleepcom + b'\n')  # 计划任务
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if "<wled>0</wled>" in result:
            print('v1 睡眠模式下发正常')
        else:
            logger.info(u'v1 睡眠模式下发正常异常')
            logger.info('v1 睡眠模式result:', result)
            raise Exception('v1 睡眠模式下发异常')
        tn.close()  # tn.write('exit\n')

        #3、关闭睡眠模式、计划任务
        # v2协议列表中的操作（搜定位第一排的序列号）
        device.click_deviceMgmt()
        time.sleep(1)
        device.input_search(v2_seq1)
        device.click_searchB()
        time.sleep(1)
        # 批量单台管理
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_Syssetup()
        time.sleep(1)
        device.click_TaskS_En()  # 计划任务
        time.sleep(0.5)
        TaskSValue = device.selelement_byName(device.TaskSValue)
        Select(TaskSValue).select_by_value('0')  # 选择计划任务无
        device.click_sleepMode_C() #睡眠模式
        device.click_save()
        time.sleep(10)
        device.click_tab_modal()
        time.sleep(2)
        tn = telnetlib.Telnet(host=host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        sqlite3cmd3 = bytes(('./' + sqlite3Tool + ' apData.db'), encoding='utf8')
        tn.write(sqlite3cmd3 + b'\n')
        tn.read_until(b'sqlite> ')
        sqlite3cmd4 = bytes(("select * from apCfg where sn = '" + v2_seq1 + "' ;"), encoding='utf8')
        tn.write(sqlite3cmd4 + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if '"scheTask":[{"pWeek":"","pCmd":"","pType":"","pMin":"","pHour":""}]' and '"SleepMode":"off"' in result:
            print('v2 计划任务下发正常')
        else:
            logger.info(u'v2 计划任务下发正常异常')
            logger.info('v2 计划任务result:', result)
            raise Exception('v2 计划任务下发正常异常')
        tn.close()  # tn.write('exit\n')

        # v1协议列表中的操作（搜定位第4排的序列号）
        device.click_deviceMgmt()
        time.sleep(1)
        device.input_search(v1_seq2)
        device.click_searchB()
        time.sleep(1)
        # 批量单台管理
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_Syssetup()
        time.sleep(1)
        device.click_TaskS_En()  # 计划任务
        time.sleep(0.5)
        TaskSValue = device.selelement_byName(device.TaskSValue)
        Select(TaskSValue).select_by_value('0')  # 选择计划任务无
        device.click_sleepMode_C()  # 睡眠模式
        device.click_save()
        time.sleep(15)
        device.click_tab_modal()
        time.sleep(10)
        tn = telnetlib.Telnet(host=host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cd /tmp/urcp/ap_configs/' + b'\n')
        tn.read_until(b'#')
        TaskScom = bytes(('cat ' + v1_seq2 + '.xml | grep reboot'), encoding='utf8')
        tn.write(TaskScom + b'\n')  # 计划任务
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if "<active>Yes</active><pMin>07</pMin><pHour>07</pHour><pWeek>03</pWeek>" not in result:
            print('v1 计划任务关闭下发正常')
        else:
            logger.info(u'v1 计划任务关闭下发正常异常')
            logger.info('v1 计划任务关闭result:', result)
            raise Exception('v1 计划任务关闭下发正常异常')
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=host, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cd /tmp/urcp/ap_configs/' + b'\n')
        tn.read_until(b'#')
        sleepcom = bytes(('cat ' + v1_seq2 + '.xml | grep wled'), encoding='utf8')
        tn.write(sleepcom + b'\n')  # 计划任务
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if "<wled>0</wled>" not in result:
            print('v1 睡眠模式关闭下发正常')
        else:
            logger.info(u'v1 睡眠模式关闭下发正常异常')
            logger.info(u'v1 睡眠模式关闭result:', result)
            raise Exception('v1 睡眠模式关闭下发异常')
        tn.close()  # tn.write('exit\n')

        # 4、删除AP计划任务
        taskPlan = ScheduledTaskPage(self.driver, self.url)
        taskPlan.click_sysConfig()
        time.sleep(0.5)
        taskPlan.click_ScheduledTask()
        time.sleep(1)
        taskPlan.click_selall()
        time.sleep(0.2)
        taskPlan.click_delall()
        time.sleep(1)
        taskPlan.click_ok()
        time.sleep(1)
        listnodata = taskPlan.getText_byXpath(taskPlan.list_nodata)
        if listnodata == nodata:
            logger.info(u'AP计划任务已删除')
        else:
            CapPic(self.driver)
            logger.info(u'AP计划任务删除失败')
            raise Exception(u'AP计划任务删除失败')

        self.driver.quit()
        win32process.TerminateProcess(handle[0], 0)  # 关闭tftp32
        logger.info('test_003_taskPlan_SleepMode passed')

    def test_004_rebootAlone(self):
        u'''单台重启'''
        SuccessOperationA = getAssertText('SuccessOperationA')
        OnlineA = getAssertText('OnlineA')
        device = deviceMgmtPage(self.driver, self.url)
        device.click_list_reboot1()
        time.sleep(1)
        device.click_ok()
        time.sleep(4)
        tips_show_in=str(device.getText_byClass(device.tipsshowin))
        self.assertEqual(tips_show_in,SuccessOperationA,msg='AP1单台操作重启 异常')
        time.sleep(1)
        device.click_list_reboot2()
        time.sleep(1)
        device.click_ok()
        time.sleep(4)
        tips_show_in = str(device.getText_byClass(device.tipsshowin))
        self.assertEqual(tips_show_in, SuccessOperationA, msg='AP2单台操作重启 异常')
        time.sleep(1)
        device.click_list_reboot3()
        time.sleep(1)
        device.click_ok()
        time.sleep(4)
        tips_show_in = str(device.getText_byClass(device.tipsshowin))
        self.assertEqual(tips_show_in, SuccessOperationA, msg='AP3单台操作重启 异常')
        time.sleep(1)
        device.click_list_reboot4()
        time.sleep(1)
        device.click_ok()
        time.sleep(4)
        tips_show_in = str(device.getText_byClass(device.tipsshowin))
        self.assertEqual(tips_show_in, SuccessOperationA, msg='AP4单台操作重启 异常')
        time.sleep(50)
        device.click_deviceMgmt()
        time.sleep(1)
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
            logger.info(u'AP 未能同步2.4G无线接口')
            raise Exception('AP 未能同步2.4G无线接口')
        self.driver.quit()
        logger.info('test_004_rebootAlone passed')

    def test_005_rebootBatch(self):
        u'''批量重启'''
        OnlineA = getAssertText('OnlineA')
        device = deviceMgmtPage(self.driver, self.url)
        # v2协议列表中的操作
        # 批量-恢复出厂(批量)（排序后第一&第二行）
        device.click_list_sel1()
        device.click_list_sel2()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_restart()
        time.sleep(1)
        device.click_ok()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V2 批量重启 异常')
                    raise Exception(u'V2 批量重启 异常')
                break
        else:
            raise Exception(u'V2 批量重启 未弹出提示框')
        device.click_close()
        time.sleep(0.5)
        self.driver.implicitly_wait(10)
        # v1协议列表中的操作
        # 取消前两行
        device.click_list_sel1()
        device.click_list_sel2()
        time.sleep(0.5)
        # 批量-恢复出厂(单独)（排序后三行）
        device.click_list_sel3()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_restart()
        time.sleep(1)
        device.click_ok()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V1 AP1恢复出厂 异常')
                    raise Exception(u'V1 AP1恢复出厂 异常')
                break
        else:
            raise Exception(u'V1 AP1恢复出厂 未弹出提示框')
        device.click_close()
        time.sleep(0.5)
        # 先取消 选中的第三行
        device.click_list_sel3()
        time.sleep(0.5)
        # 批量-恢复出厂(单独)（排序后四行）
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_restart()
        time.sleep(1)
        device.click_ok()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V1 AP2恢复出厂 异常')
                    raise Exception(u'V1 AP2恢复出厂 异常')
                break
        else:
            raise Exception(u'V1 AP2恢复出厂 未弹出提示框')
        device.click_close()
        time.sleep(2)
        # 等待AP上线
        device.click_deviceMgmt()
        time.sleep(40)
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
            raise Exception('AP  未能同步2.4G无线接口')
        self.driver.quit()
        logger.info('test_005_rebootBatch passed')

    def test_006_resertAP(self):
        u'''批量-恢复出厂（单个、多个AP）'''
        OnlineA = getAssertText('OnlineA')
        nodata = getAssertText('nodata')
        device = deviceMgmtPage(self.driver, self.url)
        #确认AP在线
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
            raise Exception('AP  未能同步2.4G无线接口')

        # v2协议列表中的操作
        # 批量-恢复出厂(批量)（排序后第一&第二行）
        device.click_list_sel1()
        device.click_list_sel2()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_factory_reset()
        time.sleep(1)
        device.click_ok()
        time.sleep(8)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin,'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V2 批量恢复出厂 异常')
                    raise Exception(u'V2 批量恢复出厂 异常')
                break
        else:
            raise Exception(u'V2 批量恢复出厂 未弹出提示框')
        device.click_close()
        time.sleep(0.5)
        self.driver.implicitly_wait(10)
        # 备份配置中确认AP配置是否已删除
        APseq1 = device.getText_byXpath(device.list_seq1)
        APseq2 = device.getText_byXpath(device.list_seq2)
        list_modes1 = device.getText_byXpath(device.list_modes1)
        list_modes2 = device.getText_byXpath(device.list_modes2)
        print(APseq1, APseq2)
        device.click_backupconfig()
        time.sleep(1)
        device.input_searchBack(APseq1)
        device.click_searchBackb()
        time.sleep(1)
        try:
            device.getText_byXpath(device.listback_nodata)
        except NoSuchElementException:
            bconfigmodel1 = device.getText_byXpath(device.bconfigmodel1)
            if bconfigmodel1 == list_modes1:  # 再匹配AP型号
                CapPic(self.driver)
                logger.info(u'v1 AP1的配置文件未删除')
                raise Exception(u'v1 AP1的配置文件未删除')
            else:  # 删除同序列号 不同AP型号的配置 以免后续误判
                device.click_sellist1()
                device.click_allDelete()
                time.sleep(1)
                device.click_ok()
                time.sleep(1)
        device.input_searchBack(APseq2)
        device.click_searchBackb()
        time.sleep(1)
        try:
            device.getText_byXpath(device.listback_nodata)
        except NoSuchElementException:
            bconfigmodel1 = device.getText_byXpath(device.bconfigmodel1)
            if bconfigmodel1 == list_modes2:  # 再匹配AP型号
                CapPic(self.driver)
                logger.info(u'v1 AP1的配置文件未删除')
                raise Exception(u'v1 AP1的配置文件未删除')
            else:  # 删除同序列号 不同AP型号的配置 以免后续误判
                device.click_sellist1()
                device.click_allDelete()
                time.sleep(1)
                device.click_ok()
                time.sleep(1)

        # v1协议列表中的操作
        # #取消前两行
        # device.click_list_sel1()
        # device.click_list_sel2()
        # time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        # 点击管理通讯协议，v2在上
        device.click_Priorityv2()
        time.sleep(1)
        # 批量-恢复出厂(单独)（排序后三行）
        device.click_list_sel3()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_factory_reset()
        time.sleep(1)
        device.click_ok()
        time.sleep(8)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V1 AP1恢复出厂 异常')
                    raise Exception(u'V1 AP1恢复出厂 异常')
                break
        else:
            raise Exception(u'V1 AP1恢复出厂 未弹出提示框')
        device.click_close()
        time.sleep(0.5)
        # 先取消 选中的第三行
        device.click_list_sel3()
        time.sleep(0.5)
        # 批量-恢复出厂(单独)（排序后四行）
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(2)
        device.click_configreboot()
        time.sleep(1)
        device.click_factory_reset()
        time.sleep(1)
        device.click_ok()
        time.sleep(8)
        # 等待弹窗提示成功
        i = 0
        while i < 40:
            try:
                self.driver.implicitly_wait(1)
                device.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(device.getAttribute_byClass(device.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'V1 AP2恢复出厂 异常')
                    raise Exception(u'V1 AP2恢复出厂 异常')
                break
        else:
            raise Exception(u'V1 AP2恢复出厂 未弹出提示框')
        device.click_close()
        time.sleep(2)
        # 备份配置中确认AP配置是否已删除
        # APseq1 = device.getText_byXpath(device.list_seq1)
        # APseq2 = device.getText_byXpath(device.list_seq2)
        APseq3 = device.getText_byXpath(device.list_seq3)
        APseq4 = device.getText_byXpath(device.list_seq4)
        list_modes3 = device.getText_byXpath(device.list_modes3)
        list_modes4 = device.getText_byXpath(device.list_modes4)
        device.click_backupconfig()
        time.sleep(1)
        device.input_searchBack(APseq3)
        device.click_searchBackb()
        time.sleep(1)
        try:
            device.getText_byXpath(device.listback_nodata)
        except NoSuchElementException:
            bconfigmodel1 = device.getText_byXpath(device.bconfigmodel1)
            if bconfigmodel1 == list_modes3: # 再匹配AP型号
                CapPic(self.driver)
                logger.info(u'v1 AP1的配置文件未删除')
                raise Exception(u'v1 AP1的配置文件未删除')
            else: #删除同序列号 不同AP型号的配置 以免后续误判
                device.click_sellist1()
                device.click_allDelete()
                time.sleep(1)
                device.click_ok()
                time.sleep(1)
        device.input_searchBack(APseq4)
        device.click_searchBackb()
        time.sleep(1)
        try:
            device.getText_byXpath(device.listback_nodata)
        except NoSuchElementException:
            bconfigmodel1 = device.getText_byXpath(device.bconfigmodel1)
            if bconfigmodel1 == list_modes4:  # 再匹配AP型号
                CapPic(self.driver)
                logger.info(u'v1 AP1的配置文件未删除')
                raise Exception(u'v1 AP1的配置文件未删除')
            else:  # 删除同序列号 不同AP型号的配置 以免后续误判
                device.click_sellist1()
                device.click_allDelete()
                time.sleep(1)
                device.click_ok()
                time.sleep(1)

        #等待AP上线
        device.click_deviceMgmt()
        time.sleep(70)
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
            raise Exception('AP  未能同步2.4G无线接口')
        print('恢复出厂后 上线')
        time.sleep(15) #稍等几秒，等AP恢复后更新到默认ssid
        device.click_deviceMgmt()
        time.sleep(1)
        # 点击管理通讯协议，v2在上
        device.click_Priorityv2()
        time.sleep(1)
        # AP恢复出厂后 获取的ssid 需要和003中配置的默认下发的 ssid 一致（更换了ssid4为自动下发）
        device.click_refreshtable()
        time.sleep(1)
        APModel1 = device.getText_byXpath(device.list_modes1)
        device.click_list_ssid1()
        time.sleep(0.5)
        ssid2_1 = device.getAttribute_byXpath(device.list_ssids1, "data-hover-title")
        print('APModel1:', APModel1, 'ssid2_1:', ssid2_1)
        self.assertEqual(ssid2_1, 'ssid_all中/ssid_all中', msg='v2AP1 恢复出厂后ssid异常')
        device.click_refreshtable()
        time.sleep(1)
        APModel2 = device.getText_byXpath(device.list_modes2)
        device.click_list_ssid2()
        time.sleep(0.5)
        ssid2_2 = device.getAttribute_byXpath(device.list_ssids2, "data-hover-title")
        print('APModel2:', APModel2, 'ssid2_2:', ssid2_2)
        self.assertEqual(ssid2_2, 'ssid_all中/ssid_all中', msg='v2AP2 恢复出厂后ssid异常')
        device.click_refreshtable()
        time.sleep(1)
        APmode1_1 = device.getText_byXpath(device.list_modes3)
        device.click_list_ssid3()
        time.sleep(0.5)
        ssid1_1 = device.getAttribute_byXpath(device.list_ssids3, "data-hover-title")
        print('APmode1_1:', APmode1_1, 'ssid1_1:', ssid1_1)
        self.assertEqual(ssid1_1, 'ssid_all中', msg='v1AP1 恢复出厂后ssid异常')
        device.click_refreshtable()
        time.sleep(1)
        APModel1_2 = device.getText_byXpath(device.list_modes4)
        device.click_list_ssid4()
        time.sleep(0.5)
        ssid1_2 = device.getAttribute_byXpath(device.list_ssids4, "data-hover-title")
        print('APModel1_2:', APModel1_2, 'ssid1_2:', ssid1_2)
        self.assertEqual(ssid1_2, 'ssid_all中', msg='v1AP2 恢复出厂后ssid异常')

        self.driver.quit()
        logger.info('test_006_resertAP passed')

    def test_007_APinVlan(self):
        u'''AP 处于vlan环境：上下线'''
        OnlineA = getAssertText('OnlineA')
        OfflineA = getAssertText('OfflineA')
        SuccessOperationA = getAssertText('SuccessOperationA')
        if Support == '√':  # 如果支持vlan接口
            device = deviceMgmtPage(self.driver, self.url)

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
                raise Exception('AP  未能同步2.4G无线接口')

            #重启AP
            device.click_list_reboot1()
            time.sleep(2)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP1单台操作重启 异常')
            device.click_list_reboot2()
            time.sleep(2)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP2单台操作重启 异常')
            device.click_list_reboot3()
            time.sleep(2)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP3单台操作重启 异常')
            device.click_list_reboot4()
            time.sleep(2)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP4单台操作重启 异常')
            time.sleep(1)
            #更改交换机端口 使AP处于access vlan下
            swconfig.test_APportAccess(self)

            #等待AP重启，vlan下urcp AP可能存在无法上线
            time.sleep(50)
            device = deviceMgmtPage(self.driver, self.url)
            x = 0
            while x < 50:
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
                device.click_deviceMgmt()
                time.sleep(1)
                device.click_Prioritystate()#状态在线 在前
                list_status1 = device.getText_byXpath(device.list_status1)
                list_status2 = device.getText_byXpath(device.list_status2)
                list_status3 = device.getText_byXpath(device.list_status3)
                list_status4 = device.getText_byXpath(device.list_status4)
                print(list_status1, list_status2, list_status3, list_status4)
                if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OfflineA and list_status4 == OfflineA:
                    CapPic(self.driver)
                    logger.info(u'vlan下 urcpAP无法上线')
                    raise Exception(u'vlan下 urcpAP无法上线')
                else:
                    CapPic(self.driver)
                    logger.info(u'AP  未能同步2.4G无线接口')
                    raise Exception(u'AP  未能同步2.4G无线接口')
        else:
            logger.info(u'参数不支持 vlan接口')
            raise Exception(u'参数不支持 vlan接口')
        self.driver.quit()
        logger.info('test_007_APinVlan passed')

    def test_008_APinvlan2(self):
        u'''AP 处于vlan环境：下发配置等'''
        OnlineA = getAssertText('OnlineA')
        SuccessOperationA = getAssertText('SuccessOperationA')
        if Support == '√':  # 如果支持vlan接口
            device = deviceMgmtPage(self.driver, self.url)
            #重启v2 AP V1AP可能不在线
            device.click_list_reboot1()
            time.sleep(1)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP1单台操作重启 异常')
            device.click_list_reboot2()
            time.sleep(1)
            device.click_ok()
            time.sleep(4)
            tips_show_in = str(device.getText_byClass(device.tipsshowin))
            self.assertEqual(tips_show_in, SuccessOperationA, msg='AP2单台操作重启 异常')
            #如果v1 AP在线则也重启掉
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            if list_status3 == OnlineA and list_status4 == OnlineA:
                device.click_list_reboot3()
                time.sleep(1)
                device.click_ok()
                time.sleep(4)
                tips_show_in = str(device.getText_byClass(device.tipsshowin))
                self.assertEqual(tips_show_in, SuccessOperationA, msg='AP3单台操作重启 异常')
                time.sleep(1)
                device.click_list_reboot4()
                time.sleep(1)
                device.click_ok()
                time.sleep(4)
                tips_show_in = str(device.getText_byClass(device.tipsshowin))
                self.assertEqual(tips_show_in, SuccessOperationA, msg='AP4单台操作重启 异常')

            #交换机端口 改回
            swconfig.test_initSwPort(self)

            # 等待AP重新上线
            time.sleep(60)
            device.click_deviceMgmt()
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
                raise Exception('AP  未能同步2.4G无线接口')
        else:
            logger.info(u'参数不支持 vlan接口')
            raise Exception(u'参数不支持 vlan接口')
        self.driver.quit()
        logger.info('test_008_APinvlan2 passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()