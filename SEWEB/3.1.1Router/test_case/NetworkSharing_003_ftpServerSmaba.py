#! -*-conding:utf-8 -*-
#@Time: 2019/1/24 0024 16:16
#@swzhou
'''
ftp服务器、samba服务器
'''

import os
import time
import unittest
import socket
import telnetlib
import ftplib
import subprocess
from smb.SMBConnection import SMBConnection
from smb.base import NotReadyError
import re #正则表达式模块
from common.LogGen import LogGen
from common.ReadConfig import getweb,gettelnet,getAssertText
from common.CapPic import CapPic
from common.loginRoute import login
from common.swconfig import swconfig
from common.pingTest import pingTestIP
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_008_NetworkSharingPage import NetworkSharingPage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
logger = LogGen(Logger = 'NetworkSharing_003_ftpServerSmaba').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'


class ftpServerSmaba(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        ftpSmaba = NetworkSharingPage(self.driver,self.url)
        # 打开网络配置-网络共享
        ftpSmaba.click_netConfig()
        time.sleep(0.5)
        ftpSmaba.click_NetworkSharing()
        time.sleep(1)
        ftpSmaba.click_NetworkSharing2()# 点击网络共享子页面
        time.sleep(1)
        # pass

    def test_001_ftpServer(self):
        u'''ftp服务器基本设置，ftp查看'''
        host = gettelnet('host')
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        # 1、设置ftp基本信息
        ftpSmaba.click_choosml()
        time.sleep(1)
        ftpSmaba.input_names('1')
        ftpSmaba.click_FTP_DIR_1_check()
        ftpSmaba.click_modal_FTP()
        time.sleep(1)
        try: #以访第一次选中后 第二次点击被取消 从而未选中共享目录
            self.driver.implicitly_wait(1)
            ftpSmaba.find_tips_show_inf()
        except NoSuchElementException:
            pass
        else:
            ftpSmaba.click_FTP_DIR_1_check()
            ftpSmaba.click_modal_FTP()
            time.sleep(3)
        self.driver.implicitly_wait(10)
        ftpEn = ftpSmaba.getAttribute_byName(ftpSmaba.ftpEns,'checked')
        print(ftpEn)
        if ftpEn != 'true':
            ftpSmaba.click_ftpEn()
            time.sleep(1)
        defaultPort = str(ftpSmaba.getAttribute_byName(ftpSmaba.ftpports,'value'))
        self.assertEqual(defaultPort, '21', msg='ftp默认端口不为21')
        ftpSmaba.click_save()
        time.sleep(1)
        enableDevice = ftpSmaba.getAttribute_byId(ftpSmaba.enableDevices,'checktype')
        print(enableDevice)
        if enableDevice != '1': #1为打开网络共享
            ftpSmaba.click_enableDevice()
            time.sleep(3)
        ftpEn = ftpSmaba.getAttribute_byName(ftpSmaba.ftpEns,'checked')
        enableDevice = ftpSmaba.getAttribute_byId(ftpSmaba.enableDevices,'checktype')
        self.assertEqual(ftpEn,'true',msg='启用FTP服务器 失败')
        self.assertEqual(enableDevice, '1', msg='网络共享 启用失败')
        time.sleep(10)
        #2、ftp查看目录文件
        IP = host
        Port = 21
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=Port, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        # print('ftpFile', ftpFile)
        ftp.quit()
        #过滤掉中文和带空格的
        zhmodel = re.compile(u'[\u4e00-\u9fa5]')  # 检查中文
        ftpFile2 = []
        for file in ftpFile:
            if ' ' not in file:
                ftpFile2.append(file[2:])
        for i in ftpFile2:
            if zhmodel.search(i):
                ftpFile2.remove(i)
        # print('ftpFile2:',ftpFile2)
        # 3、telnet后台查看目录文件
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
        tn.write(b'cd /ftpRoot/1 ; ls' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        tn.close()  # tn.write('exit\n')

        #4、判断对比 ftp查看内容在telnet查看的目录中
        for i in ftpFile2:
            if result.count(i):
                pass
            else:
                raise Exception(' 验证失败')  # 如果没有则报错

        self.driver.quit()
        logger.info('test_001_ftpServer passed')

    def test_002_ftpPort(self):
        u'''FTP端口'''

        host = gettelnet('host')
        portwarnA = getAssertText('portwarnA')
        ftpSmaba = NetworkSharingPage(self.driver, self.url)

        # defaultPort=str(self.driver.find_element_by_name('ftpport').get_attribute('value'))
        # self.assertEqual(defaultPort,'21',msg='ftp默认端口不为21') #001已验证

        #修改端口为22
        ftpSmaba.input_ftpport('22')
        ftpSmaba.click_save()
        time.sleep(10)
        Port1 = str(ftpSmaba.getAttribute_byName(ftpSmaba.ftpports,'value'))
        self.assertEqual(Port1, '22', msg='ftp修改端口不为22')
        # ftp验证端口
        IP = host
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=22, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()
        # 修改端口为65534
        ftpSmaba.input_ftpport('65534')
        ftpSmaba.click_save()
        time.sleep(10)
        Port1 = str(ftpSmaba.getAttribute_byName(ftpSmaba.ftpports, 'value'))
        self.assertEqual(Port1, '65534', msg='ftp修改端口不为65534')
        # ftp验证端口
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=65534, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()
        # 修改端口为1
        ftpSmaba.input_ftpport('1')
        ftpSmaba.click_save()
        time.sleep(10)
        Port1 = str(ftpSmaba.getAttribute_byName(ftpSmaba.ftpports, 'value'))
        self.assertEqual(Port1, '1', msg='ftp修改端口不为1')
        # ftp验证端口
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=1, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()

        #验证提示信息
        ftpSmaba.input_ftpport('65536')
        ftpSmaba.click_save()
        time.sleep(1)
        tipsport = str(ftpSmaba.getText_byXpath(ftpSmaba.tipsport))
        if portwarnA not in tipsport:
            CapPic(self.driver)
            logger.info(u'FTP端口范围提示有误')
            raise Exception('FTP端口范围提示有误')

        # 将端口改回21
        ftpSmaba.input_ftpport('21')
        ftpSmaba.click_save()
        time.sleep(2)

        self.driver.quit()
        logger.info('test_002_ftpPort passed')

    def test_003_samba(self):
        u'''samba服务器(部分型号暂未支持)'''

        host = gettelnet('host')
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        #1、未开启验证无法登录
        user_name = "anonymous"
        pass_word = ""
        my_name = "anyname"
        domain_name = ""
        remote_smb_IP = host
        smb = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except ConnectionRefusedError:
            print('未开启samba 无法访问 验证通过')

        #2、打开samba
        sambaEn = ftpSmaba.getAttribute_byName(ftpSmaba.sambaEnS,'checked')
        if sambaEn != 'true':
            ftpSmaba.click_sambaEn()
            ftpSmaba.click_save()
        time.sleep(13)
        sambaEn = str(ftpSmaba.getAttribute_byName(ftpSmaba.sambaEnS,'checked'))
        self.assertEqual(sambaEn,'true',msg='samba开启 失败')
        #samba登录
        smb = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        shareslist = smb.listShares() # 列出共享目录 这里只能看到1级菜单“1”
        smb.close()
        n = []
        for i in shareslist:
            n.append(i.name)
        print(n)
        nn = []
        for x in n:
            if '$' not in x:
                nn.append(x)
                print(nn)
        #3、打开验证
        if '1' in nn:
            pass
        else:
            raise Exception('samba验证失败')  # 如果没有则报错

        self.driver.quit()
        logger.info('test_003_samba passed')

    def test_004_WanAcessFTP(self):
        u'''WAN口访问FTP'''
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        #1、验证未打开 ‘wan口访问’ 无法从wan访问FTP
        #1）验证未打开
        WANEnable = str(self.driver.find_element_by_name('WANEnable').get_attribute('checked'))
        print(WANEnable)
        if WANEnable == 'true':
            self.driver.find_element_by_name('WANEnable').click()
            ftpSmaba.click_save()
            time.sleep(1)
            ftpSmaba.click_NetworkSharing2()  # 点击网络共享子页面
            time.sleep(1)
            WANEnable = str(self.driver.find_element_by_name('WANEnable').get_attribute('checked'))
            self.assertEqual(WANEnable, 'None', msg='允许wan口访问 关闭失败')
        #2）从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 ip变量赋值，页面读取
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)
        #3） 更改pc 交换机接口与wan口/上联口通
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
        # 重新获取地址
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
        time.sleep(2)
        #4）尝试访问FTP
        # ftp验证登录
        IP = WAN1_ip
        Port = 21
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=Port, timeout=5)
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except socket.error or socket.gaierror:
            print("未开启“WAN口访问开关”无法访问FTP服务 验证通过")
        except ftplib.error_perm:  # 当前未开启wan口访问，wan口访问时候会弹出账号密码框，但输入会提示密码错误
            print("未开启“WAN口访问开关”访问FTP服务会密码错误 验证通过")
        else:
            raise Exception("未开启“WAN口访问开关” 依旧可以访问FTP服务")
        ftp.quit()
        #5）改为lan口 并重新获取地址
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
        time.sleep(3)
        #2 验证打开 ‘wan口访问’ 可以从wan口访问FTP
        #1）打开
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        ftpSmaba.click_NetworkSharing()
        time.sleep(1)
        ftpSmaba.click_NetworkSharing2()  # 点击网络共享子页面
        time.sleep(1)
        self.driver.find_element_by_name('WANEnable').click()
        ftpSmaba.click_save()
        time.sleep(2)
        WANEnable = self.driver.find_element_by_name('WANEnable').get_attribute('checked')
        self.assertEqual(WANEnable, 'true', msg='允许wan口访问 启用失败')
        #2) 更改pc 交换机接口与wan口/上联口通
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
        # 重新获取地址
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
        time.sleep(2)
        # 3）ftp验证登陆
        try:
            ftp.connect(host=IP, port=Port, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()

        self.driver.quit()
        logger.info('test_004_WanaAcess passed')

    def test_005_WanAcessSmaba(self):
        u'''WAN口访问samba服务器(部分型号暂未支持)'''
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        #1、验证未打开 ‘wan口访问’ 无法从wan访问samba
        #1）验证未打开
        WANEnable = str(self.driver.find_element_by_name('WANEnable').get_attribute('checked'))
        print(WANEnable)
        if WANEnable == 'true':
            self.driver.find_element_by_name('WANEnable').click()
            ftpSmaba.click_save()
            time.sleep(1)
            ftpSmaba.click_NetworkSharing2()  # 点击网络共享子页面
            time.sleep(1)
            WANEnable = str(self.driver.find_element_by_name('WANEnable').get_attribute('checked'))
            self.assertEqual(WANEnable,'None', msg='允许wan口访问 关闭失败')
        #2）从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 ip变量赋值，页面读取
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        time.sleep(1)
        #3） 更改pc 交换机接口与wan口/上联口通
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
        # 重新获取地址
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
        time.sleep(2)
        #4）未开启验证无法登录
        user_name = "anonymous"
        pass_word = ""
        my_name = "anyname"
        domain_name = ""
        remote_smb_IP = WAN1_ip
        smb = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except ConnectionRefusedError:
            print('未开启samba 无法访问 验证通过')
        # 5）改为lan口 并重新获取地址
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
        p1 = subprocess.Popen('ping -n 2 -w 2 %s' % switchURL2, shell=True, stdout=subprocess.PIPE)
        # print('错误IP联网状态(ping通为0 不通为1):', p1.wait())  # ping通为0 不通为1
        ping = int(p1.wait())
        if ping == 0:
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
        time.sleep(3)
        #2 验证打开 ‘wan口访问’ 可以从wan口访问smaba
        #1）打开
        ftpSmaba = NetworkSharingPage(self.driver, self.url)
        ftpSmaba.click_NetworkSharing()
        time.sleep(1)
        ftpSmaba.click_NetworkSharing2()  # 点击网络共享子页面
        time.sleep(1)
        self.driver.find_element_by_name('WANEnable').click()
        ftpSmaba.click_save()
        time.sleep(1)
        WANEnable = self.driver.find_element_by_name('WANEnable').get_attribute('checked')
        self.assertEqual(WANEnable, 'true', msg='允许wan口访问 启用失败')
        #2) 更改pc 交换机接口与wan口/上联口通
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
        # 重新获取地址
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
        time.sleep(2)
        # 3）samba验证登陆
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        smb.close()

        self.driver.quit()
        logger.info('test_004_WanaAcess passed')

    def test_006_passwdAcessFTP(self):
        u'''启用/取消 密码访问ftp'''
        roleA = getAssertText('roleA')
        host = gettelnet('host')
        User = getweb('User')
        Passwd = getweb('Passwd')
        account = NetworkSharingPage(self.driver, self.url)
        account.click_AccountSettings()
        time.sleep(1)
        open_pswd = str(account.getAttribute_byId(account.open_pswds,'checked'))
        if open_pswd != 'true':
            account.click_open_pswd()
            time.sleep(2)
            open_pswd = str(account.getAttribute_byId(account.open_pswds, 'checked'))
        self.assertEqual(open_pswd,'true',msg='启用密码访问 开启失败')
        # 操作删除 以访已有规则
        account.click_allsel()
        time.sleep(0.2)
        account.click_delete()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            account.find_ok()
        except NoSuchElementException:
            try:
                account.find_tips_show_inf()
                time.sleep(1)
            except NoSuchElementException:
                pass
        except AttributeError:
            try:
                account.find_tips_show_inf()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('账号列表为空')
        # 新增一个账号
        account.click_add()
        time.sleep(1)
        account.input_username('1')
        account.input_passwd1('1')
        account.input_passwd2('1')
        authority = account.selelement_byName(account.authority)
        Select(authority).select_by_value('1')  # 0 读 1 读写
        account.click_add_modal()

        # self.driver.find_element_by_xpath('//*[@id="modal-add"]/div/div/div[3]/ul/li[1]/button').click()
        time.sleep(3)
        Acc3 = str(account.getText_byXpath(account.Acc3))
        auth3 = str(account.getText_byXpath(account.auth3))
        self.assertEqual(Acc3, '1', msg='新增账号失败')
        self.assertEqual(auth3, roleA, msg='新增账号权限失败')
        time.sleep(5)
        #ftp验证
        # ftp尝试使用无密码登录（应该失败）
        IP = host
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=21, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            print('启用密码访问后 ftp无密码无法登录 验证通过')
        else:
            raise Exception("启用密码访问后 ftp无密码依旧可以登录")
        ftp.quit()
        # ftp尝试使用admin登录
        try:
            ftp.connect(host=IP, port=21, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user=User,passwd=Passwd)  # admin账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        else:
            print("启用密码访问后 ftp使用admin可以登录")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()
        # ftp尝试使用guest登录
        try:
            ftp.connect(host=IP, port=21, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='guest', passwd='guest')  # guest账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        else:
            print("启用密码访问后 ftp使用修改过guest密码的账号可以登录")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()
        # ftp尝试使用新增账号1登录
        try:
            ftp.connect(host=IP, port=21, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='1', passwd='1')  # 新增账号密码
        except ftplib.error_perm:
            raise Exception("FTP账号密码验证错误")
        else:
            print("启用密码访问后 ftp使用新增账号可以登录")
        ftpFile = ftp.nlst('1')  # 获取指定目录下的文件
        print('ftpFile', ftpFile)
        ftp.quit()

        #取消密码访问
        account = NetworkSharingPage(self.driver, self.url)
        account.click_AccountSettings()
        time.sleep(1)
        account.click_open_pswd()
        time.sleep(10)
        open_pswd = str(account.getAttribute_byId(account.open_pswds, 'checked'))
        self.assertEqual(open_pswd, 'None', msg='启用密码访问 取消失败')
        # ftp尝试使用无密码登录
        ftp = ftplib.FTP()
        ftp.encoding = 'utf-8'
        try:
            ftp.connect(host=IP, port=21, timeout=5)
        except socket.error or socket.gaierror:
            raise Exception("无法访问FTP服务")
        try:
            ftp.login(user='anonymous')  # 相当于没有验证账号密码
        except ftplib.error_perm:
            raise Exception("取消密码访问后 ftp无密码无法登录")
        else:
            print('启用密码访问后 ftp无密码无法登录 验证通过')
        ftp.quit()

        # # 删除账号
        # account.click_listedit3()
        # time.sleep(1)
        # account.click_ok()
        # time.sleep(1)
        # list3_nodata = account.getText_byXpath(account.list3_nodata)
        # self.assertEqual(list3_nodata, ' ', msg='第3行账号删除失败')
        # print('账号删除')

        self.driver.quit()
        logger.info('test_005_passwdAcessFTP passed')

    def test_007_passwdAcessSAMBA(self):
        u'''启用/取消 密码访问samba'''
        host = gettelnet('host')
        User = getweb('User')
        Passwd = getweb('Passwd')
        account = NetworkSharingPage(self.driver, self.url)
        account.click_AccountSettings()
        time.sleep(1)
        open_pswd = str(account.getAttribute_byId(account.open_pswds, 'checked'))
        if open_pswd != 'true':
            account.click_open_pswd()
            time.sleep(2)
            open_pswd = str(account.getAttribute_byId(account.open_pswds, 'checked'))
        self.assertEqual(open_pswd, 'true', msg='启用密码访问 开启失败')
        time.sleep(5)
        # samba登录
        user_name = "anonymous"
        pass_word = ""
        my_name = "anyname"
        domain_name = ""
        remote_smb_IP = host
        #1 无密码登录（应该失败）
        smb = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        try:
            smb.listShares()
        except NotReadyError:
            print('启用密码访问后 samba无密码无法登录 验证通过')
        else:
            raise Exception('启用密码访问后 samba无密码依旧可以登录')
        smb.close()
        # 2 admin密码登录
        smb = SMBConnection(User, Passwd, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        try:
            smb.listShares()
        except NotReadyError:
            raise Exception('启用密码访问后 samba使用admin登录验证失败')
        smb.close()
        print('启用密码访问后 samba使用admin登录 验证通过')
        # 3 guest账号登录
        smb = SMBConnection('guest', 'guest', my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        try:
            smb.listShares()
        except NotReadyError:
            raise Exception('启用密码访问后 samba使用guest登录验证失败')
        smb.close()
        print('启用密码访问后 samba使用guest登录 验证通过')
        # 4 新增账号登录
        smb = SMBConnection('1', '1', my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        try:
            smb.listShares()
        except NotReadyError:
            raise Exception('启用密码访问后 samba使用新增账号登录验证失败')
        smb.close()
        print('启用密码访问后 samba使用新增登录 验证通过')

        #取消密码访问
        account.click_open_pswd()
        time.sleep(10)
        open_pswd = str(account.getAttribute_byId(account.open_pswds, 'checked'))
        self.assertEqual(open_pswd, 'None', msg='启用密码访问 取消失败')
        # samba无密码登录
        smb = SMBConnection(user_name, pass_word, my_name, domain_name, use_ntlm_v2=True)
        try:
            smb.connect(remote_smb_IP, 139, timeout=3)
        except socket.timeout:
            raise Exception('samba服务无法访问')
        try:
            smb.listShares()
        except NotReadyError:
            raise Exception('取消密码访问后 samba无密码无法登录')
        else:
            print('启用密码访问后 samba无密码登录 验证通过')
        smb.close()

        # 删除账号
        account.click_listdel3()
        time.sleep(1)
        account.click_ok()
        time.sleep(1)
        list3_nodata = account.getText_byXpath(account.list3_nodata)
        self.assertEqual(list3_nodata, ' ', msg='第3行账号删除失败')
        print('账号删除')

        self.driver.quit()
        logger.info('test_006_passwdAcessSAMBA passed')

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
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
