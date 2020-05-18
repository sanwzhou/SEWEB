#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 14:27
#@swzhou
'''
easyIP 及 one2one 验证，后台telnet确认有对应规则生成
'''

import os
import time
import unittest
import telnetlib
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb,getAssertText,getpath
from common.loginRoute import login
from pages.PortMapping_003_natRulePage import natRulePage
from pages.Organization_002_userStatuspage import Organization_userStatusPage
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'PortMapping_003_natRule').getlog()
tmppath = os.path.dirname(os.path.abspath('.')) + '/tmp/'
serverPcMac = getweb('serverPcMac')
pcNetworkID = getweb('pcNetworkID')
wiresharkpath = getpath('wiresharkpath')
ConnectState = getAssertText('ConnectState')

class natRule(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_easyIP(self):
        u'''验证 easyIP,后台telnet验证iptables规则'''

        # 通过用户状态获取httpserver的IP地址
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        status.input_search(serverPcMac)
        status.click_searchb()
        time.sleep(1)
        try:
            serverIP = status.getText_byXpath(status.list_IP1)
        except NoSuchElementException:
            raise Exception(u'用户状态中未找到server IP')
            # print(serverIP)

        # 从外网配置页面获取WAN1口地址
        wanpage = NetworkConfig_wanpage(self.driver, self.url)
        wanpage.click_NetworkConfig()
        time.sleep(0.5)
        wanpage.click_WANconfig()
        time.sleep(1)
        # WAN1 ip变量赋值，页面读取
        # 判断联网状态
        i = 0
        while i < 21:
            wanpage.click_refresh()
            time.sleep(1)
            list_conState = wanpage.getText_byXpath(wanpage.connectState1)
            print(str(list_conState), i)
            if str(list_conState) != ConnectState:
                time.sleep(3)
                i += 1
            else:
                break
        else:
            CapPic(self.driver)
            logger.info(u"WAN口未连接")
            raise Exception('WAN1 未连接')
        WAN1_ip = str(wanpage.getText_byXpath(wanpage.line1IP))
        print('WAN1_ip=',WAN1_ip)
        time.sleep(1)

        #判断IP
        serverIPadd = str(serverIP).split(r'.')[-1]
        print(serverIPadd)
        if (int(serverIPadd) - 1 > 1) and (int(serverIPadd) + 2 <= 255):
            serverIPadd_1 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) - 1)
            serverIPadd1 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) + 1)
            serverIPadd2 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) + 2)
        else:
            serverIPadd_1 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) + 1)
            serverIPadd1 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) - 2)
            serverIPadd2 = str(serverIP).split(r'.')[:-1] + str(int(serverIPadd) - 1)

        WAN1_ipadd = str(WAN1_ip).split(r'.')[-1]
        if int(WAN1_ipadd) + 1 <= 255:
            WAN1_ipadd1 = str(WAN1_ip).split(r'.')[:-1] + str(int(WAN1_ipadd) + 1)
        else:
            WAN1_ipadd1 = str(int(WAN1_ipadd) - 1)

        #新增
        natRule = natRulePage(self.driver, self.url)
        #1 包含 边界
        natRule.click_NetworkConfig()
        time.sleep(0.5)
        natRule.click_portMapping()
        time.sleep(1)
        natRule.click_natRule()
        time.sleep(1)
        natRule.click_add()
        time.sleep(1)
        natRule.input_RuleIDs('easyIPtest')
        natRule.input_InFromIPs(serverIP)
        natRule.input_InEndIPs(serverIPadd2)
        natRule.input_OutIPs(WAN1_ipadd1)
        time.sleep(1)
        natRule.click_save()
        time.sleep(1)
        #断言
        InFromIPs = str(natRule.getText_byXpath(natRule.list_InFromIPs))
        self.assertEqual(InFromIPs,serverIP, msg='内网起始IP地址 与设置的不一致')
        InEndIPs = str(natRule.getText_byXpath(natRule.list_InEndIPs))
        self.assertEqual(InEndIPs, serverIPadd2, msg='内网结束IP地址 与设置的不一致')
        OutIPs = str(natRule.getText_byXpath(natRule.list_OutIPs))
        self.assertEqual(OutIPs, WAN1_ipadd1, msg='外网起始IP地址 与设置的不一致')
        print('easyIP规则 已添加')

        # 3、调用wireshark 开启抓包，必须要抓到包之后才会进行下一步，因此放在设置vpn之后，通过抓下一次的log
        packetfile = tmppath + 'syslogtest.pcapng'
        dir = wiresharkpath[0:2]
        getpacket = ('tshark -i%s -f "icmp" -w %s -c 2' % (pcNetworkID, packetfile))
        os.system('%s && cd %s && %s' % (dir, wiresharkpath, getpacket))

        # 4、读取抓包显示 并存为log文件
        logfile = tmppath + 'syslogtest.log'
        savepacket = ('tshark -r %s -T fields -e "ip.src" -e ip.dst -Y "syslog" > %s ' % (packetfile, logfile))
        os.system('%s && cd %s && %s' % (dir, wiresharkpath, savepacket))

        # 5、读取判断syslog生效
        with open(logfile, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                print(lines)
                if not lines:
                    break
                if host + pcaddr in lines:
                    print(u'验证通过')



        # # 连接Telnet服务器
        # hostip = gettelnet('host')
        # port = gettelnet('port')
        # username = bytes(getweb('User'), encoding="utf8")
        # password = bytes(getweb('Passwd'), encoding="utf8")
        # tn = telnetlib.Telnet(host=hostip, port=port)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'iptables -t nat  -L wan1_nat_rule_loop' + b'\n')
        # # 输出结果，判断
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # #后台实际应有的结果
        # result1='SNAT       all  --  anywhere             anywhere            source IP range 192.168.1.200-192.168.1.202 to:192.169.122.250'
        # # 判断
        # if result1 in result:
        #     print('easyIP规则 验证成功')
        # else:
        #     raise Exception('easyIP规则 验证失败')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_001_easyIP passed')

    def test_002_one2one(self):
        u'''验证 one2one,后台telnet验证iptables规则'''
        nodata = getAssertText('nodata')
        #修改上一条规则
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        natRule = natRulePage(self.driver, self.url)
        # 配置映射
        natRule.click_NetworkConfig()
        time.sleep(0.5)
        natRule.click_portMapping()
        time.sleep(1)
        natRule.click_natRule()
        time.sleep(1)
        natRule.click_edit()
        time.sleep(1)
        natRule.input_RuleIDs('one2onetest')
        natRule.click_typeOne2one()
        natRule.input_InFromIPs('192.168.1.200')
        natRule.input_InEndIPs('192.168.1.201')
        natRule.input_OutIPs('192.169.122.250')
        time.sleep(1)
        natRule.click_save()
        time.sleep(1)
        #断言
        InFromIPs = str(natRule.getText_byXpath(natRule.list_InFromIPs))
        self.assertEqual(InFromIPs, '192.168.1.200', msg='内网起始IP地址 与设置的不一致')
        InEndIPs = str(natRule.getText_byXpath(natRule.list_InEndIPs))
        self.assertEqual(InEndIPs, '192.168.1.201', msg='内网结束IP地址 与设置的不一致')
        OutIPs = str(natRule.getText_byXpath(natRule.list_OutIPs))
        self.assertEqual(OutIPs, '192.169.122.250', msg='外网起始IP地址 与设置的不一致')
        print('easyIP规则 已添加')

        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iptables -t nat  -L wan1_nat_rule_loop' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令执行结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 后台实际应有的结果
        result1 = 'SNAT       all  --  anywhere             192.168.1.200       UTTDEV match --is-lan-in to:192.168.1.1'
        result2 = 'SNAT       all  --  192.168.1.200        anywhere            to:192.169.122.250'
        result3 = 'SNAT       all  --  anywhere             192.168.1.201       UTTDEV match --is-lan-in to:192.168.1.1'
        result4 = 'SNAT       all  --  192.168.1.201        anywhere            to:192.169.122.251'
        result_list=[result1,result2,result3,result4]
        # 判断
        if all(t in result for t in result_list):
            print('one2one规则 验证成功')
        else:
            raise Exception('one2one规则 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

        #删除NAT规则
        natRule.click_delete()
        time.sleep(1)
        natRule.click_ok()
        time.sleep(1)
        listtips=str(natRule.getText_byXpath(natRule.listtips))
        self.assertEqual(listtips,nodata,msg='删除规则有误')

        self.driver.quit()
        logger.info('test_002_one2one passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
