#! -*-conding:utf-8 -*-
#@Time: 2019/1/21 0021 16:26
#@swzhou
'''
软件升级
'''


import time
import unittest
import os.path
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb
from common.loginRoute import login
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'softwareUpdate').getlog()
tmppath = os.path.dirname(os.path.abspath('.')) + '/tmp/'


class softwareUpdate(unittest.TestCase):

    def setUp(self):
        print('sysConfig_006_softwareUpdata start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver,self.url)
        #进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        # pass

    def test_errorSoftware(self):
        u'''软件升级 - 验证错误型号'''
        errversion = getweb('errversion')
        updataWarnTips = getAssertText('updataWarnTips')

        errSoftware = (str(tmppath) + str(errversion) + '.bin' )
         # 更新一个错误型号 验证无法升级 及提示信息
        software = MaintenancePage(self.driver, self.url)
        #选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(errSoftware)
        # software.input_updatesoftware(errSoftware) #定位不到
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(2)
        # 断言提示信息内容正确：代表该项正常
        pageTip = software.getText_byClass(software.pageTip_warn)
        if pageTip != updataWarnTips :
            CapPic(self.driver)
            logger.info(u"升级错误型号 提示信息异常")
            raise Exception('升级错误型号 提示信息异常')
        else:
            print('更新 错误型号版本 验证通过')
        self.driver.quit()

    def test_oldSoftware1(self,oldversion1 = getweb('oldversion1')):
        u'''软件升级 - 更新旧版本测试'''
        # oldversion1 = getweb('oldversion1')
        self.oldversion1 = oldversion1
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        oldversioa1 = oldversion1.split(r'-')
        if len(oldversioa1) == 2: # eg:'nv640Ev1.5.0-130918'
            Expect_Version = oldversioa1[0] + '-' + oldversioa1[1]
        else: #eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(oldversioa1) - 1:
                Expect_Version += oldversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        # print(Expect_Version)

        # if '.bin' in oldversioa1[1]:
        #     oldversioa2 = oldversioa1[0] + '-' + oldversioa1[1]
        #     Expect_Version = oldversioa2[:-4]
        # else:
        #     Expect_Version = oldversioa1[0] + '-' + oldversioa1[1]

        # 版本上传
        oldSoftware=(str(tmppath) + str(oldversion1) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(oldSoftware)
        # software.input_updatesoftware(oldSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips=str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        #判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级旧版本 升级后版本号与升级版本号不一致")
            raise Exception('升级旧版本 升级后版本号与升级版本号不一致')
        else:
            print('更新 旧型号版本 验证通过')
        self.driver.quit()

    def test_newSoftware1(self,newversion1 = getweb('SoftVersion1')):
        u'''软件升级 - 更新新正常版本'''
        # newversion = getweb('SoftVersion1')
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        newversioa1 = newversion1.split(r'-')
        if len(newversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = newversioa1[0] + '-' + newversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(newversioa1) - 1:
                Expect_Version += newversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        print(Expect_Version)

        # if '.bin' in newversioa1[1]:
        #     newversioa2 = newversioa1[0] + '-' + newversioa1[1]
        #     Expect_Version = newversioa2[:-4]
        # else:
        #     Expect_Version = newversioa1[0] + '-' + newversioa1[1]

        # 版本上传
        newSoftware = (str(tmppath) + str(newversion1) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(newSoftware)
        # software.input_updatesoftware(newSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips = str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        # 判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级新版本 升级后版本号与升级版本号不一致")
            raise Exception('升级新版本 升级后版本号与升级版本号不一致')
        else:
            print('升级新版本 验证通过')
        self.driver.quit()


    def test_oldSoftware2(self,oldversion2 = getweb('oldversion2')):
        u'''软件升级 - 更新旧版本测试'''
        # oldversion1 = getweb('oldversion1')
        self.oldversion1 = oldversion2
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        oldversioa1 = oldversion2.split(r'-')
        if len(oldversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = oldversioa1[0] + '-' + oldversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(oldversioa1) - 1:
                Expect_Version += oldversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        # print(Expect_Version)

        # 版本上传
        oldSoftware=(str(tmppath) + str(oldversion2) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(oldSoftware)
        # software.input_updatesoftware(oldSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips=str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        #判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级旧版本 升级后版本号与升级版本号不一致")
            raise Exception('升级旧版本 升级后版本号与升级版本号不一致')
        else:
            print('更新 旧型号版本 验证通过')
        self.driver.quit()

    def test_newSoftware2(self,newversion2 = getweb('SoftVersion2')):
        u'''软件升级 - 更新新正常版本'''
        # newversion = getweb('SoftVersion1')
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        newversioa1 = newversion2.split(r'-')
        if len(newversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = newversioa1[0] + '-' + newversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(newversioa1) - 1:
                Expect_Version += newversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        print(Expect_Version)

        # 版本上传
        newSoftware = (str(tmppath) + str(newversion2) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(newSoftware)
        # software.input_updatesoftware(newSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips = str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        # 判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级新版本 升级后版本号与升级版本号不一致")
            raise Exception('升级新版本 升级后版本号与升级版本号不一致')
        else:
            print('升级新版本 验证通过')
        self.driver.quit()


    def test_oldSoftware3(self,oldversion3 = getweb('oldversion3')):
        u'''软件升级 - 更新旧版本测试'''
        # oldversion1 = getweb('oldversion1')
        self.oldversion1 = oldversion3
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        oldversioa1 = oldversion3.split(r'-')
        if len(oldversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = oldversioa1[0] + '-' + oldversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(oldversioa1) - 1:
                Expect_Version += oldversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        # print(Expect_Version)

        # 版本上传
        oldSoftware=(str(tmppath) + str(oldversion3) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(oldSoftware)
        # software.input_updatesoftware(oldSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips=str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        #判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级旧版本 升级后版本号与升级版本号不一致")
            raise Exception('升级旧版本 升级后版本号与升级版本号不一致')
        else:
            print('更新 旧型号版本 验证通过')
        self.driver.quit()

    def test_newSoftware3(self,newversion3 = getweb('SoftVersion3')):
        u'''软件升级 - 更新新正常版本'''
        # newversion = getweb('SoftVersion1')
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        newversioa1 = newversion3.split(r'-')
        if len(newversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = newversioa1[0] + '-' + newversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(newversioa1) - 1:
                Expect_Version += newversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        print(Expect_Version)

        # 版本上传
        newSoftware = (str(tmppath) + str(newversion3) + '.bin' )

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(newSoftware)
        # software.input_updatesoftware(newSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips = str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        # 判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version :
            CapPic(self.driver)
            logger.info(u"升级新版本 升级后版本号与升级版本号不一致")
            raise Exception('升级新版本 升级后版本号与升级版本号不一致')
        else:
            print('升级新版本 验证通过')
        self.driver.quit()


    def test_oldSoftware4(self, oldversion4=getweb('oldversion4')):
        u'''软件升级 - 更新旧版本测试'''
        # oldversion1 = getweb('oldversion1')
        self.oldversion1 = oldversion4
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        oldversioa1 = oldversion4.split(r'-')
        if len(oldversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = oldversioa1[0] + '-' + oldversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(oldversioa1) - 1:
                Expect_Version += oldversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        # print(Expect_Version)

        # 版本上传
        oldSoftware = (str(tmppath) + str(oldversion4) + '.bin')

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(oldSoftware)
        # software.input_updatesoftware(oldSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips = str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        # 判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version:
            CapPic(self.driver)
            logger.info(u"升级旧版本 升级后版本号与升级版本号不一致")
            raise Exception('升级旧版本 升级后版本号与升级版本号不一致')
        else:
            print('更新 旧型号版本 验证通过')
        self.driver.quit()

    def test_newSoftware4(self, newversion4=getweb('SoftVersion4')):
        u'''软件升级 - 更新新正常版本'''
        # newversion = getweb('SoftVersion1')
        UploadingTips = getAssertText('UploadingTips')
        WillReboottips = getAssertText('WillReboottips')

        num = 0
        Expect_Version = ''
        newversioa1 = newversion4.split(r'-')
        if len(newversioa1) == 2:  # eg:'nv640Ev1.5.0-130918'
            Expect_Version = newversioa1[0] + '-' + newversioa1[1]
        else:  # eg:'nvA655Wv3.0.0-200116-142208' ; 'TL-BWR-21v3.2.1-200304-171146'
            while num < len(newversioa1) - 1:
                Expect_Version += newversioa1[num] + '-'
                num += 1
            else:
                Expect_Version = Expect_Version[:-1]
        print(Expect_Version)

        # 版本上传
        newSoftware = (str(tmppath) + str(newversion4) + '.bin')

        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 选择文件上传
        self.driver.find_element_by_name('updatesoftware').send_keys(newSoftware)
        # software.input_updatesoftware(newSoftware)
        time.sleep(1)
        software.click_update()
        time.sleep(1)
        software.click_ok()
        time.sleep(3)
        # 小设备 上传时间较长，判断sleep时间
        tips = str(software.getText_byClass(software.u_tim_str))
        if UploadingTips in tips:
            time.sleep(50)
        elif tips == WillReboottips:
            time.sleep(3)
        # 设备重启时间不一致，做个判断
        time.sleep(30)
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            print(now_url, i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()

        # 判断是否升级成功
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        software = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-系统升级
        software.click_sysConfig()
        time.sleep(0.5)
        software.click_Maintenance()
        time.sleep(1)
        now_Version = str(software.getText_byXpath(software.version))
        if Expect_Version != now_Version:
            CapPic(self.driver)
            logger.info(u"升级新版本 升级后版本号与升级版本号不一致")
            raise Exception('升级新版本 升级后版本号与升级版本号不一致')
        else:
            print('升级新版本 验证通过')
        self.driver.quit()

    def tearDown(self):
        print('sysConfig_006_softwareUpdata over')

if __name__=='__main__':
    unittest.main()
