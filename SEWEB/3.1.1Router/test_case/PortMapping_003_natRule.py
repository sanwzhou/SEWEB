#! -*-conding:utf-8 -*-
#@Time: 2019/1/15 0015 14:27
#@swzhou
'''
easyIP 及 one2one 验证，后台telnet确认有对应规则生成
'''


import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb,getAssertText
from common.loginRoute import login
from pages.PortMapping_003_natRulePage import natRulePage
logger = LogGen(Logger = 'PortMapping_003_natRule').getlog()
host = gettelnet('host')
host1 = host.split(r'.')
host2 = host1[0] + '.' + host1[1] + '.' + host1[2] +'.'

class natRule(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_easyIP(self):
        u'''验证 easyIP,后台telnet验证iptables规则'''
        #新增
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
        natRule.click_add()
        time.sleep(1)
        natRule.input_RuleIDs('easyIPtest')
        natRule.input_InFromIPs(host2 + '200')
        natRule.input_InEndIPs(host2 + '202')
        natRule.input_OutIPs('192.169.122.250')
        time.sleep(1)
        natRule.click_save()
        time.sleep(1)
        #断言
        InFromIPs = str(natRule.getText_byXpath(natRule.list_InFromIPs))
        self.assertEqual(InFromIPs, host2 + '200', msg='内网起始IP地址 与设置的不一致')
        InEndIPs = str(natRule.getText_byXpath(natRule.list_InEndIPs))
        self.assertEqual(InEndIPs, host2 + '202', msg='内网结束IP地址 与设置的不一致')
        OutIPs = str(natRule.getText_byXpath(natRule.list_OutIPs))
        self.assertEqual(OutIPs, '192.169.122.250', msg='外网起始IP地址 与设置的不一致')
        print('easyIP规则 已添加')

        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
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
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        #后台实际应有的结果
        result1='SNAT       all  --  anywhere             anywhere            source IP range %s200-%s202 to:192.169.122.250' \
                % (host2,host2)
        # 判断
        if result1 in result:
            print('easyIP规则 验证成功')
        else:
            raise Exception('easyIP规则 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')

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
        natRule.input_InFromIPs(host2 + '200')
        natRule.input_InEndIPs(host2 + '201')
        natRule.input_OutIPs('192.169.122.250')
        time.sleep(1)
        natRule.click_save()
        time.sleep(1)
        #断言
        InFromIPs = str(natRule.getText_byXpath(natRule.list_InFromIPs))
        self.assertEqual(InFromIPs, host2 + '200', msg='内网起始IP地址 与设置的不一致')
        InEndIPs = str(natRule.getText_byXpath(natRule.list_InEndIPs))
        self.assertEqual(InEndIPs, host2 + '201', msg='内网结束IP地址 与设置的不一致')
        OutIPs = str(natRule.getText_byXpath(natRule.list_OutIPs))
        self.assertEqual(OutIPs, '192.169.122.250', msg='外网起始IP地址 与设置的不一致')
        print('easyIP规则 已添加')

        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
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
        result1 = 'SNAT       all  --  anywhere             %s200      UTTDEV match --is-lan-in to:%s' % (host2,host)
        result2 = 'SNAT       all  --  %s200       anywhere            to:192.169.122.250' % host2
        result3 = 'SNAT       all  --  anywhere             %s201      UTTDEV match --is-lan-in to:%s' % (host2,host)
        result4 = 'SNAT       all  --  %s201       anywhere            to:192.169.122.251' % host2
        result_list=[result1,result2,result3,result4]
        print(result1,result2,result3,result4)
        # 判断
        if all(t.replace(' ','') in result.replace(' ','') for t in result_list):
            print('one2one规则 验证成功')
        else:
            print('123')
            # print(t.strip())
            print('1234')
            print(result.replace(' ',''))
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
