#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 16:55
#@swzhou
'''
配置静态路由，能在命令行查看到相关路由
静态路由可绑定PPTP/L2TP接口
'''

import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb,getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from common.loginRoute import login
from pages.NetConfig_005_RouteConfigPage import RouteConfigPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'NetworkConfig_005_StaticRoute').getlog()

class staticRoute(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_staticRouting(self):
        u'''配置静态路由，能在命令行查看到相关路由'''
        ConnectState = getAssertText('ConnectState')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 ip变量赋值，页面读取
        # 判断联网状态
        i = 0
        while i < 21:
            wanpage.click_refresh()
            time.sleep(1)
            list_conState = wanpage.getText_byXpath(wanpage.connectState1)
            print(str(list_conState), i)
            if str(list_conState) != ConnectState:
                time.sleep(3)
                i += 1
            else:
                break
        else:
            CapPic(self.driver)
            logger.info(u"WAN口未连接")
            raise Exception('WAN1 未连接')
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)

        # 添加静态路由
        routeconfig = RouteConfigPage(self.driver, self.url)
        routeconfig.click_Routeconfig()
        time.sleep(1)
        routeconfig.click_add()
        time.sleep(1)
        routeconfig.input_RouteNames('static')
        routeconfig.input_DesIPs('223.5.5.5')
        routeconfig.input_DesMasks('255.255.255.255')
        routeconfig.input_GateWays(WAN1_ip)
        routeconfig.click_save()
        time.sleep(5)
        #断言
        list_dst = str(routeconfig.getText_byXpath(routeconfig.list_dst))
        self.assertEqual(list_dst , '223.5.5.5', msg='目的网络不为"223.5.5.5"')
        self.driver.quit()

        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ip route show tab 120' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "223.5.5.5" in result:
            print('命令行可以看到配置路由')
        else:
            raise Exception('命令行未看到路由')  # 如果没有则报错

        tn.close()  # tn.write('exit\n')
        logger.info('test_001_staticRouting passed')

    def test_002_bindingVPNinterface(self):
        u'''静态路由可绑定PPTP/L2TP接口'''
        nodata = getAssertText('nodata')
        bandingVPNp = getParameter('bandingVPNp')
        Support = getExcelValue(bandingVPNp)

        if Support == '√':
            logger.info(u'参数支持静态路由可绑定PPTP/L2TP接口')
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            pptpl2tp = pptpL2tpPage(self.driver,self.url)
            # 配置PPTP VPN
            pptpl2tp.click_VPNConfig()
            time.sleep(0.5)
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            pptpl2tp.click_add()
            time.sleep(1)
            pptpl2tp.input_TunNames('staticRoute')
            pptpl2tp.input_userNames('staticRoute')
            pptpl2tp.input_password('staticRoute')
            pptpl2tp.input_remoteInIp('1.2.3.4')
            pptpl2tp.input_remoteInIPMask('255.255.255.0')
            pptpl2tp.click_save()
            time.sleep(3)
            # 断言
            listtips1 = str(pptpl2tp.getText_byXpath(pptpl2tp.listtips1))
            self.assertEqual(listtips1, 'staticRoute', msg='VPN名称不为staticRoute')
            print('PPTP已添加')
            # 配置L2TP VPN
            pptpl2tp.click_add()
            time.sleep(1)
            pptpl2tp.click_l2tpB()
            pptpl2tp.input_TunNames('staticRoute2')
            pptpl2tp.input_userNames('staticRoute2')
            pptpl2tp.input_password('staticRoute2')
            pptpl2tp.input_remoteInIp('4.3.2.1')
            pptpl2tp.input_remoteInIPMask('255.255.255.0')
            pptpl2tp.click_save()
            time.sleep(3)
            # 断言
            listtips2 = str(pptpl2tp.getText_byXpath(pptpl2tp.listtips2))
            self.assertEqual(listtips2, 'staticRoute2', msg='VPN名称不为staticRoute2')
            print('L2TP已添加')

            # 修改静态路由 绑定PPTP接口
            routeconfig = RouteConfigPage(self.driver, self.url)
            routeconfig.click_NetworkConfig()
            time.sleep(0.5)
            routeconfig.click_Routeconfig()
            time.sleep(1)
            routeconfig.click_edit()
            time.sleep(1)
            se1Profiles = routeconfig.selelement_byName('Profiles')
            time.sleep(1)
            Select(se1Profiles).select_by_value('(PPTPS)staticRoute')
            time.sleep(1)
            routeconfig.click_save()
            time.sleep(3)
            #断言
            interface = str(routeconfig.getText_byXpath(routeconfig.list_Interface))
            self.assertEqual(interface , '(PPTPS)staticRoute', msg='绑定接口不为VPN接口')
            print('静态路由绑定PPTP接口 验证通过')

            # 修改静态路由 绑定L2TP接口
            routeconfig.click_edit()
            time.sleep(1)
            se1Profiles = routeconfig.selelement_byName('Profiles')
            time.sleep(1)
            Select(se1Profiles).select_by_value('(L2TPS)staticRoute2')
            time.sleep(1)
            routeconfig.click_save()
            time.sleep(3)
            # 断言
            interface = str(routeconfig.getText_byXpath(routeconfig.list_Interface))
            self.assertEqual(interface, '(L2TPS)staticRoute2', msg='绑定接口不为VPN接口')
            print('静态路由绑定L2TP接口 验证通过')

            #删除静态路由
            routeconfig.click_delete()
            time.sleep(1)
            routeconfig.click_ok()
            time.sleep(2)
            # 断言
            list_tips = str(routeconfig.getText_byXpath(routeconfig.list_nodata))
            self.assertEqual(list_tips, nodata, msg='静态路由删除失败')
            print('静态路由已删除')
            #删除两条VPN
            pptpl2tp = pptpL2tpPage(self.driver, self.url)
            pptpl2tp.click_VPNConfig()
            time.sleep(0.5)
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            pptpl2tp.click_delete1()
            time.sleep(1)
            pptpl2tp.click_ok()
            time.sleep(2)
            pptpl2tp.click_delete1()
            time.sleep(1)
            pptpl2tp.click_ok()
            time.sleep(3)
            # 断言
            list_nodata = str(pptpl2tp.getText_byXpath(pptpl2tp.list_nodata))
            self.assertEqual(list_nodata, nodata, msg='静态路由删除失败')
            print('VPN已删除')
            self.driver.quit()
        elif Support == '×':
            logger.info(u'参数不支持静态路由可绑定PPTP/L2TP接口')
        logger.info('test_002_bindingVPNinterface passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

