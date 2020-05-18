#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 9:38
#@swzhou
'''
黑名单中的用户不能访问网络
更换电脑需要注意 修改绑定的mac地址
'''
import subprocess
import time
import unittest
import os.path
import socket

from selenium.common.exceptions import NoSuchElementException

from common.LogGen import LogGen
from common.ReadConfig import getAssertText
from common.pingTest import pingTestIP
from common.loginRoute import login
from pages.Organization_004_userBlackpage import Organization_userBlackPage
logger = LogGen(Logger = 'Members_005_blacklist').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'

class blacklist(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_blacklist(self):
        u'''黑名单用户禁止上网'''
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        blacklist = Organization_userBlackPage(self.driver,self.url)
        # 打开用户管理 - 组织成员
        blacklist.click_UserManage()
        time.sleep(0.5)
        blacklist.click_blacklist()
        time.sleep(1)

        # 操作删除 以访已有规则
        blacklist.click_selall()
        time.sleep(0.2)
        blacklist.click_delall()
        time.sleep(2)
        try:
            self.driver.implicitly_wait(2)
            blacklist.find_ok()
        except NoSuchElementException:
            try:
                blacklist.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('ipsec VPN列表为空')

        blacklist.click_add()
        time.sleep(0.5)
        blacklist.input_bname('blicklistTest')
        blacklist.input_bmac('107B44AAAAAA') #mac为不能上网的mac，非实际pc的mac 要与changeMacToBack.bat中mac地址一致
        blacklist.click_save()
        time.sleep(1)
        # 断言 增加的组名称是否相同：相同代表验证通过
        bilcklist_name = str(blacklist.getText_byXpath(blacklist.blicklist_name))
        self.assertEqual(bilcklist_name, 'blicklistTest', msg='新增黑名单出错 用户名不一致')
        bilcklist_mac = str(blacklist.getText_byXpath(blacklist.blicklist_mac))
        self.assertEqual(bilcklist_mac,'10:7b:44:aa:aa:aa', msg='新增黑名单出错 MAC不一致')
        print('新增黑名单用户 完成')
        pingTestIP('www.baidu.com') #避免判断失误
        # 判断联网 ，不能上网则报错
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')

        # 修改MAC为 黑名单中绑定的MAC地址
        # 调用bat脚本
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
                print('IP地址已自动获取成功1', n)
                break
        else:
            # raise Exception('未获取到地址1')
            # 开启绑定情况下 仅更改mac 可能会获取不到地址
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
        time.sleep(3)
        # 判断联网 ,测试该项改完mac之后前几个包有可能可以ping通，为避免判断失误，加一个缓冲
        pingTestIP('www.baidu.com')#避免判断失误
        pingTestIP('www.163.com')#避免判断失误
        time.sleep(2)
        #判断联网 ,黑名单中绑定的用户应该不能上网
        p = pingTestIP('www.sina.com.cn')
        if p == 'Y':
            raise Exception('黑名单中用户依旧可以上网')
        print('黑名单用户不能上网 验证成功')

        time.sleep(1)
        #将mac改回
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
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
            raise Exception('未获取到地址')
        pingTestIP('www.baidu.com')  # 避免判断失误
        pingTestIP('www.163.com')  # 避免判断失误
        time.sleep(2)
        # 判断联网 ，不能上网则报错
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')

        logger.info('test_blacklist passed')

    def tearDown(self):
        nodata = getAssertText('nodata')
        # 判断联网 ，不能则改回mac
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            # 将mac改回
            # 调用bat脚本
            os.system('%s' % (batpath + 'changeMacToBack.bat'))
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
                raise Exception('未获取到地址')
        # 删除黑名单绑定
        blacklist = Organization_userBlackPage(self.driver, self.url)
        blacklist.click_delete()
        time.sleep(1)
        blacklist.click_ok()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        listtips = str(blacklist.getText_byXpath(blacklist.list_tips))
        time.sleep(1)
        self.assertEqual(listtips,nodata, msg='黑名单用户删除失败')
        print('黑名单用户已删除')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
