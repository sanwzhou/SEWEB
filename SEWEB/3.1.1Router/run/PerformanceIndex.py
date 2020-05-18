#-*- coding:utf-8 -*-
#@Time:2018/6/21 13:34
#@swzhou
'''
性能指标核对
'''

import os
from common.ParametersFile import delParametersFile
from common.ParametersFile import GetParameters

import time
import HTMLTestRunner
import unittest
import sys
from common.ReadConfig import getweb
from common.swconfig import swconfig
from common.initTestPC import initTestPC
# from common.ParametersFileU import parametersFile

#根据参数表生成参数文件
delParametersFile()
GetParameters()

from test_case import Parameter_010_DefaultInfo #出厂信息（包含了恢复出厂）
from test_case import Parameter_011_ManagementStyle
from test_case import Parameter_012_SysManage
from test_case import Parameter_013_NetworkPortSet
from test_case import Parameter_014_DHCPserver
from test_case import Parameter_015_basicFunction
from test_case import Parameter_016_natRules
from test_case import Parameter_017_PolicyRoute
from test_case import Parameter_018_netSecurity
from test_case import Parameter_019_actionManagement
from test_case import Parameter_020_BandwidthManagement
from test_case import Parameter_021_switchConfig
from test_case import Parameter_022_VPNconfig
from test_case import Parameter_023_userManagement
from test_case import Parameter_024_NetworkSharing
from test_case import Parameter_025_AC
from test_case import Parameter_009_wifiConfig #无线路由器无线配置
from test_case import Parameter_100_Parameter

from common.send_mail import sendMail


#手动添加用例
suite = unittest.TestSuite()


# 初始化测试主机/交换机/恢复出厂路由器
suite.addTest(swconfig('test_initSwPort'))
suite.addTest(initTestPC('test_initTestPC'))
suite.addTest(Parameter_010_DefaultInfo.DefaultInfo('test_resertFirstLogin'))
#管理方式
suite.addTest(Parameter_011_ManagementStyle.ManagementStyle('test_001_WEB_login'))
suite.addTest(Parameter_011_ManagementStyle.ManagementStyle('test_002_admin'))
suite.addTest(Parameter_011_ManagementStyle.ManagementStyle('test_003_WEBUI'))
suite.addTest(Parameter_011_ManagementStyle.ManagementStyle('test_004_accesscontrol_Language'))
suite.addTest(Parameter_011_ManagementStyle.ManagementStyle('test_005_telnet'))
#系统管理
suite.addTest(Parameter_012_SysManage.SysManage('test_001_backup_resert'))
suite.addTest(Parameter_012_SysManage.SysManage('test_002_update'))
suite.addTest(Parameter_012_SysManage.SysManage('test_003_AppLibrary'))
suite.addTest(Parameter_012_SysManage.SysManage('test_004_syslog'))
suite.addTest(Parameter_012_SysManage.SysManage('test_005_ClockServer'))
suite.addTest(Parameter_012_SysManage.SysManage('test_006_RemoteManagement'))
suite.addTest(Parameter_012_SysManage.SysManage('test_007_RemotePlannedTask'))
suite.addTest(Parameter_012_SysManage.SysManage('test_008_license'))
suite.addTest(Parameter_012_SysManage.SysManage('test_009_DiagnosticTest'))
#网口设置
suite.addTest(Parameter_013_NetworkPortSet.NetworkPortSet('test_001_portRateWAN'))
suite.addTest(Parameter_013_NetworkPortSet.NetworkPortSet('test_002_portRateLAN'))
suite.addTest(Parameter_013_NetworkPortSet.NetworkPortSet('test_003_LanMultiIP'))
suite.addTest(Parameter_013_NetworkPortSet.NetworkPortSet('test_004_changeMAC'))
# DHCP服务器
suite.addTest(Parameter_014_DHCPserver.DHCPserver('test_001_AllocationAddress'))
suite.addTest(Parameter_014_DHCPserver.DHCPserver('test_002_option43_MultiPools'))
#基本功能
suite.addTest(Parameter_015_basicFunction.basicFunction('test_001_wanParameters'))
suite.addTest(Parameter_015_basicFunction.basicFunction('test_002_DNSProxy'))
suite.addTest(Parameter_015_basicFunction.basicFunction('test_003_NetSniper'))
suite.addTest(Parameter_015_basicFunction.basicFunction('test_004_FiveDDNS'))
#转发规则
suite.addTest(Parameter_016_natRules.natRules('test_001_staticMapping'))
suite.addTest(Parameter_016_natRules.natRules('test_002_easyIP_one2one'))
suite.addTest(Parameter_016_natRules.natRules('test_003_DMZ_UPNP'))
#策略路由
suite.addTest(Parameter_017_PolicyRoute.PolicyRoute('test_001_line'))
suite.addTest(Parameter_017_PolicyRoute.PolicyRoute('test_002_PolicyRoute'))
suite.addTest(Parameter_017_PolicyRoute.PolicyRoute('test_003_bandingInter'))
#网络安全
suite.addTest(Parameter_018_netSecurity.networkSecurity('test_001_AttackPrevention'))
suite.addTest(Parameter_018_netSecurity.networkSecurity('test_002_filter'))
suite.addTest(Parameter_018_netSecurity.networkSecurity('test_003_Connection'))
#上网行为管理
suite.addTest(Parameter_019_actionManagement.actionManagement('test_001_SystemObject'))
suite.addTest(Parameter_019_actionManagement.actionManagement('test_002_actionManage'))
suite.addTest(Parameter_019_actionManagement.actionManagement('test_003_DomainFiltering'))
suite.addTest(Parameter_019_actionManagement.actionManagement('test_004_ElectronicsNotice'))
#带宽管理
suite.addTest(Parameter_020_BandwidthManagement.BandwidthManagement('test_001_appTemplate'))
suite.addTest(Parameter_020_BandwidthManagement.BandwidthManagement('test_002_BWManagement'))
suite.addTest(Parameter_020_BandwidthManagement.BandwidthManagement('test_003_Statistics'))
suite.addTest(Parameter_020_BandwidthManagement.BandwidthManagement('test_004_Fastforward'))
#交换管理
suite.addTest(Parameter_021_switchConfig.switchConfig('test_001_vlanInterface'))
suite.addTest(Parameter_021_switchConfig.switchConfig('test_002_PortMirror'))
suite.addTest(Parameter_021_switchConfig.switchConfig('test_003_PortVLAN'))
#VPN
suite.addTest(Parameter_022_VPNconfig.VPNconfig('test_001_pptpL2tp'))
suite.addTest(Parameter_022_VPNconfig.VPNconfig('test_002_IPsec'))
suite.addTest(Parameter_022_VPNconfig.VPNconfig('test_003_IPSec_binding_pptp'))
#用户管理
suite.addTest(Parameter_023_userManagement.userManagement('test_001_UserStatistics'))
suite.addTest(Parameter_023_userManagement.userManagement('test_002_binding'))
suite.addTest(Parameter_023_userManagement.userManagement('test_003_PPPoESever'))
suite.addTest(Parameter_023_userManagement.userManagement('test_004_WEBAuth'))
suite.addTest(Parameter_023_userManagement.userManagement('test_005_RemoteAuth'))
suite.addTest(Parameter_023_userManagement.userManagement('test_006_blacklist'))
#共享管理
suite.addTest(Parameter_024_NetworkSharing.NetworkSharing('test_001_NetworkSharing'))
#AP集中管理
suite.addTest(Parameter_025_AC.AC('test_002_SSIDconfig'))
suite.addTest(Parameter_025_AC.AC('test_003_Template'))
suite.addTest(Parameter_025_AC.AC('test_001_APconfig')) #v2上线信息加载时间较久，002中开启扩展，延后测试ap

#无线路由器无线配置
suite.addTest(Parameter_009_wifiConfig.WirelessParameters('test_001_wirelessMode'))
suite.addTest(Parameter_009_wifiConfig.WirelessParameters('test_002_WDSconfig'))
suite.addTest(Parameter_009_wifiConfig.WirelessParameters('test_003_WirelessSecurity'))

#参数条目数验证
suite.addTest(Parameter_100_Parameter.Parameter('test_000_configIpmort'))
suite.addTest(Parameter_100_Parameter.Parameter('test_000_deviceParameter'))
suite.addTest(Parameter_100_Parameter.Parameter('test_001_route'))
suite.addTest(Parameter_100_Parameter.Parameter('test_002_nat'))
suite.addTest(Parameter_100_Parameter.Parameter('test_003_FireWall'))
suite.addTest(Parameter_100_Parameter.Parameter('test_004_address'))
suite.addTest(Parameter_100_Parameter.Parameter('test_005_timePlan'))
suite.addTest(Parameter_100_Parameter.Parameter('test_006_actionManage'))
suite.addTest(Parameter_100_Parameter.Parameter('test_007_QQali'))
suite.addTest(Parameter_100_Parameter.Parameter('test_008_DomainFiltering'))
suite.addTest(Parameter_100_Parameter.Parameter('test_009_bandwidth'))
suite.addTest(Parameter_100_Parameter.Parameter('test_010_VPNnum'))
suite.addTest(Parameter_100_Parameter.Parameter('test_011_userNum'))
suite.addTest(Parameter_100_Parameter.Parameter('test_012_IPMACbinding'))
suite.addTest(Parameter_100_Parameter.Parameter('test_013_PPPoE'))
suite.addTest(Parameter_100_Parameter.Parameter('test_014_blacklist'))
suite.addTest(Parameter_100_Parameter.Parameter('test_015_maxAp'))
suite.addTest(Parameter_100_Parameter.Parameter('test_016_loadBalance'))
suite.addTest(Parameter_100_Parameter.Parameter('test_017_ssidNum'))


# 最后加个注释 以访报告中没有包含最后一项记录


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

    filename = os.path.dirname(
        os.path.abspath('.')) + '/report/report_' + SoftVersion1 + '版本' + now + '性能参数核对测试_result.html'

    fp = open(filename, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title=u'%s版本性能参数核对测试报告' % SoftVersion1,
        description=u'用例执行情况：')

    # runner = unittest.TextTestRunner() #不需要report则取消其他该项，启用该项
    runner.run(suite)
    fp.close()
    # 发送测试报告的邮件
    p=sendMail()
    p.test_send_mail(filename)