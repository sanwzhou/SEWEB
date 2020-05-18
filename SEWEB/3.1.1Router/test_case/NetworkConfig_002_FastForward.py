#! -*-conding:utf-8 -*-
#@Time: 2019/3/8 0008 11:30
#@swzhou
'''
快速转发
'''

import time
import unittest
import os.path
import telnetlib
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import gettelnet,getweb,getParameter
from common.GetExcelValue import getExcelValue
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'NetworkConfig_002_FastForward').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
hwNatP = getExcelValue(getParameter('hwNatP'))
# print('hwNatP:',hwNatP)


hostip = gettelnet('host')
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")

class PortRate(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wanpage = NetworkConfig_wanpage(self.driver,self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_GlobalConfig()
        time.sleep(1)
        # pass

    def test_001_hwNat(self):
        u'''硬件转发 '''
        wanpage = NetworkConfig_wanpage(self.driver, self.url)

        # 默认自动模式
        enable1 = wanpage.getAttribute_byXpath(wanpage.enable1, 'selected')
        enable2 = wanpage.getAttribute_byXpath(wanpage.enable2, 'selected')
        # print('enable1:', enable1,'enable2:', enable2,)
        if enable1 != 'true':
            logger.info(u'快速转发模式开关默认不为自动')
            CapPic(self.driver)
            raise Exception(u'快速转发模式开关默认不为自动')
        if enable2 != 'true':
            logger.info(u'模式开关默认不为硬件转发')
            CapPic(self.driver)
            raise Exception(u'模式开关默认不为硬件转发')
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        if 'fast_classifier ' in result1 and 'shortcut_fe ' in result1 and 'No such file or directory' in result1:
            print(u'自动模式 模块及转发文件正常')
        else:
            logger.info(u'自动模式 模块or转发文件 异常')
            raise Exception(u'自动模式 模块or转发文件 异常')

        # 开启
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('NatOpen')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(6)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        lsmod = ['hw_nat', 'ls: /sys/fast_classifier: No such file or directory']
        if all(x in result1 for x in lsmod):
            print(u'开启模式 模块及转发文件正常')
        else:
            logger.info(u'开启模式 模块or转发文件 异常')
            raise Exception(u'开启模式 模块or转发文件 异常')

        # 关闭
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('0')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(5)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        lsmod = ['fast_classifier ', 'shortcut_fe ', 'exceptions', 'skip_to_bridge_ingress', 'debug_info',
                 'offload_at_pkts','hw_nat']
        if all(x not in result1 for x in lsmod):
            print(u'关闭模式 模块及转发文件正常')
        else:
            logger.info(u'关闭模式 模块or转发文件 异常')
            raise Exception(u'关闭模式 模块or转发文件 异常')

        # 改回自动
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('NatAuto')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(5)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        if 'fast_classifier ' in result1 and 'shortcut_fe ' in result1 and 'No such file or directory' in result1:
            print(u'自动模式 模块及转发文件正常')
        else:
            logger.info(u'自动模式 模块or转发文件 异常')
            raise Exception(u'自动模式 模块or转发文件 异常')

        logger.info('test_001_changePortRateLAN passed')

    def test_002_sfNat(self):
        u'''软件转发 '''
        wanpage = NetworkConfig_wanpage(self.driver, self.url)

        #页面上还有硬件转发,改成软件转发模式
        if hwNatP == '√':
            FastForwardMode = wanpage.selelement_byName('FastForwardMode')
            Select(FastForwardMode).select_by_value('sfNat')
            wanpage.click_save()
            time.sleep(2)
            # 等待弹窗提示成功
            i = 0
            while i < 80:
                try:
                    self.driver.implicitly_wait(1)
                    wanpage.find_tipsshowin()
                except NoSuchElementException:
                    time.sleep(1)
                    i = i + 1
                    print(i)
                else:
                    tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                    print(tips, i)
                    if tips != 'success':
                        CapPic(self.driver)
                        logger.info(u'模式选择保存 异常')
                        raise Exception(u'模式选择保存 异常')
                    break
            else:
                raise Exception(u'模式选择保存 未弹出提示框')

        #默认自动模式
        enable1 = wanpage.getAttribute_byXpath(wanpage.enable1,'selected')
        # print('enable1:',enable1)
        if enable1 != 'true':
            logger.info(u'快速转发模式开关默认不为自动')
            CapPic(self.driver)
            raise Exception(u'快速转发模式开关默认不为自动')
        else:
            # 查看后台文件
            tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 获取WAN口对应接口名称
            result1 = str(result[3:-7])
            print(result1)
            if 'fast_classifier ' in result1 and 'shortcut_fe ' in result1 and 'No such file or directory' in result1:
                print(u'自动模式 模块及转发文件正常')
            else:
                logger.info(u'自动模式 模块or转发文件 异常')
                raise Exception(u'自动模式 模块or转发文件 异常')

        #开启
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('NatOpen')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(6)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        lsmod = ['fast_classifier ','shortcut_fe ','exceptions','skip_to_bridge_ingress','debug_info','offload_at_pkts']
        if all(x in result1 for x in lsmod):
            print(u'开启模式 模块及转发文件正常')
        else:
            logger.info(u'开启模式 模块or转发文件 异常')
            raise Exception(u'开启模式 模块or转发文件 异常')

        # 关闭
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('0')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(5)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        lsmod = ['fast_classifier ', 'shortcut_fe ', 'exceptions', 'skip_to_bridge_ingress', 'debug_info',
                 'offload_at_pkts']
        if all(x not in result1 for x in lsmod):
            print(u'关闭模式 模块及转发文件正常')
        else:
            logger.info(u'关闭模式 模块or转发文件 异常')
            raise Exception(u'关闭模式 模块or转发文件 异常')

        # 改回自动
        FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
        Select(FastForwardEnable).select_by_value('NatAuto')
        wanpage.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wanpage.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'极速模式保存 异常')
                    raise Exception(u'极速模式保存 异常')
                break
        else:
            raise Exception(u'极速模式保存 未弹出提示框')
        time.sleep(5)
        # 查看后台文件
        tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'lsmod ;ls -l /sys/fast_classifier' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = str(result[3:-7])
        print(result1)
        if 'fast_classifier ' in result1 and 'shortcut_fe ' in result1 and 'No such file or directory' in result1:
            print(u'自动模式 模块及转发文件正常')
        else:
            logger.info(u'自动模式 模块or转发文件 异常')
            raise Exception(u'自动模式 模块or转发文件 异常')

        logger.info('test_002_sfNat passed')

    def tearDown(self):
        #修改回默认 以访中间出错
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        save = 0
        enable1 = wanpage.getAttribute_byXpath(wanpage.enable1, 'selected')
        if hwNatP == '√':  # 包含硬件转转发开关
            if enable1 != 'true':
                FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
                Select(FastForwardEnable).select_by_value('NatAuto')
                save = 1
            enable2 = wanpage.getAttribute_byXpath(wanpage.enable2, 'selected')
            if enable2 != 'true':
                FastForwardMode = wanpage.selelement_byName('FastForwardMode')
                Select(FastForwardMode).select_by_value('hwNat')
                save = 1
        else:
            if enable1 != 'true':
                FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
                Select(FastForwardEnable).select_by_value('NatAuto')
                save = 1
        if save == 1:
            wanpage.click_save()
            time.sleep(2)
            # 等待弹窗提示成功
            i = 0
            while i < 80:
                try:
                    self.driver.implicitly_wait(1)
                    wanpage.find_tipsshowin()
                except NoSuchElementException:
                    time.sleep(1)
                    i = i + 1
                    print(i)
                else:
                    tips = str(wanpage.getAttribute_byClass(wanpage.tipsshowin, 'tip-sign'))
                    print(tips, i)
                    if tips != 'success':
                        CapPic(self.driver)
                        logger.info(u'极速模式保存 异常')
                        raise Exception(u'极速模式保存 异常')
                    break
            else:
                raise Exception(u'极速模式保存 未弹出提示框')
            time.sleep(2)
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

    if __name__ == '__main__':
        unittest.main()