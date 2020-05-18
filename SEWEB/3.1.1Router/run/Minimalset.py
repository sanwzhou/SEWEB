#-*- coding:utf-8 -*-
#@Time:2018/9/11 14：01
#@swzhou
'''
运行所有用例,周小集测试
'''

import os
from common.ParametersFile import delParametersFile
from common.ParametersFile import GetParameters
delParametersFile()
GetParameters() #生成参数文件
import time
import HTMLTestRunner
import unittest
import sys
from common.ReadConfig import getweb,getParameter
from common.GetExcelValue import getExcelValue
from common.GetRouteCPU import getCPUmodel
from common.GetWanNum import getWanNum
# from common.ParametersFileU import parametersFile

from test_case import ConfigGuide
from test_case import NetworkConfig_001_1WAN
from test_case import NetworkConfig_001_2WAN
from test_case import NetworkConfig_001_3WAN
from test_case import NetworkConfig_001_4WAN
from test_case import NetworkConfig_001_5WAN
from test_case import NetworkConfig_002_PlugAndPlay
from test_case import NetworkConfig_002_PortRate
from test_case import NetworkConfig_002_FastForward
from test_case import Members_001_Groups
from test_case import Members_002_members
from test_case import Members_003_binding
from test_case import Members_004_userStatus
from test_case import Members_005_blacklist
from test_case import Members_006_PPPoEAuth
from test_case import Members_007_WebAuth
from test_case import Members_008_FreeAuth
from test_case import Members_009_AuthNumber
from test_case import Members_010_remoteAuth
from test_case import NetworkConfig_003_DHCPserver
from test_case import PortMapping_001_UPNP
from test_case import PortMapping_002_staticMap
from test_case import PortMapping_003_natRule
from test_case import PortMapping_004_DMZ
from test_case import NetworkConfig_005_StaticRoute
from test_case import NetworkConfig_006_DDNSconfig
from test_case import Firewall_001_IPFilter
from test_case import Firewall_002_URLFilter
from test_case import Firewall_003_Keywordfilter
from test_case import Firewall_004_DNSfilter
from test_case import actionManage_003_actionManage
from test_case import actionManage_005_ElectronicsNotice
from test_case import actionManage_007_DomainFilter
from test_case import sysConfig_000_Getready
from test_case import sysConfig_001_administrator
from test_case import sysConfig_002_RemoteManagement
from test_case import sysConfig_003_AccessPolicy
from test_case import sysConfig_004_LanAccessControl
from test_case import sysConfig_005_Language
from test_case import sysConfig_006_softwareUpdata
from test_case import sysConfig_007_policylibAppTemp
from test_case import sysConfig_008_configuration
from test_case import sysConfig_009_Reboot
from test_case import sysConfig_010_syslogServer
from test_case import AdditionalTest
from test_case import NetworkSharing_001_UdiskMount
from test_case import NetworkSharing_002_AccountSettings
from test_case import NetworkSharing_003_ftpServerSmaba
from test_case import AC_001_ExpansionSwitch
from test_case import AC_002_APmanagement
from test_case import AC_003_netName
from test_case import AC_004_Rftemplate
from test_case import AC_005_loadBalancing
from test_case import AC_006_APSoftware
from test_case import AC_007_configlist
from test_case import VPNconfig_001_ipsec
from test_case import VPNconfig_002_PPTPL2TP
from test_case import WIFIconfig_001_configGuide
from test_case import WIFIconfig_002_BasicSet
from test_case import WIFIconfig_003_RFConfig
from test_case import SysMonitor_001_sysStatic

from common.send_mail import sendMail
from common.swconfig import swconfig
from common.initTestPC import initTestPC

CPUmodel = getCPUmodel()
WanNum = getWanNum()

os.system('D:\python\SEWEB\\3.1.1Router\\run\测试环境确认.vbs')

#手动添加用例
suite = unittest.TestSuite()

#初始化交换机/恢复出厂路由器
suite.addTest(swconfig('test_initSwPort'))
suite.addTest(initTestPC('test_initTestPC'))
suite.addTest(sysConfig_000_Getready.Getready('test_resertFirstLogin'))
suite.addTest(sysConfig_000_Getready.Getready('test_001_ntpClockServer'))
# 系统管理 （先测试006 升级 再测试008 配置备份恢复 然后其他）
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
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_000_getReady'))
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_001_dhcp'))
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_002_static'))
suite.addTest(NetworkConfig_001_1WAN.Config_WAN('test_003_pppoe'))
portTateWANp = getExcelValue('portTateWANp')

if int(WanNum) >= 2:
    #双线路
    # 测试多线路时候需注意
    # 1、恢复出厂后将除wan1之外的其余wan口都删除掉 再从少到多测(单线路脚本中已设置)
    # 2、注意wan口数量更改环境下 前面的引用恢复出厂会使wan口回到初始状态
    # 3、初始化交换机vlan需要配置交换机使用 test_000_getReady、test_005_initSwPort
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_000_getReady'))
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_001_static'))
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_002_backupLineSW'))
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_003_static_PPPoE'))
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_004_PPPoEsw'))
    suite.addTest(NetworkConfig_001_2WAN.Config_2WAN('test_005_initSwPort'))
if int(WanNum) >= 3:
    #三线路
    suite.addTest(NetworkConfig_001_3WAN.Config_3WAN('test_000_getReady'))
    suite.addTest(NetworkConfig_001_3WAN.Config_3WAN('test_001_static'))
    suite.addTest(NetworkConfig_001_3WAN.Config_3WAN('test_002_staticSW'))
    suite.addTest(NetworkConfig_001_3WAN.Config_3WAN('test_003_3PPPoE'))
    suite.addTest(NetworkConfig_001_3WAN.Config_3WAN('test_004_initSwPort'))
if int(WanNum) >= 4:
    #四线路
    suite.addTest(NetworkConfig_001_4WAN.Config_4WAN('test_000_getReady'))
    suite.addTest(NetworkConfig_001_4WAN.Config_4WAN('test_001_static'))
    suite.addTest(NetworkConfig_001_4WAN.Config_4WAN('test_002_staticSW'))
    suite.addTest(NetworkConfig_001_4WAN.Config_4WAN('test_003_4PPPoE'))
    suite.addTest(NetworkConfig_001_4WAN.Config_4WAN('test_004_initSwPort'))
if int(WanNum) >= 5:
    #五线路
    suite.addTest(NetworkConfig_001_5WAN.Config_5WAN('test_000_getReady'))
    suite.addTest(NetworkConfig_001_5WAN.Config_5WAN('test_001_static'))
    suite.addTest(NetworkConfig_001_5WAN.Config_5WAN('test_002_staticSW'))
    suite.addTest(NetworkConfig_001_5WAN.Config_5WAN('test_003_5PPPoE'))
    suite.addTest(NetworkConfig_001_5WAN.Config_5WAN('test_004_initSwPort'))

suite.addTest(sysConfig_000_Getready.Getready('test_resertFirstLogin')) #确保修改过wan口数量的设备，回到出厂状态
#端口速率修改
suite.addTest(NetworkConfig_002_PortRate.PortRate('test_001_changeRateWAN'))
suite.addTest(NetworkConfig_002_PortRate.PortRate('test_002_changeRateLAN'))
#快速转发 硬件/软件
Support = getExcelValue(getParameter('hwNatP'))
if Support == '√':
    suite.addTest(NetworkConfig_002_FastForward.PortRate('test_001_hwNat'))
Support = getExcelValue(getParameter('sfnatP'))
if Support == '√':
    suite.addTest(NetworkConfig_002_FastForward.PortRate('test_002_sfNat'))
#DDNS
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_001_SupportFiveDDNS'))
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_002_uttcare'))
suite.addTest(NetworkConfig_006_DDNSconfig.DDNS('test_003_3322_oray'))

#端口映射
suite.addTest(PortMapping_001_UPNP.UPNP('test_UPNP'))
suite.addTest(PortMapping_002_staticMap.staticMapping('test_001_tcp80'))
suite.addTest(PortMapping_002_staticMap.staticMapping('test_002_tcp21'))
suite.addTest(PortMapping_002_staticMap.staticMapping('test_003_udp69'))
suite.addTest(PortMapping_003_natRule.natRule('test_001_easyIP'))
suite.addTest(PortMapping_003_natRule.natRule('test_002_one2one'))
suite.addTest(PortMapping_004_DMZ.DMZ('test_001_server3389'))
suite.addTest(PortMapping_004_DMZ.DMZ('test_002_localDMZ'))
suite.addTest(PortMapping_004_DMZ.DMZ('test_003_GlobalDMZ'))
suite.addTest(PortMapping_004_DMZ.DMZ('test_004_DMZpriority'))
#静态路由
suite.addTest(NetworkConfig_005_StaticRoute.staticRoute('test_001_staticRouting'))
suite.addTest(NetworkConfig_005_StaticRoute.staticRoute('test_002_bindingVPNinterface'))
#系统管理
suite.addTest(sysConfig_008_configuration.configuration('test_001_configbackup'))
suite.addTest(sysConfig_008_configuration.configuration('test_002_Resert'))
suite.addTest(sysConfig_008_configuration.configuration('test_003_configIpmort'))
suite.addTest(sysConfig_001_administrator.administrator('test_001_test1'))
suite.addTest(sysConfig_001_administrator.administrator('test_002_test2'))
suite.addTest(sysConfig_001_administrator.administrator('test_003_test3'))
suite.addTest(sysConfig_001_administrator.administrator('test_004_test4'))
suite.addTest(sysConfig_002_RemoteManagement.RemoteManagement('test_001_openRemote'))
suite.addTest(sysConfig_002_RemoteManagement.RemoteManagement('test_002_CloseRemote'))
suite.addTest(sysConfig_003_AccessPolicy.AccessPolicy('test_001_AccessMode'))
suite.addTest(sysConfig_003_AccessPolicy.AccessPolicy('test_002_passwdErrNum'))
suite.addTest(sysConfig_003_AccessPolicy.AccessPolicy('test_003_WEBtimeout'))
suite.addTest(sysConfig_004_LanAccessControl.LanAccessControl('test_001_userall'))
suite.addTest(sysConfig_004_LanAccessControl.LanAccessControl('test_002_usergroup'))
suite.addTest(sysConfig_004_LanAccessControl.LanAccessControl('test_003_userip'))
suite.addTest(sysConfig_005_Language.Language('test_001_language'))
AppUpgradeP = getParameter('AppUpgradeP')
Support = getExcelValue(AppUpgradeP)
if Support == '√':
    suite.addTest(sysConfig_007_policylibAppTemp.policylibAppTemp ('test_001_policylib'))
suite.addTest(sysConfig_007_policylibAppTemp.policylibAppTemp ('test_002_AppPriority'))
suite.addTest(sysConfig_009_Reboot.Reboot('test_reboot1'))
suite.addTest(sysConfig_009_Reboot.Reboot('test_reboot2'))
suite.addTest(sysConfig_010_syslogServer.syslogServer('test_syslog'))

#用户管理
suite.addTest(Members_001_Groups.MembersGroups('test_001_groupAdd'))
suite.addTest(Members_001_Groups.MembersGroups('test_002_groupEdit'))
suite.addTest(Members_001_Groups.MembersGroups('test_003_groupDelete'))
suite.addTest(Members_001_Groups.MembersGroups('test_004_group_importMAXgroup'))
suite.addTest(Members_001_Groups.MembersGroups('test_005_import_emptyTemplate'))
suite.addTest(Members_002_members.Members('test_001_add_user'))
suite.addTest(Members_002_members.Members('test_002_operation_member'))
suite.addTest(Members_002_members.Members('test_003_import_export'))
suite.addTest(Members_003_binding.onlyBinding('test_001_IPMACBinding'))
suite.addTest(Members_003_binding.onlyBinding('test_002_MAC_binding'))
suite.addTest(Members_004_userStatus.userStatus('test_001_userList'))
suite.addTest(Members_004_userStatus.userStatus('test_002_MovetoOther'))
suite.addTest(Members_004_userStatus.userStatus('test_003_movetoBlicklist'))
suite.addTest(Members_005_blacklist.blacklist('test_blacklist'))
pppoeSp = getParameter('pppoeSp')
SupportP = getExcelValue(pppoeSp)
if SupportP != '×':
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_001_openPPPoEAuth_addAcc'))
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_002_userstatus'))
    suite.addTest(Members_006_PPPoEAuth.pppoeAuth('test_003_AuthNotice'))
suite.addTest(Members_007_WebAuth.webAuth('test_001_openWebAuth'))
suite.addTest(Members_007_WebAuth.webAuth('test_002_webAuthTest'))
suite.addTest(Members_007_WebAuth.webAuth('test_003_closeWebAuth'))
suite.addTest(Members_008_FreeAuth.FreeAuth('test_001_FreeAuthgroup'))
suite.addTest(Members_008_FreeAuth.FreeAuth('test_002_FreeAuthIP'))
suite.addTest(Members_008_FreeAuth.FreeAuth('test_003_FreeAuthAll'))
suite.addTest(Members_009_AuthNumber.AuthNumber('test_001_addWebAccNumber'))
if SupportP != '×':
    suite.addTest(Members_009_AuthNumber.AuthNumber('test_002_addpppoeAccNumber'))
suite.addTest(Members_009_AuthNumber.AuthNumber('test_003_delAccNumber'))
suite.addTest(Members_010_remoteAuth.remoteAuth('test_001_openRemoteAuth'))
suite.addTest(Members_010_remoteAuth.remoteAuth('test_002_remoteAuth_FreeAuth'))
suite.addTest(Members_010_remoteAuth.remoteAuth('test_003_closeRemoteAuth'))

#行为管理
#003爱奇艺过滤
suite.addTest(actionManage_003_actionManage.iqiyiFilter('test_iqiyiFilter'))
#005电子通告
suite.addTest(actionManage_005_ElectronicsNotice.ElectronicsNotice('test_ElectronicsNotice'))
#007域名过滤
suite.addTest(actionManage_007_DomainFilter.DomainFilter('test_001_Forbidfilter_Notice'))
suite.addTest(actionManage_007_DomainFilter.DomainFilter('test_002_allowfilter_Notice'))

#防火墙
suite.addTest(Firewall_001_IPFilter.IPfilter('test_IPfilter'))
suite.addTest(Firewall_002_URLFilter.URLFilter('test_URLFilter'))
suite.addTest(Firewall_003_Keywordfilter.Keywordfilter('test_Keywordfilter'))
suite.addTest(Firewall_004_DNSfilter.DNSfilter('test_DNSfilter'))

#即插即用
suite.addTest(NetworkConfig_002_PlugAndPlay.plug_and_play('test_001_open'))
suite.addTest(NetworkConfig_002_PlugAndPlay.plug_and_play('test_002_close'))

#DHCP server
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
#
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

# AP管理
APnumP = getParameter('APnumP')
Support = getExcelValue(APnumP)
print(Support)
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
    suite.addTest(AC_005_loadBalancing.loadBalancing('test_001_open'))
    suite.addTest(AC_005_loadBalancing.loadBalancing('test_002_close'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_001_APlist'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_002_sendTemplateSSID'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_003_taskPlan_SleepMode'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_004_rebootAlone'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_005_rebootBatch'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_006_resertAP'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_007_APinVlan'))
    suite.addTest(AC_002_APmanagement.APmanagement('test_008_APinvlan2'))
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

    filename = os.path.dirname(os.path.abspath('.')) + '/report/report_' + SoftVersion1 + '版本' + now + '周小集测试_result.html'

    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'%s版本最小集测试报告' % SoftVersion1,
        description=u'用例执行情况：')

    # runner = unittest.TextTestRunner() #不需要report则取消其他该项，启用该项
    runner.run(suite)
    fp.close()

    #发送测试报告的邮件
    p=sendMail()
    p.test_send_mail(filename)
