#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 14:47
#@swzhou
'''
DMZ主机：测试全局和单独设置WAN口均生效
设置同一个端口的情况下，优先级低于静态映射
'''

import os
import time
import unittest
import socket
import telnetlib
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getweb,gettelnet,getAssertText
from common.swconfig import swconfig
from common.pingTest import pingTestIP
from common.GetRouteCPU import getCPUmodel
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.PortMapping_002_staticMappingPage import staticMappingPage
from pages.PortMapping_004_DMZpage import DMZPage
from pages.Organization_002_userStatuspage import Organization_userStatusPage
logger = LogGen(Logger = 'PortMapping_004_DMZ').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
serverPcMac = getweb('serverPcMac')
CPUmodel =getCPUmodel()
ConnectState = getAssertText('ConnectState')

class DMZ(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_server3389(self):
        u'''验证下server 3389是否已打开'''

        # 通过用户状态获取httpserver的IP地址
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        status.input_search(serverPcMac)
        status.click_searchb()
        time.sleep(1)
        try:
            serverIP = status.getText_byXpath(status.list_IP1)
        except NoSuchElementException:
            raise Exception(u'用户状态中未找到server IP')
            # print(serverIP)
        else:
            try:
                telnetlib.Telnet(serverIP, port=3389, timeout=10)
            except socket.timeout:
                logger.info(u'内网方向无法访问server TCP3389端口')
                raise Exception(u'内网方向无法访问server TCP3389端口')
            else:
                print('server tcp3389端口已开启')
        self.driver.quit()
        logger.info('test_001_server3389 passed')

    def test_002_localDMZ(self):
        u'''验证局部DMZ'''
        # #获取本机地址
        # pcaddr=socket.gethostbyname(socket.gethostname())

        # 通过用户状态获取httpserver的IP地址
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        status.input_search(serverPcMac)
        status.click_searchb()
        time.sleep(1)
        try:
            serverIP = status.getText_byXpath(status.list_IP1)
            # print(serverIP)
        except NoSuchElementException:
            raise Exception(u'用户状态中未找到server IP')

        #局部DMZ
        dmz = DMZPage(self.driver,self.url)
        dmz.click_NetworkConfig()
        time.sleep(0.5)
        dmz.click_portMapping()
        time.sleep(1)
        dmz.click_DMZ()
        time.sleep(1)
        dmz.click_DMZEn()
        dmz.input_GlobalDMZ('0.0.0.0')#防止已经有过全局DMZ设置
        dmz.input_WAN1DMZ(serverIP)
        dmz.click_save()
        time.sleep(1)
        #断言
        dmz.click_DMZ() #相当于刷新下界面，否则on依旧没有checked参数
        time.sleep(1)
        DMZ_status = str(dmz.getAttribute_byXpath(dmz.DMZEs,'checked'))
        print(DMZ_status)
        self.assertEqual(DMZ_status, 'true', msg='DMZ 开启有问题')
        print('局部DMZ 已开启')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
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

        if CPUmodel == 'Qualcomm':
            # 部分型号，如高通1200Wv2，因为芯片问题必须关闭wan口mac学习功能，原mac未清除之前无法从wan口访问路由器
            # 这里需要设置计划任务2分钟后清空原pc的arp缓存
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
            tn.write(b"uptime" + b"\n")
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            result1 = str(result.split(r'\r\n')[1]).split(r':')
            print(result1[1])
            tn.close()  # tn.write('exit\n')
            if int(result1[1]) + 2 < 60:
                hour = result1[0]
                min = int(result1[1]) + 2
            else:
                if int(result1[0]) + 1 < 24:
                    hour = int(result1[0]) + 1
                    min = '0' + str((int(result1[1]) + 2) - 60)
                else:
                    hour = '0' + str(int(result1[0]) + 1 - 24)
                    min = '0' + str((int(result1[1]) + 2) - 60)
            print(hour)
            print(min)
            pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
            cmd = "echo '%s %s * * * arp -d %s' > cmd " % (min, hour, pcaddr)
            print(cmd)
            cmd = bytes(cmd, encoding='utf8')
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(cmd + b"\n")
            tn.read_until(b'#')
            tn.write(b"cat cmd >> /var/spool/cron/crontabs/admin" + b"\n")
            tn.read_until(b'#')
            tn.write(b"killall crond" + b"\n")
            tn.read_until(b'#')
            tn.write(b"crond &" + b"\n")
            tn.read_until(b'#')
            tn.write(b"cat /var/spool/cron/crontabs/admin" + b"\n")
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            if 'adp -d' in result:
                print('计划任务已写入')

        # 更改pc 交换机接口与wan口/上联口通
        swconfig.test_LanToWan(self)
        if CPUmodel == 'Qualcomm':
            time.sleep(120)  # 等待计划任务执行
        # 重新获取地址 应获取到上层网关下发的地址
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
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

        try:
            telnetlib.Telnet(str(WAN1_ip), port=3389, timeout=10)
            print('局部DMZ 验证成功')
        except socket.timeout:
            logger.info(u'局部DMZ 验证失败')
            raise Exception(u'局部DMZ 验证失败')
        self.driver.quit()
        logger.info('test_002_localDMZ passed')

    def test_003_GlobalDMZ(self):
        u'''验证全局DMZ'''
        # # 获取本机地址
        # pcaddr = socket.gethostbyname(socket.gethostname())

        # 通过用户状态获取httpserver的IP地址
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        status.input_search(serverPcMac)
        status.click_searchb()
        time.sleep(1)
        try:
            serverIP = status.getText_byXpath(status.list_IP1)
            # print(serverIP)
        except NoSuchElementException:
            raise Exception(u'用户状态中未找到server IP')

        # 全局DMZ
        dmz = DMZPage(self.driver, self.url)
        dmz.click_NetworkConfig()
        time.sleep(0.5)
        dmz.click_portMapping()
        time.sleep(1)
        dmz.click_DMZ()
        time.sleep(1)
        dmz.click_DMZEn()
        dmz.input_GlobalDMZ(serverIP)
        dmz.click_save()
        time.sleep(1)
        # 断言
        dmz.click_DMZ()
        time.sleep(1)
        DMZ_status = str(dmz.getAttribute_byXpath(dmz.DMZEs,'checked'))
        print(DMZ_status)
        self.assertEqual(DMZ_status, 'true', msg='DMZ 开启异常')
        print('全局DMZ 已开启')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
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

        if CPUmodel == 'Qualcomm':
            # 部分型号，如高通，因为芯片问题必须关闭wan口mac学习功能，原mac未清除之前无法从wan口访问路由器
            # 这里需要设置计划任务2分钟后清空原pc的arp缓存
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
            tn.write(b"uptime | awk '{print $1}'' + b'\n")
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            result1 = str(result.split(r'\r\n')[1]).split(r':')
            print(result1[1])
            tn.close()  # tn.write('exit\n')
            if int(result1[1]) + 2 < 60:
                hour = result1[0]
                min = int(result1[1]) + 2
            else:
                if int(result1[0]) + 1 < 24:
                    hour = int(result1[0]) + 1
                    min = '0' + str((int(result1[1]) + 2) - 60)
                else:
                    hour = '0' + str(int(result1[0]) + 1 - 24)
                    min = '0' + str((int(result1[1]) + 2) - 60)
            print(hour)
            print(min)
            pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
            cmd = "echo '%s %s * * * arp -d %s' > cmd " % (min, hour, pcaddr)
            print(cmd)
            cmd = bytes(cmd, encoding='utf8')
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(cmd + b"\n")
            tn.read_until(b'#')
            tn.write(b"cat cmd >> /var/spool/cron/crontabs/admin" + b"\n")
            tn.read_until(b'#')
            tn.write(b"killall crond" + b"\n")
            tn.read_until(b'#')
            tn.write(b"crond &" + b"\n")
            tn.read_until(b'#')
            tn.write(b"cat /var/spool/cron/crontabs/admin" + b"\n")
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            if 'adp -d' in result:
                print('计划任务已写入')

        # 更改pc 交换机接口与wan口/上联口通
        swconfig.test_LanToWan(self)
        if CPUmodel == 'Qualcomm':
            time.sleep(120)  # 等待计划任务执行
        # 重新获取地址 应获取到上层网关下发的地址
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
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

        try:
            telnetlib.Telnet(str(WAN1_ip), port=3389, timeout=10)
            print('全局DMZ 验证成功')
        except socket.timeout:
            logger.info(u'全局DMZ 验证失败')
            raise Exception(u'全局DMZ 验证失败')

        self.driver.quit()
        logger.info('test_003_GlobalDMZ passed')

    def test_004_DMZpriority(self):
        u'''验证 映射和DMZ的优先级'''

        #将3389端口映射给一个不存在的主机
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        staticMapping = staticMappingPage(self.driver, self.url)
        # 配置映射
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        staticMapping.click_add()
        time.sleep(1)
        staticMapping.input_IDs('statictest')
        staticMapping.input_IPs('1.2.3.4')
        staticMapping.input_inS('3389')
        staticMapping.input_inE('3389')
        staticMapping.input_outS('3389')
        staticMapping.input_outE('3389')
        staticMapping.click_save()
        time.sleep(1)
        #断言
        list_port = str(self.driver.find_element_by_xpath('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span').text)
        print(list_port)
        self.assertEqual(list_port, '3389~3389:3389~3389', msg='端口对应关系不一致')
        print('tcp21映射 已添加')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
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
        self.driver.quit()

        # 更改pc 交换机接口与wan口/上联口通
        swconfig.test_LanToWan(self)
        # 重新获取地址 应获取到上层网关下发的地址
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
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

        try:
            telnetlib.Telnet(str(WAN1_ip), port=3389, timeout=10)
            raise Exception('映射优先级高于DMZ 验证失败') #如果通则报错
        except socket.timeout:
            print('映射优先级高于DMZ 验证成功') #如果不通（timeout报错）则正常

        switchURL2 = gettelnet('switchURL2')
        # 调用bat脚本 地址修改为 192.168.34.39 网关192.168.34.1
        os.system('%s' % (batpath + 'changeStaticIP3_34duan.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr, n)
            if str(pcaddr) != '192.168.34.39':
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为地址 192.168.34.39', n)
                time.sleep(2)
                break
        else:
            raise Exception('地址修改为192.168.34.39 失败')

        # 更改pc 交换机接口与lan口通
        p = pingTestIP(switchURL2)
        if p == 'Y':
            swconfig.test_WanToLan(self)
        # 将IP改回自动获取 应获取到被测设备下发的地址
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
            raise Exception('未获取到地址')

        #删除映射
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        staticMapping = staticMappingPage(self.driver, self.url)
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        staticMapping.click_delete1()
        time.sleep(1)
        staticMapping.click_ok()
        time.sleep(1)
        list_tips = staticMapping.getText_byXpath(staticMapping.list_tips)
        self.assertEqual(str(list_tips), ' ', msg='映射删除失败')
        #关闭DMZ
        dmz = DMZPage(self.driver, self.url)
        dmz.click_DMZ()
        time.sleep(1)
        dmz.click_DMZC()
        dmz.input_GlobalDMZ('0.0.0.0')
        time.sleep(1)
        dmz.click_save()
        time.sleep(1)
        # 断言
        dmz.click_DMZ()# 相当于刷新下界面，否则off依旧没有checked参数
        time.sleep(1)
        DMZ_status = str(dmz.getAttribute_byXpath(dmz.DMZCs,'checked'))
        print(DMZ_status)
        self.assertEqual(DMZ_status, 'true', msg='DMZ 关闭异常')
        print('全局DMZ 已关闭')

        self.driver.quit()
        logger.info('test_003_DMZpriority passed')


    def tearDown(self):
        switchURL2 = gettelnet('switchURL2')
        # 调用bat脚本 地址修改为 192.168.34.39 网关192.168.34.1
        os.system('%s' % (batpath + 'changeStaticIP3_34duan.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr, n)
            if str(pcaddr) != '192.168.34.39':
                time.sleep(2)
                n += 1
            else:
                print('地址已修改为地址 192.168.34.39', n)
                break
        else:
            raise Exception('地址修改为192.168.34.39 失败')

        # 更改pc 交换机接口与lan口通
        p = pingTestIP(switchURL2)
        if p == 'Y':
            swconfig.test_WanToLan(self)
        # 将IP改回自动获取 应获取到被测设备下发的地址
        os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
            raise Exception('未获取到地址')
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()


