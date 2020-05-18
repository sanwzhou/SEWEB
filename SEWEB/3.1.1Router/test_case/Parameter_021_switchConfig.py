#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 9:34
#@swzhou
'''
VLAN 虚接口/端口镜像/Port VLAN
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from pages.SwitchConfig_Page import switchConfigPage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
logger = LogGen(Logger = 'Parameter_021_switchConfig').getlog()

class switchConfig(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        lanpage = NetworkConfig_LANpage(self.driver,self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        # pass

    def test_001_vlanInterface(self):
        u'''VLAN 虚接口'''
        vlanPortP = getParameter('vlanPortP')
        Support = getExcelValue(vlanPortP)
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_add()
        time.sleep(1)
        selsxjk = lanpage.selelement_byName(lanpage.selsxjk)
        if Support == '√':
            try:
                self.driver.implicitly_wait(2)
                Select(selsxjk).select_by_value('vlanid')
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持VLAN 虚接口，与参数表不符')
                raise Exception(u'软件不支持VLAN 虚接口，与参数表不符')
            else:
                logger.info(u'软件支持VLAN 虚接口，与参数表相符')
                time.sleep(0.5)
        elif Support == '×':
            try:
                self.driver.implicitly_wait(2)
                Select(selsxjk).select_by_value('vlanid')
            except NoSuchElementException:
                logger.info(u'软件支持VLAN 虚接口，与参数表不符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持VLAN 虚接口，与参数表不符')
                raise Exception(u'软件支持VLAN 虚接口，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        Select(selsxjk).select_by_value('default')
        time.sleep(0.5)

        self.driver.quit()
        logger.info('test_001_vlanInterface passed')


    def test_002_PortMirror(self):
        u'''端口镜像（某些设备可能不支持）'''
        Monitorport = getAssertText('Monitorport')
        Monitoredport = getAssertText('Monitoredport')
        portmirrorP = getParameter('portmirrorP')
        Support = getExcelValue(portmirrorP)
        switchconfig = switchConfigPage(self.driver,self.url)
        if Support == '√':
            try:
                self.driver.implicitly_wait(2)
                switchconfig.find_switchConfig()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持交换配置,则不支持端口镜像，与参数表不相符')
                raise Exception('不支持交换配置,则不支持端口镜像，与参数表不相符')
            else:
                time.sleep(1)
                try:
                    switchconfig.find_portMirror()
                except NoSuchElementException:
                    raise Exception('不支持端口镜像，与参数表不相符')
                else:
                    logger.info(u'支持端口镜像，与参数表相符')
                    MirrorEns = str(switchconfig.getAttribute_byXpath(switchConfigPage.MirrorEns, 'checked'))
                    self.assertEqual(MirrorEns, 'true', msg='端口镜像 默认未关闭')
                    line1 = str(switchconfig.getText_byXpath(switchconfig.Monitorport))
                    self.assertEqual(line1,Monitorport,msg='监控端口 名称不一致')
                    line2 = str(switchconfig.getText_byXpath(switchconfig.Monitoredport))
                    self.assertEqual(line2, Monitoredport, msg='被监控端口 名称不一致')
        elif Support == '×':
            try:
                self.driver.implicitly_wait(2)
                switchconfig.find_switchConfig()
            except NoSuchElementException:
                logger.info('不支持交换配置,则不支持端口镜像，与参数表相符')
            else:
                time.sleep(1)
                try:
                    switchconfig.find_portMirror()
                except NoSuchElementException:
                    logger.info(u'不支持 端口镜像，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持端口镜像，与参数表不符')
                    raise Exception(u'软件支持端口镜像，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_002_PortMirror passed')

    def test_003_PortVLAN(self):
        u'''Port VLAN（某些设备可能不支持）'''
        portVlanP = getParameter('portVlanP')
        Support = getExcelValue(portVlanP)
        switchconfig = switchConfigPage(self.driver, self.url)
        if Support == '√':
            try:
                self.driver.implicitly_wait(2)
                switchconfig.find_switchConfig()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持交换配置,则不支持端口VLAN，与参数表不相符')
                raise Exception('不支持交换配置,则不支持端口VLAN，与参数表不相符')
            else:
                time.sleep(1)
                try:
                    switchconfig.find_portVlan()
                except NoSuchElementException:
                    raise Exception('不支持 端口VLAN，与参数表不相符')
                else:
                    logger.info(u'支持 端口VLAN，与参数表相符')
                    time.sleep(0.5)
                    line1 = str(switchconfig.getText_byXpath(switchconfig.VLAN1))
                    self.assertEqual(line1, 'VLAN1', msg='VLAN1 名称不一致')
        elif Support == '×':
            try:
                self.driver.implicitly_wait(2)
                switchconfig.find_switchConfig()
            except NoSuchElementException:
                logger.info('不支持交换配置,则不支持端口VLAN，与参数表相符')
            else:
                time.sleep(1)
                try:
                    switchconfig.find_portVlan()
                except NoSuchElementException:
                    logger.info(u'不支持 端口VLAN，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'软件支持端口VLAN，与参数表不符')
                    raise Exception(u'软件支持端口VLAN，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_003_PortVLAN passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()