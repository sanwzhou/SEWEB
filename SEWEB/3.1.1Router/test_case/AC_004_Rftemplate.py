#! -*-conding:utf-8 -*-
#@Time: 2019/1/28 0028 15:06
#@swzhou
'''
射频模板
默认3个，最大有12个
'''

import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet,getweb
from common.loginRoute import login
from pages.AC_003_RftemplatePage import RftemplatePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'AC_004_Rftemplate').getlog()

class Rftemplate(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        rftemplate = RftemplatePage(self.driver,self.url)
        # 进入无线拓展_射频模板
        rftemplate.click_wirelessExtension()
        time.sleep(0.5)
        rftemplate.click_rfTemplate()
        time.sleep(2)
        # pass

    def test_001_maxNumTemplate(self):
        u'''射频模板默认3个，最大12个'''
        reachMax2A = getAssertText('reachMax2A')
        rftemplate = RftemplatePage(self.driver, self.url)
        #确认默认模板数量
        id1 = str(rftemplate.getText_byXpath(rftemplate.id1))
        channel1 = str(rftemplate.getText_byXpath(rftemplate.channel1))
        id2 = str(rftemplate.getText_byXpath(rftemplate.id2))
        channel2 = str(rftemplate.getText_byXpath(rftemplate.channel2))
        id3 = str(rftemplate.getText_byXpath(rftemplate.id3))
        channel3 = str(rftemplate.getText_byXpath(rftemplate.channel3))
        #默认射频模板信道改为 “不下发”
        # self.assertEqual(id1,'1',msg='id1 不为1')
        # self.assertEqual(channel1, '1', msg='模板1信道 不为1')
        # self.assertEqual(id2, '2', msg='id1 不为2')
        # self.assertEqual(channel2, '6', msg='模板2信道 不为6')
        # self.assertEqual(id3, '3', msg='id1 不为3')
        # self.assertEqual(channel3, '11', msg='模板3信道 不为11')
        if channel1 != '1':
            rftemplate.click_edit1()
            time.sleep(1)
            channel = rftemplate.selelement_byName(rftemplate.channel)
            Select(channel).select_by_value('1')
            time.sleep(0.2)
            channel_5 = rftemplate.selelement_byName(rftemplate.channel_5)
            Select(channel_5).select_by_value('0')
            time.sleep(0.2)
            rftemplate.click_save()
            time.sleep(1)
        if channel2 != '6':
            rftemplate.click_edit2()
            time.sleep(1)
            channel = rftemplate.selelement_byName(rftemplate.channel)
            Select(channel).select_by_value('6')
            time.sleep(0.2)
            channel_5 = rftemplate.selelement_byName(rftemplate.channel_5)
            Select(channel_5).select_by_value('0')
            time.sleep(0.2)
            rftemplate.click_save()
            time.sleep(1)
        if channel3 != '11':
            rftemplate.click_edit3()
            time.sleep(1)
            channel = rftemplate.selelement_byName(rftemplate.channel)
            Select(channel).select_by_value('11')
            time.sleep(0.2)
            channel_5 = rftemplate.selelement_byName(rftemplate.channel_5)
            Select(channel_5).select_by_value('0')
            time.sleep(0.2)
            rftemplate.click_save()
            time.sleep(1)

        list_nodata4 = str(rftemplate.getText_byXpath(rftemplate.list_nodata4))
        self.assertEqual(list_nodata4, ' ', msg='模板列表中第四行不为空')
        print('默认模板3个 验证通过')

        #创建模板4关闭 2.4和5G无线接口
        rftemplate.click_addModal()
        time.sleep(1)
        rftemplate.input_name('4')
        rftemplate.click_C_wireless()
        rftemplate.click_C_wireless5()
        mode2 = rftemplate.selelement_byName(rftemplate.mode)
        Select(mode2).select_by_value('1') #2.4G 仅11g
        time.sleep(0.5)
        mode5 = rftemplate.selelement_byName(rftemplate.mode_5)
        Select(mode5).select_by_value('4')  # 5G 仅11a
        time.sleep(0.5)
        rftemplate.click_save()
        time.sleep(1)
        # 创建模板5 2.4G:仅11g 20M 5G:仅11a 20M
        rftemplate.click_addModal()
        time.sleep(1)
        rftemplate.input_name('5')
        mode2=rftemplate.selelement_byName(rftemplate.mode)
        Select(mode2).select_by_value('1') #仅11g
        time.sleep(0.2)
        channel = rftemplate.selelement_byName(rftemplate.channel)
        Select(channel).select_by_value('7')
        time.sleep(0.2)
        BW_2 = rftemplate.selelement_byName(rftemplate.BW)
        Select(BW_2).select_by_value('0') #20M
        time.sleep(0.2)
        rate = rftemplate.selelement_byName(rftemplate.rate) #2.4G无线速率
        Select(rate).select_by_value('54')
        time.sleep(0.2)
        mode_5 = rftemplate.selelement_byName(rftemplate.mode_5)
        Select(mode_5).select_by_value('4') #仅11a
        time.sleep(0.2)
        channel_5 = rftemplate.selelement_byName(rftemplate.channel_5)
        Select(channel_5).select_by_value('48')
        time.sleep(0.2)
        BW_5 = rftemplate.selelement_byName(rftemplate.BW_5)
        Select(BW_5).select_by_value('0') #20M
        time.sleep(0.2)
        rftemplate.click_save()
        time.sleep(1)
        #循环创建第6-12个模板
        i = 5
        while i < 13 :
            i +=1
            if i <13:
                rftemplate.click_addModal()
                time.sleep(1)
                rftemplate.input_name(i)
                time.sleep(0.5)
                rftemplate.click_save()
                time.sleep(1)
            else:
                rftemplate.click_addModal()
                time.sleep(1)
                rftemplate.input_name(i)
                time.sleep(0.5)
                rftemplate.click_save()
                time.sleep(0.5)
                list_tips = str(self.driver.find_element_by_class_name('tips-show-in').text)
                self.assertIn(reachMax2A ,list_tips, msg='，模板超过12提示信息有误')
                print('最大模板12 个验证通过')

        self.driver.quit()
        logger.info('test_001_maxNumTemplate passed')

    def test_002_delete(self):
        u'''模板添加删除'''
        rftemplate = RftemplatePage(self.driver, self.url)
        # 删除模板 第二页全选删除（第11、12条）
        rftemplate.click_next()
        time.sleep(1)
        rftemplate.click_selall()
        time.sleep(0.5)
        rftemplate.click_allDelete()
        time.sleep(1)
        rftemplate.click_ok()
        time.sleep(1)
        # 断言 删除后 没有第二页 列表剩下10条
        rftemplate.click_next()
        time.sleep(0.5)
        list_num = str(rftemplate.getText_byXpath(rftemplate.list_num10))
        self.assertEqual(list_num, '10', msg='模板删除失败')
        self.driver.quit()
        logger.info('test_002_delete passed')

    def test_003_interface(self):
        u'''启用、禁用无线接口'''
        OnlineA = getAssertText('OnlineA')
        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_Priorityv2()
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
            raise Exception('AP  未能同步2.4G无线接口')

        # v2协议列表中的操作（排序后第一行）
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(3)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        time.sleep(0.5)
        Select(spmb).select_by_value('4') #第4个模板关闭2.4/5G接口
        time.sleep(0.5)
        device.click_save()
        time.sleep(17)
        device.click_tab_modal() # 关闭弹窗
        time.sleep(1)
        x = 0
        while x < 20:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            if list_status1 == OnlineA :
                print('v2 AP在线', x)
                channel2 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel5 =str(device.getAttribute_byXpath(device.list_channel51, 'data-local'))
                if channel2 == '' and channel5 == '':
                    print('v2 AP1模板禁用接口生效', x)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            x = x + 1
        else:
            raise Exception('v2 AP1模板禁用接口 出错')
        # v1协议列表中的操作（排序后第4行）
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(3)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        time.sleep(0.5)
        Select(spmb).select_by_value('4')  # 第4个模板关闭2.4/5G接口
        time.sleep(0.5)
        device.click_save()
        time.sleep(17)
        device.click_tab_modal()  # 关闭弹窗
        time.sleep(1)
        i = 0
        while i < 20:
            device.click_refreshtable()
            time.sleep(1)
            list_status4 = device.getText_byXpath(device.list_status4)
            if list_status4 == OnlineA:
                print('v1 AP在线', x)
                channel2 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
                # channel5 = str(device.getAttribute_byXpath(device.list_channel54, 'data-local'))
                if channel2 == '':
                    print('v1 AP2模板禁用接口生效', i)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            i = i + 1
        else:
            raise Exception('v1 AP2模板禁用接口 出错')
        #启用接口
        # v2协议列表中的操作（排序后第一行）
        device.click_list_sel1()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(3)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        time.sleep(0.5)
        Select(spmb).select_by_value('5')  # 第5个模板
        time.sleep(0.5)
        device.click_save()
        time.sleep(17)
        device.click_tab_modal()  # 关闭弹窗
        time.sleep(1)
        x = 0
        while x < 20:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            if list_status1 == OnlineA:
                print('v2 AP在线', x)
                channel2 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel5 = str(device.getAttribute_byXpath(device.list_channel51, 'data-local'))
                if channel2 == '7' and channel5 == '48':
                    print('v2 AP1模板启用接口生效', x)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            x = x + 1
        else:
            raise Exception('v2 AP1模板启用接口 出错')
        # v1协议列表中的操作（排序后第四行）
        device.click_list_sel4()
        time.sleep(0.5)
        device.click_BatchManagement()
        time.sleep(3)
        spmb = device.selelement_byName(device.spmb)  # 射频设置
        time.sleep(0.5)
        Select(spmb).select_by_value('5')  # 第4个模板关闭2.4/5G接口
        time.sleep(0.5)
        device.click_save()
        time.sleep(17)
        device.click_tab_modal()  # 关闭弹窗
        time.sleep(1)
        i = 0
        while i < 20:
            device.click_refreshtable()
            time.sleep(1)
            list_status4 = device.getText_byXpath(device.list_status4)
            if list_status4 == OnlineA:
                print('v1 AP在线', i)
                channel2 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
                # channel5 = str(device.getAttribute_byXpath(device.list_channel54, 'data-local'))
                if channel2 == '7':
                    print('v1 AP2模板启用接口生效', i)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            i = i + 1
        else:
            raise Exception('v1 AP2模板启用接口 出错')

        self.driver.quit()
        logger.info('test_003_interface passed')

    def test_004_wifiMode(self):
        u'''无线模式、信道、带宽、无限速率'''
        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        # 点击管理通讯协议，v2在上
        device.click_Priorityv2()
        time.sleep(1)
        #003中v2 AP1 V1 AP1已经引用配置过的模板5，这里仅需要验证是否生效
        # v2协议列表中的操作（排序后第一行）
        channel2_v2 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
        mode2_v2 = str(device.getText_byXpath(device.list_2mode1))
        channel5_v2 = str(device.getAttribute_byXpath(device.list_channel51, 'data-local'))
        mode5_v2 = str(device.getText_byXpath(device.list_5mode1))
        self.assertEqual(channel2_v2,'7',msg='v2 AP1 2.4G信道不符')
        self.assertEqual(mode2_v2, '11g', msg='v2 AP1 2.4G模式不符')
        self.assertEqual(channel5_v2, '48', msg='v2 AP1 5G信道不符')
        self.assertEqual(mode5_v2, '11a', msg='v2 AP1 5G模式不符')
        V2_AP1IP=str(device.getText_byXpath(device.list_IP1))
        print(V2_AP1IP)
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=V2_AP1IP, port = port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwconfig ra0' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "Channel=7" and 'Bit Rate=54 Mb/s' in result:
            print('v2 AP1 2.4G信道、无线速率验证通过')
        else:
            raise Exception('v2 AP1 2.4G信道、无线速率 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2_AP1IP, port='60023',timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwconfig rai0' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "Channel=48"in result:
            print('v2 AP1 5G信道验证通过')
        else:
            raise Exception('v2 AP1 5G信道 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2_AP1IP, port='60023',timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep HT_BW' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "HT_BW=0" in result:
            print('v2 AP1 2.4G频道带宽验证通过')
        else:
            raise Exception('v2 AP1 2.4G频道带宽 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V2_AP1IP, port='60023',timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat  | grep HT_BW ' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "HT_BW=0" in result:
            print('v2 AP1 5G频道带宽验证通过')
        else:
            raise Exception('v2 AP1 5G频道带宽 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        # v1协议列表中的操作（排序后第4行）
        channel2_v1 = str(device.getAttribute_byXpath(device.list_channel4,'data-local'))
        mode2_v1 = str(device.getText_byXpath(device.list_2mode4))
        # channel5_v1 = str(device.getAttribute_byXpath(device.list_channel54,'data-local'))
        # mode5_v1 = str(device.getText_byXpath(device.list_5mode4))
        self.assertEqual(channel2_v1, '7', msg='v2 AP1 2.4G信道不符')
        self.assertEqual(mode2_v1, '11g', msg='v2 AP1 2.4G模式不符')
        # self.assertEqual(channel5_v1, '48', msg='v2 AP1 5G信道不符')
        # self.assertEqual(mode5_v1, '11a', msg='v2 AP1 5G模式不符')
        V1_AP1IP = str(device.getText_byXpath(device.list_IP4))
        print(V1_AP1IP)
        username = b'admin'
        password = b'admin'
        tn = telnetlib.Telnet(host=V1_AP1IP, port='60023',timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwconfig ra0' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "Channel=7" and 'Bit Rate=54 Mb/s' in result:
            print('v1 AP1 2.4G信道、无线速率验证通过')
        else:
            raise Exception('v1 AP1 2.4G信道、无线速率 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        # tn = telnetlib.Telnet(host=V1_AP1IP, port='60023',timeout=10)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'iwconfig rai0' + b'\n')
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 判断
        # if "Channel=48" and 'Bit Rate=54 Mb/s' in result:
        #     print('v1 AP1 5G信道、无线速率验证通过')
        # else:
        #     raise Exception('v1 AP1 5G信道、无线速率 异常')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')
        tn = telnetlib.Telnet(host=V1_AP1IP, port='60023')
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat /etc/Wireless/RT2860/RT2860.dat | grep HT_BW' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "HT_BW=0" in result:
            print('v1 AP1 2.4G频道带宽验证通过')
        else:
            raise Exception('v1 AP1 2.4G频道带宽 异常')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        # tn = telnetlib.Telnet(host=V2_AP1IP, port='60023')
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'cat /etc/Wireless/iNIC/iNIC_ap.dat  | grep HT_BW ' + b'\n')
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 判断
        # if "HT_BW=0" in result:
        #     print('v2 AP1 5G频道带宽验证通过')
        # else:
        #     raise Exception('v2 AP1 5G频道带宽 异常')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_004_wifiMode passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
