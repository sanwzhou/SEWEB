#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 15:47
#@swzhou
'''
用户管理:
用户统计、IP/MAC地址绑定、pppoe_server、本地认证、远程认证、黑名单
'''

import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from pages.Organization_001_Memberspage import OrganizationMembersPage
from pages.Organization_002_userStatuspage import Organization_userStatusPage
from pages.Organization_003_userAuthpage import Organization_userAuthPage
from pages.Organization_004_userBlackpage import Organization_userBlackPage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException,ElementNotInteractableException
logger = LogGen(Logger = 'Parameter_023_userManagement').getlog()

class userManagement(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        userstatus = Organization_userStatusPage(self.driver,self.url)
        userstatus.click_UserManage()
        time.sleep(0.5)
        # pass

    def test_001_UserStatistics(self):
        u'''用户统计(某些型号不支持建立pppoe账号)'''
        tempUser = getAssertText('tempUser')
        Minute = getAssertText('minute')
        Ban = getAssertText('Ban')
        pppoeSp = getParameter('pppoeSp')
        SupportP = getExcelValue(pppoeSp)
        webAutnp = getParameter('webAutnp')
        SupportW = getExcelValue(webAutnp)
        
        userstatus = Organization_userStatusPage(self.driver, self.url)
        userstatus.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        selmanual = userstatus.selelement_byXpath(userstatus.selmanual)
        Select(selmanual).select_by_value('3')
        time.sleep(0.3)
        Select(selmanual).select_by_value('5')
        time.sleep(0.3)
        Select(selmanual).select_by_value('10')
        time.sleep(0.3)
        Select(selmanual).select_by_value('60')
        time.sleep(0.3)
        Select(selmanual).select_by_value('manual')
        time.sleep(0.3)
        userstatus.click_refreshtable()
        time.sleep(1)
        #右上角移动、加入黑名单按钮
        userstatus.find_move()
        userstatus.find_addToBlackList()
        # 定义页面显示元素变量
        ID = str(userstatus.getText_byXpath(userstatus.ID))
        username = str(userstatus.getText_byXpath(userstatus.username))
        group = str(userstatus.getText_byXpath(userstatus.group))
        VlanID = str(userstatus.getText_byXpath(userstatus.VlanID))
        IP = str(userstatus.getText_byXpath(userstatus.IP))
        mac = str(userstatus.getText_byXpath(userstatus.mac))
        authmode = str(userstatus.getText_byXpath(userstatus.authmode))
        online_time_length = str(userstatus.getText_byXpath(userstatus.online_time_length))
        Uploading_data = str(userstatus.getText_byXpath(userstatus.Uploading_data))
        Downing_data = str(userstatus.getText_byXpath(userstatus.Downing_data))
        Uploading_speed = str(userstatus.getText_byXpath(userstatus.Uploading_speed))
        Downing_speed = str(userstatus.getText_byXpath(userstatus.Downing_speed))
        edit = str(userstatus.getText_byXpath(userstatus.edit))

        # 断言 用户列表是否显示有误
        time.sleep(1)
        self.assertEqual(ID, '1', msg='ID出错')
        print('用户状态 - ID 验证成功')
        self.assertIsNotNone(username, msg='用户名 出错')
        print('用户状态 - 用户名 验证成功')
        self.assertEqual(group, tempUser, msg='所属组 出错')  # 脚本在最后会清空组织架构，所以脚本在一开始新建组，用户都是 临时用户
        print('用户状态 - 所属组 验证成功')
        self.assertIsNotNone(VlanID, msg='VLANID 出错')
        print('用户状态 - VLANID 验证成功')
        self.assertIn('192.168.', IP, msg='IP 出错')  # lan口地址段
        print('用户状态 - IP 验证成功')
        self.assertEqual(len(mac), 17, msg='mac 出错')  # 判断mac地址长度
        print('用户状态 - mac 验证成功')
        self.assertIsNotNone(authmode, msg='认证方式 出错')
        print('用户状态 - 认证方式 验证成功')
        self.assertIn(Minute, online_time_length, msg='在线时长 出错')  # 在线时长是否包含“分”
        print('用户状态 - 在线时长 验证成功')
        self.assertIsNotNone(Uploading_data, msg='上传数据 出错')
        print('用户状态 - 上传数据 验证成功')
        self.assertIsNotNone(Downing_data, msg='下载数据 出错')
        print('用户状态 - 下载数据 验证成功')
        self.assertIsNotNone(Uploading_speed, msg='上传速度 出错')
        print('用户状态 - 上传速度 验证成功')
        self.assertIsNotNone(Downing_speed, msg='下载速度 出错')
        print('用户状态 - 下载速度 验证成功')
        self.assertEqual(edit, Ban, msg='拉黑菜单显示 出错')
        print('用户状态 - 拉黑菜单显示 验证成功')

        userauth = Organization_userAuthPage(self.driver,self.url)
        userauth.click_userAuth()
        time.sleep(1)
        userauth.click_account()
        time.sleep(2)
        userauth.click_addUser()
        time.sleep(1)
        selauthType = userauth.selelement_byName(userauth.authType)
        if SupportW == '√':
            try:
                self.driver.implicitly_wait(2)
                Select(selauthType).select_by_value('Web')
            except NoSuchElementException:
                raise Exception('认证账号中不能选择web类型')
        elif SupportW == '×':
            try:
                self.driver.implicitly_wait(2)
                Select(selauthType).select_by_value('Web')
            except NoSuchElementException:
                logger.info(u'认证账号中不能选择web类型,与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'认证账号中能选择web类型,与参数表不相符')
                raise Exception('认证账号中能选择web类型,与参数表不相符')
        else:
            logger.info(u'web参数表读取异常')
            logger.info(u'web参数表读取值为：',SupportW)
            raise Exception(u'web参数表读取异常')
        time.sleep(0.3)
        if SupportP != '×':
            try:
                self.driver.implicitly_wait(2)
                Select(selauthType).select_by_value('PPPoE')
            except NoSuchElementException:
                raise Exception('认证账号中不能选择pppoe类型')
        elif SupportP == '×':
            try:
                self.driver.implicitly_wait(2)
                Select(selauthType).select_by_value('PPPoE')
            except NoSuchElementException:
                logger.info(u'认证账号中不能选择pppoe类型,与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'认证账号中能选择pppoe类型,与参数表不相符')
                raise Exception('认证账号中能选择pppoe类型,与参数表不相符')
        else:
            logger.info(u'pppoe参数表读取异常')
            logger.info(u'pppoe参数表读取值为：',SupportP)
            raise Exception(u'pppoe参数表读取异常')
        time.sleep(0.3)
        self.driver.implicitly_wait(10)

        self.driver.quit()
        logger.info('test_001_UserStatistics passed')

    def test_002_binding(self):
        u'''IP/MAC地址绑定'''
        member = OrganizationMembersPage(self.driver,self.url)
        member.click_userGroup()
        time.sleep(1)
        member.click_globalconfig()
        time.sleep(1)
        #仅IP/MAC绑定用户能上网
        member.click_IPMACb_E()
        member.click_IPMACb_C()
        # 仅MAC绑定用户能上网
        member.click_MACb_E()
        member.click_MACb_C()

        self.driver.quit()
        logger.info('test_002_binding passed')

    def test_003_PPPoESever(self):
        u'''PPPoE-Sever拨号用户（某些设备可能不支持）'''
        pppoeSp = getParameter('pppoeSp')
        Support = getExcelValue(pppoeSp)
        pppoeauth = Organization_userAuthPage(self.driver, self.url)
        pppoeauth.click_userAuth()
        time.sleep(1)
        if Support != '×':
            logger.info(u'参数支持PPPoE-Sever')
            try:
                self.driver.implicitly_wait(2)
                pppoeauth.click_PPPoEConfig()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持PPPoE Server，与参数表不符')
                raise Exception(u'软件不支持PPPoE Server，与参数表不符')
            else:
                logger.info(u'软件支持PPPoE Server，与参数表相符')
                self.driver.implicitly_wait(10)
                time.sleep(1)
                pppoeauth.click_PPPoEOnly()
                pppoeauth.find_selexceptIpGroup()
                pppoeauth.input_smaxconv('100')
                pppoeauth.click_selfHelpEnable()
                pppoeauth.click_PppoeNoticeEn()
                pppoeauth.input_remainDays('50')
                pppoeauth.click_edipage()
                time.sleep(1)
                pppoeauth.click_NoticePageName()
                pppoeauth.input_NoticePageNote('test')
                pppoeauth.input_NoticePageTitle('test')
                pppoeauth.input_SkipUrl('test')
                pppoeauth.input_SkipTime('5')
                pppoeauth.input_NoticeBody('test')
                pppoeauth.click_close()#关闭
                time.sleep(0.5)
                pppoeauth.click_modalhide()
                time.sleep(0.5)

                pppoeauth.click_account()
                time.sleep(1)
                pppoeauth.click_addUser()
                time.sleep(1)
                #并发数
                pppoeauth.input_concurrency('10')
                #绑定方式
                pppoeauth.click_addautoBind()
                pppoeauth.click_IPBind()
                pppoeauth.click_MacBind()
                pppoeauth.click_IPMacBind()
                pppoeauth.click_noBind()
                #账号计费
                pppoeauth.click_accountBillEn()
                pppoeauth.click_accountBillC()
        elif Support == '×':
            logger.info(u'参数不支持PPPoE-Sever')
            try:
                self.driver.implicitly_wait(2)
                pppoeauth.click_PPPoEConfig()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持PPPoE，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持PPPoE，与参数表不符')
                raise Exception(u'软件支持PPPoE，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_003_PPPoESever passed')

    def test_004_WEBAuth(self):
        u'''本地认证（某些设备可能不支持）'''
        webAutnp = getParameter('webAutnp')
        Support = getExcelValue(webAutnp)
        webauth = Organization_userAuthPage(self.driver, self.url)
        webauth.click_userAuth()
        time.sleep(1)
        if Support == '√':
            logger.info(u'参数支持本地认证')
            try:
                self.driver.implicitly_wait(2)
                webauth.click_WebConfig()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持本地认证，与参数表不符')
                raise Exception(u'软件不支持本地认证，与参数表不符')
            else:
                logger.info(u'软件支持本地认证，与参数表相符')
                self.driver.implicitly_wait(10)
                time.sleep(1)
                #认证页面
                webauth.click_modaifyAuthPage()
                time.sleep(1)
                webauth.input_webAuthSuccessNote('test')
                webauth.selelement_byName(webauth.en_picture)
                webauth.click_activePicEn()
                time.sleep(0.5)
                webauth.click_activePicC()
                time.sleep(0.5)
                webauth.input_tipstitle('test')
                webauth.input_tipsinfo('test')
                webauth.input_hidcontact('test')
                webauth.click_close_webauth()
                time.sleep(0.5)
                webauth.input_staleTime('5')
                webauth.click_selfenabled()
                time.sleep(0.2)
                webauth.click_modalhide()
                time.sleep(0.5)

                webauth.click_account()
                time.sleep(1)
                webauth.click_addUser()
                time.sleep(1)
                selauthType = webauth.selelement_byName(webauth.authType)
                Select(selauthType).select_by_value('Web')
                time.sleep(0.3)
                # 并发数
                webauth.input_concurrency('10')
                # 计费
                webauth.click_accountBillEn()
                time.sleep(0.3)
                selbillType = webauth.selelement_byName(webauth.billType)
                Select(selbillType).select_by_value('timeBill')
                time.sleep(0.3)
                Select(selbillType).select_by_value('dateBill')
                time.sleep(0.3)
                webauth.click_accountBillC()
                time.sleep(0.3)
        elif Support == '×':
            logger.info(u'参数不支持本地认证')
            try:
                self.driver.implicitly_wait(2)
                webauth.click_WebConfig()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持web认证，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持web认证，与参数表不符')
                raise Exception(u'软件支持web认证，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_004_WEBAuth passed')

    def test_005_RemoteAuth(self):
        u'''远程认证（某些设备可能不支持）'''
        remoteAuthP = getParameter('remoteAuthP')
        Support = getExcelValue(remoteAuthP)
        remoteauth = Organization_userAuthPage(self.driver, self.url)
        remoteauth.click_userAuth()
        time.sleep(1)
        if Support == '√':
            logger.info(u'参数支持远程认证')
            try:
                self.driver.implicitly_wait(2)
                remoteauth.click_remoteConfig()
            except AttributeError or NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持远程认证，与参数表不符')
                raise Exception(u'软件不支持远程认证，与参数表不符')
            else:
                logger.info(u'软件支持远程认证，与参数表相符')
                self.driver.implicitly_wait(10)
                time.sleep(1)
                #判断没有无流量下线
                try:
                    self.driver.implicitly_wait(2)
                    remoteauth.find_wllxxsj()
                except ElementNotVisibleException:
                    pass
                except ElementNotInteractableException:
                    pass
                else:
                    raise Exception('远程认证界面存在无流量下线')
                #域名名称
                remoteauth.click_ymmc()
                # 白名单列表
                remoteauth.click_bmdlb()
        elif Support == '×':
            logger.info(u'参数不支持远程认证')
            try:
                self.driver.implicitly_wait(2)
                remoteauth.click_remoteConfig()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持远程认证，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持远程认证，与参数表不符')
                raise Exception(u'软件支持远程认证，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',Support)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_005_RemoteAuth passed')

    def test_006_blacklist(self):
        u'''黑名单'''
        blacklist = Organization_userBlackPage(self.driver,self.url)
        blacklist.click_blacklist()
        time.sleep(1)
        blacklist.click_add()
        time.sleep(1)
        blacklist.input_bname('test')
        blacklist.input_bmac('1')
        blacklist.click_modalhide()
        time.sleep(0.5)
        blacklist.find_deleteB()
        blacklist.find_importB()
        blacklist.find_exportB()

        self.driver.quit()
        logger.info('test_006_blacklist passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
