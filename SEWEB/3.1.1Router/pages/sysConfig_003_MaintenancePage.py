#! -*-conding:utf-8 -*-
#@Time: 2019/1/18 0018 14:40
#@swzhou
'''
系统管理 - 系统维护界面
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'MaintenancePage').getlog()
from common.ReadConfig import getMenu

class MaintenancePage(BasePage):
    MaintenanceM = getMenu('MaintenanceM')
    configurationM = getMenu('configurationM')
    RebootDeviceM = getMenu('RebootDeviceM')
    policylibM = getMenu('policylibM')
    licenseM = getMenu('licenseM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    Maintenance = (By.LINK_TEXT, MaintenanceM)  # 系统维护菜单
    #配置管理
    configuration = (By.LINK_TEXT,configurationM) #配置管理菜单
    output = (By.ID,'output')
    restore = (By.ID,'restore')
    ok = (By.ID,'u-cfm-ok')
    no = (By.ID,'u-cfm-no')
    chooseFile = (By.ID,'chooseFile')
    innerput = (By.ID,'innerput')
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    output1 = ('output')
    restore1 = ('restore')
    chooseFile1 = ('chooseFile')
    innerput1 = ('innerput')
    #系统升级
    updatesoftware = (By.NAME,'updatesoftware')
    update = (By.ID,'update')
    pageTip_warn = ('pageTip-warn')
    u_tim_str = ('u-tim-str')
    version = ('//*[@id="iframe1"]/table/tbody/tr[2]/td[2]/span')
    handOnChange1 = ('handOnChange') #选择文件
    update1 = ('update')
    #重启
    headerReboot = (By.ID,'header_reboot_link_span')
    RebootDevice = (By.LINK_TEXT,RebootDeviceM)
    reboot = (By.ID,'reboot')
    #策略库
    policylib = (By.LINK_TEXT,policylibM)
    showState = ('showState') #版本状态
    strategyName = ('strategyName') #应用策略库版本
    onkeyup = (By.ID,'onkeyup')
    recheck = (By.ID,'recheck')
    policyVer1 =('//*[@id="3"]/table/tbody/tr[1]/td[1]/label') #应用策略库版本
    priorityTemp1 = ('//*[@id="3"]/table/tbody/tr[2]/td[1]/label') #应用优先模板版本
    versions1 = ('//*[@id="3"]/table/tbody/tr[3]/td[1]/label') #版本状态
    #电子授权
    license = (By.LINK_TEXT,licenseM)
    days1 = ('//*[@id="iframe5"]/table/tbody/tr[1]/td/span[2]') #有效期永久
    days2 = ('//*[@id="iframe5"]/table/tbody/tr[1]/td/span[5]') #有效期天数

    innerputl = (By.XPATH,'//*[@id="iframe5"]/table/tbody/tr[6]/td[3]/button')



    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_Maintenance(self):
        self.find_element(*self.Maintenance).click()
        logger.info('点击系统维护')

    def click_configuration(self):
        self.find_element(*self.configuration).click()
        logger.info('点击配置管理')

    def click_output(self):
        self.find_element(*self.output).click()

    def click_restore(self):
        self.find_element(*self.restore).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_no(self):
        self.find_element(*self.no).click()

    def click_chooseFile(self):
        self.find_element(*self.chooseFile).click()

    def click_innerput(self):
        self.find_element(*self.innerput).click()

    def input_updatesoftware(self,updatesoftware):
        self.find_element(*self.updatesoftware).send_keys(updatesoftware)

    def click_update(self):
        self.find_element(*self.update).click()

    def click_headerReboot(self):
        self.find_element(*self.headerReboot).click()

    def click_RebootDevice(self):
        self.find_element(*self.RebootDevice).click()

    def click_reboot(self):
        self.find_element(*self.reboot).click()

    def click_policylib(self):
        self.find_element(*self.policylib).click()

    def click_onkeyup(self):
        self.find_element(*self.onkeyup).click()

    def click_recheck(self):
        self.find_element(*self.recheck).click()

    def click_license(self):
        self.exist_element(*self.license).click()
        logger.info('点击电子授权')

    def click_licensel(self):
        self.exist_element(*self.licensel).click()