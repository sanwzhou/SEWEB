#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 9:41
#@swzhou
'''
网路配置 - 交换配置
'''

'''
191031 修改二级菜单 交换配置为一级菜单
'''

from selenium.webdriver.common.by import By
from pages.basepage import BasePage
from common.LogGen import LogGen
logger = LogGen(Logger = 'switchConfigPage').getlog()
from common.ReadConfig import getMenu

class switchConfigPage(BasePage):

    portVlanM = getMenu('portVlanM')
    portMirrorM = getMenu('portMirrorM')

    switchConfig = (By.XPATH, '//span[@data-local="{switchConfig}"]')# 交换配置

    # 端口vlan
    portVlan = (By.LINK_TEXT,portVlanM )
    VLAN1 = ('//*[@id="1"]/table/tbody/tr[1]/td[1]/label')
    VLAN2 = ('//*[@id="1"]/table/tbody/tr[2]/td[1]/label')
    #端口镜像
    portMirror = (By.LINK_TEXT,portMirrorM)
    MirrorEns = ('//input[@name="MirrorEnable"and@value="off"]')
    Monitorport = ('//*[@id="1"]/table/tbody/tr[2]/td[1]/label') #监控端口
    Monitoredport = ('//*[@id="1"]/table/tbody/tr[3]/td[1]/label') #被监控端口


    def click_switchConfig(self):
        self.find_element(*self.switchConfig).click()
        logger.info('点击交换配置')

    def click_portVlan(self):
        self.find_element(*self.portVlan).click()
        logger.info('点击端口vlan二级菜单')

    def click_portMirror(self):
        self.find_element(*self.portMirror).click()
        logger.info('点击端口镜像二级菜单')

    def find_switchConfig(self):
        self.exist_element(*self.switchConfig).click()
        logger.info('点击交换配置')

    def find_portVlan(self):
        self.exist_element(*self.portVlan).click()
        logger.info('点击端口vlan二级菜单')

    def find_portMirror(self):
        self.exist_element(*self.portMirror).click()
        logger.info('点击端口镜像二级菜单')