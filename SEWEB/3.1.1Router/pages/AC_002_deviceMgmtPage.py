#! -*-conding:utf-8 -*-
#@Time: 2019/1/25 0025 14:47
#@swzhou
'''
无线扩展 - 设备管理 页面
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'deviceMgmtPage').getlog()
from common.ReadConfig import getMenu

class deviceMgmtPage(BasePage):
    deviceMgmtM = getMenu('deviceMgmtM') #设备管理

    wirelessExtension = (By.XPATH, '//span[@data-local="{wirelessExtension}"]')
    deviceMgmt = (By.LINK_TEXT, deviceMgmtM)

    u_cfm_boxT = ('u-cfm-box')
    no = (By.ID, 'u-cfm-no')
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    refreshtable = (By.ID,'refreshtable')
    list_state1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span') #时间短 IP为空，状态位置为7

    Priorityv2 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[3]/div/img[1]') #点击管理通讯协议,v2优先
    list_status1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span') #正常时间 IP不为空，状态位置为8
    list_status2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[8]/span')
    list_status2by = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[8]/span')
    list_status3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[8]/span')
    list_status4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[8]/span')
    list_channel1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/a')
    list_channel2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[9]/a')
    list_channel3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[9]/a')
    list_channel4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[9]/a')
    list_channel1c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/a')
    list_channel2c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[9]/a')
    list_channel3c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[9]/a')
    list_channel4c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[9]/a')
    list_channel51 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[12]/a')
    list_channel52 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[12]/a')
    list_channel53 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[12]/a')
    list_channel54 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[12]/a')
    list_channel51c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[12]/a')
    list_channel52c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[12]/a')
    list_channel53c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[12]/a')
    list_channel54c = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[12]/a')
    list_sel1 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input')  # 勾选第一行
    BatchManagement = (By.ID, 'BatchManagement')  # 批量管理
    spmb = ('spmb')  # 射频设置
    tab_modal = (By.XPATH, '//*[@id="tab_modal"]/div/div/div[1]/button/span')  # 批量管理 - 关闭弹窗右上角
    modal_hide = (By.ID, 'modal-hide')  # 单台管理 - 关闭弹窗
    list_sel4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[1]/input')  # 勾选第4行
    list_2mode1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[10]/span')
    list_5mode1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[13]/span')
    list_IP1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    list_2mode4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[10]/span')
    list_5mode4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[13]/span')
    list_IP4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[7]/span')
    save = (By.ID,'save')
    #002 AP管理 001
    roamingSetM = getMenu('roamingSetM') #漫游阈值
    list_seq1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[6]/span') #序列号
    list_seq2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[6]/span')
    list_seq3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[6]/span')
    list_seq4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[6]/span')
    search = (By.XPATH,'//input[@data-local="{enterSearchContent}"]') #搜索框
    searchB = (By.CLASS_NAME,'icon-search')
    list_name1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/a')
    list_name1s = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/a')
    list_namein1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/div/input')
    list_nameS1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/div/button')
    list_name2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/a')
    list_name2s = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/a')
    list_namein2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/div/input')
    list_nameS2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/div/button')
    list_name3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/a')
    list_name3s = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/a')
    list_namein3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/div/input')
    list_nameS3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/div/button')
    list_name4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/a')
    list_name4s = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/a')
    list_namein4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/div/input')
    list_nameS4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/div/button')
    selchannel2_1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/div/select')
    selchannel2S_1 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/div/button')
    selchannel5_1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[12]/div/select')
    selchannel5S_1 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[12]/div/button')
    list_mangement1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[17]/a[2]') #单台管理1
    modifyPw = (By.NAME,'modifyPw') #修改密码
    pw1 = (By.NAME,'pw1')
    pw2 = (By.NAME,'pw2')
    roamingSet = (By.LINK_TEXT,roamingSetM) #漫游阈值
    roaming_en = (By.XPATH,'//input[@name="roaming_en"and@value="1"]')
    roaming_cs = ('//input[@name="roaming_en"and@value="0"]')
    roaming_ens = ('//input[@name="roaming_en"and@value="1"]')
    roaming_th = (By.NAME,'roaming_th')
    roaming_ths = ('roaming_th')
    roaming_en5 = (By.XPATH,'//input[@name="roaming_en5G"and@value="1"]')
    roaming_en5s = ('//input[@name="roaming_en5G"and@value="1"]')
    roaming_c5s = ('//input[@name="roaming_en5G"and@value="0"]')
    roaming_th5 = (By.NAME, 'roaming_th5G')
    roaming_ths5 = ('roaming_th5G')
    #002
    list_sel2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[1]/input')  # 勾选第2行
    ssidM = (By.XPATH,'//*[@id="tab_modal"]/div/div/div[2]/nav/ul/li[2]/a') #批量管理中的网络名称
    selall_w = (By.XPATH,'//*[@id="e2"]/div/div[1]/table/thead/tr/th[1]/input') #批量管理网络名称中全选
    sendToApM = (By.ID,'sendToApM')
    ok = (By.ID,'u-cfm-ok')
    list_ssid1 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[16]/span')
    list_ssids1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[16]/span')
    list_modes1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')
    list_ssid2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[16]/span')
    list_ssids2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[16]/span')
    list_modes2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[5]/span')
    list_ssid3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[16]/span')
    list_ssids3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[16]/span')
    list_modes3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[5]/span')
    list_ssid4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[16]/span')
    list_ssids4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[16]/span')
    list_modes4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[5]/span')
    list_selwn1 = (By.XPATH, '//*[@id="e2"]/div/div[1]/table/tbody/tr[1]/td[1]/input')
    list_selwn2 = (By.XPATH, '//*[@id="e2"]/div/div[1]/table/tbody/tr[2]/td[1]/input')#批量管理网络名称中第二
    list_selwn3 = (By.XPATH, '//*[@id="e2"]/div/div[1]/table/tbody/tr[3]/td[1]/input')
    list_sel3 = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[1]/input')#勾选第3行
    #003
    configrebootM = getMenu('configrebootM')
    backupconfigM = getMenu('backupconfigM')
    list_reboot1 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[17]/a[1]')
    list_reboot2 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[17]/a[1]')
    list_reboot3 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[17]/a[1]')
    list_reboot4 = (By.XPATH, '//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[17]/a[1]')
    tipsshowin = ('tips-show-in')
    ftipsshowin = (By.CLASS_NAME,'tips-show-in')
    configreboot = (By.LINK_TEXT,configrebootM) #配置重启
    factory_reset = (By.ID,'factory-reset')
    restart = (By.ID, 'restart') #重启
    backupconfig = (By.LINK_TEXT,backupconfigM)
    searchBack = (By.XPATH,'//*[@id="2"]/div/div/header/ul/div[2]/input')
    searchBackb = (By.XPATH,'//*[@id="2"]/div/div/header/ul/div[2]/i')
    listback_nodata = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    listback_nodatab = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    close = (By.CLASS_NAME,'close')
    allDelete = (By.ID,'allDelete')  #备份配置中删除
    clearOutlineAP = (By.ID,'clearOutlineAP')
    bconfigseq1 = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span/span')
    bconfigmodel1 = ('//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[5]/span')
    backup = (By.ID,'backup')
    selall_b = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/thead/tr/th[1]/input') #备份配置中全选
    sellist1 = (By.XPATH,'//*[@id="2"]/div/div/div[1]/table/tbody/tr[1]/td[1]/input') #备份配置中选中第一行
    uploadBackup = (By.ID,'uploadBackup')
    chooseFile = (By.ID,'chooseFile')
    demo_id = (By.ID,'demo_id')
    #系统设置
    SyssetupM = getMenu('SyssetupM')
    Syssetup = (By.LINK_TEXT,SyssetupM)
    TaskS_En = (By.XPATH,'//input[@name="TaskS"and@value="1"]')
    TaskS_C = (By.XPATH, '//input[@name="TaskS"and@value="0"]')
    sleepMode_En = (By.XPATH,'//input[@name="sleepMode"and@value="on"]')
    sleepMode_C = (By.XPATH, '//input[@name="sleepMode"and@value="off"]')
    TaskSValue = ('TaskSValue')

    Prioritystate = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[8]/div/img[1]') #状态，在线在上

    def click_wirelessExtension(self):
        self.find_element(*self.wirelessExtension).click()
        logger.info('点击无线扩展')

    def click_deviceMgmt(self):
        self.find_element(*self.deviceMgmt).click()
        logger.info('点击设备管理')

    def click_no(self):
        self.find_element(*self.no).click()

    def click_refreshtable(self):
        self.find_element(*self.refreshtable).click()

    def click_Priorityv2(self):
        self.find_element(*self.Priorityv2).click()

    def click_list_sel1(self):
        self.find_element(*self.list_sel1).click()

    def click_BatchManagement(self):
        self.find_element(*self.BatchManagement).click()

    def click_tab_modal(self):
        self.find_element(*self.tab_modal).click()

    def click_modal_hide(self):
        self.find_element(*self.modal_hide).click()

    def click_list_sel3(self):
        self.find_element(*self.list_sel3).click()

    def click_list_sel4(self):
        self.find_element(*self.list_sel4).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def input_search(self,search):
        self.find_element(*self.search).clear()
        self.find_element(*self.search).send_keys(search)

    def click_searchB(self):
        self.find_element(*self.searchB).click()

    def click_list_name1(self):
        self.find_element(*self.list_name1).click()

    def click_list_nameS1(self):
        self.find_element(*self.list_nameS1).click()

    def find_list_nameS1(self):
        self.exist_element(*self.list_nameS1)

    def click_list_name2(self):
        self.find_element(*self.list_name2).click()

    def click_list_nameS2(self):
        self.find_element(*self.list_nameS2).click()

    def click_list_name3(self):
        self.find_element(*self.list_name3).click()

    def click_list_nameS3(self):
        self.find_element(*self.list_nameS3).click()

    def click_list_name4(self):
        self.find_element(*self.list_name4).click()

    def click_list_nameS4(self):
        self.find_element(*self.list_nameS4).click()

    def input_list_namein1(self, list_namein1):
        self.find_element(*self.list_namein1).clear()
        self.find_element(*self.list_namein1).send_keys(list_namein1)

    def input_list_namein2(self, list_namein2):
        self.find_element(*self.list_namein2).clear()
        self.find_element(*self.list_namein2).send_keys(list_namein2)

    def input_list_namein3(self, list_namein3):
        self.find_element(*self.list_namein3).clear()
        self.find_element(*self.list_namein3).send_keys(list_namein3)

    def input_list_namein4(self, list_namein4):
        self.find_element(*self.list_namein4).clear()
        self.find_element(*self.list_namein4).send_keys(list_namein4)

    def click_list_channel1c(self):
        self.find_element(*self.list_channel1c).click()

    def click_selchannel2S_1(self):
        self.find_element(*self.selchannel2S_1).click()

    def find_selchannel2S_1(self):
        self.exist_element(*self.selchannel2S_1)

    def click_list_channel51c(self):
        self.find_element(*self.list_channel51c).click()

    def click_selchannel5S_1(self):
        self.find_element(*self.selchannel5S_1).click()

    def find_selchannel5S_1(self):
        self.exist_element(*self.selchannel5S_1)

    def click_list_mangement1(self):
        self.find_element(*self.list_mangement1).click()

    def click_modifyPw(self):
        self.find_element(*self.modifyPw).click()

    def input_pw1(self, pw1):
        self.find_element(*self.pw1).clear()
        self.find_element(*self.pw1).send_keys(pw1)

    def input_pw2(self, pw2):
        self.find_element(*self.pw2).clear()
        self.find_element(*self.pw2).send_keys(pw2)

    def click_roamingSet(self):
        self.find_element(*self.roamingSet).click()

    def click_roaming_en(self):
        self.find_element(*self.roaming_en).click()

    def input_roaming_th(self, roaming_th):
        self.find_element(*self.roaming_th).clear()
        self.find_element(*self.roaming_th).send_keys(roaming_th)

    def click_roaming_en5(self):
        self.find_element(*self.roaming_en5).click()

    def input_roaming_th5(self, roaming_th5):
        self.find_element(*self.roaming_th5).clear()
        self.find_element(*self.roaming_th5).send_keys(roaming_th5)

    def click_list_sel2(self):
        self.find_element(*self.list_sel2).click()

    def click_ssidM(self):
        self.find_element(*self.ssidM).click()

    def click_selall_w(self):
        self.find_element(*self.selall_w).click()

    def click_sendToApM(self):
        self.find_element(*self.sendToApM).click()

    def find_sendToApM(self):
        self.exist_element(*self.sendToApM)


    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def click_list_ssid1(self):
        self.find_element(*self.list_ssid1).click()

    def click_list_ssid2(self):
        self.find_element(*self.list_ssid2).click()

    def click_list_ssid3(self):
        self.find_element(*self.list_ssid3).click()

    def click_list_ssid4(self):
        self.find_element(*self.list_ssid4).click()

    def click_list_selwn1(self):
        self.exist_element(*self.list_selwn1).click()

    def click_list_selwn2(self):
        self.find_element(*self.list_selwn2).click()

    def click_list_selwn3(self):
        self.find_element(*self.list_selwn3).click()

    def click_list_reboot1(self):
        self.find_element(*self.list_reboot1).click()

    def find_list_reboot1(self):
        self.exist_element(*self.list_reboot1)

    def click_list_reboot2(self):
        self.find_element(*self.list_reboot2).click()

    def click_list_reboot3(self):
        self.find_element(*self.list_reboot3).click()

    def click_list_reboot4(self):
        self.find_element(*self.list_reboot4).click()

    def click_configreboot(self):
        self.find_element(*self.configreboot).click()

    def click_factory_reset(self):
        self.find_element(*self.factory_reset).click()

    def find_factory_reset(self):
        self.exist_element(*self.factory_reset)

    def click_restart(self):
        self.find_element(*self.restart).click()

    def find_restart(self):
        self.exist_element(*self.restart)

    def click_backupconfig(self):
        self.find_element(*self.backupconfig).click()

    def input_searchBack(self,searchBack):
        self.find_element(*self.searchBack).clear()
        self.find_element(*self.searchBack).send_keys(searchBack)

    def click_searchBackb(self):
        self.find_element(*self.searchBackb).click()

    def find_tipsshowin(self):
        self.exist_element(*self.ftipsshowin).click()

    def click_close(self):
        self.find_element(*self.close).click()

    def click_clearOutlineAP(self):
        self.find_element(*self.clearOutlineAP).click()

    def find_list_status2(self):
        self.exist_element(*self.list_status2by).click()

    def click_backup(self):
        self.find_element(*self.backup).click()

    def find_backup(self):
        self.exist_element(*self.backup)

    def click_selall_b(self):
        self.find_element(*self.selall_b).click()

    def click_sellist1(self):
        self.find_element(*self.sellist1).click()

    def click_allDelete(self):
        self.find_element(*self.allDelete).click()

    def find_allDelete(self):
        self.exist_element(*self.allDelete)

    def find_listback_nodata(self):
        self.exist_element(*self.listback_nodatab)

    def click_uploadBackup(self):
        self.find_element(*self.uploadBackup).click()

    def find_uploadBackup(self):
        self.exist_element(*self.uploadBackup)

    def click_chooseFile(self):
        self.find_element(*self.chooseFile).click()

    def click_demo_id(self):
        self.find_element(*self.demo_id).click()

    def click_Syssetup(self):
        self.find_element(*self.Syssetup).click()

    def click_TaskS_En(self):
        self.find_element(*self.TaskS_En).click()

    def click_TaskS_C(self):
        self.find_element(*self.TaskS_C).click()

    def click_sleepMode_En(self):
        self.find_element(*self.sleepMode_En).click()

    def click_sleepMode_C(self):
        self.find_element(*self.sleepMode_C).click()

    def click_Prioritystate(self):
        self.find_element(*self.Prioritystate).click()