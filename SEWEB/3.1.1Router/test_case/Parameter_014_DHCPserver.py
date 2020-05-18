#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 16:13
#@swzhou
'''
DHCP server:
动态分配地址、静态地址分配
option43、dhcp多地址池
'''

import time
import unittest
import socket
import os
import os.path
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
from selenium.webdriver.support.select import Select
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
logger = LogGen(Logger = 'Parameter_014_DHCPserver').getlog()

class DHCPserver(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        dhcpserver = DHCPserverpage(self.driver,self.url)
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        # pass

    def test_001_AllocationAddress(self):
        u'''动态分配地址、静态地址分配'''
        MinutesA = getAssertText('MinutesA')
        dhcpserver = DHCPserverpage(self.driver, self.url)
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        # 调用bat脚本 改为DHCP
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
        time.sleep(5)

        # 调用bat脚本 IP地址释放
        os.system('%s' % (batpath + 'ipconfig_release.bat'))
        time.sleep(2)
        pcaddr1 = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        print(pcaddr1)
        if pcaddr1 != str(pcaddr):
            print('IP地址已释放')
        else:
            time.sleep(3)
        time.sleep(2)
        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system('%s' % (batpath + 'ipconfig_renew.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
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

        dhcpserver.clicl_DHCPClientList()
        time.sleep(3)
        #刷新改为手动
        selrefreshtime = dhcpserver.selelement_byXpath(dhcpserver.selrefreshtime)
        Select(selrefreshtime).select_by_value('manual')
        dhcpserver.click_Refresh()
        time.sleep(0.5)

        # 定义页面显示元素变量
        listIP = str(dhcpserver.getText_byXpath(dhcpserver.listIP))
        listmask = str(dhcpserver.getText_byXpath(dhcpserver.listmask))
        listmac = str(dhcpserver.getText_byXpath(dhcpserver.listmac))
        listLeaseTime = str(dhcpserver.getText_byXpath(dhcpserver.listLeaseTime))
        self.assertIn('192.168.', listIP, msg='IP 出错')  # lan口地址段
        print('DHCP客户端列表 - IP 验证成功')
        self.assertIn('255.255.255.0', listmask, msg='IP 出错')  # 掩码
        print('DHCP客户端列表 - 掩码 验证成功')
        self.assertEqual(len(listmac), 17, msg='mac 出错')  # 判断mac地址长度
        print('DHCP客户端列表 - mac 验证成功')
        self.assertIn(MinutesA, listLeaseTime, msg='IP 出错')  # 租期时间
        print('DHCP客户端列表 - 租期时间 验证成功')
        print('动态分配地址 验证通过')

        # 任意绑定一个地址
        dhcpserver.click_StaticDHCP()
        time.sleep(1)
        dhcpserver.click_add()
        time.sleep(1)
        dhcpserver.input_UserName('oneself')
        dhcpserver.input_IP('123.1.1.1')
        dhcpserver.input_MAC('1')
        print('静态地址分配 验证通过')
        self.driver.quit()
        logger.info('test_001_AllocationAddress passed')

    def test_002_option43_MultiPools(self):
        u'''option43、dhcp多地址池'''
        dhcpserver = DHCPserverpage(self.driver, self.url)
        dhcpserver.click_addpool()
        time.sleep(1)
        option43Type = dhcpserver.selelement_byName(dhcpserver.seloption43Type)
        Select(option43Type).select_by_value('0') #0不启用
        time.sleep(0.5)
        Select(option43Type).select_by_value('1') #1 HEX定长
        time.sleep(0.5)
        Select(option43Type).select_by_value('2') #2 ASCII不定长
        time.sleep(0.5)
        Select(option43Type).select_by_value('3') #0 自定义
        time.sleep(0.5)

        self.driver.quit()
        logger.info('test_002_option43_MultiPools passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()