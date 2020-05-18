#! -*-conding:utf-8 -*-
#@Time: 2019/1/24 0024 14:06
#@swzhou
'''
网络配置 - U盘共享 界面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'NetworkSharingPage').getlog()
from common.ReadConfig import getMenu

class NetworkSharingPage(BasePage):
    NetworkSharingM = getMenu('NetworkSharingM')
    DeviceStatusM = getMenu('DeviceStatusM')
    NetworkSharing2M = getMenu('NetworkSharing2M') #子页面
    AccountSettingsM = getMenu('AccountSettingsM')

    netConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    NetworkSharing = (By.LINK_TEXT, NetworkSharingM)  # 网络共享菜单
    #设备状态
    DeviceStatus = (By.LINK_TEXT,DeviceStatusM)
    UsageRate = ('//*[@id="1"]/table/tbody/tr[1]/td[2]/span') # U盘使用率
    Total = ('//*[@id="1"]/table/tbody/tr[2]/td[2]') # U盘总容量 后元素（所有）
    Usedtext = ('//*[@id="1"]/table/tbody/tr[2]/td[2]/span[1]') # “已使用容量”提示
    Usedtext1 = 'M' + Usedtext
    Residualtext = ('//*[@id="1"]/table/tbody/tr[2]/td[2]/span[2]') # “剩余容量”提示
    Residualtext1 = 'M' + Residualtext
    Eject = (By.XPATH,'//*[@id="1"]/table/tbody/tr[3]/td[1]/button') #弹出
    ok = (By.ID,'u-cfm-ok')
    # 账号设置
    AccountSettings = (By.LINK_TEXT,AccountSettingsM)
    add = (By.ID,'add')
    username = (By.NAME,'username')
    passwd1 = (By.NAME,'passwd1')
    passwd2 = (By.NAME,'passwd2')
    authority = ('authority')
    save = (By.ID,'save')
    tips_show_inf = (By.CLASS_NAME,'tips-show-in')
    tips_show_in = ('tips-show-in')
    modal_hide = (By.ID,'modal-hide')
    Acc3 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[3]/td[2]/span')
    auth3 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[3]/td[3]/span')
    Acc4 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[4]/td[2]/span')
    auth4 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[4]/td[3]/span')
    Acc5 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[5]/td[2]/span')
    auth5 = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[5]/td[3]/span')
    list_del1 = (By.XPATH,'//span[@data-primarykey="0"and@event-type="delete"]')
    list_del2 = (By.XPATH, '//span[@data-primarykey="1"and@event-type="delete"]')
    list_del3 = (By.XPATH, '//span[@data-primarykey="2"and@event-type="delete"]')
    list_edit1 = (By.XPATH, '//span[@data-primarykey="0"and@data-event="edit"]')
    list_edit2 = (By.XPATH, '//span[@data-primarykey="1"and@data-event="edit"]')
    list_edit3 = (By.XPATH, '//span[@data-primarykey="2"and@data-event="edit"]')
    list_del5 = (By.XPATH, '//span[@data-primarykey="4"and@event-type="delete"]')
    list5_nodata = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[5]/td')
    allsel = (By.XPATH,'//*[@id="3"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delete = (By.ID,'delete')
    list3_nodata = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[3]/td')
    # 网络共享
    NetworkSharing2 = (By.XPATH,NetworkSharing2M)
    choosml = (By.ID,'choosml') #设置共享目录
    names = (By.NAME,'names')
    FTP_DIR_1_check = (By.ID,'FTP_DIR_1_check')
    modal_FTP = (By.XPATH,'//*[@id="modal-FTP"]/div/div/div[3]/ul/li[1]/button')
    ftpEn = (By.NAME,'ftpEn')
    ftpEns = ('ftpEn')
    ftpports = ('ftpport')
    ftpport = (By.NAME,'ftpport')
    tipsport = ('//*[@id="2"]/table/tbody/tr[4]/td[2]/span/span[2]')
    enableDevice = (By.ID,'enableDevice')
    enableDevices = ('enableDevice')
    sambaEn = (By.NAME,'sambaEn')
    sambaEnS = ('sambaEn')
    open_pswds = ('open_pswd')
    open_pswd = (By.ID,'open_pswd')
    add_modal = (By.XPATH,'//*[@id="modal-add"]/div/div/div[3]/ul/li[1]/button')
    adminuser = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    guestuser = ('//*[@id="3"]/div/div/div[1]/table/tbody/tr[2]/td[2]/span')
    WANEnable = (By.NAME,'WANEnable')

    def click_netConfig(self):
        self.find_element(*self.netConfig).click()
        logger.info('点击网络配置')

    def click_NetworkSharing(self):
        self.find_element(*self.NetworkSharing).click()
        logger.info('点击网络共享')

    def find_NetworkSharing(self):
        self.exist_element(*self.NetworkSharing).click()
        logger.info('点击网络共享')

    def click_DeviceStatus(self):
        self.find_element(*self.DeviceStatus).click()
        logger.info('点击设备状态')

    def click_Eject(self):
        self.find_element(*self.Eject).click()

    def find_Eject(self):
        self.exist_element(*self.Eject)

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_AccountSettings(self):
        self.find_element(*self.AccountSettings).click()
        logger.info('点击账号设置')

    def click_add(self):
        self.find_element(*self.add).click()

    def find_add(self):
        self.exist_element(*self.add)

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

    def click_modal_hide(self):
        self.find_element(*self.modal_hide).click()

    def click_listdel1(self):
        self.find_element(*self.list_del1).click()

    def click_listdel2(self):
        self.find_element(*self.list_del2).click()

    def click_listdel3(self):
        self.find_element(*self.list_del3).click()

    def click_listedit1(self):
        self.find_element(*self.list_edit1).click()

    def click_listedit2(self):
        self.find_element(*self.list_edit2).click()

    def click_listedit3(self):
        self.find_element(*self.list_edit3).click()

    def click_listdel5(self):
        self.find_element(*self.list_del5).click()

    def click_allsel(self):
        self.find_element(*self.allsel).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def find_delete(self):
        self.exist_element(*self.delete)

    def click_NetworkSharing2(self):
        self.find_element(*self.NetworkSharing2).click()
        logger.info('点击网络共享子页面')

    def click_choosml(self):
        self.find_element(*self.choosml).click()

    def input_names(self, names):
        self.find_element(*self.names).clear()
        self.find_element(*self.names).send_keys(names)

    def click_FTP_DIR_1_check(self):
        self.find_element(*self.FTP_DIR_1_check).click()

    def click_modal_FTP(self):
        self.find_element(*self.modal_FTP).click()

    def click_ftpEn(self):
        self.find_element(*self.ftpEn).click()

    def input_ftpport(self, ftpport):
        self.find_element(*self.ftpport).clear()
        self.find_element(*self.ftpport).send_keys(ftpport)

    def click_enableDevice(self):
        self.find_element(*self.enableDevice).click()

    def click_sambaEn(self):
        self.find_element(*self.sambaEn).click()

    def find_sambaEn(self):
        self.exist_element(*self.sambaEn).click()

    def click_open_pswd(self):
        self.find_element(*self.open_pswd).click()

    def click_add_modal(self):
        self.find_element(*self.add_modal).click()

    def find_tips_show_inf(self):
        self.exist_element(*self.tips_show_inf).click()

    def click_WANEnable(self):
        self.find_element(*self.WANEnable).click()