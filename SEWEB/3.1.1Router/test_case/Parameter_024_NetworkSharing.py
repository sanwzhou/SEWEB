#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 17:30
#@swzhou
'''
网络共享
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getParameter
from common.GetExcelValue import getExcelValue
from pages.NetConfig_008_NetworkSharingPage import NetworkSharingPage
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
logger = LogGen(Logger = 'Parameter_024_NetworkSharing').getlog()

class NetworkSharing(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        networkshare = NetworkSharingPage(self.driver,self.url)
        networkshare.click_netConfig()
        time.sleep(0.5)
        # pass

    def test_001_NetworkSharing(self):
        u'''网络共享&FTP服务器（某些设备可能不支持）'''
        netShareP = getParameter('netShareP')
        Support = getExcelValue(netShareP)
        networkshare = NetworkSharingPage(self.driver, self.url)
        if Support == '√':
            logger.info(u'参数支持网络共享')
            try:
                self.driver.implicitly_wait(2)
                networkshare.find_NetworkSharing()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持 网络共享，与参数表不符')
                raise Exception('软件不支持 网络共享，与参数表不符')
            else:
                logger.info(u'软件支持网络共享，与参数表相符')
                self.driver.implicitly_wait(10)
                time.sleep(1)
                # 开/关访问控制
                enableDevice = networkshare.getAttribute_byId(networkshare.enableDevices, 'checktype')  # checktype 0未开启，1开启
                self.assertEqual(enableDevice, '0', msg='网络共享 默认未关闭')
                networkshare.click_enableDevice()
                time.sleep(2)
                enableDevice = networkshare.getAttribute_byId(networkshare.enableDevices, 'checktype')
                self.assertEqual(enableDevice, '1', msg='网络共享 开启失败')
                networkshare.click_enableDevice()
                time.sleep(2)
                enableDevice = networkshare.getAttribute_byId(networkshare.enableDevices, 'checktype')
                self.assertEqual(enableDevice, '0', msg='网络共享 关闭失败')
                # U盘使用率
                UsageRate = networkshare.getText_byXpath(networkshare.UsageRate)
                self.assertIn('%', UsageRate, msg='U盘使用率 显示异常')
                # U盘总容量 已使用容量 剩余容量 三个值+提示是一个元素,判断条件特殊
                # U盘总容量 后元素（所有）
                Total = networkshare.getText_byXpath(networkshare.Total)
                # “已使用容量”提示
                Usedtext = networkshare.getText_byXpath(networkshare.Usedtext)
                Usedtext1 = 'M' + Usedtext
                # “剩余容量”提示
                Residualtext = networkshare.getText_byXpath(networkshare.Residualtext)
                Residualtext1 = 'M' + Residualtext
                if Usedtext1 in Total and Residualtext1 in Total:
                    print('U盘总容量信息 显示正常')
                else:
                    raise Exception('U盘总容量信息 显示异常')
                #弹出设备
                networkshare.find_Eject()

                # 账号设置
                networkshare.click_AccountSettings()
                time.sleep(1)
                networkshare.click_open_pswd()
                time.sleep(2)
                networkshare.find_add()
                networkshare.find_delete()
                # admin账号
                adminuser = str(networkshare.getText_byXpath(networkshare.adminuser))
                self.assertEqual(adminuser, 'admin', msg='admin账号有误')
                guestuser = str(networkshare.getText_byXpath(networkshare.guestuser))
                self.assertEqual(guestuser, 'guest', msg='guest账号有误')

                #网络共享
                networkshare.click_NetworkSharing2()
                time.sleep(1)
                networkshare.click_choosml()
                time.sleep(1)
                networkshare.input_names('test')
                networkshare.click_modal_hide()
                time.sleep(0.5)
                networkshare.click_ftpEn()
                networkshare.input_ftpport('222')
                networkshare.click_WANEnable()
                try:
                    self.driver.implicitly_wait(2)
                    networkshare.find_sambaEn() # 启用SAMBA
                except ElementNotVisibleException:
                    raise Exception('sambaEn 页面无显示')
        elif Support == '×':
            logger.info(u'参数不支持网络共享')
            try:
                self.driver.implicitly_wait(2)
                networkshare.find_NetworkSharing()
            except NoSuchElementException:
                logger.info(u'软件不支持网络共享，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持网络共享，与参数表不符')
                raise Exception(u'软件支持网络共享，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_001_NetworkSharing passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
