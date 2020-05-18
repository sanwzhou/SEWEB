#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 15:10
#@swzhou
'''
VPN配置 -- ipsec
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'ipsecPage').getlog()
from common.ReadConfig import getMenu

class IPsecPage(BasePage):
    IPSecM = getMenu('IPSecM')

    VPNConfig = (By.XPATH, '//span[@data-local="{VPNConfig}"]') #VPN配置菜单
    IPSec = (By.LINK_TEXT, IPSecM)  # ipsec配置菜单

    add = (By.ID,'add')
    connType = ('connType')
    transform = ('transform[0]') #加密认证算法
    highChoosen = (By.ID,'highChoosen') # 高级选项
    negMode = ('//*[@id="highChoosen"]/div/div/div[2]/table/tbody/tr[2]/td[2]/select') #协商模式
    policy = ('//*[@id="highChoosen"]/div/div/div[2]/table/tbody/tr[4]/td[2]/select') #加密认证算法1
    anti_replay = (By.XPATH,'//input[@type="checkbox"and@name="anti_replay"]') #抗重播
    dpdEn = (By.XPATH,'//input[@type="checkbox"and@name="dpdEnable"]') #DPD
    nattEn = (By.XPATH,'//input[@type="checkbox"and@name="nattEnable"]') #NAT穿透
    HeartbeatInt = (By.XPATH,'//*[@id="highChoosen"]/div/div/div[2]/table/tbody/tr[17]/td[2]/input') #心跳
    natPort = (By.XPATH,'//*[@id="highChoosen"]/div/div/div[2]/table/tbody/tr[18]/td[2]/input') #端口
    Keepalive = (By.XPATH,'//*[@id="highChoosen"]/div/div/div[2]/table/tbody/tr[19]/td[2]/input') #维持
    localBind = ('localBind') #本地绑定
    selall = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/thead/tr/th[1]')
    delall = (By.ID,'delete')
    ok = (By.ID,'u-cfm-ok')
    no = (By.ID,'u-cfm-no')
    u_tim_str = ('u-tim-str')
    tipsshowin = (By.CLASS_NAME, 'tips-show-in')
    ids = (By.NAME,'ids') #隧道名称
    peer = (By.NAME,'peer') #远端网关地址
    remoteAddr = (By.NAME,'remoteAddr')  #远端内网地址
    remoteMask = (By.NAME,'remoteMask') #远端内网子网掩码
    preshareKey = (By.NAME,'preshareKey') #预共享密钥
    save = (By.ID,'save')
    list_status = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td[4]/span') #VPN状态
    list_nodata = ('//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')
    list_nodataX = (By.XPATH,'//*[@id="1"]/div/div/div[1]/table/tbody/tr[1]/td/div')


    def click_VPNConfig(self):
        self.find_element(*self.VPNConfig).click()
        logger.info('点击VPN配置')

    def click_IPSec(self):
        self.find_element(*self.IPSec).click()
        logger.info('点击IPSec')

    def click_add(self):
        self.find_element(*self.add).click()

    def click_highChoosen(self):
        self.find_element(*self.highChoosen).click()

    def click_anti_replay(self):
        self.find_element(*self.anti_replay).click()

    def click_dpdEn(self):
        self.find_element(*self.dpdEn).click()

    def click_nattEn(self):
        self.find_element(*self.nattEn).click()

    def input_HeartbeatInt(self,HeartbeatInt):
        self.find_element(*self.HeartbeatInt).clear()
        self.find_element(*self.HeartbeatInt).send_keys(HeartbeatInt)

    def input_natPort(self, natPort):
        self.find_element(*self.natPort).clear()
        self.find_element(*self.natPort).send_keys(natPort)

    def input_Keepalive(self, Keepalive):
        self.find_element(*self.Keepalive).clear()
        self.find_element(*self.Keepalive).send_keys(Keepalive)

    def click_selall(self):
        self.find_element(*self.selall).click()

    def click_delall(self):
        self.find_element(*self.delall).click()

    def find_ok(self):
        self.exist_element(*self.ok).click()

    def find_no(self):
        self.exist_element(*self.no).click()

    def click_ok(self):
        self.find_element(*self.ok).click()

    def find_tipsshowin(self):
        self.exist_element(*self.tipsshowin)

    def input_ids(self, ids):
        self.find_element(*self.ids).clear()
        self.find_element(*self.ids).send_keys(ids)

    def input_peer(self,peer):
        self.find_element(*self.peer).clear()
        self.find_element(*self.peer).send_keys(peer)

    def input_remoteAddr(self,remoteAddr):
        self.find_element(*self.remoteAddr).clear()
        self.find_element(*self.remoteAddr).send_keys(remoteAddr)

    def input_remoteMask(self,remoteMask):
        self.find_element(*self.remoteMask).clear()
        self.find_element(*self.remoteMask).send_keys(remoteMask)

    def input_preshareKey(self,preshareKey):
        self.find_element(*self.preshareKey).clear()
        self.find_element(*self.preshareKey).send_keys(preshareKey)

    def click_save(self):
        self.find_element(*self.save).click()

    def find_list_nodataX(self):
        self.exist_element(*self.list_nodataX)