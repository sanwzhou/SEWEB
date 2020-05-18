#! -*-conding:utf-8 -*-
#@Time: 2019/9/5 0005 16:43
#@swzhou
'''
云AC 路由器
'''

import time
import unittest
import telnetlib
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet,getweb
from common.loginRoute import login
from common.loginYun import loginYun
from pages.sysConfig_007_CloudServePage import CloudServePage
from pages.LoginYunPage import LoginYunPage
from pages.AC_003_RftemplatePage import RftemplatePage
from pages.SysMonitor_001_sysStaticPage import sysStaticPage
from test_case.AC_003_netName import netName
from test_case.AC_004_Rftemplate import Rftemplate
logger = LogGen(Logger = 'cloud_001_basic').getlog()

class cloud(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_information(self):
        u'''导入上线、解绑'''
        OnlineA = getAssertText('OnlineA')
        nodata = getAssertText('nodata')
        OfflineA = getAssertText('OfflineA')

        #1、导入上线
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        cloudServe = CloudServePage(self.driver,self.url)
        cloudServe.click_sysConfig()
        time.sleep(0.5)
        cloudServe.click_CloudServe()
        time.sleep(1)
        enable = cloudServe.getAttribute_byXpath(cloudServe.cloudEns,'checked')
        # print(enable)
        if enable == None:
            # print('123')
            cloudServe.click_cloudEn()
            cloudServe.click_save()
            time.sleep(1)
        webSN = cloudServe.getText_byXpath(cloudServe.webSN)
        code = cloudServe.getText_byXpath(cloudServe.code)
        self.driver.quit()

        loginYun.loginYunWeb(self)
        self.driver.implicitly_wait(10)
        loginyun = LoginYunPage(self.driver, self.url)
        loginyun.click_device()
        time.sleep(1)
        loginyun.click_Import()
        time.sleep(1)
        loginyun.click_Bureau()
        time.sleep(0.5)
        loginyun.click_treeEdit_1_switch()
        time.sleep(0.5)
        loginyun.click_treeEdit_2_check()
        time.sleep(0.5)
        loginyun.click_groupBg()
        time.sleep(0.5)
        sel = loginyun.selelement_byName(loginyun.selImportMode)
        Select(sel).select_by_value('1')
        loginyun.input_deviceName(webSN)
        loginyun.input_SN(webSN)
        loginyun.input_jhm(code)
        loginyun.click_confirm()
        time.sleep(1)
        tips = loginyun.getText_byName(loginyun.errorMsg)
        if tips == '绑定成功':
            logger.info('导入设备验证通过')
        else:
            CapPic(self.driver)
            logger.info('导入设备 异常')
            raise Exception(u'导入设备 异常')
        loginyun.click_tipClose()
        time.sleep(0.5)
        #判断上线
        loginyun.input_search(webSN)
        loginyun.click_glyphicon_search()
        time.sleep(1)
        i = 0
        while i <30:
            loginyun.click_refurbish()
            time.sleep(0.5)
            state = loginyun.getText_byXpath(loginyun.state)
            if state == OnlineA:
                logger.info('设备已上线')
                break
            else:
                i +=1
        else:
            logger.info(u'设备未上线')
            CapPic(self.driver)
            raise Exception(u'设备未上线')

        #2、解绑
        loginyun.click_btns2()
        time.sleep(1)
        loginyun.click_cancel()
        time.sleep(2)
        list_nodata = loginyun.getText_byXpath(loginyun.list_nodata)
        if list_nodata == nodata:
            logger.info(u'解绑成功')
        else:
            logger.info(u'解绑未成功')
            CapPic(self.driver)
            raise Exception(u'解绑未成功')
        time.sleep(3)
        # --重新绑定
        loginyun.click_Import()
        time.sleep(1)
        loginyun.click_Bureau()
        time.sleep(0.5)
        loginyun.click_treeEdit_1_switch()
        time.sleep(0.5)
        loginyun.click_treeEdit_2_check()
        time.sleep(0.5)
        loginyun.click_groupBg()
        time.sleep(0.5)
        sel = loginyun.selelement_byName(loginyun.selImportMode)
        Select(sel).select_by_value('1')
        loginyun.input_deviceName(webSN)
        loginyun.input_SN(webSN)
        loginyun.input_jhm(code)
        loginyun.click_confirm()
        time.sleep(1)
        tips = loginyun.getText_byName(loginyun.errorMsg)
        if tips == '绑定成功':
            logger.info('导入设备验证通过')
        else:
            CapPic(self.driver)
            logger.info('导入设备 异常')
            raise Exception(u'导入设备 异常')
        loginyun.click_tipClose()
        time.sleep(0.5)
        # 重新绑定 判断上线
        loginyun.input_search(webSN)
        loginyun.click_glyphicon_search()
        time.sleep(1)
        i = 0
        while i < 30:
            loginyun.click_refurbish()
            time.sleep(0.5)
            state = loginyun.getText_byXpath(loginyun.state)
            if state == OnlineA:
                logger.info('重新绑定设备已上线')
                break
            else:
                i += 1
        else:
            logger.info(u'重新绑定设备未上线')
            CapPic(self.driver)
            raise Exception(u'重新绑定设备未上线')
        self.driver.quit()

        logger.info('test_001_information passed')

    def test_002_information(self):
        u'''信息显示、重启、远程管理、'''
        OnlineA = getAssertText('OnlineA')
        nodata = getAssertText('nodata')
        OfflineA = getAssertText('OfflineA')
        #3、路由器详情及管理
         #1）使设备离线
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        cloudServe = CloudServePage(self.driver, self.url)
        cloudServe.click_sysConfig()
        time.sleep(0.5)
        cloudServe.click_CloudServe()
        time.sleep(1)
        enable = cloudServe.getAttribute_byXpath(cloudServe.cloudEns, 'checked')
        # print(enable)
        if enable != None:
            cloudServe.click_cloudC()
            cloudServe.click_save()
            time.sleep(1)
        webSN = cloudServe.getText_byXpath(cloudServe.webSN)
        #本地显示系统信息
        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)
        # 系统负载 - 产品型号
        webmodel = sysstatic.getText_byXpath(sysstatic.Model)
        webhdmodel = sysstatic.getText_byXpath(sysstatic.hdmodel)
        websoftware = sysstatic.getText_byXpath(sysstatic.software)
        webSN2 = sysstatic.getText_byXpath(sysstatic.SN)

        #2)本地配置ssid及模板
        netName.test_001_ssidNum(self)
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        rftemplate = RftemplatePage(self.driver, self.url)
        rftemplate.click_wirelessExtension()
        time.sleep(0.5)
        rftemplate.click_rfTemplate()
        time.sleep(2)
        Rftemplate.test_001_maxNumTemplate(self)
        #3)离线设备不能进入设备详情页
        loginYun.loginYunWeb(self)
        self.driver.implicitly_wait(10)
        loginyun = LoginYunPage(self.driver, self.url)
        loginyun.click_device()
        time.sleep(1)
        # 判断离线
        loginyun.input_search(webSN)
        loginyun.click_glyphicon_search()
        time.sleep(1)
        i = 0
        while i < 30:
            loginyun.click_refurbish()
            time.sleep(0.5)
            state = loginyun.getText_byXpath(loginyun.state)
            if state == OfflineA:
                logger.info('设备已离线')
                break
            else:
                i += 1
        else:
            logger.info(u'设备未离线')
            CapPic(self.driver)
            raise Exception(u'设备未离线')
        try:
            loginyun.click_name()
        except AttributeError:
            logger.info(u'离线设备不能进入设备详情及管理页面')
        else:
            logger.info(u'离线设备依旧可以进入设备详情及管理页面')
            CapPic(self.driver)
            raise Exception(u'离线设备依旧可以进入设备详情及管理页面')
        self.driver.quit()
        #4）使设备上线，在线设备可以进入设备详情页
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        cloudServe = CloudServePage(self.driver, self.url)
        cloudServe.click_sysConfig()
        time.sleep(0.5)
        cloudServe.click_CloudServe()
        time.sleep(1)
        enable = cloudServe.getAttribute_byXpath(cloudServe.cloudEns, 'checked')
        # print(enable)
        if enable == None:
            # print('123')
            cloudServe.click_cloudEn()
            cloudServe.click_save()
            time.sleep(1)
        self.driver.quit()

        loginYun.loginYunWeb(self)
        self.driver.implicitly_wait(10)
        loginyun = LoginYunPage(self.driver, self.url)
        loginyun.click_device()
        time.sleep(1)
        # 判断上线
        loginyun.input_search(webSN)
        loginyun.click_glyphicon_search()
        time.sleep(1)
        i = 0
        while i < 30:
            loginyun.click_refurbish()
            time.sleep(0.5)
            state = loginyun.getText_byXpath(loginyun.state)
            if state == OnlineA:
                logger.info('设备已上线')
                break
            else:
                i += 1
        else:
            logger.info(u'设备未上线')
            CapPic(self.driver)
            raise Exception(u'设备未上线')
        loginyun.click_name()
        time.sleep(1)
        yunmodel = loginyun.getText_byXpath(loginyun.yunmodel)
        yunSN = loginyun.getText_byXpath(loginyun.yunSN)
        yunhdmodel = loginyun.getText_byXpath(loginyun.yunhdmodel)
        yunsoftware = loginyun.getText_byXpath(loginyun.yunsoftware)

        if yunmodel ==  webmodel:
            logger.info(u'设备型号显示一致')
        else:
            logger.info(u'设备型号显示不一致')
            CapPic(self.driver)
            raise Exception(u'设备型号显示不一致')
        if yunSN == webSN2:
            logger.info(u'序列号显示一致')
        else:
            logger.info(u'序列号显示不一致')
            CapPic(self.driver)
            raise Exception(u'序列号显示不一致')
        if yunhdmodel == webhdmodel:
            logger.info(u'硬件版本显示一致')
        else:
            logger.info(u'硬件版本显示不一致')
            CapPic(self.driver)
            raise Exception(u'硬件版本显示不一致')
        if yunsoftware == websoftware:
            logger.info(u'软件版本显示一致')
        else:
            logger.info(u'软件版本显示不一致')
            CapPic(self.driver)
            raise Exception(u'软件版本显示不一致')




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