#! -*-conding:utf-8 -*-
#@Time: 2019/1/22 0022 13:45
#@swzhou
'''
策略库升级：升级后策略库应用可识别，应用优先模板正确
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from pages.TrafficManagement_001_AppPriorityPage import AppPriorityPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'sysConfig_007_policylibAppTemp').getlog()

class policylibAppTemp(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_policylib(self):
        u'''应用特征库'''
        policylibsucess = getAssertText('policylibsucess') #更新成功
        notdetected = getAssertText('notdetected') #未检测到更新版本
        NewVersionDetected = getAssertText('NewVersionDetected') #检测到新版本
        DetectedFailed = getAssertText('DetectedFailed') #检测失败

        policylib = MaintenancePage(self.driver,self.url)
        #进入系统配置-系统维护-应用特征库
        policylib.click_sysConfig()
        time.sleep(0.5)
        policylib.click_Maintenance()
        time.sleep(1)
        policylib.click_policylib()
        time.sleep(10)
        showState = policylib.getText_byID(policylib.showState)
        strategyName = policylib.getText_byName(policylib.strategyName)
        if showState == policylibsucess:
            print('已更新成功')
        elif showState == notdetected:
            self.assertNotEqual(strategyName,'1.0')
            print(showState,strategyName,'特征库版本已经更新过')
        elif NewVersionDetected in showState :
            policylib.click_onkeyup()
            time.sleep(7)
            showState2 = policylib.getText_byID(policylib.showState)
            strategyName2 = policylib.getText_byName(policylib.strategyName)
            if showState2 == policylibsucess:
                if float(strategyName2) > float(strategyName) :
                    print('更新成功')
            else:
                raise Exception('更新失败')
        elif DetectedFailed in showState :
            policylib.click_recheck()
            time.sleep(10)
            showState = policylib.getText_byID(policylib.showState)
            strategyName = policylib.getText_byName(policylib.strategyName)
            if showState == policylibsucess:
                print('已更新成功')
            elif showState == notdetected:
                self.assertNotEqual(strategyName, '1.0')
                print(showState, strategyName, '特征库版本已经更新过')
            elif NewVersionDetected in showState:
                policylib.click_onkeyup()
                time.sleep(7)
                showState2 = policylib.getText_byID(policylib.showState)
                strategyName2 = policylib.getText_byName(policylib.strategyName)
                if showState2 == policylibsucess:
                    if float(strategyName2) > float(strategyName):
                        print('更新成功')
                else:
                    raise Exception('更新失败')
            elif DetectedFailed in showState:
                logger.info(showState, strategyName, u'检测失败')
                CapPic(self.driver)
                raise Exception('检测失败2')
            else:
                logger.info(showState, strategyName, u'检测失败')
                CapPic(self.driver)
                raise Exception('策略库检测更新状态 提示异常')
        else:
            logger.info(showState, strategyName, u'检测失败')
            CapPic(self.driver)
            raise Exception('策略库检测更新状态 提示异常')
        # self.driver.quit()
        logger.info('test_001_policylib passed')

    def test_002_AppPriority(self):
        u'''应用优先 模板'''
        RuleName = getAssertText('RuleName')
        RuleName2 = getAssertText('RuleName2')

        #进入流量管理-应用优先
        appPriority = AppPriorityPage(self.driver,self.url)
        appPriority.click_TrafficManagement()
        time.sleep(0.5)
        appPriority.click_AppPriority()
        time.sleep(1)
        #选择办公优先
        selappType=appPriority.selelement_byName(appPriority.appType)
        Select(selappType).select_by_value('exp0')
        time.sleep(1)
        appPriority.click_changeAppType()
        time.sleep(5)
        #验证 规则名称 中的第一项值是否是‘办公优先’，来判断是否应用正常
        rule_name1 = appPriority.getText_byXpath(appPriority.list_name1)
        self.assertEqual(rule_name1,RuleName,msg='办公优先模板应用错误')
        # time.sleep(1)

        #选择娱乐优先
        selappType=self.driver.find_element_by_name('appType')
        time.sleep(1)
        Select(selappType).select_by_value('exp1')
        time.sleep(1)
        appPriority.click_changeAppType()
        time.sleep(3)
        rule_name1 = appPriority.getText_byXpath(appPriority.list_name1)
        # print(rule_name1)
        self.assertEqual(rule_name1,RuleName2,msg='模板应用错误')
        logger.info('test_002_AppPriority passed')

    def tearDown(self):
        self.driver.quit()
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
