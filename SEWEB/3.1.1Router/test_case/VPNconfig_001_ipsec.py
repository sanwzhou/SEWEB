#! -*-conding:utf-8 -*-
#@Time: 2019/3/12 0012 10:02
#@swzhou
'''
ipsec VPN
'''

import os
import socket
import time
import unittest
import subprocess
from common.LogGen import LogGen
from selenium.common.exceptions import NoSuchElementException
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,getweb,gettelnet
from common.loginRoute import login
from pages.VPNconfig_IPsecPage import IPsecPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from common.organization_edit import organization_group
logger = LogGen(Logger = 'VPNconfig_001_ipsec').getlog()
vpnRouteWan = getweb('vpnRouteWan')
vpnRouteUrl = 'http://' + vpnRouteWan + ':8081'
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
ConnectState = getAssertText('ConnectState')

class ipsec(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_ipsec(self):
        u'''ipsec VPN'''
        vpnRouteLan = getweb('vpnRouteLan')
        host = gettelnet('host')
        StateVPN1 = getAssertText('StateVPN1')
        WillReboottips = getAssertText('WillReboottips')

        #先判断是否可以上网
        p = pingTestIP()
        if p == 'N':
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
            time.sleep(5)
            n = 0
            while n < 30:
                pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr, n)
                if '192.168.' not in str(pcaddr):
                    time.sleep(2)
                    n += 1
                else:
                    print('IP地址已自动获取成功', n)
                    break
            else:
                raise Exception('未获取到地址')
            # 删除绑定绑定 清空组
            organization_group.group_delete(self)

        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        ipsec = IPsecPage(self.driver,self.url)
        ipsec.click_VPNConfig()
        time.sleep(0.5)
        ipsec.click_IPSec()
        time.sleep(1)
        # 操作删除 以访已有规则
        ipsec.click_selall()
        time.sleep(0.2)
        ipsec.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            ipsec.find_ok()
        except NoSuchElementException:
            try:
                ipsec.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('ipsec VPN列表为空')

        ipsec.click_add()
        time.sleep(1)
        ipsec.input_ids('test')
        ipsec.input_peer(vpnRouteWan)
        ipsec.input_remoteAddr(vpnRouteLan)
        # ipsec.input_remoteMask('255.255.255.0')
        ipsec.input_preshareKey('12345678')
        ipsec.click_save()
        time.sleep(2)
        try: #无线设备增加ac功能后 配置第一条ipsec时会提示重启
            ipsec.find_ok()
        except NoSuchElementException:
            pass
        else:
            time.sleep(2)
            tips = str(ipsec.getText_byClass(ipsec.u_tim_str))
            self.assertEqual(tips, WillReboottips, msg='点击提示重启 操作失败')
            # 设备重启时间不一致，做个判断
            time.sleep(30)
            i = 0
            while i < 20:
                now_url = str(self.driver.current_url)
                # print(now_url,i)
                if '/noAuth/login.html' not in now_url:  # 如果不同
                    time.sleep(5)
                else:
                    break
                i += 1
            else:
                raise Exception('设备重启未正常启动')
            self.driver.quit()
            login.loginWeb(self)

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)

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
        i = 0
        while i < 21:
            # 判断联网 ，不能上网则报错
            p = pingTestIP('www.baidu.com')
            print(p, i)
            if p == 'N':
                time.sleep(3)
                i +=1
            else:
                break
        else:
            logger.info(u"connect failed")
            raise Exception('connect failed.')

        # WAN1 ip变量赋值，页面读取
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        # print('WAN1_ip=',WAN1_ip)
        time.sleep(1)
        self.driver.quit()

        # 另外一台路由器 配置ipsec
        i = 0 #以访刚重启wan口还不通
        while i < 60:
            pingTestIP(vpnRouteWan)
            if p == 'N' :
                time.sleep(1)
                i += 1
            else:
                break
        else:
            raise Exception(u'无法ping通vpnRoute')
        # time.sleep(5)
        login.test_enableLoginWeb(self,url= vpnRouteUrl)
        ipsec = IPsecPage(self.driver, self.url)
        ipsec.click_VPNConfig()
        time.sleep(0.5)
        ipsec.click_IPSec()
        time.sleep(1)
        # 操作删除 以访已有规则
        ipsec.click_selall()
        time.sleep(0.2)
        ipsec.click_delall()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            ipsec.find_ok()
        except NoSuchElementException:
            try:
                ipsec.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('ipsec VPN列表为空')

        ipsec.click_add()
        time.sleep(1)
        ipsec.input_ids('test')
        ipsec.input_peer(WAN1_ip)
        ipsec.input_remoteAddr(host)
        # ipsec.input_remoteMask('255.255.255.0')
        ipsec.input_preshareKey('12345678')
        ipsec.click_save()
        time.sleep(2)

        i = 0
        while i < 100:
            ipsec.click_IPSec()
            time.sleep(1)
            list_status = ipsec.getText_byXpath(ipsec.list_status)
            print(list_status)
            if list_status == StateVPN1 :
                logger.info(u'ipsec 已建立')
                break
            else:
                time.sleep(3)
                i += 1
        else:
            logger.info(u'ipsec 未建立成功')
            CapPic(self.driver)
            raise Exception(u'ipsec未建立成功')

        self.driver.quit()
        logger.info('test_001_ipsec passed')

    def tearDown(self):

        nodata = getAssertText('nodata')
        #删除ipsec
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        ipsec = IPsecPage(self.driver, self.url)
        ipsec.click_VPNConfig()
        time.sleep(0.5)
        ipsec.click_IPSec()
        time.sleep(1)
        ipsec.click_selall()
        time.sleep(0.2)
        ipsec.click_delall()
        time.sleep(1)
        ipsec.click_ok()
        time.sleep(2)
        list_nodata = ipsec.getText_byXpath(ipsec.list_nodata)
        if list_nodata == nodata:
            logger.info(u'R1 ipsec 已删除')
        else:
            CapPic(self.driver)
            logger.info(u'R1 ipsec删除失败')
            raise Exception(u'R1 ipsec删除失败')
        self.driver.quit()
        login.test_enableLoginWeb(self,url = vpnRouteUrl)
        ipsec = IPsecPage(self.driver, self.url)
        ipsec.click_VPNConfig()
        time.sleep(0.5)
        ipsec.click_IPSec()
        time.sleep(1)
        ipsec.click_selall()
        time.sleep(0.2)
        ipsec.click_delall()
        time.sleep(1)
        ipsec.click_ok()
        time.sleep(2)
        try: #VPN 路由器是中文简体，在测试其他语言版本时，删除的nodata会不一致
            ipsec.find_list_nodataX()
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'R2 ipsec删除失败')
            raise Exception(u'R2 ipsec删除失败')
        else:
            logger.info(u'R2 ipsec 已删除')

        # list_nodata = ipsec.getText_byXpath(ipsec.list_nodata)
        # if list_nodata == nodata:
        #     logger.info(u'R2 ipsec 已删除')
        # else:
        #     CapPic(self.driver)
        #     logger.info(u'R2 ipsec删除失败')
        #     raise Exception(u'R2 ipsec删除失败')

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
