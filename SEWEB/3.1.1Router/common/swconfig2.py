#! -*-conding:utf-8 -*-
#@Time: 2019/2/28 0028 10:29
#@swzhou
'''
交换机设置 端口vlan相关
命令适用于 3552Fv1
交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，33口接lan口
34口与上级路由lan口相连，35、36与测试主机pc1、pc2(备份)相连，37口与内网server相连(可任意接)
13/14 接v1/v2 AP1,15\16接v1/v2 AP2
'''

import telnetlib
import unittest
import time
from common.ReadConfig import gettelnet
from common.LogGen import LogGen
logger = LogGen(Logger = 'switchconfig').getlog()
hostip = gettelnet('switchURL')
hostip2 = gettelnet('switchURL2')
port = gettelnet('switchport')
username = bytes(gettelnet('switchUser'), encoding="utf8")
password = bytes(gettelnet('switchPwd'), encoding="utf8")

class swconfig(unittest.TestCase):

    def setUp(self):
        print('switchconfig start')
        # pass

    def test_initSwPort(self):
        u'''初始化交换机接口vlan'''
        #交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，33口接lan口，34口与上级路由lan口相连
        #25口与34口同属于vlan34，26-vlan26，27-vlan27，28-vlan28，29-vlan29，33允许vlan1、1000、1999

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 增加vlan 25/26/27/28/29/34/1000/1999
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'vlan 25' + b'\n')
        tn.read_until(b'ST3552F(config-vlan25)#')
        tn.write(b'vlan 26' + b'\n')
        tn.read_until(b'ST3552F(config-vlan26)#')
        tn.write(b'vlan 27' + b'\n')
        tn.read_until(b'ST3552F(config-vlan27)#')
        tn.write(b'vlan 28' + b'\n')
        tn.read_until(b'ST3552F(config-vlan28)#')
        tn.write(b'vlan 29' + b'\n')
        tn.read_until(b'ST3552F(config-vlan29)#')
        tn.write(b'vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-vlan34)#')
        tn.write(b'vlan 1000' + b'\n')
        tn.read_until(b'ST3552F(config-vlan1000)#')
        tn.write(b'vlan 1999' + b'\n')
        tn.read_until(b'ST3552F(config-vlan1999)#')
        # 设置vlan34虚接口地址，与config以及changeStaticIP3_34duan.bat 网段一致
        tn.write(b'interface vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-vlan34)#')
        tn.write(b'ip address 192.168.34.254 255.255.255.0' + b'\n')
        tn.write(b'exit' + b'\n')
        # 25口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/25' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
        tn.write(b'exit' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        # 27口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport access vlan 27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'exit' + b'\n')
        # 28口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'switchport access vlan 28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'exit' + b'\n')
        # 29口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/29' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'switchport access vlan 29' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'exit' + b'\n')
        # 34口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
        tn.write(b'exit' + b'\n')
        # 35口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/35' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
        tn.write(b'switchport access vlan 1' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
        tn.write(b'exit' + b'\n')
        # 36口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/36' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
        tn.write(b'switchport access vlan 1' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
        tn.write(b'exit' + b'\n')
        # 13-16 接AP,33接lan口，设置为trunk 允许 vlan1，1000，1999
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/13-16;1/0/33' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode trunk' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'end' + b'\n')
        # 输出结果，判断
        #26
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 26' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/26' in result1:
            print('port 26 in vlan 26')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 26 not in vlan 26')
            raise Exception(u'port 26 not in vlan 26')
        tn.close()
        # 27
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 27' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/27' in result1:
            print('port 27 in vlan 27')
        else:
            logger.info(u'result2: %s' % result1)
            logger.info(u'port 27 not in vlan 27')
            raise Exception(u'port 27 not in vlan 27')
        tn.close()
        # 28
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 28' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/28' in result1:
            print('port 28 in vlan 28')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 28 not in vlan 28')
            raise Exception(u'port 28 not in vlan 28')
        tn.close()
        # 29
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 29' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        if 'Ethernet1/0/29' in result1:
            print('port 29 in vlan 29')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 29 not in vlan 29')
            raise Exception(u'port 29 not in vlan 29')
        tn.close()
        # 1
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 1' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/13' and 'Ethernet1/0/14' and 'Ethernet1/0/33' in result1:
            print('port 13/14/33 in vlan 34')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 13 or 14 or 33 not in vlan 34')
            raise Exception(u'port13 or 14 or 33 not in vlan 34')
        # 1000
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 1000' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/13(T)' and 'Ethernet1/0/14(T)' and 'Ethernet1/0/33(T)' in result1:
            print('port 13/14/33 in vlan 1000')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 13 or 14 or 33 not in vlan 1000')
            raise Exception(u'port13 or 14 or 33 not in vlan 1000')
        # 1999
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 1999' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/13(T)' and 'Ethernet1/0/14(T)' and 'Ethernet1/0/33(T)' in result1:
            print('port 13/14/33 in vlan 1999')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 13 or 14 or 33 not in vlan 1999')
            raise Exception(u'port13 or 14 or 33 not in vlan 1999')

        tn.close()
        logger.info(u'交换机vlan接口 初始化完成')

    def test_changeWAN2(self):
        u'''调整wan2 与上联口 互通'''
        #交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连
        #设置wan2 与 上联口 同属于vlan34

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 34' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/34','Ethernet1/0/25','Ethernet1/0/26']
        for x in inter:
            if x in result1:
                print('port 25/34/26 in vlan 34')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 25/34/26 not in vlan 34')
                raise Exception(u'port 25/34/26 not in vlan 34')
        tn.close()
        logger.info(u'调整wan2 与上联口 互通 完成')

    def test_changeWAN3(self):
        u'''调整wan2\wan3 与上联口 互通'''
        #交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连
        #设置wan2\wan3 与 上联口 同属于vlan30

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        # 27口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 34' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/34', 'Ethernet1/0/25', 'Ethernet1/0/26','Ethernet1/0/27']
        for x in inter:
            if x in result1:
                print('port 25/34/26/27 in vlan 34')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 25/34/26 not in vlan 34')
                raise Exception(u'port 25/34/26 not in vlan 34')
        tn.close()
        logger.info(u'调整wan3 与上联口 互通 完成')

    def test_changeWAN4(self):
        u'''调整wan2/wan3/wan4 与上联口 互通'''
        #交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连
        #设置wan2/wan3/wan4 与 上联口 同属于vlan34

        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        # 27口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'exit' + b'\n')
        # 28口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 34' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1:', result1)
        inter = ['Ethernet1/0/34', 'Ethernet1/0/25', 'Ethernet1/0/26', 'Ethernet1/0/27','Ethernet1/0/28']
        for x in inter:
            if x in result1:
                print('port 25/34/26/27/28 in vlan 34')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 25/34/26/27/28 not in vlan 34')
                raise Exception(u'port 25/34/26/27/28 not in vlan 34')
        tn.close()
        logger.info(u'调整wan4 与上联口 互通 完成')

    def test_changeWAN5(self):
        u'''调整wan2\wan3\wan4\wan5 与上联口 互通'''
        #交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连
        #设置wan2\wan3\wan4\wan5 与 上联口 同属于vlan34

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        # 27口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'exit' + b'\n')
        # 28口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'exit' + b'\n')
        # 29口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/29' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 34' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/34', 'Ethernet1/0/25', 'Ethernet1/0/26', 'Ethernet1/0/27', 'Ethernet1/0/28','Ethernet1/0/29']
        for x in inter:
            if x in result1:
                print('port 25/34/26/27/28/29 in vlan 34')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 25/34/26/27/28/29 not in vlan 34')
                raise Exception(u'port 25/34/26/27/28/29 not in vlan 34')
        tn.close()
        logger.info(u'调整wan5 与上联口 互通 完成')

    def test_LanToWan(self):
        u'''调整PC接线口 与上联口/wan1口 互通'''
        # 交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连，35、36口接测试pc
        # 设置35/36口与 上联口/wan1口 同属于vlan34

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        #  35 - 36口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/35-36' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'end' + b'\n')
        tn.read_until(b'ST3552F#')
        tn.write(b'exit' + b'\n')
        # tn.read_until(b'ST3552F(config)#')
        # tn.write(b'show vlan id 34' + b'\n')
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 获取WAN1对应接口名称
        # result1 = result[1:]
        # # print('result1', result1)
        # inter = ['Ethernet1/0/34', 'Ethernet1/0/25', 'Ethernet1/0/36']
        # for x in inter:
        #     if x in result1:
        #         print('port 25/30/36 in vlan 30')
        #     else:
        #         logger.info(u'result1: %s' % result1)
        #         logger.info(u'port 25/30/36 not in vlan 30')
        #         raise Exception(u'port 25/30/36 not in vlan 30')
        tn.close()
        logger.info(u'设置36口与 上联口/wan1口 完成')

    def test_WanToLan(self):
        u'''PC口改回与lan口 互通'''
        # 交换机25、26、27、28、29分别与被测路由wan1 - wan5相连，34口与上级路由lan口相连，33口与pc口相连
        # 设置35、36改回没有vlan，lanToWan之后，需要交换机上设置34vlan的虚接口才能再登录

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip2, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 35 - 36口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/35-36' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'no switchport access vlan' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'end' + b'\n')
        tn.read_until(b'ST3552F#')
        tn.write(b'exit' + b'\n')
        # time.sleep(1)
        # result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # # 获取WAN1对应接口名称
        # result1 = result[1:]
        # # print('result1', result1)
        # if  'Ethernet1/0/36' not in result1:
        #     print('port 36 in vlan1')
        # else:
        #     logger.info(u'result1: %s' % result1)
        #     logger.info(u'port 36 not in vlan1')
        #     raise Exception(u'port 36 not in vlan1')
        # tn.close()
        logger.info(u'pc口改回与lan口 互通 完成')

    def test_getLANSpeed(self):
        u'''交换机接口协商速率'''

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show interface ethernet 1/0/33' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        if 'BW 1000000 Kbit' in result1:
            return 'speed1000M'
        elif 'BW 100000 Kbit' in result1:
            return 'speed100M'
        elif 'BW 10000 Kbit' in result1:
            return 'speed10M'
        tn.close()
        logger.info(u'LAN口端口速率获取 完成')

    def test_getWAN1Speed(self):
        u'''交换机接口协商速率'''

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show interface ethernet 1/0/25' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        if   'BW 1000000 Kbit' in result1:
            return 'speed1000M'
        elif 'BW 100000 Kbit' in result1:
            return 'speed100M'
        elif 'BW 10000 Kbit' in result1:
            return 'speed10M'
        tn.close()
        logger.info(u'WAN1口端口速率获取 完成')

    def test_APportAccess(self):
        u'''AP接口改为Access'''
        # 13、14 为一组v1、v2 AP，改为Acess vlan1000
        # 15、16 为一组v1、v2 AP，改为Acess vlan1999

        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 增加vlan 25/26/27/28/29/34/1000/1999
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        # 13-14 接AP,改为trunk vlan 1000
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/13-14' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 1000' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        # 15-16 接AP,改为trunk vlan 1999
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/15-16' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 1999' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'end' + b'\n')
        # 输出结果，判断
        # 1000
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 1000' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/13', 'Ethernet1/0/14']
        for x in inter:
            if x in result1:
                print('port 13/14 in vlan 1000')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 13/14 not in vlan 1000')
                raise Exception(u'port 13/14 not in vlan 1000')
        tn.close()
        # 1999
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 1999' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/15', 'Ethernet1/0/16']
        for x in inter:
            if x in result1:
                print('port 15/16 in vlan 1999')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 15/16 not in vlan 1999')
                raise Exception(u'port 15/16 not in vlan 1999')
        tn.close()


    def tearDown(self):
        print('swconfig over')

if __name__=='__main__':
    unittest.main()