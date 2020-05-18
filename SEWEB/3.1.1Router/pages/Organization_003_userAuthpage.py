#! -*-conding:utf-8 -*-
#@Time: 2019/1/14 0014 10:09
#@swzhou
'''
用户管理 - PPPoE认证页面
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'Organization_userAuthPage').getlog()
from common.ReadConfig import getMenu

class Organization_userAuthPage(BasePage):
    userAuthM = getMenu('userAuthM') #用户认证

    UserManage = (By.XPATH, '//span[@data-local="{UserManage}"]')
    userAuth = (By.LINK_TEXT, userAuthM)

    PPPoEConfig = (By.ID,'PPPoEConfig')
    pppoeStart = (By.NAME,'pppoeStart')
    pppoePriDns = (By.NAME,'pppoePriDns')
    PppoeNoticeEn = (By.XPATH,'//input[@name="PppoeNoticeEnable"and@value="1"]')
    remainDays = (By.NAME,'remainDays')
    save = (By.ID,'save')
    pppoeAuthEn = (By.XPATH,'//input[@name="PPPoEAuth"and@value="on"]')
    pppoeAuthEns = ('//input[@name="PPPoEAuth"and@value="on"]')
    account = (By.LINK_TEXT,getMenu('accountM'))
    addUser = (By.ID,'addUser')
    name = (By.NAME,'name')
    authType = ('authType')
    authAccount = (By.NAME,'authAccount')
    authPassword = (By.NAME,'authPassword')
    list_authtype = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    list_authAcc = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    PPPoEOnly = (By.XPATH,'//input[@name="PPPoEOnly"and@value="1"]')
    selexceptIpGroup = (By.NAME,'exceptIpGroup') #例外地址组
    smaxconv = (By.NAME,'smaxconv') #系统最大会话数
    smaxconvs = ('smaxconv')
    ipcount = ('ipcount') #总地址池数
    selfHelpEnable = (By.NAME,'selfHelpEnable') #允许用户修改拨号密码
    edipage = (By.ID,'edipage')  #账号通告页面
    NoticePageName = (By.NAME, 'NoticePageName')
    NoticePageNote = (By.NAME, 'NoticePageNote')
    NoticePageTitle = (By.NAME, 'NoticePageTitle')
    SkipUrl = (By.NAME, 'SkipUrl')
    SkipTime = (By.NAME, 'SkipTime')
    NoticeBody = (By.NAME, 'NoticeBody')
    close = (By.XPATH,'//*[@id="notepageEdit_Modal"]/div/div/div[3]/ul/li[4]') #关闭
    modalhide = (By.ID, 'modal-hide')
    concurrency = (By.NAME,'concurrency') #并发数
    addautoBind = (By.XPATH,'//input[@name="authUserLinkType"and@value="autoBind"]') #认证账号新增自动绑定
    IPBind = (By.XPATH,'//input[@name="authUserLinkType"and@value="IP"]')
    MacBind = (By.XPATH,'//input[@name="authUserLinkType"and@value="Mac"]')
    IPMacBind = (By.XPATH,'//input[@name="authUserLinkType"and@value="IPMac"]')
    noBind = (By.XPATH,'//input[@name="authUserLinkType"and@value="no"]')
    # 账号计费
    accountBillC = (By.XPATH,'//input[@name="accountBill"and@value="off"]')

    accountBillEn = (By.XPATH,'//input[@name="accountBill"and@value="on"]') #计费
    accountOpenDate = (By.NAME,'accountOpenDate')
    bn_preMonth = (By.ID,'bn_preMonth')  # 向前一个月
    day1 = (By.XPATH,'//*[@id="JTC_TheCurDay8"]') # 任意选择
    accountStopDate = (By.NAME,'accountStopDate')
    day2 = (By.XPATH,'//*[@id="JTC_TheCurDay9"]')
    list_authtype2 = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[2]/td[6]/span')
    list_authAcc2 = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[2]/td[3]/span')

    bn_postMonth = (By.XPATH,'//*[@type="button"and@value=">"]')  # 向后一个月
    day3 = (By.XPATH,'//*[@id="JTC_TheCurDay6"]')# 第一行最后一个位置，一定有值
    list_authtype3 = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[3]/td[6]/span')
    list_authAcc3 = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[3]/td[3]/span')
    pppoeAuthC = (By.XPATH, '//input[@name="PPPoEAuth"and@value="off"]')
    pppoeAuthCs = ('//input[@name="PPPoEAuth"and@value="off"]')

    WebAuthEn = (By.XPATH,'//input[@name="WebAuth"and@value="on"]')
    WebAuthEs = ('//input[@name="WebAuth"and@value="on"]')
    userName = (By.NAME,'userName')
    userPasswd = (By.NAME,'userPasswd')
    login_btn = (By.ID,'login_btn')
    WebAuthC = (By.XPATH, '//input[@name="WebAuth"and@value="off"]')
    WebAuthCs = ('//input[@name="WebAuth"and@value="off"]')
    WebConfig = (By.ID,'WebConfig')
    modaifyAuthPage = (By.ID,'modaifyAuthPage') #认证页面编辑
    webAuthSuccessNote = (By.NAME,'webAuthSuccessNote') #备注
    en_picture = ('en_picture') #页面使用
    activePicEn = (By.XPATH,'//input[@name="activePic"and@value="1"]') #背景图片使用
    activePicC = (By.XPATH, '//input[@name="activePic"and@value="0"]')
    tipstitle = (By.NAME,'tipstitle')
    tipsinfo = (By.NAME,'tipsinfo')
    hidcontact = (By.NAME,'hidcontact')
    close_webauth = (By.XPATH,'//*[@id="webAuthEditModal"]/div/div/div[3]/ul/li[4]')
    staleTime = (By.NAME,'staleTime') #无流量下线时间
    selfenabled = (By.NAME,'selfenabled') #允许用户修改认证密码
    billType = ('billType')

    FreeAuthEn = (By.XPATH,'//input[@name="noAuth"and@value="on"]')
    FreeAuthEs = ('//input[@name="noAuth"and@value="on"]')
    noConfig = (By.ID,'noConfig')
    alluser =(By.XPATH,'//input[@name="applyType"and@value="all"]')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    Root = (By.ID,'newTree_1_check')
    starip = (By.NAME,'starip')
    endip = (By.NAME,'endip')
    FreeAuthC = (By.XPATH, '//input[@name="noAuth"and@value="off"]')
    FreeAuthCs = ('//input[@name="noAuth"and@value="off"]')

    list_edit1 = (By.XPATH,'//*[@data-primarykey="0"and@data-event="edit"]')
    list_AccountingType = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[1]/td[10]/span')
    autoBind = (By.XPATH,'//input[@type="radio"and@value="autoBind"]')
    list_bindingMode = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    selAll = (By.XPATH,'//*[@id="2"]/div/div/div/div[1]/table/thead/tr/th[1]/input')
    deleteAll = (By.ID,'deleteAll')
    ok = (By.ID,'u-cfm-ok')
    list_tips = ('//*[@id="2"]/div/div/div/div[1]/table/tbody/tr[1]/td/div')

    #远程认证
    remoteAuthEn = (By.XPATH,'//input[@name="remoteAuth"and@value="on"]')
    remoteAuthEs = ('//input[@name="remoteAuth"and@value="on"]')
    pageTip = ('tips-show-in')
    remoteAuthC = (By.XPATH, '//input[@name="remoteAuth"and@value="off"]')
    remoteAuthCs = ('//input[@name="remoteAuth"and@value="off"]')
    remoteConfig = (By.ID,'remoteConfig')
    wllxxsj = (By.NAME,'wllxxsj')  #判断没有无流量下线
    ymmc = (By.NAME,'ymmc') #域名名称
    bmdlb = (By.NAME,'bmdlb') # 白名单列表


    def click_UserManage(self):
        self.find_element(*self.UserManage).click()
        logger.info('点击用户管理')

    def click_userAuth(self):
        self.find_element(*self.userAuth).click()
        logger.info('点击用户认证')

    def click_PPPoEConfig(self):
        self.find_element(*self.PPPoEConfig).click()

    def input_pppoeStart(self,pppoeStart):
        self.find_element(*self.pppoeStart).clear()
        self.find_element(*self.pppoeStart).send_keys(pppoeStart)

    def input_pppoePriDns(self,pppoePriDns):
        self.find_element(*self.pppoePriDns).clear()
        self.find_element(*self.pppoePriDns).send_keys(pppoePriDns)

    def click_PppoeNoticeEn(self):
        self.find_element(*self.PppoeNoticeEn).click()

    def input_remainDays(self,remainDays):
        self.find_element(*self.remainDays).clear()
        self.find_element(*self.remainDays).send_keys(remainDays)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_pppoeAuthEn(self):
        self.find_element(*self.pppoeAuthEn).click()

    def click_account(self):
        self.find_element(*self.account).click()
        logger.info('点击认证账号子页面')

    def click_addUser(self):
        self.find_element(*self.addUser).click()

    def input_name(self,name):
        self.find_element(*self.name).clear()
        self.find_element(*self.name).send_keys(name)

    def input_authAccount(self,authAccount):
        self.find_element(*self.authAccount).clear()
        self.find_element(*self.authAccount).send_keys(authAccount)

    def input_authPassword(self,authPassword):
        self.find_element(*self.authPassword).clear()
        self.find_element(*self.authPassword).send_keys(authPassword)

    def click_accountBillEn(self):
        self.find_element(*self.accountBillEn).click()

    def click_accountOpenDater(self):
        self.find_element(*self.accountOpenDate).click()

    def click_bnpreMonth(self):
        self.find_element(*self.bn_preMonth).click()

    def click_day1(self):
        self.find_element(*self.day1).click()

    def click_accountStopDate(self):
        self.find_element(*self.accountStopDate).click()

    def click_day2(self):
        self.find_element(*self.day2).click()

    def click_bnpostMonth(self):
        self.find_element(*self.bn_postMonth).click()

    def click_day3(self):
        self.find_element(*self.day3).click()

    def click_pppoeAuthC(self):
        self.find_element(*self.pppoeAuthC).click()

    def find_pppoeAuthC(self):
        self.exist_element(*self.pppoeAuthC).click()

    def click_WebAuthEn(self):
        self.find_element(*self.WebAuthEn).click()

    def input_userName(self,userName):
        self.find_element(*self.userName).clear()
        self.find_element(*self.userName).send_keys(userName)

    def input_userPasswd(self,userPasswd):
        self.find_element(*self.userPasswd).clear()
        self.find_element(*self.userPasswd).send_keys(userPasswd)

    def click_loginbtn(self):
        self.find_element(*self.login_btn).click()

    def click_WebAuthC(self):
        self.find_element(*self.WebAuthC).click()

    def find_WebAuthC(self):
        self.exist_element(*self.WebAuthC).click()

    def click_FreeAuthEn(self):
        self.find_element(*self.FreeAuthEn).click()

    def click_noConfig(self):
        self.find_element(*self.noConfig).click()

    def click_alluser(self):
        self.find_element(*self.alluser).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def click_Root(self):
        self.find_element(*self.Root).click()

    def input_starip(self,starip):
        self.find_element(*self.starip).clear()
        self.find_element(*self.starip).send_keys(starip)

    def input_endip(self,endip):
        self.find_element(*self.endip).clear()
        self.find_element(*self.endip).send_keys(endip)

    def click_FreeAuthC(self):
        self.find_element(*self.FreeAuthC).click()

    def click_deleteAll(self):
        self.find_element(*self.deleteAll).click()

    def click_listedit1(self):
        self.find_element(*self.list_edit1).click()

    def click_autoBind(self):
        self.find_element(*self.autoBind).click()

    def click_selAll(self):
        self.find_element(*self.selAll).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_remoteAuthEn(self):
        self.find_element(*self.remoteAuthEn).click()

    def click_remoteAuthC(self):
        self.find_element(*self.remoteAuthC).click()

    def click_PPPoEOnly(self):
        self.find_element(*self.PPPoEOnly).click()

    def find_selexceptIpGroup(self):
        self.exist_element(*self.selexceptIpGroup).click()

    def input_smaxconv(self, smaxconv):
        self.find_element(*self.smaxconv).clear()
        self.find_element(*self.smaxconv).send_keys(smaxconv)

    def click_selfHelpEnable(self):
        self.find_element(*self.selfHelpEnable).click()

    def click_edipage(self):
        self.find_element(*self.edipage).click()

    def click_NoticePageName(self):
        self.find_element(*self.NoticePageName).click()

    def input_NoticePageNote(self, NoticePageNote):
        self.find_element(*self.NoticePageNote).clear()
        self.find_element(*self.NoticePageNote).send_keys(NoticePageNote)

    def input_NoticePageTitle(self, NoticePageTitle):
        self.find_element(*self.NoticePageTitle).clear()
        self.find_element(*self.NoticePageTitle).send_keys(NoticePageTitle)

    def input_SkipUrl(self, SkipUrl):
        self.find_element(*self.SkipUrl).clear()
        self.find_element(*self.SkipUrl).send_keys(SkipUrl)

    def input_SkipTime(self, SkipTime):
        self.find_element(*self.SkipTime).clear()
        self.find_element(*self.SkipTime).send_keys(SkipTime)

    def input_NoticeBody(self, NoticeBody):
        self.find_element(*self.NoticeBody).clear()
        self.find_element(*self.NoticeBody).send_keys(NoticeBody)

    def click_close(self):
        self.find_element(*self.close).click()

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def input_concurrency(self, concurrency):
        self.find_element(*self.concurrency).clear()
        self.find_element(*self.concurrency).send_keys(concurrency)

    def click_addautoBind(self):
        self.find_element(*self.addautoBind).click()

    def click_IPBind(self):
        self.find_element(*self.IPBind).click()

    def click_MacBind(self):
        self.find_element(*self.MacBind).click()

    def click_IPMacBind(self):
        self.find_element(*self.IPMacBind).click()

    def click_noBind(self):
        self.find_element(*self.noBind).click()

    def click_accountBillC(self):
        self.find_element(*self.accountBillC).click()

    def click_WebConfig(self):
        self.find_element(*self.WebConfig).click()

    def click_modaifyAuthPage(self):
        self.find_element(*self.modaifyAuthPage).click()

    def input_webAuthSuccessNote(self, webAuthSuccessNote):
        self.find_element(*self.webAuthSuccessNote).clear()
        self.find_element(*self.webAuthSuccessNote).send_keys(webAuthSuccessNote)

    def click_activePicEn(self):
        self.find_element(*self.activePicEn).click()

    def click_activePicC(self):
        self.find_element(*self.activePicC).click()

    def input_tipstitle(self, tipstitle):
        self.find_element(*self.tipstitle).clear()
        self.find_element(*self.tipstitle).send_keys(tipstitle)

    def input_tipsinfo(self, tipsinfo):
        self.find_element(*self.tipsinfo).clear()
        self.find_element(*self.tipsinfo).send_keys(tipsinfo)

    def input_hidcontact(self,hidcontact):
        self.find_element(*self.hidcontact).clear()
        self.find_element(*self.hidcontact).send_keys(hidcontact)

    def click_close_webauth(self):
        self.find_element(*self.close_webauth).click()

    def input_staleTime(self, staleTime):
        self.find_element(*self.staleTime).clear()
        self.find_element(*self.staleTime).send_keys(staleTime)

    def click_selfenabled(self):
        self.find_element(*self.selfenabled).click()

    def click_remoteConfig(self):
            self.find_element(*self.remoteConfig).click()

    def find_wllxxsj(self):
        self.exist_element(*self.wllxxsj).click()

    def click_ymmc(self):
        self.find_element(*self.ymmc).click()

    def click_bmdlb(self):
        self.find_element(*self.bmdlb).click()
