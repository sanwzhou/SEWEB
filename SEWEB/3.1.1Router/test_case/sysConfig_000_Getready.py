#! -*-conding:utf-8 -*-
#@Time: 2019/1/21 0018 13:55
#@swzhou
'''
恢复出厂 && 第一次登录 ： 放在所有测试之前，未后续测试做准备
'''

import time
import unittest
from common.LogGen import LogGen
from common.loginRoute import login
from common.ReadConfig import getAssertText,getweb
from common.pingTest import pingTestIP
from pages.sysConfig_002_sysTimePage import sysTimePage
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from test_case.sysConfig_008_configuration import configuration
logger = LogGen(Logger = 'sysConfig_000_Getready').getlog()

class Getready(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')

    def test_resertFirstLogin(self):
        u'''准备工作：清理windows进程 &&恢复出厂 && 第一次登录'''
        configuration.test_002_Resert(self)
        print('第一次登录已完成')
        logger.info('test_resertFirstLogin passed')

    def test_001_ntpClockServer(self):
        u'''时钟管理'''
        ntpServer = getweb('ntpServer')
        i = 0
        while i < 80:
            p = pingTestIP('www.baidu.com')
            if p != 'Y':
                time.sleep(1)
            else:
                break
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        config = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护
        config.click_sysConfig()
        time.sleep(0.5)
        config.click_Maintenance()
        time.sleep(1)
        TimeInternetA = getAssertText('TimeInternetA')
        sysTime = sysTimePage(self.driver,self.url)

        sysTime.click_SystemTime()
        time.sleep(1)
        switch = str(sysTime.getAttribute_byXpath(sysTime.SntpEns,'checked'))
        tips = str(sysTime.getText_byXpath(sysTime.withInternet1))
        self.assertEqual(switch, 'true', msg='网络时间同步 默认开启 有误')
        self.assertEqual(tips, TimeInternetA, msg='网络时间同步 按钮有误')
        #判断页面时间 日期
        dates = sysTime.getText_byID(sysTime.dates)
        now = time.strftime("%Y-%m-%d")
        if dates != now: #判断默认配置下是否能同步 不同同步则更改ntp server使同步 同时报默认不能同步错
            sysTime.input_NTPServerIP(ntpServer)
            sysTime.click_save()
            time.sleep(2)
            i = 0
            while i< 20:
                sysTime.click_SystemTime()
                time.sleep(1)
                dates = sysTime.getText_byID(sysTime.dates)
                if dates == now:
                    break
                else:
                    i +=1
            else:
                raise Exception('时间不同步，输入新ntp sever依旧不能更新')
            raise Exception('默认配置下ntp 时间不同步')


        self.driver.quit()
        logger.info('test_001_ntpClockServer passed')

    def tearDown(self):
        # self.dr.close()
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
