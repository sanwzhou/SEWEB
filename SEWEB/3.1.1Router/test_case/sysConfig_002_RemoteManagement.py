#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 11:13
#@swzhou
'''
开启远程管理，验证登录
'''

import os
import time
import unittest
import socket
import telnetlib
from selenium import webdriver
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.swconfig import swconfig
from common.ReadConfig import gettelnet,getweb,getAssertText
from common.GetRouteCPU import getCPUmodel
from common.pingTest import pingTestIP
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
from pages.PortMapping_002_staticMappingPage import staticMappingPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'sysConfig_002_RemoteManagement').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
CPUmodel = getCPUmodel()
ConnectState = getAssertText('ConnectState')

class RemoteManagement(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        remoteManage = ManagementPolicyPage(self.driver,self.url)
        # 进入系统配置-网管策略-远程管理
        remoteManage.click_sysConfig()
        time.sleep(0.5)
        remoteManage.click_ManagementPolicy()
        time.sleep(1)
        remoteManage.click_RemoteManagement()
        time.sleep(1)
        # pass

    def test_001_openRemote(self):
        u'''开启远程管理'''
        # 开启远程管理
        remoteManage = ManagementPolicyPage(self.driver, self.url)
        remoteManage.click_httpEn()
        time.sleep(0.5)
        remoteManage.click_save()
        time.sleep(1)

        #检查admin的映射是否开启
        staticMapping = staticMappingPage(self.driver, self.url)
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        list_Ens = staticMapping.getAttribute_byXpath(staticMapping.list1_Ens,'checked')
        if list_Ens != 'true':
            CapPic(self.driver)
            logger.info(u'开启远程管理 静态映射未打开')
            raise Exception(u'远程管理 静态映射未打开')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
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
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)
        self.driver.quit()

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

        #更改pc 交换机接口与wan口/上联口通
        swconfig.test_LanToWan(self)
        if CPUmodel == 'Qualcomm':
            time.sleep(110)  # 等待计划任务执行
        #重新获取地址 应获取到上层网关下发的地址
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
        while n < 60:
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
        n = 0
        while n < 30:
            ping = pingTestIP(WAN1_ip)
            if ping != "Y" :
                time.sleep(1)
                n += 1
            else:
                break
        else:
            logger.info(u'切换IP后wan口方向 无法ping通wan口')
            logger.info(u'pcIP地址为 %s' % pcaddr)
            raise Exception(u'切换IP后wan口方向 无法ping通wan口')
        logger.info(u'pcIP地址为 %s' % pcaddr)
        WANURL = str('http://'+str(WAN1_ip)+':8081')
        #使用页面获取的WAN1 ip验证登录
        login.test_enableLoginWeb(self , url = WANURL)
        self.driver.quit()

        #改回lan口方向
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

        logger.info('test_001_openRemote passed')

    def test_002_CloseRemote(self):
        u'''关闭远程管理'''
        # 关闭远程管理
        remoteManage = ManagementPolicyPage(self.driver, self.url)
        remoteManage.click_httpC()
        time.sleep(0.5)
        remoteManage.click_save()
        time.sleep(1)

        # 检查admin的映射是否开启
        staticMapping = staticMappingPage(self.driver, self.url)
        staticMapping.click_NetworkConfig()
        time.sleep(0.5)
        staticMapping.click_portMapping()
        time.sleep(1)
        list_Ens = staticMapping.getAttribute_byXpath(staticMapping.list1_Ens,'checked')
        if list_Ens == 'true':
            CapPic(self.driver)
            logger.info(u'关闭远程管理 静态映射未关闭')
            raise Exception(u'关闭管理 静态映射未关闭')

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
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
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)
        self.driver.quit()
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
            time.sleep(110)  # 等待计划任务执行
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
        while n < 60:
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

        WANURL = str('http://' + str(WAN1_ip) + ':8081')
        # 使用页面获取的WAN1 ip验证登录
        self.dr = webdriver.Chrome()
        # self.dr.maximize_window()
        self.dr.implicitly_wait(10)
        self.dr.get(WANURL)
        time.sleep(1)
        url = self.dr.current_url
        if '/noAuth/login.html' not in url:
            logger.info(u'远程管理开启 验证通过')
        else:
            raise Exception(u'关闭远程 wan口依旧可以访问')
        self.dr.close()

        # 改回lan口方向
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
        logger.info('test_002_CloseRemote passed')

    def tearDown(self):
        #避免未改回
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

            # 更改pc 交换机接口与lan口通
            try:
                swconfig.test_WanToLan(self)
            except TimeoutError:
                logger.info(u'telnet不到交换机')
                pass
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
