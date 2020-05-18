#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 13:21
#@swzhou
'''
静态映射:配置80\21\69端口静态映射及开启相关服务结果
'''

import os
import time
import socket
import os.path
import unittest
import telnetlib
import subprocess
import win32process
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import gettelnet,getweb,getAssertText
from common.loginRoute import login
from common.swconfig import swconfig
from common.GetRouteCPU import getCPUmodel
from pages.PortMapping_002_staticMappingPage import staticMappingPage
from pages.Organization_002_userStatuspage import Organization_userStatusPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'PortMapping_002_staticMapping').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
serverPcMac = getweb('serverPcMac')
CPUmodel = getCPUmodel()
ConnectState = getAssertText('ConnectState')

class staticMapping(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_tcp80(self):
        u'''验证tcp80 映射'''

        # #改用另外设置的server pc
        # # 打开Everthing,Evering充当80server（需事先设置开启相关http服务）
        # handle = win32process.CreateProcess("D:\Program Files\Everything\Everything.exe", '', None,
        #                                     None, 0, win32process.CREATE_NO_WINDOW, None, None,
        #                                     win32process.STARTUPINFO())  # 打开Evering，获得其句柄
        # #获取本机地址
        # pcaddr=socket.gethostbyname(socket.gethostname())

        #通过用户状态获取httpserver的IP地址
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
                telnetlib.Telnet(serverIP, port=80, timeout=10)
                print('server tcp80端口已开启')
            except socket.timeout:
                logger.info(u'内网方向无法访问server TCP80端口')
                raise Exception(u'内网方向无法访问server TCP80端口')

        staticMapping = staticMappingPage(self.driver,self.url)
        #配置映射
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        staticMapping.click_add()
        time.sleep(1)
        staticMapping.input_IDs('statictest')
        staticMapping.input_IPs(serverIP)
        Selprotocols = staticMapping.selelement_byName(staticMapping.Protocols)
        Select(Selprotocols).select_by_value('1')#1:tcp 2:udp 3:tcp/udp
        time.sleep(0.5)
        staticMapping.input_inS('80')
        time.sleep(0.5)
        staticMapping.input_inE('80')
        time.sleep(1)
        staticMapping.input_outS('80')
        time.sleep(0.5)
        staticMapping.input_outE('80')
        staticMapping.click_save()
        time.sleep(1)
        #断言
        list_port = str(staticMapping.getText_byXpath(staticMapping.list_port))
        print(list_port)
        self.assertEqual(list_port, '80~80:80~80', msg='端口对应关系不一致')
        print('tcp80映射 已添加')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver,self.url)
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
        print('WAN1_ip=',WAN1_ip)
        time.sleep(1)
        self.driver.quit()
        url='http://'+str(WAN1_ip)
        print(url)

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
            time.sleep(120)#等待计划任务执行
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

        print('url:',url)
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        title = self.driver.title
        print(title)
        self.assertEqual(title,'探索昆虫世界，用老蛙24mm f/14微距镜头试试 - 摄影,镜头 - IT之家',msg='http访问有误')
        self.driver.quit()

        # win32process.TerminateProcess(handle[0], 0)  # 关闭Everying,没有能关闭掉就不关了
        logger.info('test_001_tcp80 passed')

    def test_002_tcp21(self):
        u'''验证tcp21 映射'''
        # #获取本机地址
        # pcaddr=socket.gethostbyname(socket.gethostname())
        # # 打开Everthing,Evering充当80server（需事先设置开启相关http服务）
        # handle = win32process.CreateProcess("D:\Program Files\Everything\Everything.exe", '', None,
        #                                     None, 0, win32process.CREATE_NO_WINDOW, None, None,
        #                                     win32process.STARTUPINFO())  # 打开Evering，获得其句柄

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
        else:
            try:
                telnetlib.Telnet(serverIP, port=21, timeout=10)
                print('server tcp21端口已开启')
            except socket.timeout:
                logger.info(u'内网方向无法访问server TCP21端口')
                raise Exception(u'内网方向无法访问server TCP21端口')

        staticMapping = staticMappingPage(self.driver, self.url)
        # 配置映射
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        staticMapping.click_add()
        time.sleep(1)
        staticMapping.input_IDs('statictest')
        staticMapping.input_IPs(serverIP)
        Selprotocols = staticMapping.selelement_byName(staticMapping.Protocols)
        Select(Selprotocols).select_by_value('1')  # 1:tcp 2:udp 3:tcp/udp
        time.sleep(0.5)
        staticMapping.input_inS('21')
        staticMapping.input_inE('21')
        staticMapping.input_outS('21')
        staticMapping.input_outE('21')
        staticMapping.click_save()
        time.sleep(1)
        # 断言
        list_port = str(staticMapping.getText_byXpath(staticMapping.list_port))
        print(list_port)
        self.assertEqual(list_port, '21~21:21~21', msg='端口对应关系不一致')
        print('tcp80映射 已添加')

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
        # print('WAN1_ip=',WAN1_ip)
        time.sleep(1)
        self.driver.quit()
        url = 'ftp://' + str(WAN1_ip)+':21/'
        print(url)

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
            time.sleep(120) #等待计划任务执行
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

        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        time.sleep(2)
        title = self.driver.title
        print(title)
        self.assertEqual(title, '/ 的索引', msg='ftp访问有误')

        self.driver.quit()

        # win32process.TerminateProcess(handle[0], 0)  # 关闭Everying,没有能关闭掉就不关了
        logger.info('test_002_tcp21 passed')

    def test_003_udp69(self):
        u'''验证udp69 映射'''
        #获取本机地址
        pcaddr=socket.gethostbyname(socket.gethostname())

        # 打开tftp32.exe,
        # 注意：tftp32打开后的目录是由 由哪个脚本执行 所在的路径决定
        #直接运行该脚本，则tftp32的目录是‘test_003_udp69’所在的‘D:\python\SEWEB\3.1.1Router\test_case\Port_mapping’
        #由all_test.py或者ProductModel_test.py调用执行，则目录为‘D:\python\SEWEB\3.1.1Router\run’
        #因此 需把握好 对应目录中包含上传的文件，此脚本设定上传的文件为'tftpd32.exe'
        handle = win32process.CreateProcess(r"D:\python\SEWEB\3.1.1Router\test_case\tftpd32.exe", '', None,
                                            None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())  # 打开tftp32.exe，获得其句柄

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
        staticMapping.input_IPs(pcaddr)
        Selprotocols = staticMapping.selelement_byName(staticMapping.Protocols)
        Select(Selprotocols).select_by_value('2')  # 1:tcp 2:udp 3:tcp/udp
        time.sleep(0.5)
        staticMapping.input_inS('69')
        staticMapping.input_inE('69')
        staticMapping.input_outS('69')
        staticMapping.input_outE('69')
        staticMapping.click_save()
        time.sleep(1)
        # 断言
        list_port = str(staticMapping.getText_byXpath(staticMapping.list_port))
        print(list_port)
        self.assertEqual(list_port, '69~69:69~69', msg='端口对应关系不一致')
        print('tcp69映射 已添加')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 gw变量赋值，页面读取
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
        WAN1_gw = str(wanpage.getText_byXpath(wanpage.line1gw))
        # print('WAN1_gw=',WAN1_gw)
        time.sleep(1)
        # WAN1_gw = '192.168.11.1'
        # 连接Telnet服务器
        hostip = WAN1_gw
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b"rm tftpd32.exe lanip" + b'\n')
        tn.read_until(b'#')
        tn.write(
            b"cat /proc/net/nf_conntrack |grep tcp | grep `uttcli get interface 0 ethernet static ip`| grep 'dport=60023' | awk '{print $7}' |awk -F'=' '{print $2}' | sed -n '1p' >lanip" + b'\n')
        tn.read_until(b'#')
        tn.write(b"lanip=`cat lanip`" + b'\n')
        tn.read_until(b'#')
        tn.write(b'tftp -gr tftpd32.exe `cat lanip` 69' + b'\n')
        time.sleep(1)
        # print('1')
        tn.read_until(b'#')
        # print('2')
        tn.write(b"ls | grep tftpd32" + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)

        # 后台实际应有的结果
        # result1=  b' ls | grep tftpd32\r\ntftpd32.exe\r\n# '
        # 判断
        if 'tftpd32.exe' in result:
            print('ftfp 验证成功')
        else:
            raise Exception('ftfp 验证失败')  # 如果没有则报错
        tn.close()

        win32process.TerminateProcess(handle[0], 0)  # 关闭tftp32，注意脚本执行前关闭所有的tftp32进程 否则不能关闭会报错

        self.driver.quit()

        logger.info('test_003_udp69 passed')

    def tearDown(self):
        switchURL2 = gettelnet('switchURL2')
        p = pingTestIP()
        if p == 'N':
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
            time.sleep(2)

            # 更改pc 交换机接口与lan口通
            p = pingTestIP(switchURL2)
            if p == 'N':
                raise Exception(u'无法ping通交换机switchURL2地址')
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

        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        staticMapping = staticMappingPage(self.driver, self.url)
        # 配置映射
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            staticMapping.find_delete1()
        except NoSuchElementException:
            pass
        else:
            time.sleep(1)
            staticMapping.click_ok()
            time.sleep(1)
            list_tips = staticMapping.getText_byXpath(staticMapping.list_tips)
            self.assertEqual(str(list_tips), ' ', msg='映射删除失败')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

