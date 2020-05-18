#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 11:46
#@swzhou
'''
UPNP功能：会新建对应的静态映射
'''

import os
import time
import unittest
import win32process

from selenium.common.exceptions import NoSuchElementException

from common.CapPic import CapPic
from common.loginRoute import login
from pages.PortMapping_001_UPNPpage import UPNPpage
from common.LogGen import LogGen
logger = LogGen(Logger = 'PortMapping_001_UPNP').getlog()

class UPNP(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_UPNP(self):
        u'''UPnP自动添加映射'''
        # Thunderpath = str(getpath('Thunderpath'))
        # print('13',Thunderpath)
        # Thunderpath1 = '%s' % Thunderpath
        #关闭 迅雷进程
        os.system('taskkill /im "Thunder.exe" /F')
        time.sleep(2)

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        upnp = UPNPpage(self.driver,self.url)
        upnp.click_NetworkConfig()
        time.sleep(0.5)
        upnp.click_portMapping()
        time.sleep(1)
        upnp.click_UPnP()
        time.sleep(1)
        # 开启UPNP
        switch0 = upnp.getAttribute_byId(upnp.checkOn,'checktype')  # checktype 0未开启，1开启
        if switch0 == '0':
            upnp.click_checkOnc()
            time.sleep(2)
        print('UPnP 已开启')

        # 打开迅雷
        handle = win32process.CreateProcess('D:\\Program Files (x86)\\Thunder Network\\Thunder\\Program\\Thunder.exe', '', None,
                                            None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())  # 打开迅雷，获得其句柄

        #断言
        time.sleep(5)
        i = 0
        while i < 30:
            upnp.click_refreshTable()
            time.sleep(1)
            try:
                list_tips1 = upnp.getText_byXpath(upnp.list_tips1)
                print('list_1protocol:', list_tips1)
            except NoSuchElementException:
                time.sleep(1)
                i += 1
            else:
                if "TCP" or 'UDP'  in str(list_tips1):
                    print("UPnP自动添加映射 验证通过 %s" % i)
                else:  # 未有规则生成
                    raise Exception('UPnP自动添加映射 验证失败')
                break

        # 关闭UPNP
        switch1 = upnp.getAttribute_byId(upnp.checkOn,'checktype')  # checktype 0未开启，1开启
        if switch1 == '1':
            upnp.click_checkOnc()
            time.sleep(2)
        print('UPnP 已关闭')

        self.driver.quit()

        win32process.TerminateProcess(handle[0], 0) #关闭迅雷
        logger.info('test_UPNP passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()



