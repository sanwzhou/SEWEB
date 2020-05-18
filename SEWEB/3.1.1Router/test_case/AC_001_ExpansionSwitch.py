#! -*-conding:utf-8 -*-
#@Time: 2019/1/25 0025 14:58
#@swzhou
'''
无线拓展 、兼容模式 开关
'''

import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet,getweb
from common.loginRoute import login
from pages.AC_001_NetNamePage import netNamePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
logger = LogGen(Logger = 'AC_001_ExpansionSwitch').getlog()


class ExpansionSwitch(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        netname = netNamePage(self.driver,self.url)
        #进入无线扩展
        try:
            netname.click_wirelessExtension()
            time.sleep(0.5)
        except AttributeError:
            raise Exception(u'软件不支持无线扩展')
        # pass

    def test_001_information(self):
        u'''默认关闭，网络名称、设备管理页面提示正确'''
        wirelessTipsA = getAssertText('wirelessTipsA')

        netname = netNamePage(self.driver, self.url)
        #网络名称页面的提示
        netname.click_netName()
        time.sleep(1)
        boxtips=netname.getText_byClass(netname.u_cfm_boxT)
        if wirelessTipsA not in boxtips:
            CapPic(self.driver)
            logger.info(u'网络名称页面 无线扩展提示有误')
            raise Exception('网络名称页面 无线扩展提示有误')
        netname.click_u_cfm_nox() #提示窗右上角×号
        time.sleep(1)

        #确认按钮默认关闭
        checkOpens = netname.getAttribute_byId(netname.checkOpens,'checktype')
        self.assertEqual(checkOpens,'0',msg='无限扩展默认未关闭')#0关闭，1打开

        # 设备管理页面的提示
        device = deviceMgmtPage(self.driver,self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        boxtips = netname.getText_byClass(netname.u_cfm_boxT)
        if wirelessTipsA not in boxtips:
            CapPic(self.driver)
            logger.info(u'设备管理页面 无线扩展提示有误')
            raise Exception('设备管理页面 无线扩展提示有误')
        device.click_no() #取消按钮
        time.sleep(1)
        self.driver.quit()

        logger.info('test_001_information passed')

    def test_002_ExpansionSW(self):
        u'''开启、关闭 无线扩展 正常'''
        nodata = getAssertText('nodata')
        OnlineA = getAssertText('OnlineA')
        OfflineA = getAssertText('OfflineA')

        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        device.click_no()  # 取消按钮
        time.sleep(1)
        list_nodata = device.getText_byXpath(device.list_nodata)
        self.assertEqual(list_nodata,nodata,msg='未开启开关 设备管理列表显示有误')

        netname = netNamePage(self.driver, self.url)
        netname.click_netName()
        time.sleep(1)
        netname.click_ok() # 点确认开启
        time.sleep(1)
        checkOpens = netname.getAttribute_byId(netname.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '1', msg='无线扩展默认未打开')  # 0关闭，1打开
        #发现AP
        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(15)
        device.click_refreshtable()
        time.sleep(1)
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_state1 = device.getText_byXpath(device.list_state1)
            if str(list_state1) == OnlineA or OfflineA:
                print('扩展开启 验证通过')
                break
            else:
                time.sleep(3)
                x = x + 1
        else:
            raise Exception('扩展打开 未发现AP上线')

        #关闭无线拓展
        netname = netNamePage(self.driver, self.url)
        netname.click_netName()
        time.sleep(1)
        netname.click_checkOpen()
        time.sleep(1)
        # 断言 开关关闭
        checkOpens = netname.getAttribute_byId(netname.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '0', msg='无线扩展默认未关闭')  # 0关闭，1打开
        # AP列表为空
        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        list_nodata = device.getText_byXpath(device.list_nodata)
        self.assertEqual(list_nodata, nodata, msg='关闭开关 列表显示有误')
        print('扩展关闭 验证通过')

        #再打开无线扩展
        netname.click_ok()  # 点确认开启
        time.sleep(1)
        self.driver.quit()
        logger.info('test_002_ExpansionSW passed')

    def test_003_ProtocolSW(self):
        u'''开启、关闭 兼容模式 '''
        netname = netNamePage(self.driver, self.url)
        netname.click_netName()
        time.sleep(1)
        # 兼容模式 默认关闭
        ManageProtocol = netname.getAttribute_byId(netname.ManageProtocolss,'checktype')
        self.assertEqual(ManageProtocol, '0', msg='兼容模式未关闭')  # 0关闭，1打开
        # 打开兼容模式
        netname.click_ManageProtocols()
        time.sleep(5)
        ManageProtocol = netname.getAttribute_byId(netname.ManageProtocolss, 'checktype')
        self.assertEqual(ManageProtocol, '1', msg='兼容模式未打开')  # 0关闭，1打开
        # 确认打开后有acd进程
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ps | grep -v grep |grep acd' + b'\n')  # SSID加密密码
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "/sbin/acd_guard.sh " in result:
            print('acd进程存在')
        else:
            raise Exception('打开兼容模式后 acd进程未存在')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        #关闭兼容模式
        netname.click_ManageProtocols()
        time.sleep(2)
        ManageProtocol = netname.getAttribute_byId(netname.ManageProtocolss, 'checktype')
        self.assertEqual(ManageProtocol, '0', msg='兼容模式未关闭')  # 0关闭，1打开
        # 确认关闭后没有acd进程
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ps | grep -v grep |grep acd' + b'\n')  # SSID加密密码
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "/sbin/acd_guard.sh " not in result:
            print('acd进程不存在')
        else:
            raise Exception('关闭兼容模式后 acd进程依旧存在')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        # 再打开兼容模式
        netname.click_ManageProtocols()
        time.sleep(2)
        ManageProtocol = netname.getAttribute_byId(netname.ManageProtocolss, 'checktype')
        self.assertEqual(ManageProtocol, '1', msg='兼容模式未打开')  # 0关闭，1打开

        self.driver.quit()
        logger.info('test_003_ProtocolSW passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' %('=' * 50))

if __name__=='__main__':
    unittest.main()