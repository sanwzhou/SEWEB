#! -*-conding:utf-8 -*-
#@Time: 2019/1/25 0025 14:20
#@swzhou
'''
无线扩展 - 网络名称 页面
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'netNamePage').getlog()
from common.ReadConfig import getMenu

class netNamePage(BasePage):
    netNameM = getMenu('netNameM') #网络名称

    wirelessExtension = (By.XPATH, '//span[@data-local="{wirelessExtension}"]')
    netName = (By.LINK_TEXT, netNameM )

    u_cfm_boxT = ('u-cfm-box')
    ok = (By.ID,'u-cfm-ok')
    u_cfm_nox = (By.ID, 'u-cfm-nox')
    checkOpens = ('checkOpen')
    checkOpen = (By.ID,'checkOpen')
    ManageProtocols = (By.ID,'ManageProtocol')
    ManageProtocolss = ('ManageProtocol')

    list_edit1 = (By.XPATH,'//span[@data-primarykey="0"and@data-event="edit"]')
    ssid = (By.NAME,'ssid')
    next_tab = (By.ID,'next_tab')
    encryType = ('encryType')
    pskPsswd = (By.NAME,'pskPsswd')
    txBand = (By.NAME,'txBand')
    rxBand = (By.NAME,'rxBand')
    list_ssid1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    zoneName = (By.NAME,'zoneName')
    cli_5g = (By.XPATH,'//input[@name="spjk"and@value="fre5"]') #ssid 5G 勾
    vlanId = ('vlanId')
    gjxx = (By.ID,'gjxx') #高级选项
    broadcastEn = (By.XPATH,'//input[@name="broadcastEn"and@value="0"]') #隐藏ssid
    isolateEn = (By.XPATH,'//input[@name="isolateEn"and@value="1"]') #无线客户端隔离
    cli_2g = (By.XPATH, '//input[@name="spjk"and@value="fre2"]') #ssid 2G 勾
    list_ssid2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/span')
    list_ssid3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/span')
    list_ssid4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/span')
    save = (By.ID,'save')
    list_edit4 = (By.XPATH, '//span[@data-primarykey="3"and@data-event="edit"]')
    list_del4 = (By.XPATH, '//span[@data-primarykey="3"and@event-type="delete"]')
    add = (By.ID,'add')
    list_nodata4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td')
    sharelimit = (By.XPATH,'//*[@id="e4"]/table/tbody/tr[1]/td[2]/input[1]')
    #003
    list_autosend1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[11]/input')
    list_autosend1c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[11]/input')
    #004
    list_sutosend4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[11]/input')
    list_sutosend4c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[11]/input')
    encodeType = ('encodeType') # 选电脑优先/电脑优先
    list_ssid5 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[4]/span')
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input') #全选
    sellist1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input') #第一个ssid前的勾
    delete = (By.ID,'delete')
    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 组1页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_wirelessExtension(self):
        self.find_element(*self.wirelessExtension).click()
        logger.info('点击无线扩展')

    def click_netName(self):
        self.find_element(*self.netName).click()
        logger.info('点击网络名称')

    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def click_checkOpen(self):
        self.find_element(*self.checkOpen).click()

    def click_ManageProtocols(self):
        self.find_element(*self.ManageProtocols).click()

    def click_u_cfm_nox(self):
        self.find_element(*self.u_cfm_nox).click()

    def click_list_edit1(self):
        self.find_element(*self.list_edit1).click()

    def input_ssid(self,ssid):
        self.find_element(*self.ssid).clear()
        self.find_element(*self.ssid).send_keys(ssid)

    def click_next_tab(self):
        self.find_element(*self.next_tab).click()

    def input_pskPsswd(self,pskPsswd):
        self.find_element(*self.pskPsswd).clear()
        self.find_element(*self.pskPsswd).send_keys(pskPsswd)

    def input_txBand(self,txBand):
        self.find_element(*self.txBand).clear()
        self.find_element(*self.txBand).send_keys(txBand)

    def input_rxBand(self,rxBand):
        self.find_element(*self.rxBand).clear()
        self.find_element(*self.rxBand).send_keys(rxBand)

    def input_zoneName(self, zoneName):
        self.find_element(*self.zoneName).clear()
        self.find_element(*self.zoneName).send_keys(zoneName)

    def click_gjxx(self):
        self.find_element(*self.gjxx).click()

    def click_broadcastEn(self):
        self.find_element(*self.broadcastEn).click()

    def click_isolateEn(self):
        self.find_element(*self.isolateEn).click()

    def click_cli_2g(self):
        self.find_element(*self.cli_2g).click()

    def click_list_edit4(self):
        self.find_element(*self.list_edit4).click()

    def click_list_del4(self):
        self.find_element(*self.list_del4).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_add(self):
        self.find_element(*self.add).click()

    def click_list_autosend1c(self):
        self.find_element(*self.list_autosend1c).click()

    def click_list_sutosend4c(self):
        self.find_element(*self.list_sutosend4c).click()

    def click_cli_5g(self):
        self.find_element(*self.cli_5g).click()

    def click_sharelimit(self):
        self.find_element(*self.sharelimit).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_sellist1(self):
        self.find_element(*self.sellist1).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()