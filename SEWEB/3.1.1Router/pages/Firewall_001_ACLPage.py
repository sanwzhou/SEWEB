#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 16:39
#@swzhou
'''
防火墙 - 设备访问控制 页面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'AccessControlPage').getlog()
from common.ReadConfig import getMenu

class AccessControlPage(BasePage):
    AccessControlM = getMenu('AccessControlM')

    FireWall = (By.XPATH, '//span[@data-local="{fireWall}"]') #防火墙菜单
    AccessControl = (By.LINK_TEXT, AccessControlM)  # 访问控制菜单

    add = (By.ID,'add')
    PolicyNames = (By.NAME,'PolicyNames')
    sourceIP = (By.NAME,'sourceIP')
    usergroup = (By.XPATH, '//input[@name="applyType"and@value="org"]')
    Root = (By.ID,'newTree_1_check')
    saveW1 = (By.XPATH,'//*[@id="modal-applyUser"]/div/div/div[3]/ul/li[1]') #弹窗保存
    seltime = ('timeGrpName')
    selservice = ('cyfw')
    save = (By.ID,'save')
    checkTraffic = (By.ID,'checkTraffic') #开关
    list_dstport = ('//*[@id="1"]/div[1]/div/div[1]/table/tbody/tr[1]/td[13]/span')
    checkTrafficS = ('checkTraffic')
    delete = (By.XPATH,'//*[@data-primarykey="0"and@event-type="delete"]')
    ok = (By.ID,'u-cfm-ok')
    listnodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')

    userip = (By.XPATH, '//input[@name="applyType"and@value="ip"]')
    starip = (By.NAME,'starip')
    endip = (By.NAME,'endip')
    glnrUrl = (By.NAME,'glnr_url')
    selFilterTypes = ('FilterTypes')

    list_Content = ('//*[@id="1"]/div[1]/div/div[1]/table/tbody/tr[1]/td[10]/span')
    glnrKeyword = (By.NAME,'glnr_keyword')
    OAloginid = (By.NAME,'loginid')
    OApassword = (By.NAME,'userpassword')
    OAlogin = (By.ID,'login')
    # notice = (By.XPATH,'//*[@id="_Draghandle_1554168195385"]/td/div[2]') #以访出现通告
    OAsearcn = (By.XPATH,'//*[@id="sample"]/div[1]/a/span') #OA搜索框
    OAsearcnWD = (By.XPATH,'//*[@id="sample"]/div[2]/ul/li[3]') #OA搜索改为文档类型
    OAsearchvalue = (By.ID,'searchvalue')
    OAsearchbt = (By.ID,'searchbt') #搜索按钮
    OAlogout = (By.CLASS_NAME,'logout')
    OAsubmit = (By.XPATH,'//*[@class="zd_btn_submit"and@value="确定"]')
    HeaderForXtalbe = (By.CLASS_NAME,'HeaderForXtalbe') #如果关键字过滤不生效，能出现文档列表栏

    glnrdns = (By.NAME,'glnr_dns')
    userall = (By.XPATH,'//input[@name="applyType"and@value="all"]')
    selProtocol = ('Protocol')
    list1_name = ('//*[@id="1"]/div[1]/div/div[1]/table/tbody/tr[1]/td[3]/span')
    u_moveto_1 = ('u_moveto_1')
    u_movetosave = (By.ID,'u_movetosave')
    selall = (By.XPATH,'//*[@id="1"]/div[1]/div/div[1]/table/thead/tr/th[1]/input')
    delall = (By.ID,'delete')
    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 静态映射界面页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 静态映射跳转最后页
    def click_FireWall(self):
        self.find_element(*self.FireWall).click()
        logger.info('点击防火墙')

    def click_AccessControl(self):
        self.find_element(*self.AccessControl).click()
        logger.info('点击访问控制')

    def click_add(self):
        self.find_element(*self.add).click()

    def input_PolicyNames(self, PolicyNames):
        self.find_element(*self.PolicyNames).clear()
        self.find_element(*self.PolicyNames).send_keys(PolicyNames)

    def click_sourceIP(self):
        self.find_element(*self.sourceIP).click()

    def click_usergroup(self):
        self.find_element(*self.usergroup).click()

    def click_Root(self):
        self.find_element(*self.Root).click()

    def click_saveW1(self):
        self.find_element(*self.saveW1).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_checkTraffic(self):
        self.find_element(*self.checkTraffic).click()

    def click_delete(self):
        self.find_element(*self.delete).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_userip(self):
        self.find_element(*self.userip).click()

    def input_starip(self, starip):
        self.find_element(*self.starip).clear()
        self.find_element(*self.starip).send_keys(starip)

    def input_endip(self, endip):
        self.find_element(*self.endip).clear()
        self.find_element(*self.endip).send_keys(endip)

    def input_glnrUrl(self, glnrUrl):
        self.find_element(*self.glnrUrl).clear()
        self.find_element(*self.glnrUrl).send_keys(glnrUrl)
    
    def input_glnrKeyword(self, glnrKeyword):
        self.find_element(*self.glnrKeyword).clear()
        self.find_element(*self.glnrKeyword).send_keys(glnrKeyword)
        
    def input_OAloginid(self, OAloginid):
        self.find_element(*self.OAloginid).clear()
        self.find_element(*self.OAloginid).send_keys(OAloginid)
        
    def input_OApassword(self, OApassword):
        self.find_element(*self.OApassword).clear()
        self.find_element(*self.OApassword).send_keys(OApassword)
        
    def click_OAlogin(self):
        self.find_element(*self.OAlogin).click()

    # def click_notice(self):
    #     self.find_element(*self.notice).click()

    def click_OAsearcn(self):
        self.find_element(*self.OAsearcn).click()
    
    def click_OAsearcnWD(self):
        self.find_element(*self.OAsearcnWD).click()

    def input_OAsearchvalue(self, OAsearchvalue):
        self.find_element(*self.OAsearchvalue).clear()
        self.find_element(*self.OAsearchvalue).send_keys(OAsearchvalue)

    def find_OAsearchbt(self):
        self.exist_element(*self.OAsearchbt).click()

    def find_HeaderForXtalbe(self,*loc):
        self.exist_element(*self.HeaderForXtalbe)

    def click_OAlogout(self):
        self.find_element(*self.OAlogout).click()

    def click_OAsubmit(self):
        self.find_element(*self.OAsubmit).click()

    def input_glnrdns(self, glnrdns):
        self.find_element(*self.glnrdns).clear()
        self.find_element(*self.glnrdns).send_keys(glnrdns)

    def click_userall(self):
        self.find_element(*self.userall).click()

    def click_movetosave(self):
        self.find_element(*self.u_movetosave).click()

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()