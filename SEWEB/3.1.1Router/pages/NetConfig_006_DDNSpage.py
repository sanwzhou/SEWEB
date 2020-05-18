#! -*-conding:utf-8 -*-
#@Time: 2019/1/18 0018 9:34
#@swzhou
'''
网络配置 动态域名页面
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'DDNSpage').getlog()
from common.ReadConfig import getMenu

class DDNSpage(BasePage):
    DDNSconfigM = getMenu('DDNSconfigM')

    netConfig = (By.XPATH, '//span[@data-local="{netConfig}"]') #网络配置菜单
    DDNSconfig = (By.LINK_TEXT, DDNSconfigM)  # 动态域名菜单

    add = (By.ID,'add')
    selDDNSProvider = ('DDNSProvider')
    Interface = (By.NAME,'Profile')

    save = (By.ID,'save')
    list_status = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    list_ServiceProvider = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    list_ip = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span')
    fresh = (By.ID,'fresh')
    delete = (By.XPATH,'//*[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    #3322
    DDNS3322= (By.NAME,'DDNS3322')
    Account3322 = (By.NAME,'Account3322')
    Password3322 = (By.NAME,'Password3322')
    ipcnUrl = ('https://ip.cn/')
    Extranet_ip1 = ('//*[@id="result"]/div/p[1]/code') #IP.cn 查询到IP地址
    Extranet_ip2 = ('//*[@id="rightinfo"]/dl/dd[1]') #http://ip.tool.chinaz.com/siteip 查询到IP地址
    #花生壳
    AccountNut = (By.NAME,'AccountNut')
    PasswordNut = (By.NAME,'PasswordNut')
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID,'delete')
    tipsshowin = (By.CLASS_NAME, 'tips-show-in')


    def click_netConfig(self):
        self.find_element(*self.netConfig).click()
        logger.info('点击网络配置')

    def click_DDNSconfig(self):
        self.find_element(*self.DDNSconfig).click()
        logger.info('点击动态域名')

    def click_add(self):
        self.find_element(*self.add).click()

    def click_Interface(self):
        self.find_element(*self.Interface).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_fresh(self):
        self.find_element(*self.fresh).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def input_DDNS3322(self, DDNS3322):
        self.find_element(*self.DDNS3322).clear()
        self.find_element(*self.DDNS3322).send_keys(DDNS3322)

    def input_Account3322(self, Account3322):
        self.find_element(*self.Account3322).clear()
        self.find_element(*self.Account3322).send_keys(Account3322)

    def input_Password3322(self, Password3322):
        self.find_element(*self.Password3322).clear()
        self.find_element(*self.Password3322).send_keys(Password3322)

    def input_AccountNut(self,AccountNut):
        self.find_element(*self.AccountNut).clear()
        self.find_element(*self.AccountNut).send_keys(AccountNut)

    def input_PasswordNut(self, PasswordNut):
        self.find_element(*self.PasswordNut).clear()
        self.find_element(*self.PasswordNut).send_keys(PasswordNut)

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)