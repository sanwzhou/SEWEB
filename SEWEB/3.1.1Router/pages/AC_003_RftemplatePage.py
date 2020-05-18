#! -*-conding:utf-8 -*-
#@Time: 2019/1/28 0028 14:31
#@swzhou
'''
射频模板 页面
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
from common.ReadConfig import getMenu
logger = LogGen(Logger = 'RftemplatePage').getlog()

class RftemplatePage(BasePage):
    rfTemplateM = getMenu('rfTemplateM') #射频模板

    wirelessExtension = (By.XPATH, '//span[@data-local="{wirelessExtension}"]')
    rfTemplate = (By.LINK_TEXT,rfTemplateM)
    #001
    id1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/span')
    channel1 =('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')
    edit1 = (By.XPATH,'//span[@data-primarykey="0"and@data-event="edit"]')
    id2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[2]/span')
    channel2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[5]/span')
    edit2 = (By.XPATH, '//span[@data-primarykey="1"and@data-event="edit"]')
    id3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[2]/span')
    channel3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[5]/span')
    edit3 = (By.XPATH, '//span[@data-primarykey="2"and@data-event="edit"]')
    list_nodata4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td')
    addModal = (By.ID,'addModal')
    name = (By.NAME,'name')
    en_wirelessS = ('//input[@name="en_wireless"and@value="1"]') #2.4G
    C_wireless = (By.XPATH,'//input[@name="en_wireless"and@value="0"]') #关闭2G
    C_wireless1 = (By.XPATH, '//input[@name="en_wireless"and@value="1"]')  #打开2G
    en_wireless5S = ('//input[@name="en_wireless_5"and@value="1"]')  # 5G
    C_wireless5 = (By.XPATH, '//input[@name="en_wireless_5"and@value="0"]')  # 关闭5G
    C_wireless51 = (By.XPATH, '//input[@name="en_wireless_5"and@value="1"]')  # 打开5G
    mode = ('mode') #无线模式
    mode_5 = ('mode_5')
    save = (By.ID,'save')
    channel = ('channel')
    BW = ('BW') # 频道带宽
    rate = ('rate') #无线速率
    channel_5 = ('channel_5')
    BW_5 = ('BW_5')
    power = ('power') #无线传输功率
    manual = ('manual')
    gjxxa = (By.ID,'gjxxa') #高级选项
    SGIs = ('//input[@name="SGI"and@value="1"]') #短间隔
    SGIc = (By.XPATH,'//input[@name="SGI"and@value="0"]') #关闭短间隔
    wmms = ('//input[@name="wmm"and@value="1"]')
    wmmc = (By.XPATH,'//input[@name="wmm"and@value="0"]')
    preambles = ('//input[@name="preamble"and@value="1"]')  #短前导码
    preamblesc = (By.XPATH,'//input[@name="preamble"and@value="0"]')
    BeaconPeriod = (By.NAME,'BeaconPeriod') #信标间隔
    VHTBW = ('VHTBW') #VHT频道带宽
    power_5 = ('power_5')
    manual_5 = ('manual_5')
    SGI5s = ('//input[@name="SGI_5"and@value="1"]')  # 5G短间隔
    SGI5c = (By.XPATH, '//input[@name="SGI_5"and@value="0"]')  # 关闭5G短间隔
    wmm5s = ('//input[@name="wmm_5"and@value="1"]')
    wmm5c = (By.XPATH, '//input[@name="wmm_5"and@value="0"]')
    preamble5s = ('//input[@name="preamble_5"and@value="1"]')  # 5G短前导码
    preambles5c = (By.XPATH, '//input[@name="preamble_5"and@value="0"]')
    BeaconPeriod5 = (By.NAME, 'BeaconPeriod_5')  # 5G信标间隔
    #002
    next = (By.ID,'next')
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input') #全选
    allDelete = (By.ID,'allDelete')
    ok = (By.ID,'u-cfm-ok')
    list_num10 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[10]/td[2]/span')
    list_edit1 = (By.XPATH,'//span[@data-primarykey="0"and@data-event="edit"]')


    def click_wirelessExtension(self):
        self.find_element(*self.wirelessExtension).click()
        logger.info('点击无线扩展')

    def click_rfTemplate(self):
        self.find_element(*self.rfTemplate).click()
        logger.info('点击射频模板')

    def click_addModal(self):
        self.find_element(*self.addModal).click()

    def input_name(self, name):
        self.find_element(*self.name).clear()
        self.find_element(*self.name).send_keys(name)

    def click_C_wireless(self):
        self.find_element(*self.C_wireless).click()

    def click_C_wireless1(self):
        self.find_element(*self.C_wireless1).click()

    def click_C_wireless5(self):
        self.find_element(*self.C_wireless5).click()

    def click_C_wireless51(self):
        self.find_element(*self.C_wireless51).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_next(self):
        self.find_element(*self.next).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_allDelete(self):
        self.find_element(*self.allDelete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_list_edit1(self):
        self.find_element(*self.list_edit1).click()

    def click_gjxxa(self):
        self.find_element(*self.gjxxa).click()

    def click_SGIc(self):
        self.find_element(*self.SGIc).click()

    def click_wmmc(self):
        self.find_element(*self.wmmc).click()

    def click_preamblesc(self):
        self.find_element(*self.preamblesc).click()

    def input_BeaconPeriod(self,BeaconPeriod):
        self.find_element(*self.BeaconPeriod).clear()
        self.find_element(*self.BeaconPeriod).send_keys(BeaconPeriod)

    def click_SGI5c(self):
        self.find_element(*self.SGI5c).click()

    def click_wmm5c(self):
        self.find_element(*self.wmm5c).click()

    def click_preambles5c(self):
        self.find_element(*self.preambles5c).click()

    def input_BeaconPeriod5(self,BeaconPeriod5):
        self.find_element(*self.BeaconPeriod5).clear()
        self.find_element(*self.BeaconPeriod5).send_keys(BeaconPeriod5)

    def click_edit1(self):
        self.find_element(*self.edit1).click()

    def click_edit2(self):
        self.find_element(*self.edit2).click()

    def click_edit3(self):
        self.find_element(*self.edit3).click()

