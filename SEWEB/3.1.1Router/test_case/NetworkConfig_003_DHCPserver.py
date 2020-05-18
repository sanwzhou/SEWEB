#! -*-conding:utf-8 -*-
#@Time: 2019/1/10 0010 19:18
#@swzhou
'''
DHCP 服务器
'''

import os
import time
import unittest
import os.path
import socket
import subprocess
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,getweb,gettelnet
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.NetConfig_003_DHCPserverpage import DHCPserverpage
logger = LogGen(Logger = 'NetworkConfig_003_DHCPserver').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
PcMac = getweb('PcMac')
batSameIP = getweb('batSameIP')
nodata = getAssertText('nodata')
saveSucess = getAssertText('saveSucess')


class dhcpServer(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_ServerStatus(self):
        u'''DHCP服务器功能默认开启'''
        host = gettelnet('host')

        #即插即用中修改了IP 这里加一个判断联网
        pingTestIP() #避免失误
        p = pingTestIP()
        if p == 'N':
            # 将IP改回自动获取（设置dns为自动获取）
            # 调用bat脚本
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
                    logger.info(u'IP地址已自动获取成功')
                    break
            else:
                raise Exception('未获取到地址')
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        logger.info(u'IP地址为：%s' % pcaddr)
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        dhcpserver = DHCPserverpage(self.driver, self.url)
        # 打开网络配置 - 内网配置
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        #确认 DHCP服务器功能 是否 默认开启
        dhcp_status=dhcpserver.getAttribute_byXpath(dhcpserver.dhcpEn,'checked')
        self.assertEqual(str(dhcp_status), 'true', msg='DHCP服务器功能默认未开启')
        self.driver.quit()
        logger.info('test_001_ServerStatus passed')

    def test_002_StaticList(self):
        u'''静态列表显示'''
        organization_group.import_empty_template(self)  # 判断组织架构是否有其他组 有则清空
        #新增一个组
        organization_group.group_add(self)
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        if pcaddr == batSameIP:
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
                    if pcaddr == batSameIP:
                        raise Exception(u'IP地址已经为1.39')
                    break
            else:
                raise Exception('未获取到地址')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        dhcpserver = DHCPserverpage(self.driver, self.url)
        # 打开网络配置 - DHCP服务
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        # 对当前PC 进行静态绑定
        dhcpserver.click_StaticDHCP()
        time.sleep(1)
        #新增（注意add会有多个元素被识别到 这里用绝对路径）
        dhcpserver.click_add()
        time.sleep(1)
        dhcpserver.input_UserName('oneself')
        dhcpserver.input_IP(pcaddr)
        dhcpserver.input_MAC(PcMac) #如更换PC 注意修改config.ini中mac地址
        dhcpserver.click_save()
        time.sleep(1)

        #静态列表显示变量赋值
        list_username = dhcpserver.getText_byXpath(dhcpserver.list_username)
        list_poolname = dhcpserver.getText_byXpath(dhcpserver.list_poolname)
        list_IP = dhcpserver.getText_byXpath(dhcpserver.list_IP)
        list_MAC = dhcpserver.getText_byXpath(dhcpserver.list_MAC)
        #断言 判断列表显示是否正常
        self.assertEqual(list_username,'oneself',msg='列表中用户名显示不一致')
        self.assertEqual(list_poolname,'default',msg='列表中 地址池名称 不为default') #默认地址池名称
        self.assertEqual(list_IP,pcaddr,msg='列表中IP地址 显示不一致')
        self.assertEqual(list_MAC,PcMac,msg='列表中MAC地址池显示不一致')
        self.driver.quit()
        logger.info('test_002_StaticList passed')

    def test_003_dhcpPool(self):
        u'''PC1 PC2 获取地址在地址池范围内'''
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr_old = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        # print(pcaddr_old)
        lastNum = pcaddr_old.split(r'.')[3]
        # print(lastNum)
        #判断IP是否在地址池范围内
        if 50 <int(lastNum) < 250 or len(pcaddr_old) ==11:
            print('获取地址在地址池范围内')
        else:
            raise Exception('获取地址不在地址池范围内')

        # 修改MAC为 另一个MAC地址
        # 调用bat脚本 MAC地址修改为 107B44AAAAAA
        os.system('%s' % (batpath + 'changeMac.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            # raise Exception('未获取到地址1')
            #  仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')
        if pcaddr_new == pcaddr_old:
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            n = 0
            while n < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, n)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    n += 1
                else:
                    print('IP地址已自动获取成功', n)
                    break
            else:
                raise Exception('未获取到地址2')

        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr4 = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        # print(pcaddr4)
        lastNum = pcaddr4.split(r'.')[3]
        # print(lastNum)

        if 50 < int(lastNum) < 250 or len(lastNum) ==11:
            print('获取地址在地址池范围内')
        else:
            raise Exception('获取地址不在地址池范围内')

        logger.info('test_003_dhcpPool passed')

    def test_004_releaseIP(self):
        u'''PC2释放IP，客户端列表显示正确'''
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))

        # 调用bat脚本 MAC地址释放
        os.system('%s' % (batpath + 'ipconfig_release.bat'))
        time.sleep(2)
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr1 = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        print(pcaddr1)
        if pcaddr1 != str(pcaddr):
            print('IP地址已释放')
        else:
            time.sleep(3)

        # 调用bat脚本 MAC地址修改回
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr2 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr2, n)
            if '192.168.' not in str(pcaddr2):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            # raise Exception('未获取到地址1')
            #  仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')

        #登陆页面查看DHCP客户端列表是否还有pc的ip
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        dhcpserver = DHCPserverpage(self.driver, self.url)
        # 打开网络配置 - 内网配置
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        dhcpserver.clicl_DHCPClientList()
        time.sleep(1)
        # #刷新时间改为手动
        # se1 = self.driver.find_element_by_xpath('//*[@id="btns"]/ul/li[1]/select')
        # time.sleep(1)
        # Select(se1).select_by_value('manual')
        # self.driver.find_element_by_xpath('//*[@id="add"and@data-local="刷新"]').click()
        # time.sleep(1)
        #输入pc的IP地址来过滤验证断言
        dhcpserver.input_search(pcaddr)
        dhcpserver.click_searchb()
        time.sleep(1)
        list_tips=dhcpserver.getText_byXpath(dhcpserver.list_tips)
        self.assertEqual(list_tips,nodata,msg='DHCP客户端列表不为空')
        self.driver.quit()
        logger.info('test_004_releaseIP passed')

    def test_005_dnsProxy(self):
        u'''dns代理可以上网'''
        baidutitle = getAssertText('baidutitle')
        # 开dns代理
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        dhcpserver = DHCPserverpage(self.driver, self.url)
        dhcpserver.click_NetworkConfig()
        time.sleep(0.5)
        dhcpserver.click_DHCPserver()
        time.sleep(1)
        dhcpserver.click_GlobalConfig()
        time.sleep(1)
        dhcpserver.click_dnspEn()
        dhcpserver.click_save()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        tips = str(dhcpserver.getText_byClass(dhcpserver.tips))
        time.sleep(1)
        self.assertEqual(tips, saveSucess, msg='"DNS代理" 开启出错')
        print('DNS代理 已开启')

        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system(('%s' % batpath + 'changeDhcpIp.bat'))
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
        pingTestIP('www.baidu.com') #避免失误
        self.driver.get('http://www.baidu.com')
        time.sleep(2)
        title3 = self.driver.title
        print(title3)
        self.assertEqual(title3, baidutitle, msg='dns代理 无法打开网页')
        self.driver.quit()
        logger.info('test_005_dnsProxy passed')

    def test_006_binding(self):
        u'''启用ip/mac绑定生效；删除组织架构中的成员，查看绑定是否生效(是否可上网)'''
        host = gettelnet('host')
        # 判断联网 ，不能上网则报错
        p = pingTestIP('www.163.com')
        if p == 'N':
            raise Exception('connect failed.')

        # # 获取本机ip 默认有线地址，有线断开会显示无线
        # pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

        # 调用bat脚本 地址修改为非绑定地址 192.168.1.39 网关192.168.1.1
        if '192.168.1.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_1duan.bat'))
        elif '192.168.16.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_16duan.bat'))
        else:
            raise Exception('lan口非 1网段、16网段')
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if str(pcaddr1) != batSameIP:
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为非绑定地址 192.168.1.39', n)
                break
        else:
            raise Exception('地址修改为非绑定地址 192.168.1.39失败')

        # 判断联网 ,切换非绑定IP后应该不能上网
        time.sleep(5)
        pingTestIP('114.114.114.114')
        pingTestIP('www.baidu.com')
        time.sleep(2)
        p = pingTestIP('www.baidu.com')
        if p == 'Y':
            logger.info('非绑定IP 依旧可以上网')
            logger.info(u'pc当前mac为：%s' % pcaddr1)
            raise Exception('非绑定IP 依旧可以上网')

        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system(('%s' % batpath + 'changeDhcpIp.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if '192.168.' not in str(pcaddr1):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址')

        #删除绑定绑定 清空组
        organization_group.group_delete(self)

        # 调用bat脚本 地址修改为非绑定地址 192.168.1.39 网关192.168.1.1
        if '192.168.1.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_1duan.bat'))
        elif '192.168.16.1' in host:
            os.system(('%s' % batpath + 'changeStaticIP2_16duan.bat'))
        else:
            raise Exception('lan口非 1网段、16网段')
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if str(pcaddr1) != batSameIP:
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为非绑定地址 192.168.1.39', n)
                break
        else:
            raise Exception('地址修改为非绑定地址 192.168.1.39失败')

        # 判断联网 ,删除绑定后 切换非绑定IP后应该能上网
        time.sleep(3)
        p = pingTestIP('www.163.com')
        if p == 'N' :
            raise Exception('connect failed.')

        # 将IP改回自动获取（设置dns为自动获取）
        # 调用bat脚本
        os.system(('%s' % batpath + 'changeDhcpIp.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr1 = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr1, n)
            if '192.168.' not in str(pcaddr1):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址')
        logger.info('test_006_binding passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()



