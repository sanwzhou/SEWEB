#! -*-conding:utf-8 -*-
#@Time: 2019/1/24 0024 14:22
#@swzhou
'''
U盘挂载、卸载、弹出
'''

import time
import telnetlib
import unittest
from common.LogGen import LogGen
from common.ReadConfig import gettelnet,getweb
from common.loginRoute import login
from pages.NetConfig_008_NetworkSharingPage import NetworkSharingPage
logger = LogGen(Logger = 'NetworkSharing_001_UdiskMount').getlog()

class UdiskMount(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        sharing = NetworkSharingPage(self.driver,self.url)
        # 打开网络配置-网络共享
        sharing.click_netConfig()
        time.sleep(0.5)
        sharing.click_NetworkSharing()
        time.sleep(1)
        # pass

    def test_001_Mount(self):
        u'''U盘挂载 显示'''

        sharing = NetworkSharingPage(self.driver, self.url)
        # U盘使用率
        UsageRate = sharing.getText_byXpath(sharing.UsageRate)
        self.assertIn('%',UsageRate,msg='U盘使用率 显示异常')
        # U盘总容量 已使用容量 剩余容量 三个值+提示是一个元素,判断条件特殊
        # U盘总容量 后元素（所有）
        Total = sharing.getText_byXpath(sharing.Total)
        # “已使用容量”提示
        Usedtext = sharing.getText_byXpath(sharing.Usedtext)
        Usedtext1 = 'M' + Usedtext
        # “剩余容量”提示
        Residualtext = sharing.getText_byXpath(sharing.Residualtext)
        Residualtext1 = 'M' + Residualtext
        if Usedtext1 in Total and Residualtext1 in Total:
            print('U盘总容量信息 显示正常')
        else:
            raise Exception('U盘总容量信息 显示异常')
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
        tn.write(b'mount | grep /media/' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 后台实际应有的结果
        result1 = 'codepage'
        result2 = 'iocharset=utf8'
        # 判断
        if result1 in result and result2 in result:
            print('挂载mount显示 验证成功')
        else:
            raise Exception('挂载mount显示 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_001_Mount passed')

    def test_002_unMount(self):
        u'''U盘弹出 显示'''

        sharing = NetworkSharingPage(self.driver, self.url)
        # 弹出设备
        sharing.click_Eject()
        time.sleep(1)
        sharing.click_ok()
        time.sleep(2)
        #弹出后使用率、容量等都为0
        # U盘使用率
        UsageRate = sharing.getText_byXpath(sharing.UsageRate)
        self.assertEqual(UsageRate, '0', msg='弹出后U盘使用率 显示异常')
        # U盘总容量 已使用容量 剩余容量 三个值+提示是一个元素,判断条件特殊
        # U盘总容量 后元素（所有）
        Total = sharing.getText_byXpath(sharing.Total)
        # “已使用容量”提示
        Usedtext = sharing.getText_byXpath(sharing.Usedtext)
        # “剩余容量”提示
        Residualtext = sharing.getText_byXpath(sharing.Residualtext)
        Total1 = '0' + Usedtext + ' 0' + Residualtext + ' 0'
        if Total == Total1:
            print('弹出后U盘总容量信息 显示正常')
        else:
            raise Exception('弹出后U盘总容量信息 显示异常')
        # 连接Telnet服务器
        hostip = gettelnet('host')
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
        tn.write(b'mount | grep /media/' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 后台实际应有的结果
        result1 = 'codepage=cp437,iocharset=utf8'
        # 判断
        if result1 not in result:
            print('卸载后mount显示 验证成功')
        else:
            raise Exception('卸载后mount显示 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_002_unMount passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

