#! -*-conding:utf-8 -*-
#@Time: 2019/1/22 0022 13:27
#@swzhou
'''
测试重启 2种
'''

import time
import unittest
from common.LogGen import LogGen
logger = LogGen(Logger = 'sysConfig_009_Reboot').getlog()
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.sysConfig_003_MaintenancePage import MaintenancePage

class Reboot(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_reboot1(self):
        u'''重启 - 页面上方'''
        WillReboottips = getAssertText('WillReboottips')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        reboot = MaintenancePage(self.driver,self.url)
        reboot.click_headerReboot()
        time.sleep(0.5)
        reboot.click_ok()
        time.sleep(2)
        tips = str(reboot.getText_byClass(reboot.u_tim_str))
        self.assertEqual(tips,WillReboottips,msg='点击页面上方重启 操作失败')
        #设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i <20:
            now_url=str(self.driver.current_url)
            # print(now_url,i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        else:
            raise Exception('设备重启未正常启动')

        self.driver.quit()

        #待重启后验证 登录是否正常
        login.loginWeb(self) #admin账号登录
        time.sleep(1)
        self.driver.quit()
        logger.info('test_reboot1 passed')

    def test_reboot2(self):
        u'''重启 - 系统维护页面''' #系统配置-系统维护-重启设备 页面的重启
        WillReboottips = getAssertText('WillReboottips')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        reboot = MaintenancePage(self.driver, self.url)
        reboot.click_sysConfig()
        time.sleep(0.5)
        reboot.click_Maintenance()
        time.sleep(1)
        reboot.click_RebootDevice()
        time.sleep(1)
        reboot.click_reboot()
        time.sleep(1)
        reboot.click_ok()
        time.sleep(1)
        tips = str(reboot.getText_byClass(reboot.u_tim_str))
        self.assertEqual(tips, WillReboottips, msg='点击页面上方重启 操作失败')
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            # print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1

        self.driver.quit()

        #待重启后验证 登录是否正常
        login.loginWeb(self) #admin账号登录
        time.sleep(1)
        self.driver.quit()
        print('系统维护页面 设备重启 验证通过')
        logger.info('test_reboot2 passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
