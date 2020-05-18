#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 15:10
#@swzhou
'''
语言选择
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
logger = LogGen(Logger = 'sysConfig_005_language').getlog()


class Language(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        language = ManagementPolicyPage(self.driver,self.url)
        self.driver.implicitly_wait(10)
        #进入系统配置-网管策略-语言选择
        language.click_sysConfig()
        time.sleep(0.5)
        language.click_ManagementPolicy()
        time.sleep(1)
        language.click_Language()
        time.sleep(1)
        # pass

    def test_001_language(self): #待后续调整，目前只有一个
        u'''网管策略 语言管理'''
        languageA = getAssertText('languageA')
        language = ManagementPolicyPage(self.driver, self.url)
        #判断语言 显示
        languageText=str(language.getText_byXpath(language.languageText))
        self.assertEqual(languageText,languageA,msg='语言 显示字符异常')
        self.driver.quit()
        logger.info('test_001_language passed')

    # def test_002_language(self): #页面上方
    #     u'''页面上方 语言'''
    #     languageA = getAssertText('languageA')
    #     language = ManagementPolicyPage(self.driver, self.url)
    #     #判断语言 显示
    #     languageText=str(language.getText_byXpath(language.languageText))
    #     self.assertEqual(languageText,languageA,msg='语言 显示字符正常')
    #     self.driver.quit()

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

