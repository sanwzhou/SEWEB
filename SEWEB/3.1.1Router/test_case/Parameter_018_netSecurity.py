#! -*-conding:utf-8 -*-
#@Time: 2019/2/15 0015 16:18
#@swzhou
'''
攻击防御、访问控制策略、连接数限制
'''


import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText
from pages.Firewall_003_AttackPreventionPage import AttackPreventionPage
from pages.Firewall_001_ACLPage import AccessControlPage
from pages.Firewall_002_SessionControlPage import SessionControlPage
from pages.sysObj_timePlanPage import timePlanPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_018_netSecurity').getlog()

class networkSecurity(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        firewall = AttackPreventionPage(self.driver,self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        # pass

    def test_001_AttackPrevention(self):
        u'''攻击防范'''
        firewall = AttackPreventionPage(self.driver, self.url)
        firewall.click_AttackPrevention()
        time.sleep(1)

        #ARP欺骗主动防御
        ArpBroadcastIntervalVal=str(firewall.getAttribute_byName(firewall.ArpBroadcastIntervalVal,'value'))
        self.assertEqual(ArpBroadcastIntervalVal,'100',msg='arp默认广播间隔不为100毫秒')
        ArpBroadcastIntervalValsw = str(firewall.getAttribute_byName(firewall.ArpBroadcastIntervalVals,'checked'))
        self.assertEqual(ArpBroadcastIntervalValsw, 'None', msg='ARP欺骗主动防御 默认未关闭')
        firewall.click_ArpBroadcastIntervalValEn()
        # FLOOD攻击防御 UDP
        UDPFlood = str(firewall.getAttribute_byName(firewall.UDPFlood,'value'))
        self.assertEqual(UDPFlood, '500', msg='UDP FLOOD防御 默认阈值不为500个/秒')
        UDPFloodsw = str(firewall.getAttribute_byName(firewall.UDPFloods,'checked'))
        self.assertEqual(UDPFloodsw, 'None', msg='UDP FLOOD防御 默认未关闭')
        firewall.click_UDPFloodEn()
        # FLOOD攻击防御 ICMP
        ICMPFlood = str(firewall.getAttribute_byName(firewall.ICMPFlood,'value'))
        self.assertEqual(ICMPFlood, '500', msg='ICMP FLOOD防御 默认阈值不为500个/秒')
        ICMPFloodsw = str(firewall.getAttribute_byName(firewall.ICMPFloods,'checked'))
        self.assertEqual(ICMPFloodsw, 'None', msg='ICMP FLOOD防御 默认未关闭')
        firewall.click_ICMPFloodEn()
        # FLOOD攻击防御 SYN
        SYNFlood = str(firewall.getAttribute_byName(firewall.SYNFlood,'value'))
        self.assertEqual(SYNFlood, '500', msg='SYN FLOOD防御 默认阈值不为500个/秒')
        SYNFloodsw = str(firewall.getAttribute_byName(firewall.SYNFloods,'checked'))
        self.assertEqual(SYNFloodsw, 'None', msg='SYN FLOOD防御 默认未关闭')
        firewall.click_SYNFloodEn()
        # IP欺骗防御
        IPCheatsw = str(firewall.getAttribute_byName(firewall.IPCheats,'checked'))
        self.assertEqual(IPCheatsw, 'None', msg='IP欺骗防御 默认未关闭')
        firewall.click_IPCheateEn()
        # DDoS攻击防御
        DDOSEnablesw = str(firewall.getAttribute_byName(firewall.DDOSEnables,'checked'))
        self.assertEqual(DDOSEnablesw, 'None', msg='DDoS攻击防御 默认未关闭')
        firewall.click_DDOSEnableEn()
        # 外网PING防御
        PingDisablesw = str(firewall.getAttribute_byName(firewall.PingDisables,'checked'))
        self.assertEqual(PingDisablesw, 'None', msg='外网PING防御 默认未关闭')
        firewall.click_PingDisableEn()

        self.driver.quit()
        logger.info('test_001_AttackPrevention passed')

    def test_002_filter(self):
        u'''ACL防火墙'''
        nodata = getAssertText('nodata')
        #创建时间计划 为当天
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        timePlan.click_add()
        time.sleep(1)
        timePlan.input_TimeRangeName('TimePlan')
        timePlan.click_save()
        time.sleep(1)
        list_name = str(timePlan.getText_byXpath(timePlan.listName))
        time.sleep(1)
        self.assertEqual(list_name, 'TimePlan', msg='时间段名 与配置的不一致')
        print('时间计划已添加')

        # 配置防火墙
        #新建一条IP过滤
        firewall = AccessControlPage(self.driver, self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        firewall.click_add()
        time.sleep(1)
        firewall.input_PolicyNames('IPfilter')
        firewall.click_sourceIP()
        time.sleep(1)
        firewall.click_usergroup()
        time.sleep(0.5)
        firewall.click_userip()
        time.sleep(0.5)
        firewall.click_userall()
        time.sleep(0.5)
        firewall.click_saveW1()# 弹窗中的保存
        time.sleep(1)
        seltime = firewall.selelement_byName('timeGrpName')
        time.sleep(1)
        Select(seltime).select_by_value('TimePlan')
        time.sleep(0.5)
        selFilterTypes = firewall.selelement_byName(firewall.selFilterTypes)
        Select(selFilterTypes).select_by_value('1')  # ip过滤
        time.sleep(0.5)
        selProtocol = firewall.selelement_byName(firewall.selProtocol)
        Select(selProtocol).select_by_value('4') #4 AH
        time.sleep(0.3)
        Select(selProtocol).select_by_value('5') #all
        time.sleep(0.3)
        Select(selProtocol).select_by_value('1') #ICMP
        time.sleep(0.3)
        Select(selProtocol).select_by_value('2') #TCP
        time.sleep(0.3)
        Select(selProtocol).select_by_value('3') #UDP
        time.sleep(0.5)
        selservice = firewall.selelement_byName('cyfw')
        Select(selservice).select_by_value('137')
        time.sleep(0.5)
        firewall.click_save()
        time.sleep(1)
        #新建一条URL
        firewall.click_add()
        time.sleep(1)
        firewall.input_PolicyNames('URLfilter')
        firewall.click_sourceIP()
        time.sleep(1)
        firewall.click_usergroup()
        time.sleep(0.5)
        firewall.click_userip()
        time.sleep(0.5)
        firewall.click_userall()
        time.sleep(0.5)
        firewall.click_saveW1()  # 弹窗中的保存
        time.sleep(1)
        seltime = firewall.selelement_byName('timeGrpName')
        Select(seltime).select_by_value('TimePlan')
        time.sleep(0.5)
        selFilterTypes = firewall.selelement_byName(firewall.selFilterTypes)
        Select(selFilterTypes).select_by_value('4')  # DNS过滤
        time.sleep(1)
        Select(selFilterTypes).select_by_value('3')  # 关键字过滤
        time.sleep(1)
        Select(selFilterTypes).select_by_value('2')  # URL过滤
        time.sleep(1)
        firewall.input_glnrUrl('www.123.com')
        time.sleep(1)
        firewall.click_save()
        time.sleep(1)
        print('访问控制策略 已添加')
        # 开/关访问控制
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS, 'checktype')  # checktype 0未开启，1开启
        self.assertEqual(checkTrafficS,'0',msg='访问控制 默认未关闭')
        if checkTrafficS == '0':
            firewall.click_checkTraffic()
            time.sleep(2)
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS, 'checktype')
        self.assertEqual(checkTrafficS, '1', msg='访问控制 开启失败')
        if checkTrafficS == '1':
            firewall.click_checkTraffic()
            time.sleep(3)
        checkTrafficS = firewall.getAttribute_byId(firewall.checkTrafficS, 'checktype')
        self.assertEqual(checkTrafficS, '0', msg='访问控制 关闭失败')
        #测试移动策略
        list1_name = str(firewall.getText_byXpath(firewall.list1_name))
        self.assertEqual(list1_name,'IPfilter',msg='访问控制列表 顺序1不为 IPfilter')
        selmoveto_1 = firewall.selelement_byID(firewall.u_moveto_1)
        Select(selmoveto_1).select_by_value('URLfilter')
        time.sleep(0.5)
        firewall.click_movetosave()
        time.sleep(1)
        i = 0
        while i < 30:
            firewall.click_AccessControl()
            time.sleep(1)
            list1_name = str(firewall.getText_byXpath(firewall.list1_name))
            if list1_name == 'URLfilter':
                print('访问控制列表 移动验证通过')
                break
            else:
                time.sleep(1)
                i += 1
        else:
            raise Exception(u'访问控制列表 移动出错')

        #删除
        firewall.click_selall()
        time.sleep(0.5)
        firewall.click_delall()
        time.sleep(1)
        firewall.click_ok()
        time.sleep(1)
        listnodata = str(firewall.getText_byXpath(firewall.listnodata))
        self.assertEqual(listnodata, nodata, msg='策略删除失败')
        print('策略已删除')
        # 删除时间计划
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        timePlan.click_delete()
        time.sleep(1)
        timePlan.click_ok()
        time.sleep(1)
        # 断言
        listtips2 = str(timePlan.getText_byXpath(timePlan.listnodata))
        self.assertEqual(listtips2, nodata, msg='时间计划删除失败')

        self.driver.quit()
        logger.info('test_002_filter passed')

    def test_003_Connection(self):
        u'''连接数限制'''
        firell = SessionControlPage(self.driver,self.url)
        firell.click_SessionControl()
        time.sleep(1)
        swEn = firell.getAttribute_byXpath(firell.swENs,'checked')
        self.assertEqual(swEn, 'true', msg='连接控制 默认未关闭')

        totalCnt = str(firell.getAttribute_byName(firell.totalCnt,'value'))
        self.assertEqual(totalCnt, '1500', msg='总连接数 默认不为 1500')
        tcp = str(firell.getAttribute_byName(firell.tcp,'value'))
        self.assertEqual(tcp, '1000', msg='tcp连接数 默认不为 1000')
        udp = str(firell.getAttribute_byName(firell.udp,'value'))
        self.assertEqual(udp, '800', msg='udp连接数 默认不为 800')
        icmp = str(firell.getAttribute_byName(firell.icmp,'value'))
        self.assertEqual(icmp, '100', msg='icmp连接数 默认不为 100')

        self.driver.quit()

        logger.info('test_003_Connection passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

