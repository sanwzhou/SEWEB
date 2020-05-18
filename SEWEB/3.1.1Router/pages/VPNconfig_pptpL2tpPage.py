#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 16:34
#@swzhou
'''
VPN配置 -- PPTP/L2TP
'''


from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.ReadConfig import getMenu
from common.LogGen import LogGen
logger = LogGen(Logger = 'pptpL2tpPage').getlog()

class pptpL2tpPage(BasePage):
    pptpL2tpM = getMenu('pptpL2tpM')
    TunnellistM = getMenu('TunnellistM')
    PPTPGlobalSetM = getMenu('PPTPGlobalSetM')
    l2tpGlobalSetM = getMenu('l2tpGlobalSetM')

    VPNConfig = (By.XPATH, '//span[@data-local="{VPNConfig}"]') #VPN配置菜单
    pptpL2tp = (By.LINK_TEXT, pptpL2tpM)  # PPTP/L2TP配置菜单
    Tunnellist = (By.LINK_TEXT,TunnellistM) #隧道列表 菜单
    PPTPGlobalSet = (By.LINK_TEXT,PPTPGlobalSetM) #PPTP服务器全局配置 菜单
    l2tpGlobalSet = (By.LINK_TEXT,l2tpGlobalSetM) #L2TP服务器全局配置 菜单

    add = (By.ID,'add')
    TunNames = (By.NAME,'TunNames')
    userNames = (By.NAME,'userNames')
    password = (By.NAME,'password')
    remoteInIp = (By.NAME,'remoteInIp')
    remoteInIPMask = (By.NAME,'remoteInIPMask')
    save = (By.ID,'save')
    listtips1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    l2tpB = (By.XPATH,'//input[@name="protoType"and@value="L2TP"]')
    listtips2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[2]/span')
    delete1 = (By.XPATH,'//span[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    list_nodataX = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')

    selauthtypeP = ('//*[@id="2"]/table/tbody/tr[3]/td[2]/select') #pptpserver密码验证方式
    pptpEncryS = (By.XPATH,'//input[@name="EncryptionMode"and@value="MPPE"]') #pptpserver隧道加密
    selauthtypeL = ('//*[@id="3"]/table/tbody/tr[2]/td[2]/select')  # l2tpserver密码验证方式
    workMode1 = (By.XPATH,'//input[@name="workMode"and@value="1"]') #拨入
    workModepptp = (By.XPATH,('//input[@name="protoType"and@value="PPTP"]'))
    seluserType = ('userType')
    staticIPs = (By.NAME,'staticIPs') #固定IP
    LanMac = (By.NAME,'LanMac') #移动用户 硬件特征码
    workModel2tp = (By.XPATH, ('//input[@name="protoType"and@value="L2TP"]'))
    workMode2 = (By.XPATH, '//input[@name="workMode"and@value="2"]')  # 拨出
    natEn = (By.XPATH,'//input[@name="natEnables"and@value="on"]')  # nat模式
    pptpEncryC = (By.XPATH, '//input[@name="EncryptionModes"and@value="MPPE"]')  # pptpClient隧道加密
    PPTP2AuthType = ('PPTP2AuthType') #pptp客户端密码验证方式
    L2TPAuthTypes = ('L2TPAuthTypes')  # l2tp客户端密码验证方式
    list_del1 = (By.XPATH,'//span[@data-primarykey="0"and@event-type="delete"]')

    selall = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID, 'delete')
    tipsshowin = (By.CLASS_NAME, 'tips-show-in')
    pptpserverEn = (By.XPATH,'//input[@name="enable"and@value="ENABLE"]')
    pptpserverEs = ('//input[@name="enable"and@value="ENABLE"]')
    pptpserverC = (By.XPATH, '//input[@name="enable"and@value="DISABLE"]')
    pptpserverCs = ('//input[@name="enable"and@value="DISABLE"]')
    L2tpserverEn = (By.XPATH, '//input[@name="enable"and@value="ENABLE"]')
    L2tpserverEs = ('//input[@name="enable"and@value="ENABLE"]')
    L2tpserverC = (By.XPATH, '//*[@id="3"]/table/tbody/tr[1]/td[2]/input[2]')
    L2tpserverCs = ('//*[@id="3"]/table/tbody/tr[1]/td[2]/input[2]')
    priDns = (By.NAME,'priDns')
    TunNamesIP = (By.NAME,'TunNamesIP') #隧道服务器地址
    list_status = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span') #会话状态
    saveS = (By.XPATH,'//*[@id="modal-add"]/div/div/div[3]/ul/li[1]/button') #新增服务端保存
    saveSl2tp = (By.XPATH,'//*[@id="3"]/ul/li[1]/button') #l2tp服务器保存

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 静态映射界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 静态映射跳转最后页

    def click_VPNConfig(self):
        self.find_element(*self.VPNConfig).click()
        logger.info('点击VPN配置')

    def click_pptpL2tp(self):
        self.find_element(*self.pptpL2tp).click()
        logger.info('点击PPTP/L2TP')

    def click_Tunnellist(self):
        self.find_element(*self.Tunnellist).click()
        logger.info('点击隧道列表菜单')

    def click_PPTPGlobalSet(self):
        self.find_element(*self.PPTPGlobalSet).click()
        logger.info('点击PPTP服务器全局配置 菜单')

    def click_l2tpGlobalSet(self):
        self.find_element(*self.l2tpGlobalSet).click()
        logger.info('点击L2TP服务器全局配置 菜单')

    def click_add(self):
        self.find_element(*self.add).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_saveS(self):
        self.find_element(*self.saveS).click()

    def input_TunNames(self, TunNames):
        self.find_element(*self.TunNames).clear()
        self.find_element(*self.TunNames).send_keys(TunNames)

    def input_userNames(self, userNames):
        self.find_element(*self.userNames).clear()
        self.find_element(*self.userNames).send_keys(userNames)

    def input_password(self, password):
        self.find_element(*self.password).clear()
        self.find_element(*self.password).send_keys(password)

    def input_remoteInIp(self,remoteInIp):
        self.find_element(*self.remoteInIp).clear()
        self.find_element(*self.remoteInIp).send_keys(remoteInIp)

    def input_remoteInIPMask(self, remoteInIPMask):
        self.find_element(*self.remoteInIPMask).clear()
        self.find_element(*self.remoteInIPMask).send_keys(remoteInIPMask)

    def click_l2tpB(self):
        self.find_element(*self.l2tpB).click()

    def click_delete1(self):
        self.find_element(*self.delete1).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_pptpEncryS(self):
        self.find_element(*self.pptpEncryS).click()

    def click_pptpEncryC(self):
        self.find_element(*self.pptpEncryC).click()

    def click_workMode1(self):
        self.find_element(*self.workMode1).click()

    def click_workModepptp(self):
        self.find_element(*self.workModepptp).click()

    def input_staticIPs(self, staticIPs):
        self.find_element(*self.staticIPs).clear()
        self.find_element(*self.staticIPs).send_keys(staticIPs)

    def input_LanMac(self,LanMack):
        self.find_element(*self.LanMac).clear()
        self.find_element(*self.LanMac).send_keys(LanMack)

    def click_workMode2(self):
        self.find_element(*self.workMode2).click()

    def click_workModel2tp(self):
        self.find_element(*self.workModel2tp).click()

    def click_natEn(self):
        self.find_element(*self.natEn).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)

    def click_pptpserverEn(self):
        self.find_element(*self.pptpserverEn).click()

    def click_pptpserverC(self):
        self.find_element(*self.pptpserverC).click()

    def click_L2tpserverEn(self):
        self.find_element(*self.L2tpserverEn).click()

    def click_L2tpserverC(self):
        self.find_element(*self.L2tpserverC).click()

    def input_priDns(self, priDns):
        self.find_element(*self.priDns).clear()
        self.find_element(*self.priDns).send_keys(priDns)

    def input_TunNamesIP(self,TunNamesIP):
        self.find_element(*self.TunNamesIP).clear()
        self.find_element(*self.TunNamesIP).send_keys(TunNamesIP)

    def click_saveSl2tp(self):
        self.find_element(*self.saveSl2tp).click()

    def find_list_nodataX(self):
        self.exist_element(*self.list_nodataX)

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()
