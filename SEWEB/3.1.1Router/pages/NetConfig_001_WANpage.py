#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 18:15
#@swzhou
'''
网络配置 外网配置页面 元素定位
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'NetworkConfig_wan').getlog()
from common.ReadConfig import getMenu

class NetworkConfig_wanpage(BasePage):
    wanconfigM = getMenu('wanconfigM')

    NetworkConfig = (By.XPATH,'//span[@data-local="{netConfig}"]')
    #外网配置
    WANconfig = (By.LINK_TEXT,wanconfigM)
    line1edit = (By.XPATH, '//*[@data-primarykey="0"and@data-event="edit"]')
    line2edit = (By.XPATH, '//*[@data-primarykey="1"and@data-event="edit"]')
    line3edit = (By.XPATH, '//*[@data-primarykey="2"and@data-event="edit"]')
    line4edit = (By.XPATH, '//*[@data-primarykey="3"and@data-event="edit"]')
    line5edit = (By.XPATH, '//*[@data-primarykey="4"and@data-event="edit"]')
    PortName = ('PortName') #接口
    # PortNameOptions = (By.TAG_NAME,'option') #接口中option 统计wan口数量
    PortNameOptions = ('option')  # 接口中option 统计wan口数量
    back = (By.ID,'back')
    cfm_ok = (By.ID,'u-cfm-ok')

    line2delete = (By.XPATH, '//span[@data-primarykey="1"and@event-type="delete"]')
    line3delete = (By.XPATH, '//span[@data-primarykey="2"and@event-type="delete"]')
    line4delete = (By.XPATH, '//span[@data-primarykey="3"and@event-type="delete"]')
    line5delete = (By.XPATH, '//span[@data-primarykey="4"and@event-type="delete"]')

    line1Type = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span') #wan口连接类型
    line2Type = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[4]/span')
    line3Type = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[4]/span')
    line4Type = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[4]/span')
    line5Type = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[4]/span')

    connectionType = ('connectionType') #连接类型
    save = (By.ID,'save')

    refresh = (By.XPATH, '//*[@id="otherBtns"]/button[3]') #刷新
    refresh_s = (By.XPATH,'//*[@id="otherBtns"]/button') #固定IP线路的刷新
    connectState1 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[2]/a') #连接状态
    connectState2 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[2]/a')
    connectState3 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[2]/a')
    connectState4 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[2]/a')
    connectState5 = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[2]/a')

    line1IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[3]/span')
    line2IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[3]/span')
    line3IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[3]/span')
    line4IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[3]/span')
    line5IP = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[3]/span')
    line1gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[7]/span')
    line2gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[7]/span')
    line3gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[7]/span')
    line4gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[7]/span')
    line5gw = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[7]/span')
    line1Dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[9]/span')
    line2Dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[9]/span')
    line3Dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[9]/span')
    line4Dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[9]/span')
    line5Dns = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[9]/span')
    line1Mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[8]/span')
    line2Mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[2]/td[8]/span')
    line3Mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[3]/td[8]/span')
    line4Mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[4]/td[8]/span')
    line5Mac = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[5]/td[8]/span')
    # 固定
    staticIp = (By.NAME, 'staticIp')
    staticGateway = (By.NAME, 'staticGateway')
    staticPriDns = (By.NAME, 'staticPriDns')
    refreshstatic = (By.XPATH, '//*[@id="otherBtns"]/button')  # 刷新

    #002
    line_type = ('//*[@id="1"]/table[2]/tbody/tr[1]/td[2]/select') #固定为table[2] dhcp为3 ppoe为4
    globalconfigM = getMenu('globalconfigM')
    GlobalConfig = (By.LINK_TEXT,globalconfigM)
    KeepLive1 = (By.NAME,'KeepLive1')   #检测间隔
    KeepLive1v = ('KeepLive1')
    RetryTimes1 = (By.NAME,'RetryTimes1')   #检测次数
    RetryTimes1v = ('RetryTimes1')
    PriAddrType1 = ('PriAddrType1') #检测目标
    DestIP1 = (By.NAME,'DestIP1') # 检测地址
    DestIP1v = ('DestIP1')
    KeepLive2 = (By.NAME, 'KeepLive2')  # 检测间隔
    KeepLive2v = ('KeepLive2')
    RetryTimes2 = (By.NAME, 'RetryTimes2')  # 检测次数
    RetryTimes2v = ('RetryTimes2')
    PriAddrType2 = ('PriAddrType2')  # 检测目标
    DestIP2 = (By.NAME, 'DestIP2')  # 检测地址
    DestIP2v = ('DestIP2')
    KeepLive3 = (By.NAME, 'KeepLive3')  # 检测间隔
    KeepLive3v = ('KeepLive3')
    RetryTimes3 = (By.NAME, 'RetryTimes3')  # 检测次数
    RetryTimes3v = ('RetryTimes3')
    PriAddrType3 = ('PriAddrType3')  # 检测目标
    DestIP3 = (By.NAME, 'DestIP3')  # 检测地址
    DestIP3v = ('DestIP3')
    KeepLive4 = (By.NAME, 'KeepLive4')  # 检测间隔
    KeepLive4v = ('KeepLive4')
    RetryTimes4 = (By.NAME, 'RetryTimes4')  # 检测次数
    RetryTimes4v = ('RetryTimes4')
    PriAddrType4 = ('PriAddrType4')  # 检测目标
    DestIP4 = (By.NAME, 'DestIP4')  # 检测地址
    DestIP4v = ('DestIP4')
    KeepLive5 = (By.NAME, 'KeepLive5')  # 检测间隔
    KeepLive5v = ('KeepLive5')
    RetryTimes5 = (By.NAME, 'RetryTimes5')  # 检测次数
    RetryTimes5v = ('RetryTimes5')
    PriAddrType5 = ('PriAddrType5')  # 检测目标
    DestIP5 = (By.NAME, 'DestIP5')  # 检测地址
    DestIP5v = ('DestIP5')
    tipsshowin = ('tips-show-in')
    ftipsshowin = (By.CLASS_NAME, 'tips-show-in')
    selPortNumber = ('PortNumber') #wan口数量
    PortNumber = (By.NAME,'PortNumber')

    #003 PPPoE
    pppoeUser = (By.NAME,'pppoeUser')
    pppoePass = (By.NAME,'pppoePass')
    dial = (By.XPATH,'//*[@id="otherBtns"]/button[2]')

    wanRateseled = ('//*[@id="1"]/table[3]/tbody/tr[7]/td[2]/select/option[1]')  # 默认协商速率
    selwanRate = ('//*[@id="1"]/table[3]/tbody/tr[7]/td[2]/select') #协商速率
    line1editmac = (By.XPATH,'//*[@id="1"]/table[3]/tbody/tr[8]/td[2]/input') #line1编辑中得mac 接口类型dhcp
    wan_tips = ('//*[@id="1"]/table[3]/tbody/tr[8]/td[2]/span/span[2]') # wan1口mac地址清空保存提示
    workMode = ('enabled') #工作模式
    pppoeOPMode = ('pppoeOPMode') # 拨号类型
    pppoeDailMode = ('pppoeDailMode') # 拨号类型
    # 注意这里下拉框select_by_value('0')有问题，使用xpath选择 主备份线路
    backline1 = (By.XPATH,'//*[@id="1"]/table[3]/tbody/tr[1]/td[2]/select/option[2]')
    mainline1 = (By.XPATH, '//*[@id="1"]/table[3]/tbody/tr[1]/td[2]/select/option[1]')
    txBands2 = (By.NAME,'txBands2') #上行带宽
    rxBands2 = (By.NAME, 'rxBands2') #下行带宽
    rMin2 = (By.NAME,'rMin2') #带宽下限
    rMax2 = (By.NAME, 'rMax2') #带宽上限
    limitRatio2 = (By.NAME,'limitRatio2') #限制比
    ISPType = (By.NAME,'ISPType') #运行商 电信 移动 联通
    ISPType1 = (By.NAME, 'ISPType1')
    ISPType2 = (By.NAME, 'ISPType2')

    #全局配置中的快速转发
    FastForwardEnable = ('FastForwardEnable') #模式开关
    enable1 = ('//*[@name="FastForwardEnable"]/option[1]') #极速模式1 自动
    FastForwardEnableC = (By.NAME,'FastForwardEnable')

    FastForwardModeC = (By.NAME,'FastForwardMode') #转发模式
    enable2 = ('//*[@name="FastForwardMode"]/option[2]')  # 模式选择 2硬件加速

    def click_NetworkConfig(self):
        self.find_element(*self.NetworkConfig).click()
        logger.info('点击网络配置')

    def click_WANconfig(self):
        self.find_element(*self.WANconfig).click()
        logger.info('点击外网配置')

    def click_line1edit(self):
        self.find_element(*self.line1edit).click()

    def click_line2edit(self):
        self.find_element(*self.line2edit).click()

    def click_line3edit(self):
        self.find_element(*self.line3edit).click()

    def click_line4edit(self):
        self.find_element(*self.line4edit).click()

    def click_line5edit(self):
        self.find_element(*self.line5edit).click()

    # def sel_PortName(self):
    #     self.selName_element(*self.PortName)

    # def get_PortNameOptions(self):
    #     self.find_element(*self.PortNameOptions)

    def click_back(self):
        self.find_element(*self.back).click()

    def click_cfm_ok(self):
        self.find_element(*self.cfm_ok).click()

    def find_cfm_ok(self):
        self.exist_element(*self.cfm_ok).click()

    def click_line2delete(self):
        self.find_element(*self.line2delete).click()

    def click_line3delete(self):
        self.find_element(*self.line3delete).click()

    def click_line4delete(self):
        self.find_element(*self.line4delete).click()

    def click_line5delete(self,):
        self.find_element(*self.line5delete).click()

    def find_PortNumber(self):
        self.exist_element(*self.PortNumber).click()

    def click_save(self):
        self.find_element(*self.save).click()

    def click_refresh(self):
        self.find_element(*self.refresh).click()

    def click_refresh_s(self):
        self.find_element(*self.refresh_s).click()

    def input_staticIp(self,staticIp):
        self.find_element(*self.staticIp).clear()
        self.find_element(*self.staticIp).send_keys(staticIp)

    def input_staticGateway(self,staticGateway):
        self.find_element(*self.staticGateway).clear()
        self.find_element(*self.staticGateway).send_keys(staticGateway)

    def input_staticPriDns(self,staticPriDns):
        self.find_element(*self.staticPriDns).clear()
        self.find_element(*self.staticPriDns).send_keys(staticPriDns)

    def click_GlobalConfig(self):
        self.find_element(*self.GlobalConfig).click()

    def find_GlobalConfig(self):
        self.exist_element(*self.GlobalConfig).click()

    def input_KeepLive1 (self,KeepLive1 ):
        self.find_element(*self.KeepLive1).clear()
        self.find_element(*self.KeepLive1 ).send_keys(KeepLive1 )

    def input_RetryTimes1 (self,RetryTimes1 ):
        self.find_element(*self.RetryTimes1).clear()
        self.find_element(*self.RetryTimes1 ).send_keys(RetryTimes1 )

    def input_DestIP1 (self,DestIP1):
        self.find_element(*self.DestIP1).clear()
        self.find_element(*self.DestIP1).send_keys(DestIP1)

    def input_KeepLive2 (self,KeepLive2 ):
        self.find_element(*self.KeepLive2).clear()
        self.find_element(*self.KeepLive2 ).send_keys(KeepLive2 )

    def input_RetryTimes2 (self,RetryTimes2 ):
        self.find_element(*self.RetryTimes2).clear()
        self.find_element(*self.RetryTimes2 ).send_keys(RetryTimes2)

    def input_DestIP2 (self,DestIP2):
        self.find_element(*self.DestIP2).clear()
        self.find_element(*self.DestIP2).send_keys(DestIP2)

    def input_KeepLive3 (self,KeepLive3 ):
        self.find_element(*self.KeepLive3).clear()
        self.find_element(*self.KeepLive3 ).send_keys(KeepLive3 )

    def input_RetryTimes3 (self,RetryTimes3 ):
        self.find_element(*self.RetryTimes3).clear()
        self.find_element(*self.RetryTimes3 ).send_keys(RetryTimes3 )

    def input_DestIP3(self,DestIP3):
        self.find_element(*self.DestIP3).clear()
        self.find_element(*self.DestIP3).send_keys(DestIP3)

    def input_KeepLive4 (self,KeepLive4 ):
        self.find_element(*self.KeepLive4).clear()
        self.find_element(*self.KeepLive4 ).send_keys(KeepLive4 )

    def input_RetryTimes4 (self,RetryTimes4):
        self.find_element(*self.RetryTimes4).clear()
        self.find_element(*self.RetryTimes4).send_keys(RetryTimes4)

    def input_DestIP4 (self,DestIP4):
        self.find_element(*self.DestIP4).clear()
        self.find_element(*self.DestIP4).send_keys(DestIP4)

    def input_KeepLive5 (self,KeepLive5 ):
        self.find_element(*self.KeepLive5).clear()
        self.find_element(*self.KeepLive5 ).send_keys(KeepLive5 )

    def input_RetryTimes5(self,RetryTimes5 ):
        self.find_element(*self.RetryTimes5).clear()
        self.find_element(*self.RetryTimes5 ).send_keys(RetryTimes5 )

    def input_DestIP5 (self,DestIP5):
        self.find_element(*self.DestIP5).clear()
        self.find_element(*self.DestIP5).send_keys(DestIP5)

    def input_pppoeUser (self,pppoeUser):
        self.find_element(*self.pppoeUser).clear()
        self.find_element(*self.pppoeUser).send_keys(pppoeUser)

    def input_pppoePass (self,pppoePass):
        self.find_element(*self.pppoePass).clear()
        self.find_element(*self.pppoePass).send_keys(pppoePass)

    def click_connectState1 (self):
        self.find_element(*self.connectState1).click()

    def click_dial(self):
        self.find_element(*self.dial).click()

    def click_refreshstatic(self):
        self.find_element(*self.refreshstatic).click()

    def clear_line1editmac(self):
        self.find_element(*self.line1editmac).clear()

    def click_backline1(self):
        self.find_element(*self.backline1).click()

    def click_mainline1(self):
        self.find_element(*self.mainline1).click()

    def input_txBands2(self,txBands2 ):
        self.find_element(*self.txBands2).clear()
        self.find_element(*self.txBands2).send_keys(txBands2)

    def input_rxBands2 (self,rxBands2):
        self.find_element(*self.rxBands2).clear()
        self.find_element(*self.rxBands2).send_keys(rxBands2)

    def input_rMin2 (self,rMin2):
        self.find_element(*self.rMin2).clear()
        self.find_element(*self.rMin2).send_keys(rMin2)

    def input_rMax2(self,rMax2):
        self.find_element(*self.rMax2).clear()
        self.find_element(*self.rMax2).send_keys(rMax2)

    def input_limitRatio2(self,limitRatio2):
        self.find_element(*self.limitRatio2).clear()
        self.find_element(*self.limitRatio2).send_keys(limitRatio2)

    def click_ISPType (self):
        self.find_element(*self.ISPType).click()

    def click_ISPType1(self):
        self.find_element(*self.ISPType1).click()

    def click_ISPType2(self):
        self.find_element(*self.ISPType2).click()

    def find_tipsshowin(self):
        self.exist_element(*self.ftipsshowin).click()

    def click_FastForwardEnableC(self):
        self.find_element(*self.FastForwardEnableC).click()

    def click_FastForwardModeC(self):
        self.find_element(*self.FastForwardModeC).click()
