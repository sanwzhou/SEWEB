#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 17:35
#@swzhou
'''
附加测试
'''

import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb
from common.loginRoute import login
from pages.AdditionalTestPage import AdditionalTestPage
from test_case.sysConfig_009_Reboot import Reboot
logger = LogGen(Logger = 'AdditionalTest').getlog()


class AdditionalTest(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_closeWAN60023(self):
        u'''关闭WAN口60023'''

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
        tn.write(b'ps | grep telnetd | grep -v grep' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断

        if ("telnetd -b %s " % hostip) in result:
            print('telnetd默认未仅对lan口开放 验证成功')
        else:
            CapPic(self.driver)
            logger.info(u'result：%s' % result)
            raise Exception('telnetd默认未仅对lan口开放 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        additionalTest = AdditionalTestPage(self.driver,self.url)
        # 打开uttCli页面
        self.driver.get(additionalTest.aspUrl)
        time.sleep(1)
        additionalTest.click_deleteall()
        time.sleep(1)
        self.driver.switch_to.alert.accept()# 接受警告框
        time.sleep(1)
        #输入命令
        additionalTest.input_addCommand('killall telnetd')
        time.sleep(1)
        additionalTest.click_add()
        time.sleep(1)
        additionalTest.input_addCommand('telnetd')
        time.sleep(1)
        additionalTest.click_add()
        time.sleep(10)

        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ps | grep telnet | grep -v grep' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if ("telnetd -b %s " % hostip) not in result:
            #已经可以tlenet证明进程已经在了，区别不是默认的针对lan口
            print('打开telnetd 验证成功')
        else:
            CapPic(self.driver)
            logger.info(u'telnetd开启 验证失败')
            logger.info(u'result：%s' % result)
            raise Exception('telnetd开启 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        #清除命令并重启
        additionalTest = AdditionalTestPage(self.driver, self.url)
        additionalTest.click_deleteall()
        time.sleep(1)
        self.driver.switch_to.alert.accept()  # 接受警告框
        time.sleep(1)
        self.driver.quit()
        Reboot.test_reboot1(self)

        # 判断telnet ，不能通则报错
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        if tn:
            print('telnet可以通')

        logger.info('test_001_closeWAN60023 passed')

    def test_002_uttWaitSerch(self):
        u'''验证 自动激活保修期'''
        time.sleep(60)#001中刚重启好，进程可能没有完全启动完毕，等待一下
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
        tn.write(b'ps | grep uttWaitSerch | grep -v grep' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "uttWaitSerch -f" in result:
            print('success')
        else:
            raise Exception('自动激活保修期 验证失败')  #如果没有则报错

        tn.close()  # tn.write('exit\n')
        logger.info('test_002_uttWaitSerch passed')

    def test_003_MTKlibuClibc(self):
        u'''验证 MTK确认库版本升级'''
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
        tn.write(b'ls /lib/|grep libuClibc | grep -v grep' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "libuClibc-0.9.33.2.so" in result:
            print('success')
        else:
            raise Exception('MTK确认库版本升级 验证失败')  # 如果没有则报错

        tn.close()  # tn.write('exit\n')
        logger.info('test_003_MTKlibuClibc passed')

    def test_004_X86_CONFIG4KSTACKS(self):
        u'''验证 X86设备内核CONFIG_4KSTACKS关闭'''
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
        tn.write(b'cat /sbin/config.sh | grep CONFIG_4KSTACKS' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "CONFIG_4KSTACKS=y" not in result:
            print('X86设备内核CONFIG_4KSTACKS已关闭')
        else:
            raise Exception('X86设备内核CONFIG_4KSTACKS未关闭')  # 如果没有则报错

        tn.close()  # tn.write('exit\n')
        logger.info('test_004_X86_CONFIG4KSTACKS passed')

    def test_005_cloundDownloadFile(self):
        u'''验证 支持云管理检测下发新版本'''
        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'cat  /sbin/lua/Router/genMqttPak.lua | grep DownloadFile' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if "function DownloadFile(msg)" in result:
            print('设备支持云管理检测下发新版本')
        else:
            raise Exception('设备支持云管理检测下发新版本方法未存在')  # 如果没有则报错

        tn.close()  # tn.write('exit\n')
        logger.info('test_005_cloundDownloadFile passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
