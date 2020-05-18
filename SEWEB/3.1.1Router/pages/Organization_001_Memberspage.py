#! -*-conding:utf-8 -*-
#@Time: 2018/12/28 0028 14:47
#@swzhou
'''
用户管理 - 组织成员页面
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'OrganizationMembersPage').getlog()
from common.ReadConfig import getMenu,getAssertText


class OrganizationMembersPage(BasePage):
    userGroupM = getMenu('userGroupM') #组织成员

    UserManage = (By.XPATH,'//span[@data-local="{UserManage}"]')
    userGroupM = (By.LINK_TEXT,userGroupM)
    # 新增 第一个组
    addBtnNewTree1 = (By.ID,'addBtn_newTree_1')
    groupName = (By.NAME,'name')
    save = (By.ID,'save')
    list_groupName1 = ('newTree_2_span') #新增后显示的组名
    list_groupName1_c = (By.ID,'newTree_2_span')
    delBtnNewTree1 = (By.ID,'newTree_2_remove') #删除第一个新增组
    ok = (By.ID,'u-cfm-ok')
    list_Rootgroup = ('newTree_1_span')  # Root组
    list_Rootgroup_c = (By.ID,'newTree_1_span')
    listTips = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td/div') #列表中的显示
    #002
    editBtnnewTree1 = (By.ID, 'editDemoBtn_newTree_2')  # 编辑第一个新增组
    #003
    groupID = (getAssertText('tempUser'))
    download = (By.ID,'download')
    chooseFile = (By.ID,'chooseFile')

    addUser = (By.ID,'addUser')
    UserName = (By.NAME,'name')
    normalIP = (By.NAME,'normalIP')
    listAddIP = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span')

    #认证用户
    authuser = (By.XPATH,'//input[@type="radio"and@value="authUser"]')
    authType = ('authType')
    authAccount = (By.NAME,'authAccount')
    authPassword = (By.NAME,'authPassword')
    list_authType = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[2]/td[5]/span')
    list_authAccount = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span')

    search = (By.XPATH,'//*[@id="page-count-control"]/div[2]/input') #搜索框
    searchB = (By.XPATH,'//*[@id="page-count-control"]/div[2]/i[2]') #搜索按钮
    checklist = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input') #列表第一行前勾
    moveUserTo = (By.ID,'moveUserTo')
    selmoveUserTo = ('moveUserTo')
    list_groupName2 = (By.ID,'newTree_3_span')  # 新增后显示的第二个组名
    list_authAccount2 = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    list_authgroup2 = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span')
    edituser1 = (By.XPATH,'//*[@data-primarykey="0"and@data-event="edit"]')
    changedusername = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    deluser1 = (By.XPATH, '//*[@data-primarykey="0"and@event-type="delete"]')
    allScan = (By.ID,'allScan') #扫描
    allScan1 = (By.XPATH, '//*[@id="topelms"]/button') #扫描中的扫描
    ScanTips = ('u-tim-str')
    Scanlist = ('//*[@id="modal-scan"]/div/div/div[2]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]/span')

    outload = (By.ID,'outload')
    list_groupName3 = ('newTree_4_span')  # 新增后显示的第3个组名
    #绑定
    IPMACb = (By.XPATH,'//input[@name="normalUserLinkType"and@value="IPMac"]')
    normalIPMac_IP = (By.NAME,'normalIPMac_IP')
    normalIPMac_Mac = (By.NAME,'normalIPMac_Mac')
    listAddMAC = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[9]/span')
    globalconfig = (By.LINK_TEXT,getMenu('globalconfigM'))
    IPMACb_E = (By.XPATH,'//input[@name="AllowOtherEnable"and@value="on"]')
    IPMACb_C = (By.XPATH, '//input[@name="AllowOtherEnable"and@value="off"]')
    IPMACb_Cs = ('//input[@name="AllowOtherEnable"and@value="off"]')
    saveAllSetting = (By.ID,'saveAllSetting')
    tips = ('pageTip-success')
    MACb = (By.XPATH,'//input[@name="normalUserLinkType"and@value="Mac"]')
    normalMac = (By.NAME,'normalMac')
    MACb_E = (By.XPATH,'//input[@name="forbidMac"and@value="on"]')
    MACb_C = (By.XPATH, '//input[@name="forbidMac"and@value="off"]')
    MACb_Cs = ('//input[@name="forbidMac"and@value="off"]')

    maxpagenums1 = ('//*[@id="1"]/div/div/div[2]/div/input')  # 组1页数框
    pageend1 = (By.XPATH, '//*[@id="1"]/div/div/div[2]/div/img[4]')  # 跳转最后页
    maxpagenums2 = ('//*[@id="2"]/div/div/div[2]/div/input')  # 组2页数框
    pageend2 = (By.XPATH, '//*[@id="2"]/div/div/div[2]/div/img[4]')  # 跳转最后页

    def click_UserManage(self):
        self.find_element(*self.UserManage).click()
        logger.info('点击用户管理')

    def click_userGroup(self):
        self.find_element(*self.userGroupM).click()
        logger.info('点击组织成员')

    def click_addBtnNewTree1(self):
        self.find_element(*self.addBtnNewTree1).click()

    def input_groupName(self,user):
        self.find_element(*self.groupName).clear()
        self.find_element(*self.groupName).send_keys(user)

    def click_save(self):
        self.find_element(*self.save).click()

    def click_list_groupName_c(self):
        self.find_element(*self.list_groupName1_c).click()

    def click_delBtnNewTree1(self):
        self.find_element(*self.delBtnNewTree1).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def click_list_Rootgroup_c(self):
        self.find_element(*self.list_Rootgroup_c).click()

    def click_editBtnnewTree1(self):
        self.find_element(*self.editBtnnewTree1).click()

    def click_download(self):
        self.find_element(*self.download).click()

    def click_chooseFile(self):
        self.find_element(*self.chooseFile).click()

    def click_addUser(self):
        self.find_element(*self.addUser).click()

    def input_UserName(self,UserName):
        self.find_element(*self.UserName).clear()
        self.find_element(*self.UserName).send_keys(UserName)

    def input_normalIP(self,normalIP):
        self.find_element(*self.normalIP).clear()
        self.find_element(*self.normalIP).send_keys(normalIP)

    def click_authuser(self):
        self.find_element(*self.authuser).click()

    def input_authAccount(self,authAccount):
        self.find_element(*self.authAccount).clear()
        self.find_element(*self.authAccount).send_keys(authAccount)

    def input_authPassword(self,authPassword):
        self.find_element(*self.authPassword).clear()
        self.find_element(*self.authPassword).send_keys(authPassword)

    def input_search(self,search):
        self.find_element(*self.search).clear()
        self.find_element(*self.search).send_keys(search)

    def click_searchB(self):
        self.find_element(*self.searchB).click()

    def click_checklist(self):
        self.find_element(*self.checklist).click()

    def click_moveUserTo(self):
        self.find_element(*self.moveUserTo).click()

    def click_list_groupName2(self):
        self.find_element(*self.list_groupName2).click()

    def click_edituser1(self):
        self.find_element(*self.edituser1).click()

    def click_deluser1(self):
        self.find_element(*self.deluser1).click()

    def click_allScan(self):
        self.find_element(*self.allScan).click()

    def click_allScan1(self):
        self.find_element(*self.allScan1).click()

    def click_outload(self):
        self.find_element(*self.outload).click()

    def click_IPMACb(self):
        self.find_element(*self.IPMACb).click()

    def input_normalIPMac_IP(self,normalIPMac_IP):
        self.find_element(*self.normalIPMac_IP).clear()
        self.find_element(*self.normalIPMac_IP).send_keys(normalIPMac_IP)

    def input_normalIPMac_Mac(self,normalIPMac_Mac):
        self.find_element(*self.normalIPMac_Mac).clear()
        self.find_element(*self.normalIPMac_Mac).send_keys(normalIPMac_Mac)

    def click_globalconfig(self):
        self.find_element(*self.globalconfig).click()

    def click_IPMACb_E(self):
        self.find_element(*self.IPMACb_E).click()

    def click_IPMACb_C(self):
        self.find_element(*self.IPMACb_C).click()

    def click_saveAllSetting(self):
        self.find_element(*self.saveAllSetting).click()

    def click_MACb(self):
        self.find_element(*self.MACb).click()

    def input_normalMac(self, normalMac):
        self.find_element(*self.normalMac).clear()
        self.find_element(*self.normalMac).send_keys(normalMac)

    def click_MACb_E(self):
        self.find_element(*self.MACb_E).click()

    def click_MACb_C(self):
        self.find_element(*self.MACb_C).click()

    def click_pageend1(self):
        self.find_element(*self.pageend1).click()

    def click_pageend2(self):
        self.find_element(*self.pageend2).click()