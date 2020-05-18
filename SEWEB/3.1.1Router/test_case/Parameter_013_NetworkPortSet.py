#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 15:03
#@swzhou
'''
网口设置：
端口速率修改、LAN口多IP、MAC地址修改
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb
from common.loginRoute import login
from pages.Loginpage import LoginPage
from pages.SysMonitor_001_sysStaticPage import sysStaticPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
logger = LogGen(Logger = 'Parameter_013_NetworkPortSet').getlog()

class NetworkPortSet(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # pass

    def test_001_portRateWAN(self):
        u'''wan默认协商速率及端口速率修改 '''
        # 进入-系统监控-系统状态 获取型号判断是否支持千M
        sysmonitor = sysStaticPage(self.driver,self.url)
        sysmonitor.click_systemWatch()
        time.sleep(0.5)
        sysmonitor.click_sysStatic()
        time.sleep(1)
        Model = str(sysmonitor.getText_byXpath(sysmonitor.Model))
        print(Model)

        #判断速率wan口
        wanpage = NetworkConfig_wanpage(self.driver,self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        connectionType = wanpage.selelement_byName(wanpage.connectionType)
        Select(connectionType).select_by_value('DHCP')
        time.sleep(1)
        WanMode_seled1 = str(wanpage.getAttribute_byXpath(wanpage.wanRateseled,'value'))
        self.assertEqual(WanMode_seled1,'3',msg='WAN默认端口速率不为自动协商')
        WanMode_seled2 = str(wanpage.getAttribute_byXpath(wanpage.wanRateseled,'selected'))
        self.assertEqual(WanMode_seled2, 'true', msg='WAN默认端口速率不为自动协商')
        WanMode = wanpage.selelement_byXpath(wanpage.selwanRate)
        time.sleep(1)
        # 0-10M全双工 1-100M全双工 2-1000M全双工 3-自动 4-10M半双工 5-100M半双工
        Select(WanMode).select_by_value('0')
        time.sleep(1)
        Select(WanMode).select_by_value('1')
        Select(WanMode).select_by_value('3')
        Select(WanMode).select_by_value('4')
        Select(WanMode).select_by_value('5')
        if 'G' in str(Model) or 'g' in str(Model):
            try:
                Select(WanMode).select_by_value('2')
            except NoSuchElementException:
                raise Exception('WAN口不支持千M协商速率')
        self.driver.quit()

        logger.info('test_001_portRateWAN passed')

    def test_002_portRateLAN(self):
        u'''lan默认协商速率及端口速率修改'''
        # 进入-系统监控-系统状态 获取型号判断是否支持千M
        sysmonitor = sysStaticPage(self.driver,self.url)
        sysmonitor.click_systemWatch()
        time.sleep(0.5)
        sysmonitor.click_sysStatic()
        time.sleep(1)
        Model = str(sysmonitor.getText_byXpath(sysmonitor.Model))
        print(Model)

        # 协商速率LAN口
        lanpage = NetworkConfig_LANpage(self.driver,self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        LanMode_seled1 = lanpage.getAttribute_byXpath(lanpage.lanRateseled,'value')
        self.assertEqual(str(LanMode_seled1), '3', msg='LAN默认端口速率不为自动协商')
        LanMode_seled2 = lanpage.getAttribute_byXpath(lanpage.lanRateseled,'selected')
        self.assertEqual(str(LanMode_seled2), 'true', msg='LAN默认端口速率不为自动协商')
        LanMode = lanpage.selelement_byXpath(lanpage.sellanRate)
        time.sleep(1)
        # 0-10M全双工 1-100M全双工 2-1000M全双工 3-自动 4-10M半双工 5-100M半双工
        Select(LanMode).select_by_value('0')
        time.sleep(1)
        Select(LanMode).select_by_value('1')
        Select(LanMode).select_by_value('3')
        Select(LanMode).select_by_value('4')
        Select(LanMode).select_by_value('5')
        if 'G' in str(Model) or 'g' in str(Model):
            try:
                Select(LanMode).select_by_value('2')
            except NoSuchElementException:
                raise Exception('LAN口不支持千M协商速率')
        self.driver.quit()

        logger.info('test_002_portRateLAN passed')

    def test_003_LanMultiIP(self):
        u'''Lan口多IP'''
        reachMax3A = getAssertText('reachMax3A')
        User = getweb('User')
        Passwd = getweb('Passwd')
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        # 新增lan口
        num = 1
        while num <5:
            num += 1
            lanpage.click_add()
            time.sleep(1)
            lanpage.input_lanIpName('lan%s' %num)
            lanpage.input_lanIp('213.18.%s.1' %num)
            lanpage.click_save()
            if num < 5:
                time.sleep(5)
                i = 0
                while i <10:
                    now_url=str(self.driver.current_url)
                    if '/noAuth/login.html' not in now_url:
                        time.sleep(2)
                    else:
                        break
                    i +=1
                    print(now_url,i)
                self.driver.quit()
                login.loginWeb(self)
                self.driver.implicitly_wait(10)
                loginPage = LoginPage(self.driver,self.url)
                lanpage = NetworkConfig_LANpage(self.driver, self.url)
                lanpage.click_NetworkConfig()
                time.sleep(0.5)
                lanpage.click_LANconfig()
                time.sleep(1)
            elif num >= 5 :
                time.sleep(1)
                tips = (lanpage.getText_byClass(lanpage.tipsshowin))
                self.assertIn(reachMax3A ,tips,msg='提示信息有误')
                print('lan口数量最大为4 验证通过')
                time.sleep(1)
                lanpage.click_modalhide()
                time.sleep(0.5)
        lanpage.click_allsel()
        time.sleep(0.2)
        lanpage.click_delete()
        time.sleep(1)
        lanpage.click_ok()
        time.sleep(15) #删除接口要等等
        self.driver.quit()
        logger.info('test_003_LanMultiIP passed')

    def test_004_changeMAC(self):
        u'''MAC地址修改'''
        CannotbeblankA = getAssertText('CannotbeblankA')
        lanpage = NetworkConfig_LANpage(self.driver, self.url)
        lanpage.click_NetworkConfig()
        time.sleep(0.5)
        lanpage.click_LANconfig()
        time.sleep(1)
        lanpage.click_globalconfig()
        time.sleep(1)
        # lan口MAC 清空lan mac的值保存 确认是否可以修改
        lanpage.clear_mac()
        time.sleep(0.5)
        lanpage.click_save()
        time.sleep(0.5)
        lan_tips = str(lanpage.getText_byXpath(lanpage.lan_tips))
        self.assertIn(CannotbeblankA,lan_tips,msg='lan口mac地址清空保存提示错误')
        print('lan口mac地址更改 验证通过')
        # wan1口MAC 清空lan mac的值保存 确认是否可以修改
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_WANconfig()
        time.sleep(1)
        wanpage.click_line1edit()
        time.sleep(1)
        connectionType = wanpage.selelement_byName(wanpage.connectionType)
        Select(connectionType).select_by_value('DHCP')
        time.sleep(0.5)
        wanpage.clear_line1editmac()
        time.sleep(0.5)
        wanpage.click_save()
        time.sleep(0.5)
        wan_tips = str(wanpage.getText_byXpath(wanpage.wan_tips))
        self.assertIn(CannotbeblankA, lan_tips, msg='wan口mac地址清空保存提示错误')
        print('wan口mac地址更改 验证通过')
        self.driver.quit()
        logger.info('test_004_changeMAC passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()