#! -*-conding:utf-8 -*-
#@Time: 2019/1/22 0022 16:58
#@swzhou
'''
系统管理 - 网管策略界面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ManagementPolicyPage').getlog()
from common.ReadConfig import getMenu

class ManagementPolicyPage(BasePage):
    ManagementPolicyM = getMenu('ManagementPolicyM')
    lanAccessControlM = getMenu('lanAccessControlM')
    RemoteManagementM = getMenu('RemoteManagementM')
    AccessPolicyM = getMenu('AccessPolicyM')
    LanguageM = getMenu('LanguageM')

    sysConfig = (By.XPATH, '//span[@data-local="{sysConfig}"]') #系统配置菜单
    ManagementPolicy = (By.LINK_TEXT, ManagementPolicyM)  # 网管策略菜单
    #系统管理员
    add = (By.ID,'add')
    username = (By.NAME,'username')
    passwd1 = (By.NAME,'passwd1')
    passwd2 = (By.NAME,'passwd2')
    role = ('role')
    save = (By.ID,'save')
    list_name1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[2]/span')
    list_role1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[3]/span')
    list_edit1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/span[1]')
    input_group = (By.CLASS_NAME,'input-group') #修改后点击下其他元素，避免没有保存成功
    list_delete1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/span[2]')
    ok = (By.ID,'u-cfm-ok')
    pageTip_warn = ('pageTip-warn')
    list2_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td')
    defaultAcc = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span') #admin账号
    defaultRole = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')

    #远程管理
    RemoteManagement = (By.LINK_TEXT,RemoteManagementM)
    httpEn = (By.XPATH,'//input[@name="HttpEnable"and@value="1"]')
    httpEnS = ('//input[@name="HttpEnable"and@value="1"]')
    httpC = (By.XPATH, '//input[@name="HttpEnable"and@value="0"]')
    httpCs = ('//input[@name="HttpEnable"and@value="0"]')
    OutPort1 = ('OutPort')
    #内网访问控制
    lanAccessControl = (By.LINK_TEXT,lanAccessControlM)
    choosePeople = (By.NAME,'choosePeople')
    userall = (By.XPATH, '//input[@name="applyType"and@value="all"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    Root = (By.ID, 'newTree_1_check')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    starip = (By.NAME, 'starip')
    endip = (By.NAME, 'endip')
    saveW1 = (By.XPATH, '//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]')  # 弹窗保存
    innerAccessControlEn = (By.XPATH,'//input[@name="innerAccessControl"and@value="on"]')
    innerAccessControlEns = ('//input[@name="innerAccessControl"and@value="on"]')
    innerAccessControlC = (By.XPATH, '//input[@name="innerAccessControl"and@value="off"]')
    innerAccessControlCs = ('//input[@name="innerAccessControl"and@value="off"]')
    #语言
    Language = (By.LINK_TEXT,LanguageM)
    languageText = ('//*[@id="5"]/table/tbody/tr/td[2]/span')
    #网管访问策略
    AccessPolicy = (By.XPATH,AccessPolicyM)
    httpwebEn = (By.XPATH,'//input[@value="1"and@data-control-src="HTTP"]')
    httpwebEns = ('//input[@value="1"and@data-control-src="HTTP"]')
    httpswebEn = (By.XPATH, '//input[@value="2"and@data-control-src="HTTPS"]')
    httpswebEns = ('//input[@value="2"and@data-control-src="HTTPS"]')
    passwdErrNum = (By.NAME,'passwdErrNum')
    loginSpan = (By.NAME,'loginSpan')
    sessionLife = (By.NAME,'sessionLife')
    passwdErrNum1 = ('passwdErrNum')
    loginSpan1 = ('loginSpan')
    sessionLife1 = ('sessionLife')


    def click_sysConfig(self):
        self.find_element(*self.sysConfig).click()
        logger.info('点击系统配置')

    def click_ManagementPolicy(self):
        self.find_element(*self.ManagementPolicy).click()
        logger.info('点击网管策略')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_username(self, username):
        self.find_element(*self.username).clear()
        self.find_element(*self.username).send_keys(username)

    def input_passwd1(self, passwd1):
        self.find_element(*self.passwd1).clear()
        self.find_element(*self.passwd1).send_keys(passwd1)

    def input_passwd2(self, passwd2):
        self.find_element(*self.passwd2).clear()
        self.find_element(*self.passwd2).send_keys(passwd2)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_listEdit1(self):
        self.find_element(*self.list_edit1).click()

    def click_input_group(self):
        self.find_element(*self.input_group).click()

    def click_listDelete1(self):
        self.find_element(*self.list_delete1).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_RemoteManagement(self):
        self.find_element(*self.RemoteManagement).click()

    def click_httpEn(self):
        self.find_element(*self.httpEn).click()

    def click_httpC(self):
        self.find_element(*self.httpC).click()

    def click_lanAccessControl(self):
        self.find_element(*self.lanAccessControl).click()
        logger.info('点击内网访问控制')

    def click_choosePeople(self):
        self.find_element(*self.choosePeople).click()

    def click_userall(self):
        self.find_element(*self.userall).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_Root(self):
        self.find_element(*self.Root).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_saveW1(self):
        self.find_element(*self.saveW1).click()

    def click_innerAccessControlEn(self):
        self.find_element(*self.innerAccessControlEn).click()

    def input_starip(self, starip):
        self.find_element(*self.starip).clear()
        self.find_element(*self.starip).send_keys(starip)

    def input_endip(self, endip):
        self.find_element(*self.endip).clear()
        self.find_element(*self.endip).send_keys(endip)

    def click_innerAccessControlC(self):
        self.find_element(*self.innerAccessControlC).click()

    def click_Language(self):
        self.find_element(*self.Language).click()
        logger.info('点击语言选择')

    def click_AccessPolicy(self):
        self.find_element(*self.AccessPolicy).click()
        logger.info('点击网管访问策略')

    def click_httpwebEn(self):
        self.find_element(*self.httpwebEn).click()

    def click_httpswebEn(self):
        self.find_element(*self.httpswebEn).click()

    def input_passwdErrNum(self, passwdErrNum):
        self.find_element(*self.passwdErrNum).clear()
        self.find_element(*self.passwdErrNum).send_keys(passwdErrNum)

    def input_loginSpan(self, loginSpan):
        self.find_element(*self.loginSpan).clear()
        self.find_element(*self.loginSpan).send_keys(loginSpan)

    def input_sessionLife(self, sessionLife):
        self.find_element(*self.sessionLife).clear()
        self.find_element(*self.sessionLife).send_keys(sessionLife)