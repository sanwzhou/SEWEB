#! -*-conding:utf-8 -*-
#@Time: 2018/7/19 0019 9:41
#@swzhou
'''
产品型号测试
'''

import os
from common.ParametersFile import delParametersFile
from common.ParametersFile import GetParameters
delParametersFile()
GetParameters()

import time
import HTMLTestRunner
import unittest
import sys
from common.ReadConfig import getweb,getParameter
from common.GetExcelValue import getExcelValue
from common.GetRouteCPU import getCPUmodel
from common.swconfig import swconfig
from common.initTestPC import initTestPC
from common.send_mail import sendMail
# from common.ParametersFileU import parametersFile

from test_case import sysConfig_000_Getready #准备工作恢复出厂
from test_case import AdditionalTest  #60023 1 ；动激活保修期     2；MTK确认库版本升级  3
#系统信息  4
from test_case import SysMonitor_001_sysStatic
#硬件相关  5
from test_case import ConfigGuide
from test_case import NetworkConfig_001_1WAN
from test_case import NetworkConfig_003_DHCPserver
from test_case import NetworkConfig_006_DDNSconfig
from test_case import PortMapping_002_staticMap
from test_case import Members_007_WebAuth
from test_case import Members_008_FreeAuth
from test_case import Members_010_remoteAuth
from test_case import Members_006_PPPoEAuth
#IP/MAC绑定 dhcp_server中验证
from test_case import actionManage_005_ElectronicsNotice
from test_case import sysConfig_002_RemoteManagement
from test_case import sysConfig_006_softwareUpdata
from test_case import sysConfig_007_policylibAppTemp
#系统状态 16
#流量管理
#VPN
from test_case import VPNconfig_001_ipsec
from test_case import VPNconfig_002_PPTPL2TP
#网络共享
from test_case import NetworkSharing_001_UdiskMount
from test_case import NetworkSharing_002_AccountSettings
from test_case import NetworkSharing_003_ftpServerSmaba

#电子授权
#AC功能
from test_case import AC_001_ExpansionSwitch
from test_case import AC_002_APmanagement
from test_case import AC_003_netName
from test_case import AC_004_Rftemplate
from test_case import AC_006_APSoftware
from test_case import AC_007_configlist
#无线
from test_case import WIFIconfig_001_configGuide
from test_case import WIFIconfig_002_BasicSet
from test_case import WIFIconfig_003_RFConfig
#附加

CPUmodel = getCPUmodel()

#手动添加用例
suite = unittest.TestSuite()

#初始化交换机/恢复出厂路由器
suite.addTest(swconfig('test_initSwPort'))
suite.addTest(initTestPC('test_initTestPC'))
suite.addTest(sysConfig_000_Getready.Getready('test_resertFirstLogin'))
suite.addTest(sysConfig_000_Getready.Getready('test_001_ntpClockServer'))
#软件升级
suite.addTest(sysConfig_006_softwareUpdata.softwareUpdate('test_errorSoftware'))
suite.addTest(sysConfig_006_softwareUpdata.softwareUpdate('test_oldSoftware1'))
suite.addTest(sysConfig_006_softwareUpdata.softwareUpdate('test_newSoftware1'))

#附加测试 60023 1 ；动激活保修期     2；MTK确认库版本升级  3
suite.addTest(AdditionalTest.AdditionalTest('test_001_closeWAN60023'))
suite.addTest(AdditionalTest.AdditionalTest('test_002_uttWaitSerch'))
APnumP = getParameter('APnumP')
Support = getExcelValue(APnumP)
if Support != None and CPUmodel == "MTK": #以访有些参数表里未包含ac相关数据
    suite.addTest(AdditionalTest.AdditionalTest('test_003_MTKlibuClibc'))
if CPUmodel == 'X86':
    suite.addTest(AdditionalTest.AdditionalTest('test_004_X86_CONFIG4KSTACKS'))
suite.addTest(AdditionalTest.AdditionalTest('test_005_cloundDownloadFile'))  # 目前3.2.2发布软件均支持上云
#配置向导
suite.addTest(ConfigGuide.guide('test_001_dhcp'))
suite.addTest(ConfigGuide.guide('test_002_static'))
suite.addTest(ConfigGuide.guide('test_003_pppoe'))
#系统状态
suite.addTest(SysMonitor_001_sysStatic.sysStatic('test_001_Modelcorrelation'))
suite.addTest(SysMonitor_001_sysStatic.sysStatic('test_001_AppFlowRanking'))
suite.addTest(SysMonitor_001_sysStatic.sysStatic('test_002_UserFlowRanking'))
ipsecP = getParameter('ipsecP')
Support = getExcelValue(ipsecP)
L2tpP = getParameter('L2tpP')
pptpP = getParameter('pptpP')
SupportL = getExcelValue(L2tpP)
SupportP = getExcelValue(pptpP)
if Support == '√' or SupportP == '√':
    suite.addTest(SysMonitor_001_sysStatic.sysStatic('test_003_VPNStatus'))

#外网配置单线路
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_001_dhcp'))
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_002_static'))
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_003_pppoe'))

#DDNS
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_001_SupportFiveDDNS'))
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_002_uttcare'))
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_003_3322_oray'))
#静态映射
suite.addTest(PortMapping_002_staticMap.staticMapping('test_001_tcp80'))
suite.addTest(PortMapping_002_staticMap.staticMapping('test_002_tcp21'))
suite.addTest(PortMapping_002_staticMap.staticMapping('test_003_udp69'))
#web认证 本地
suite.addTest(Members_007_WebAuth.webAuth('test_001_openWebAuth'))
suite.addTest(Members_007_WebAuth.webAuth('test_002_webAuthTest'))
suite.addTest(Members_007_WebAuth.webAuth('test_003_closeWebAuth'))
#web认证免认证 本地 +组织架构
suite.addTest(Members_008_FreeAuth.FreeAuth('test_001_FreeAuthgroup'))
suite.addTest(Members_008_FreeAuth.FreeAuth('test_002_FreeAuthIP'))
suite.addTest(Members_008_FreeAuth.FreeAuth('test_003_FreeAuthAll'))
#web认证 远程+组织架构
suite.addTest(Members_010_remoteAuth.remoteAuth('test_001_openRemoteAuth'))
suite.addTest(Members_010_remoteAuth.remoteAuth('test_002_remoteAuth_FreeAuth'))
suite.addTest(Members_010_remoteAuth.remoteAuth('test_003_closeRemoteAuth'))
#PPPoE服务器
pppoeSp = getParameter('pppoeSp')
SupportP = getExcelValue(pppoeSp)
if SupportP != '×':
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_001_openPPPoEAuth_addAcc'))
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_002_userstatus'))
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_003_AuthNotice'))
#电子通告
suite.addTest(actionManage_005_ElectronicsNotice.ElectronicsNotice('test_ElectronicsNotice'))
#远程管理
suite.addTest(sysConfig_002_RemoteManagement.RemoteManagement('test_001_openRemote'))
suite.addTest(sysConfig_002_RemoteManagement.RemoteManagement('test_002_CloseRemote'))
#策略库升级
AppUpgradeP = getParameter('AppUpgradeP')
Support = getExcelValue(AppUpgradeP)
if Support == '√':
    suite.addTest(sysConfig_007_policylibAppTemp.policylibAppTemp ('test_001_policylib'))

#低优先级
#DHCP server #DHCP &DNS代理 &验证IP/MAC绑定
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_001_ServerStatus'))
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_002_StaticList'))
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_003_dhcpPool'))
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_004_releaseIP'))
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_005_dnsProxy'))
suite.addTest(NetworkConfig_003_DHCPserver.dhcpServer('test_006_binding'))

#VPN
ipsecP = getParameter('ipsecP')
Support = getExcelValue(ipsecP)
if Support == '√':
    suite.addTest(VPNconfig_001_ipsec.ipsec('test_001_ipsec'))
L2tpP = getParameter('L2tpP')
pptpP = getParameter('pptpP')
SupportL = getExcelValue(L2tpP)
SupportP = getExcelValue(pptpP)
if SupportL == '√' and SupportP == '√':
    suite.addTest(VPNconfig_002_PPTPL2TP.PPTPL2TP('test_001_PPTPserver'))
    suite.addTest(VPNconfig_002_PPTPL2TP.PPTPL2TP('test_002_PPTPclient'))
    suite.addTest(VPNconfig_002_PPTPL2TP.PPTPL2TP('test_003_L2tpserver'))
    suite.addTest(VPNconfig_002_PPTPL2TP.PPTPL2TP('test_004_L2tpclient'))

#网络共享
netShareP = getParameter('netShareP')
Support = getExcelValue(netShareP)
if Support == '√':
    suite.addTest(NetworkSharing_001_UdiskMount.UdiskMount('test_001_Mount'))
    suite.addTest(NetworkSharing_002_AccountSettings.AccountSettings('test_001_AccountSettings'))
    suite.addTest(NetworkSharing_002_AccountSettings.AccountSettings('test_002_systemAccount'))
    suite.addTest(NetworkSharing_002_AccountSettings.AccountSettings('test_003_otherAccount'))
    suite.addTest(NetworkSharing_002_AccountSettings.AccountSettings('test_004_delAccount'))
    suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_001_ftpServer'))
    suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_002_ftpPort'))
    if CPUmodel != 'P1010':
        suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_003_samba'))
    suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_004_WanAcessFTP'))
    if CPUmodel != 'P1010':
        suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_005_WanAcessSmaba'))
    suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_006_passwdAcessFTP'))
    if CPUmodel != 'P1010':
        suite.addTest(NetworkSharing_003_ftpServerSmaba.ftpServerSmaba('test_007_passwdAcessSAMBA'))
    suite.addTest(NetworkSharing_001_UdiskMount.UdiskMount('test_002_unMount')) #最后弹出

#无线路由器无线配置
wifiload2Gp = getParameter('wifiload2Gp')
support = getExcelValue(wifiload2Gp)
wifiload5Gp = getParameter('wifiload5Gp')
support5 = getExcelValue(wifiload5Gp)
if support != '--':
    suite.addTest(WIFIconfig_001_configGuide.guide('test_ConfigGuide'))
    suite.addTest(WIFIconfig_002_BasicSet.BasicSet('test_001_wifi2'))
    if support5 != '--':
        suite.addTest(WIFIconfig_002_BasicSet.BasicSet('test_002_wifi5'))
    suite.addTest(WIFIconfig_003_RFConfig.RFConfig('test_001_RFConfig2'))
    if support5 != '--':
        suite.addTest(WIFIconfig_003_RFConfig.RFConfig('test_002_RFConfig5'))

#部分AC 功能
APnumP = getParameter('APnumP')
Support = getExcelValue(APnumP)
if str(Support).isdigit(): #判断字符串是否为数字
    suite.addTest(AC_001_ExpansionSwitch.ExpansionSwitch('test_001_information'))
    suite.addTest(AC_001_ExpansionSwitch.ExpansionSwitch('test_002_ExpansionSW'))
    suite.addTest(AC_001_ExpansionSwitch.ExpansionSwitch('test_003_ProtocolSW'))
    suite.addTest(AC_003_netName.netName('test_001_ssidNum'))
    suite.addTest(AC_003_netName.netName('test_002_editDelSSID'))
    suite.addTest(AC_003_netName.netName('test_003_AutoSend'))
    suite.addTest(AC_003_netName.netName('test_004_hairDown'))
    suite.addTest(AC_004_Rftemplate.Rftemplate('test_001_maxNumTemplate'))
    suite.addTest(AC_004_Rftemplate.Rftemplate('test_002_delete'))
    suite.addTest(AC_004_Rftemplate.Rftemplate('test_003_interface'))
    suite.addTest(AC_004_Rftemplate.Rftemplate('test_004_wifiMode'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_001_APlist'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_002_sendTemplateSSID'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_004_rebootAlone'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_005_rebootBatch'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_006_resertAP'))
    suite.addTest(AC_007_configlist.Configlist('test_000_makeconfig'))
    suite.addTest(AC_007_configlist.Configlist('test_001_configlist'))
    suite.addTest(AC_007_configlist.Configlist('test_002_configOperation'))
    suite.addTest(AC_007_configlist.Configlist('test_003_rebootAC'))
    suite.addTest(AC_006_APSoftware.APSoftware('test_001_ManualUpgrade'))
    suite.addTest(AC_006_APSoftware.APSoftware('test_002_autoUpodate'))


#

if __name__=='__main__':
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    SoftVersion1 = getweb('SoftVersion1')

    path_png = os.path.dirname(os.path.abspath('.')) + '/picture/'
    sys.path.append(r'%s' % path_png)
    files_gz = os.listdir(r'%s' % path_png)
    for filename_gz in files_gz:
        portion_gz = os.path.splitext(filename_gz)
        if SoftVersion1 in portion_gz[0]:
            if portion_gz[1] == '.png':
                filenamedir_gz = (r'%s' % path_png) + filename_gz
                os.remove(filenamedir_gz)

    filename = os.path.dirname(os.path.abspath('.')) + '/report/report_' + SoftVersion1 + '版本' + now + '产品型号测试_result.html'

    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'%s版本产品型号测试报告' % SoftVersion1,
        description=u'用例执行情况：')

    # runner = unittest.TextTestRunner() #不需要report则取消其他该项，启用该项
    runner.run(suite)
    fp.close()
    #发送测试报告的邮件
    p=sendMail()
    p.test_send_mail(filename)