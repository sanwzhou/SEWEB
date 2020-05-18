#! -*-conding:utf-8 -*-
#@Time: 2019/9/6 0006 11:39
#@swzhou
'''
云AC 页面元素
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'LoginPage').getlog()

class LoginYunPage(BasePage):
    username = (By.NAME,'user')
    password = (By.NAME,'password')
    # need_move_span = (By.XPATH,'//*[@id="slider"]/div[4]')  #滑动验证码
    login = (By.ID,'btn')
    # 设备管理
    device = (By.ID,'device') #设备管理菜单
    #导入设备小页面
    Import = (By.ID,'Import') #导入设备
    Bureau = (By.XPATH,'//*[@id="groupTable"]/tbody/tr[2]/td[2]/div/div[1]/p')#选择所属局点
    treeEdit_1_switch = (By.ID,'treeEdit_1_switch') #局点下第一行展开
    treeEdit_2_check = (By.ID,'treeEdit_2_check') #展开后第一行
    groupBg = (By.CLASS_NAME,'groupBg') #选中局点后任意点下
    selImportMode = ('ImportMode') #导入方式
    deviceName = (By.NAME,'deviceName') #设备名称
    SN = (By.NAME,'SN')
    jhm = (By.NAME, 'jhm')
    confirm = (By.ID, 'confirm') #保存
    errorMsg = ('errorMsg') #保存提示
    tipClose = (By.CLASS_NAME,'tipClose') #关闭导入页面
    #搜索框
    search = (By.XPATH,'//*[@class="search"]/input')
    glyphicon_search =(By.CLASS_NAME,'glyphicon-search')
    #列表
    name = (By.NAME,'//*[@id="table"]/tbody/tr[1]/td[5]/a')
    state = ('//*[@id="table"]/tbody/tr[1]/td[6]')
    btns0 = (By.ID, 'btns0')  # 重启
    btns1 = (By.ID, 'btns1')  # 远程管理
    btns2 = (By.ID,'btns2') #解绑
    cancel = (By.ID,'cancel') #解绑确定
    list_nodata = ('//*[@id="table"]/tbody/tr[1]/td')
    #设备管理 右上角刷新
    refurbish = (By.ID,'refurbish')
    #设备名称 - 路由器详情页
    yunmodel = ('//*[@id="ImportDevice"]/div[3]/div[2]/div[2]/li/table/tbody/tr[1]/td[2]')
    yunSN = ('//*[@id="ImportDevice"]/div[3]/div[2]/div[2]/li/table/tbody/tr[2]/td[2]')
    yunhdmodel = ('//*[@id="ImportDevice"]/div[3]/div[2]/div[2]/li/table/tbody/tr[3]/td[2]')
    yunsoftware = ('//*[@id="ImportDevice"]/div[3]/div[2]/div[2]/li/table/tbody/tr[4]/td[2]')


    def input_username(self,user):
        self.find_element(*self.username).clear()
        self.find_element(*self.username).send_keys(user)

    def input_password(self,passwd):
        self.find_element(*self.password).clear()
        self.find_element(*self.password).send_keys(passwd)

    def click_login(self):
        self.find_element(*self.login).click()
        logger.info('点击登录')

    def click_device(self):
        self.find_element(*self.device).click()

    def click_Import(self):
        self.find_element(*self.Import).click()

    def click_Bureau(self):
        self.find_element(*self.Bureau).click()

    def click_treeEdit_1_switch(self):
        self.find_element(*self.treeEdit_1_switch).click()

    def click_treeEdit_2_check(self):
        self.find_element(*self.treeEdit_2_check).click()

    def click_groupBg(self):
        self.find_element(*self.groupBg).click()

    def input_deviceName(self,deviceName):
        self.find_element(*self.deviceName).clear()
        self.find_element(*self.deviceName).send_keys(deviceName)

    def input_SN(self,SN):
        self.find_element(*self.SN).clear()
        self.find_element(*self.SN).send_keys(SN)

    def input_jhm(self,jhm):
        self.find_element(*self.jhm).clear()
        self.find_element(*self.jhm).send_keys(jhm)

    def click_confirm(self):
        self.find_element(*self.confirm).click()

    def click_tipClose(self):
        self.find_element(*self.tipClose).click()

    def input_search(self,search):
        self.find_element(*self.search).clear()
        self.find_element(*self.search).send_keys(search)

    def click_glyphicon_search(self):
        self.find_element(*self.glyphicon_search).click()

    def click_btns0(self):
        self.find_element(*self.btns0).click()

    def click_btns1(self):
        self.find_element(*self.btns1).click()

    def click_btns2(self):
        self.find_element(*self.btns2).click()

    def click_cancel(self):
        self.find_element(*self.cancel).click()

    def click_refurbish(self):
        self.find_element(*self.refurbish).click()

    def click_name(self):
        self.find_element(*self.name).click()

