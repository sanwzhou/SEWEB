#! -*-conding:utf-8 -*-
#@Time: 2019/3/8 0008 11:30
#@swzhou
'''
LAN/WAN 端口速率修改
'''

import time
import unittest
import os.path
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.swconfig import swconfig
from common.ReadConfig import getParameter
from common.GetExcelValue import getExcelValue
from common.pingTest import pingTestIP
from pages.SysMonitor_001_sysStaticPage import sysStaticPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
logger = LogGen(Logger = 'NetworkConfig_002_PortRate').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
portTateWANp = getParameter('portTateWANp')
portTateLANp = getParameter('portTateLANp')
# print(portTateWANp)
# print(portTateLANp)

class PortRate(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_changeRateWAN(self):
        u'''wan1端口协商速率修改 '''
        # # 进入-系统监控-系统状态 获取型号判断是否支持千M
        # sysmonitor = sysStaticPage(self.driver, self.url)
        # sysmonitor.click_systemWatch()
        # time.sleep(0.5)
        # sysmonitor.click_sysStatic()
        # time.sleep(1)
        # Model = str(sysmonitor.getText_byXpath(sysmonitor.Model))
        # print(Model)
        #wan口速率修改
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        connectionType = wanpage.selelement_byName(wanpage.connectionType)
        Select(connectionType).select_by_value('DHCP')
        time.sleep(0.5)
        WanMode = wanpage.selelement_byXpath(wanpage.selwanRate)
        # 0-10M全双工 1-100M全双工 2-1000M全双工 3-自动 4-10M半双工 5-100M半双工
        #改为10M
        try:
            Select(WanMode).select_by_value('4')
            time.sleep(0.5)
        except ElementNotVisibleException:
            CapPic(self.driver)
            logger.info(u'WAN口不支持修改为10M半双工')
            raise Exception(u'WAN口不支持修改为10M半双工')
        wanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()
        i= 0
        while i < 30:
            swRate = swconfig.test_getWAN1Speed(self)
            print(swRate)
            if swRate != 'speed10M':
                time.sleep(1)
                i +=1
            else:
                break
        else:
            logger.info(u'交换机端口速率为: %s' % swRate)
            logger.info(u'交换机协商速率 不为10M')
            raise Exception(u'交换机协商速率 不为10M')
        # 改为100M
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        WanMode = wanpage.selelement_byXpath(wanpage.selwanRate)
        Select(WanMode).select_by_value('5')
        time.sleep(0.5)
        wanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()
        i = 0
        while i < 30:
            swRate = swconfig.test_getWAN1Speed(self)
            print(swRate)
            if swRate != 'speed100M':
                time.sleep(1)
                i +=1
            else:
                break
        else:
            logger.info(u'交换机端口速率为: %s' % swRate)
            logger.info(u'交换机协商速率 不为100M')
            raise Exception(u'交换机协商速率 不为100M')
        # 改为1000M
        support = getExcelValue(portTateWANp)
        if '千' in str(support): #参数表中包含“千”兆
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            wanpage = NetworkConfig_wanpage(self.driver, self.url)
            wanpage.click_NetworkConfig()
            time.sleep(0.5)
            wanpage.click_WANconfig()
            time.sleep(1)
            wanpage.click_line1edit()
            time.sleep(1)
            WanMode = wanpage.selelement_byXpath(wanpage.selwanRate)
            try:
                Select(WanMode).select_by_value('2')
                time.sleep(0.5)
                wanpage.click_save()
                time.sleep(10)
                n = 0
                while n < 20:
                    ping = pingTestIP()
                    if ping != 'Y':
                        time.sleep(1)
                        n += 1
                    else:
                        break
                self.driver.quit()
                i = 0
                while i < 30:
                    swRate = swconfig.test_getWAN1Speed(self)
                    print(swRate)
                    if swRate != 'speed1000M':
                        time.sleep(1)
                        i +=1
                    else:
                        break
                else:
                    logger.info(u'交换机端口速率为: %s' % swRate)
                    logger.info(u'交换机协商速率 不为1000M')
                    raise Exception(u'交换机协商速率 不为1000M')
            except NoSuchElementException:
                raise Exception('WAN口不支持千M协商速率')
        # 改为auto
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        WanMode = wanpage.selelement_byXpath(wanpage.selwanRate)
        Select(WanMode).select_by_value('3')
        time.sleep(0.5)
        wanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()
        time.sleep(2)
        swRate = swconfig.test_getWAN1Speed(self)
        print(swRate)
        if '千' in str(support):
            i = 0
            while i < 30:
                swRate = swconfig.test_getWAN1Speed(self)
                print(swRate)
                if swRate != 'speed1000M':
                    time.sleep(1)
                    i += 1
                else:
                    break
            else:
                logger.info(u'交换机端口速率为: %s' % swRate)
                logger.info(u'交换机协商速率 不为1000M')
                raise Exception(u'交换机协商速率 不为1000M')
        else:
            i = 0
            while i < 30:
                swRate = swconfig.test_getWAN1Speed(self)
                print(swRate)
                if swRate != 'speed100M':
                    time.sleep(1)
                    i += 1
                else:
                    break
            else:
                logger.info(u'交换机端口速率为: %s' % swRate)
                logger.info(u'交换机协商速率 不为100M')
                raise Exception(u'交换机协商速率 不为100M')

        logger.info('test_001_changePortRateWAN passed')

    def test_002_changeRateLAN(self):
        u'''lan1端口协商速率修改 '''
        # # 进入-系统监控-系统状态 获取型号判断是否支持千M
        # sysmonitor = sysStaticPage(self.driver, self.url)
        # sysmonitor.click_systemWatch()
        # time.sleep(0.5)
        # sysmonitor.click_sysStatic()
        # time.sleep(1)
        # Model = str(sysmonitor.getText_byXpath(sysmonitor.Model))
        # print(Model)
        #Lan口速率修改
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
        # 0-10M全双工 1-100M全双工 2-1000M全双工 3-自动 4-10M半双工 5-100M半双工
        #改为10M
        try:
            Select(LanMode).select_by_value('0')
            time.sleep(0.5)
        except ElementNotVisibleException:
            CapPic(self.driver)
            logger.info(u'lan口不支持修改为10M全双工')
            raise Exception(u'lan口不支持修改为10M全双工')
        lanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20 :
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n +=1
            else:
                break
        self.driver.quit()
        i = 0
        while i < 30:
            swRate = swconfig.test_getLANSpeed(self)
            print(swRate)
            if swRate != 'speed10M':
                time.sleep(1)
                i += 1
            else:
                break
        else:
            logger.info(u'交换机端口速率为: %s' % swRate)
            logger.info(u'交换机协商速率 不为10M')
            raise Exception(u'交换机协商速率 不为10M')
        # 改为100M
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        time.sleep(2) #谨防10M页面卡住
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
        Select(LanMode).select_by_value('1')
        time.sleep(0.5)
        lanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()
        i = 0
        while i < 30:
            swRate = swconfig.test_getLANSpeed(self)
            print(swRate)
            if swRate != 'speed100M':
                time.sleep(1)
                i += 1
            else:
                break
        else:
            logger.info(u'交换机端口速率为: %s' % swRate)
            logger.info(u'交换机协商速率 不为100M')
            raise Exception(u'交换机协商速率 不为100M')
        # 改为1000M
        support = getExcelValue(portTateLANp)
        # print('support:',support)
        if '千' in str(support):
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            lanpage = NetworkConfig_LANpage(self.driver, self.url)
            lanpage.click_NetworkConfig()
            time.sleep(0.5)
            lanpage.click_LANconfig()
            time.sleep(1)
            lanpage.click_globalconfig()
            time.sleep(1)
            LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
            try:
                Select(LanMode).select_by_value('2')
                time.sleep(0.5)
                lanpage.click_save()
                time.sleep(10)
                n = 0
                while n < 20:
                    ping = pingTestIP()
                    if ping != 'Y':
                        time.sleep(1)
                        n += 1
                    else:
                        break
                self.driver.quit()
                i = 0
                while i < 30:
                    swRate = swconfig.test_getWAN1Speed(self)
                    print(swRate)
                    if swRate != 'speed1000M':
                        time.sleep(1)
                        i += 1
                    else:
                        break
                else:
                    logger.info(u'交换机端口速率为: %s' % swRate)
                    logger.info(u'交换机协商速率 不为1000M')
                    raise Exception(u'交换机协商速率 不为1000M')
            except NoSuchElementException:
                raise Exception('WAN口不支持千M协商速率')
        # 改为auto
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
        Select(LanMode).select_by_value('3')
        time.sleep(0.5)
        lanpage.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()
        swRate = swconfig.test_getWAN1Speed(self)
        print(swRate)
        if '千' in str(support):
            i = 0
            while i < 30:
                swRate = swconfig.test_getWAN1Speed(self)
                print(swRate)
                if swRate != 'speed1000M':
                    time.sleep(1)
                    i += 1
                else:
                    break
            else:
                logger.info(u'交换机端口速率为: %s' % swRate)
                logger.info(u'交换机协商速率 不为1000M')
                raise Exception(u'交换机协商速率 不为1000M')
        else:
            i = 0
            while i < 30:
                swRate = swconfig.test_getLANSpeed(self)
                print(swRate)
                if swRate != 'speed100M':
                    time.sleep(1)
                    i += 1
                else:
                    break
            else:
                logger.info(u'交换机端口速率为: %s' % swRate)
                logger.info(u'交换机协商速率 不为100M')
                raise Exception(u'交换机协商速率 不为100M')

        logger.info('test_002_changePortRateLAN passed')

    def tearDown(self):
        #修改lan口为自动模式，谨防lan口速率出问题 太卡
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        lanmodenow = lanpage.getAttribute_byXpath(lanpage.lanmodenow,'selected')
        print(lanmodenow)
        if lanmodenow != 'true':
            LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
            Select(LanMode).select_by_value('3')
            time.sleep(0.5)
            lanpage.click_save()
            time.sleep(10)
            n = 0
            while n < 20:
                ping = pingTestIP()
                if ping != 'Y':
                    time.sleep(1)
                    n += 1
                else:
                    break
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

    if __name__ == '__main__':
        unittest.main()