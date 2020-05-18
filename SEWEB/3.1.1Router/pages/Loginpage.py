#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 17:12
#@swzhou
'''
路由器登录页面元素
'''


from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'LoginPage').getlog()


class LoginPage(BasePage):
    username = (By.NAME,'username')
    password = (By.NAME,'pwd')
    login = (By.ID,'login_btn')
    passwd1 = (By.NAME,'passwd1')
    passwd2 = (By.NAME, 'passwd2')
    cfm = (By.ID,'u-cfm-demo')
    logout = (By.ID,'logout_span')  #注销
    warning = (By.ID,'warning-msg') #登录页面告警信息
    #电子授权首页显示
    model = ('//*[@id="iframe1"]/table/tbody/tr[3]/td[2]')
    sn = ('//*[@id="iframe1"]/table/tbody/tr[4]/td[2]')
    chooseFile = (By.NAME,'chooseFile')
    updatesoftware = ('/html/body/div[3]/div[2]/form/table/tbody/tr[6]/td[2]/input[2]')
    innerputs = ('/html/body/div[3]/div[2]/form/table/tbody/tr[6]/td[3]/button')
    innerput = (By.XPATH,'/html/body/div[3]/div[2]/form/table/tbody/tr[6]/td[3]/button')
    ok = (By.ID,'u-cfm-ok')
    no = (By.ID,'u-cfm-no')

    #https模式 浏览器提示证书不对 url正确，无法进入页面，需要点击"高级"-下一步
    #高级
    details_button = (By.ID,'details-button')
    #继续
    proceed_link = (By.ID,'proceed-link')

    def find_username(self):
        self.exist_element(*self.username)

    def input_username(self,user):
        self.find_element(*self.username).clear()
        self.find_element(*self.username).send_keys(user)

    def input_password(self,passwd):
        self.find_element(*self.password).clear()
        self.find_element(*self.password).send_keys(passwd)

    def click_login(self):
        self.find_element(*self.login).click()
        logger.info('点击登录WEB')

    # 恢复出厂后弹出的密码确认框
    def find_passwd1(self):
        self.exist_element(*self.passwd1).click()

    def input_passwd1(self,passwd):
        self.find_element(*self.passwd1).clear()
        self.find_element(*self.passwd1).send_keys(passwd)

    def input_passwd2(self,passwd):
        self.find_element(*self.passwd2).clear()
        self.find_element(*self.passwd2).send_keys(passwd)

    def click_cfm(self):
        self.find_element(*self.cfm).click()

    #注销
    def click_logout(self):
        self.find_element(*self.logout).click()
    ##登录页面告警信息
    def warning_msg(self):
        self.find_element(*self.warning)

    # 选择文件
    def flid_chooseFile(self):
        self.find_element(*self.chooseFile)

    def click_innerput(self):
        self.find_element(*self.innerput).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_no(self):
        self.exist_element(*self.no).click()

    #证书
    def find_details_button(self):
        self.exist_element(*self.details_button)

    def click_details_button(self):
        self.find_element(*self.details_button).click()

    def click_proceed_link(self):
        self.find_element(*self.proceed_link).click()
