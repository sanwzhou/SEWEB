#! -*-conding:utf-8 -*-
#@Time: 2019/1/12 0012 16:59
#@swzhou
'''
用户管理 - 黑名单页面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'Organization_userBlackPage').getlog()
from common.ReadConfig import getMenu


class Organization_userBlackPage(BasePage):
    blacklistM = getMenu('blacklistM') #黑名单

    UserManage = (By.XPATH, '//span[@data-local="{UserManage}"]')
    blacklist = (By.LINK_TEXT, blacklistM)

    blicklist_mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    delete = (By.XPATH,'//span[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    list_tips = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')

    add = (By.ID,'add')
    bname = (By.NAME,'username')
    bmac = (By.NAME,'filterMac')
    save = (By.ID,'save')
    blicklist_name = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    blicklist_deldte = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span[2]')
    modalhide = (By.ID,'modal-hide')
    deleteB = (By.ID,'delete') #删除按钮
    importB = (By.ID, 'import')
    exportB = (By.ID, 'export')
    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 组1页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID,'delete')
    tipsshowin = (By.CLASS_NAME, 'tips-show-in')

    def click_UserManage(self):
        self.find_element(*self.UserManage).click()
        logger.info('点击用户管理')

    def click_blacklist(self):
        self.find_element(*self.blacklist).click()
        logger.info('点击黑名单')

    def click_delete(self):
        self.find_element(*self.delete).click()


    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_add(self):
        self.find_element(*self.add).click()

    def input_bname(self,bname):
        self.find_element(*self.bname).clear()
        self.find_element(*self.bname).send_keys(bname)

    def input_bmac(self,bmac):
        self.find_element(*self.bmac).clear()
        self.find_element(*self.bmac).send_keys(bmac)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_modalhide(self):
        self.find_element(*self.modalhide).click()

    def find_deleteB(self):
        self.exist_element(*self.deleteB)

    def find_importB(self):
        self.exist_element(*self.importB)

    def find_exportB(self):
        self.exist_element(*self.exportB)

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)
