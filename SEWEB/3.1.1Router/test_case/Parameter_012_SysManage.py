#! -*-conding:utf-8 -*-
#@Time: 2019/2/14 0014 11:07
#@swzhou
'''
系统管理
'''


import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter,getweb
from common.loginRoute import login
from common.GetExcelValue import getExcelValue
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
from pages.sysConfig_002_sysTimePage import sysTimePage
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from pages.sysConfig_004_ToolsPage import ToolsPage
from pages.sysConfig_005_syslogPage import syslogPage
from pages.sysConfig_006_ScheduledTaskPage import ScheduledTaskPage
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException
logger = LogGen(Logger = 'Parameter_012_SysManage').getlog()

class SysManage(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        config = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护
        config.click_sysConfig()
        time.sleep(0.5)
        config.click_Maintenance()
        time.sleep(1)
        # pass

    def test_001_backup_resert(self):
        u'''配置备份及还原'''
        ExportA = getAssertText('ExportA')
        ImportA = getAssertText('ImportA')
        SelectFileA = getAssertText('SelectFileA')
        ResetA = getAssertText('ResetA')
        config = MaintenancePage(self.driver, self.url)
        config.click_configuration()
        time.sleep(1)
        output = str(config.getText_byID(config.output1))
        chooseFile = str(config.getText_byID(config.chooseFile1))
        innerput = str(config.getText_byID(config.innerput1))
        restore = str(config.getText_byID(config.restore1))
        self.assertEqual(output,ExportA ,msg='导出 按钮有误')
        self.assertEqual(chooseFile, SelectFileA, msg='选择文件 按钮有误')
        self.assertEqual(innerput, ImportA, msg='导入 按钮有误')
        self.assertEqual(restore, ResetA, msg='恢复出厂设置 按钮有误')
        self.driver.quit()
        logger.info('test_001_backup_resert passed')

    def test_002_update(self):
        u'''固件升级'''
        UpgradeA = getAssertText('UpgradeA')
        SelectFileA = getAssertText('SelectFileA')
        software = MaintenancePage(self.driver, self.url)
        handOnChange = str(software.getText_byID(software.handOnChange1))
        update = str(software.getText_byID(software.update1))
        self.assertEqual(handOnChange, SelectFileA, msg='选择文件 按钮有误')
        self.assertEqual(update, UpgradeA, msg='升级 按钮有误')
        self.driver.quit()
        logger.info('test_002_update passed')

    def test_003_AppLibrary(self):
        u'''应用特征库升级'''
        AppUpgradeP = getParameter('AppUpgradeP')
        Support = getExcelValue(AppUpgradeP)
        policyVerA = getAssertText('policyVerA')
        priorityTempA = getAssertText('priorityTempA')
        versionsA = getAssertText('versionsA')
        policylib = MaintenancePage(self.driver, self.url)
        if Support == '√' :
            logger.info(u'参数支持应用特征库升级')
            try:
                self.driver.implicitly_wait(2)
                policylib.click_policylib()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持应用特征库升级,与参数表不相符')
                raise Exception('不支持应用特征库升级,与参数表不相符')
            else:
                time.sleep(1)
                self.driver.implicitly_wait(10)
                policyVer1 = str(policylib.getText_byXpath(policylib.policyVer1))
                priorityTemp1 = str(policylib.getText_byXpath(policylib.priorityTemp1))
                versions1 = str(policylib.getText_byXpath(policylib.versions1))
                self.assertEqual(policyVer1, policyVerA, msg='应用策略库版本 按钮有误')
                self.assertEqual(priorityTemp1, priorityTempA, msg='应用优先模板版本 按钮有误')
                self.assertEqual(versions1, versionsA, msg='版本状态 按钮有误')
        elif Support == '×' :
            logger.info(u'参数不支持应用特征库升级')
            try:
                self.driver.implicitly_wait(2)
                policylib.click_policylib()
            except AttributeError:
                logger.info('不支持应用特征库升级，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'支持应用特征库升级，与参数表不相符')
                raise Exception('支持应用特征库升级，与参数表不相符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_003_AppLibrary passed')

    def test_004_syslog(self):
        u'''系统日志、syslog'''
        ExportA = getAssertText('ExportA')
        syslog = syslogPage(self.driver,self.url)
        syslog.click_Syslog()
        time.sleep(1)
        export = str(syslog.getText_byID(syslog.export1))
        self.assertEqual(export, ExportA, msg='系统日志页面导出 按钮有误')

        syslog.click_SyslogServer()
        time.sleep(1)
        switch = str(syslog.getAttribute_byXpath(syslog.SyslogCs,'checked'))
        self.assertEqual(switch, 'true', msg='syslog默认关闭 有误')

        syslog.click_Logtype()
        time.sleep(0.5)

        self.driver.quit()
        logger.info('test_004_syslog passed')

    def test_005_ClockServer(self):
        u'''时钟管理'''
        TimeInternetA = getAssertText('TimeInternetA')
        ntpServer = getweb('ntpServer')
        sysTime = sysTimePage(self.driver,self.url)

        sysTime.click_SystemTime()
        time.sleep(1)
        switch = str(sysTime.getAttribute_byXpath(sysTime.SntpEns,'checked'))
        tips = str(sysTime.getText_byXpath(sysTime.withInternet1))
        self.assertEqual(switch, 'true', msg='网络时间同步 默认开启 有误')
        self.assertEqual(tips, TimeInternetA, msg='网络时间同步 按钮有误')

        # 判断页面时间 日期 如不同步更换ntpserver
        dates = sysTime.getText_byID(sysTime.dates)
        now = time.strftime("%Y-%m-%d")
        if dates != now:
            sysTime.input_NTPServerIP(ntpServer)
            sysTime.click_save()
            time.sleep(2)
        i = 0
        while i < 20:
            sysTime.click_SystemTime()
            time.sleep(1)
            dates = sysTime.getText_byID(sysTime.dates)
            if dates == now:
                break
            else:
                i += 1
        else:
            logger.info('页面时间为：%s' % dates)
            logger.info('PC时间为：%s' % now)
            raise Exception('时间不同步')


        self.driver.quit()
        logger.info('test_005_ClockServer passed')

    def test_006_RemoteManagement(self):
        u'''远程管理'''
        management = ManagementPolicyPage(self.driver,self.url)
        management.click_ManagementPolicy()
        time.sleep(1)
        management.click_RemoteManagement()
        time.sleep(0.5)
        switch = str(management.getAttribute_byXpath(management.httpCs,'checked'))
        port = str(management.getAttribute_byName(management.OutPort1,'value'))
        self.assertEqual(switch, 'true', msg='远程管理默认关闭 有误')
        self.assertEqual(port, '8081', msg='远程管理端口 默认不为8081')
        self.driver.quit()
        logger.info('test_006_RemoteManagement passed')

    def test_007_RemotePlannedTask(self):
        u'''计划任务（某些型号不支持AP的计划任务）'''
        APnumP = getParameter('APnumP')
        Support = getExcelValue(APnumP)
        scheduled = ScheduledTaskPage(self.driver,self.url)
        scheduled.click_ScheduledTask()
        time.sleep(1)
        scheduled.click_add()
        time.sleep(1)
        selobj = scheduled.selelement_byName(scheduled.obj)
        Select(selobj).select_by_value('01')#01本设备
        time.sleep(0.5)
        if Support != None and Support != '×' :
            logger.info(u'参数支持 AP管理')
            try:
                Select(selobj).select_by_value('02')  # 02 AP
            except ElementNotVisibleException:
                CapPic(self.driver)
                logger.info(u'软件不支持AP的计划任务，与参数表不符')
                raise Exception('软件不支持AP的计划任务，与参数表不符')
            else:
                logger.info(u'软件支持AP的计划任务，与参数表相符')
                time.sleep(0.5)
                selcontent = scheduled.selelement_byName(scheduled.selContent)
                Select(selcontent).select_by_value('rebootS')  # 仅一个选择
                time.sleep(0.5)
        else:
            logger.info(u'参数不支持 AP管理')
            try:
                self.driver.implicitly_wait(2)
                Select(selobj).select_by_value('02')
            except ElementNotVisibleException:
                logger.info(u'软件不支持AP的计划任务，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持AP的计划任务，与参数表不符')
                raise Exception(u'软件支持AP的计划任务，与参数表不符')
        self.driver.quit()
        logger.info('test_007_RemotePlannedTask passed')

    def test_008_license(self):
        u'''电子授权（某些型号可能不支持）'''
        dayA = getAssertText('dayA')
        day2A = getAssertText('day2A')
        SelectFileA = getAssertText('SelectFileA')
        ImportA = getAssertText('ImportA')
        licenseP = getParameter('licenseP')
        Support = getExcelValue(licenseP)
        maintenance = MaintenancePage(self.driver,self.url)
        time.sleep(1)
        if Support == '√':
            try:
                self.driver.implicitly_wait(2)
                maintenance.click_license()
                time.sleep(1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'软件不支持电子授权，与参数表不相符')
                raise Exception('软件不支持电子授权，与参数表不相符')
            else:
                try:
                    days1 = maintenance.getText_byXpath(maintenance.days1)
                    self.assertIn(day2A, days1, msg='剩余时间 显示不为永久 ')
                except AssertionError:
                    try:
                        days = maintenance.getText_byXpath(maintenance.days2)
                        self.assertIn(dayA, days,msg='剩余时间 显示不为 天数')
                    except AssertionError:
                        raise Exception('剩余时间不显示')
                chooseFile = str(maintenance.getText_byID(maintenance.chooseFile1))
                innerput = str(maintenance.getText_byID(maintenance.innerput1))
                self.assertEqual(chooseFile, SelectFileA, msg='选择文件 按钮有误')
                self.assertEqual(innerput, ImportA, msg='导入 按钮有误')
        elif Support == '×' or '--':
            try:
                self.driver.implicitly_wait(2)
                maintenance.click_license()
            except NoSuchElementException:
                logger.info('软件不支持电子授权,与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持电子授权，与参数表不符')
                raise Exception(u'软件支持电子授权，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_008_license passed')

    def test_009_DiagnosticTest(self):
        u'''诊断测试'''
        pingsA = getAssertText('pingsA')
        MaxTTLA = getAssertText('MaxTTLA')
        tools = ToolsPage(self.driver,self.url)
        tools.click_Tools()
        time.sleep(1)
        ping = (tools.getText_byXpath(tools.ping))
        self.assertEqual(ping ,pingsA ,'ping页面按钮有误')

        tools.click_TraceRoute()
        time.sleep(1)
        maxTTL = (tools.getText_byXpath(tools.maxTTL1))
        self.assertEqual(maxTTL, MaxTTLA , 'TraceRoute页面按钮有误')

        self.driver.quit()
        logger.info('test_009_DiagnosticTest passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
