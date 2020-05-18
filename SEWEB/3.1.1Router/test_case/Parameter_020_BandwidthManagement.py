#! -*-conding:utf-8 -*-
#@Time: 2019/2/18 0018 17:02
#@swzhou
'''
带宽管理：
应用优先、流量管理、
统计：用户流量统计、应用流量统计、端口流量统计、VPN流量统计
'''

import time
import unittest

from selenium.common.exceptions import NoSuchElementException

from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from pages.TrafficManagement_001_AppPriorityPage import AppPriorityPage
from pages.TrafficManagement_002_BWManagementPage import BWManagementPage
from pages.SysMonitor_001_sysStaticPage import sysStaticPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_020_BandwidthManagement').getlog()
hwNatP = getExcelValue(getParameter('hwNatP'))
sfnatP = getExcelValue(getParameter('sfnatP'))

class BandwidthManagement(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) 
        self.driver.implicitly_wait(10)
        # pass

    def test_001_appTemplate(self):
        u'''应用优先'''
        nodata = getAssertText('nodata')

        appPriority = AppPriorityPage(self.driver, self.url)
        appPriority.click_TrafficManagement()
        time.sleep(0.5)
        appPriority.click_AppPriority()
        time.sleep(1)
        # 开/关
        checkOpens = appPriority.getAttribute_byId(appPriority.checkOpens,'checktype')  # checktype 0未开启，1开启
        self.assertEqual(checkOpens, '0', msg='应用优先 默认未关闭')
        appPriority.click_checkOpen()
        time.sleep(2)
        checkOpens = appPriority.getAttribute_byId(appPriority.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '1', msg='应用优先 开启失败')
        if checkOpens == '1':
            self.driver.find_element_by_id('checkOpen').click()
            time.sleep(2)
        checkOpens = appPriority.getAttribute_byId(appPriority.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '0', msg='应用优先 关闭失败')
        #
        appPriority.find_add()
        appPriority.find_delete()
        appPriority.find_import1()
        appPriority.find_export()
        listnodata = str(appPriority.getText_byXpath(appPriority.listnodata))
        self.assertEqual(listnodata,nodata,msg='应用优先 默认列表不为空')
        #模板选择
        appPriority.click_changeAppType()
        time.sleep(2)
        selappType = appPriority.selelement_byName(appPriority.appType)
        Select(selappType).select_by_value('exp0')#  办公优先
        time.sleep(0.5)
        Select(selappType).select_by_value('exp1') #  娱乐优先
        self.driver.quit()
        logger.info('test_001_appTemplate passed')

    def test_002_BWManagement(self):
        u'''流量管理'''
        bandwidth = BWManagementPage(self.driver,self.url)
        bandwidth.click_Qos()
        time.sleep(0.5)
        bandwidth.click_TrafficManagement()
        time.sleep(1)
        bandwidth.click_add()
        time.sleep(1)
        bandwidth.input_GroupNames('test')
        bandwidth.input_notes('test')
        bandwidth.input_order('1')
        bandwidth.click_orgShow()
        time.sleep(2)
        bandwidth.click_usergroup()
        time.sleep(0.5)
        bandwidth.click_userip()
        time.sleep(0.5)
        bandwidth.click_userall()
        time.sleep(0.5)
        bandwidth.click_saveW1()
        time.sleep(1)
        #限制/保障
        bandwidth.click_lkcl1()
        time.sleep(0.3)
        bandwidth.click_lkcl0()
        time.sleep(0.3)
        #独享/共享
        bandwidth.click_policy2()
        time.sleep(0.3)
        bandwidth.click_policy1()
        time.sleep(0.3)
        #上传下载速度
        bandwidth.input_uRate('1')
        bandwidth.input_dRate('2')
        #生效时间
        bandwidth.selelement_byName(bandwidth.effecttime)

        self.driver.quit()
        logger.info('test_002_BWManagement passed')

    def test_003_Statistics(self):
        u'''统计：用户流量统计、应用流量统计、端口流量统计、VPN流量统计'''
        sysStatic1A = getAssertText('sysStatic1A')
        sysStatic2A = getAssertText('sysStatic2A')
        sysStatic3A = getAssertText('sysStatic3A')
        sysStatic4A = getAssertText('sysStatic4A')
        sysStatic5A = getAssertText('sysStatic5A')
        sysstatic = sysStaticPage(self.driver,self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)

        tips1 = str(sysstatic.getText_byXpath(sysstatic.tips1))
        self.assertEqual(tips1, sysStatic1A, msg='带宽 表名不一致')
        tips2 = str(sysstatic.getText_byXpath(sysstatic.tips2))
        self.assertEqual(tips2, sysStatic2A, msg='系统负载 表名不一致')
        tips3 = str(sysstatic.getText_byXpath(sysstatic.tips3))
        self.assertEqual(tips3, sysStatic3A, msg='今日应用流量排名 表名不一致')
        tips4 = str(sysstatic.getText_byXpath(sysstatic.tips4))
        self.assertEqual(tips4, sysStatic4A, msg='今日用户网络流量排名 表名不一致')
        L2tpP = getParameter('L2tpP')
        pptpP = getParameter('pptpP')
        SupportL = getExcelValue(L2tpP)
        SupportP = getExcelValue(pptpP)
        ipsecP = getParameter('ipsecP')
        SupportI = getExcelValue(ipsecP)
        if (SupportL or SupportP or SupportI) == '√':
            logger.info(u'参数支持VPN')
            tips5 = str(sysstatic.getText_byXpath(sysstatic.tips5))
            self.assertEqual(tips5, sysStatic5A, msg='VPN状态 表名不一致')

        self.driver.quit()
        logger.info('test_003_Statistics passed')

    def test_004_Fastforward(self):
        u'''硬件转发/软件转发 '''
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_GlobalConfig()
        time.sleep(1)

        if hwNatP == '√':
            logger.info(u'参数支持硬件快速转发')
            try:
                self.driver.implicitly_wait(2)
                # 默认自动模式
                wanpage.click_FastForwardEnableC()
                wanpage.click_FastForwardModeC()
            except AttributeError:
                CapPic(self.driver)
                logger.info(u'不支持硬件快速转发，与参数表不相符')
                raise Exception('不支持硬件快速转发，与参数表不相符')
            else:
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
                FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
                Select(FastForwardEnable).select_by_value('NatOpen')
                time.sleep(0.3)
                Select(FastForwardEnable).select_by_value('0')
                time.sleep(0.3)
                Select(FastForwardEnable).select_by_value('NatAuto')
                time.sleep(0.3)
                FastForwardMode = wanpage.selelement_byName('FastForwardMode')
                Select(FastForwardMode).select_by_value('sfNat')
                time.sleep(0.3)
                Select(FastForwardMode).select_by_value('hwNat')
        elif hwNatP == '×':
            logger.info(u'参数不支持硬件快速转发')
            try:
                self.driver.implicitly_wait(2)
                wanpage.click_FastForwardModeC()
            except AttributeError:
                logger.info('不支持硬件快速转，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持硬件快速转，与参数表不相符')
                raise Exception('支持硬件快速转，与参数表不相符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', hwNatP)
            raise Exception(u'参数表读取异常')

        if hwNatP == '×' and sfnatP == '√':
            logger.info(u'参数支持软件快速转发')
            try:
                self.driver.implicitly_wait(2)
                # 默认自动模式
                wanpage.click_FastForwardEnableC()
            except AttributeError:
                CapPic(self.driver)
                logger.info(u'不支持软件快速转发，与参数表不相符')
                raise Exception('不支持软件快速转发，与参数表不相符')
            else:
                enable1 = wanpage.getAttribute_byXpath(wanpage.enable1, 'selected')
                # print('enable1:', enable1)
                if enable1 != 'true':
                    logger.info(u'快速转发模式开关默认不为自动')
                    CapPic(self.driver)
                    raise Exception(u'快速转发模式开关默认不为自动')
                FastForwardEnable = wanpage.selelement_byName('FastForwardEnable')
                Select(FastForwardEnable).select_by_value('NatOpen')
                time.sleep(0.3)
                Select(FastForwardEnable).select_by_value('0')
                time.sleep(0.3)
                Select(FastForwardEnable).select_by_value('NatAuto')
        elif sfnatP == '×':
            logger.info(u'参数不支持软件快速转发')
            try:
                self.driver.implicitly_wait(2)
                wanpage.click_FastForwardEnableC()
            except AttributeError:
                logger.info('不支持软件快速转，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持软件快速转，与参数表不相符')
                raise Exception('支持软件快速转，与参数表不相符')
        self.driver.quit()
        logger.info('test_004_Fastforward passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()


