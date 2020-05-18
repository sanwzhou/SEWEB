#! -*-conding:utf-8 -*-
#@Time: 2019/1/23 0023 16:09
#@swzhou
'''
系统配置-网管策略-网管访问策略,修改登录页模式、页面超时等
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getweb,gettelnet
from common.loginRoute import login
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
from pages.NetConfig_002_LANpage import NetworkConfig_LANpage
logger = LogGen(Logger = 'sysConfig_003_AccessPolicy').getlog()

class AccessPolicy(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        accessStrategy = ManagementPolicyPage(self.driver,self.url)
        #进入系统配置-网管策略-网管访问策略
        accessStrategy.click_sysConfig()
        time.sleep(0.5)
        accessStrategy.click_ManagementPolicy()
        time.sleep(1)
        accessStrategy.click_AccessPolicy()
        time.sleep(1)
        # pass

    def test_001_AccessMode(self):
        u'''https模式登录'''
        host = gettelnet('host')
        RouteUrls = 'https://' + host + '/'

        # 修改网管模式，端口切换到443，https模式下可登录设备
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.click_httpswebEn()
        accessStrategy.click_save()
        # 加个判断 某些型号等待时间长（6550G）
        time.sleep(1)
        x = 0
        while x < 15:
            now_url = str(self.driver.current_url)
            print(now_url, x)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(2)
            else:
                break
            x += 1
        self.driver.quit()

        #https模式下验证登录设备
        login.test_enableLoginWeb(self,url=RouteUrls) #https登录
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        # 改回http 方式登录
        accessStrategy.click_sysConfig()
        time.sleep(0.5)
        accessStrategy.click_ManagementPolicy()
        time.sleep(1)
        accessStrategy.click_AccessPolicy()
        time.sleep(1)
        accessStrategy.click_httpwebEn()
        accessStrategy.click_save()
        time.sleep(1)
        i = 0
        while i < 30:
            url = self.driver.current_url
            if '/login.html' in url:
                break
            else:
                time.sleep(2)
            i +=1

        self.driver.quit()
        logger.info('test_001_AccessMode passed')

    def test_002_passwdErrNum(self,passwdErrNum='3',loginSpan='1'):
        u'''修改最大错误登录次数&超出最大次数惩罚时间'''
        #修改最大错误登录次数&超出最大次数惩罚时间
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.input_passwdErrNum(passwdErrNum)
        accessStrategy.input_loginSpan(loginSpan)
        accessStrategy.click_save()
        time.sleep(1)
        self.driver.quit()

        #使用错误密码多次登录以达到最大错误登录次数
        while int(passwdErrNum) > 0:
            passwdErrNum=int(passwdErrNum) - 1
            login.test_unableLoginWeb(self,password='1')
            # print(self.driver.find_element_by_id('warning-msg').text)
            time.sleep(1)
            if int(passwdErrNum) > 0:
                self.driver.quit()
        #停留60s
        print('超过错误次数，等待60s')
        time.sleep(60)
        self.driver.quit()
        #使用正确账号密码测试登录
        login.loginWeb(self) #admin账号登录
        self.driver.quit()
        logger.info('test_002_passwdErrNum passed')

    def test_003_WEBtimeout(self,timeout='1'): #因为字母顺序问题 该项会在最后执行
        u'''修改UI超时时间'''
        #修改UI超时时间
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.input_sessionLife(timeout)
        accessStrategy.click_save()
        self.driver.quit()

        login.loginWeb(self)
        #任意点击一个页面，这里点击网络配置-内网配置
        lanconfig = NetworkConfig_LANpage(self.driver,self.url)
        lanconfig.click_NetworkConfig()
        time.sleep(0.5)
        lanconfig.click_LANconfig()
        time.sleep(1)
        print('等待超时时间，在这里等待80s')
        time.sleep(120)
        #等待超时时间后，任意点击其他页面 测试超时（返回登录页面）
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.click_sysConfig()
        time.sleep(0.5)
        accessStrategy.click_ManagementPolicy()
        time.sleep(2)
        url = self.driver.current_url
        if '/login.html' not in url:
            CapPic(self.driver)
            logger.info(u"未跳回登录页面")
            raise Exception('未跳回登录页面')
        self.driver.quit()

        # 将超时时间改回默认值
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略-网管访问策略
        accessStrategy.click_sysConfig()
        time.sleep(0.5)
        accessStrategy.click_ManagementPolicy()
        time.sleep(1)
        accessStrategy.click_AccessPolicy()
        time.sleep(1)
        accessStrategy.input_sessionLife('10')
        accessStrategy.click_save()
        self.driver.quit()
        logger.info('test_003_WEBtimeout passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
