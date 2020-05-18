#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 13:29
#@swzhou
'''
电子通告：开启功能，首次访问外网会接收到通告，上网业务正常
'''


import time
import unittest
from selenium import webdriver
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.actionManage_004_ElectronicsNoticePage import ElectronicsNoticePage
logger = LogGen(Logger = 'actionManage_005_ElectronicsNotice').getlog()
httpWebUrl = getAssertText('httpWebUrl')

class ElectronicsNotice(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_ElectronicsNotice(self):
        u'''电子通告：首次访问外网会接收到通告'''
        message = getAssertText('ElectronicsNotice')
        httptitle = getAssertText('httptitle')
        # 打开行为管理 - 电子通告
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        electronicsNotice = ElectronicsNoticePage(self.driver,self.url)
        electronicsNotice.click_BehaviorManagement()
        time.sleep(0.5)
        electronicsNotice.click_ElectronicsNotice()
        time.sleep(1)
        #开启电子通告
        electronicsNotice.input_rulename('EleNoticetest1')
        electronicsNotice.click_swEn()
        electronicsNotice.click_save()
        time.sleep(1)

        # 断言 提示信息是否有误
        time.sleep(1)
        status = str(electronicsNotice.getAttribute_byXpath(electronicsNotice.swEs,'checked'))
        time.sleep(1)
        print(status)
        self.assertEqual(status,'true',msg='电子通告开启出错')
        self.driver.quit()
        print('电子通告开启 成功')

        time.sleep(5)
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        #打开网页测试
        self.driver.get('http://' + httpWebUrl + '/')
        time.sleep(1)
        title1=self.driver.title
        print(title1)
        self.assertEqual(title1, message, msg='未跳转到 电子通告页面')
        time.sleep(1)
        self.driver.get('http://' + httpWebUrl + '/')
        time.sleep(1)
        title2 = self.driver.title
        print(title2)
        self.assertIn(httptitle,title2, msg='通告第二次未跳转到正确页面')
        self.driver.quit()
        logger.info('test_ElectronicsNotice passed')

    def tearDown(self):
        # 关闭电子通告
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        electronicsNotice = ElectronicsNoticePage(self.driver, self.url)
        electronicsNotice.click_BehaviorManagement()
        time.sleep(0.5)
        electronicsNotice.click_ElectronicsNotice()
        time.sleep(1)
        electronicsNotice.click_swC()
        electronicsNotice.click_save()
        time.sleep(1)

        # 断言 提示信息是否有误
        status = str(electronicsNotice.getAttribute_byXpath(electronicsNotice.swCs,'checked'))
        time.sleep(1)
        self.assertEqual(status, 'true', msg='电子通告开启出错')
        self.driver.quit()
        print('电子通告关闭 成功')
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()
