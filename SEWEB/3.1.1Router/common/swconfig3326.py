#! -*-conding:utf-8 -*-
#@Time: 2019/3/6 0006 11:52
#@swzhou
'''
交换机设置 tag vlan
端口vlan因为 当有SE设备两个lan口同时接入交换机时，即便有端口vlan也出现广播风暴，这里使用tag vlan
命令适用于 3326GPv1
'''

import telnetlib
import unittest
import time
from common.ReadConfig import gettelnet
from common.LogGen import LogGen
logger = LogGen(Logger = 'switchconfig').getlog()


class swconfig(unittest.TestCase):

    def setUp(self):
        print('switchconfig start')
        # pass

    def test_initSwPort(self):
        u'''初始化交换机接口vlan'''
        # 交换机17、18、19、20、21分别与被测路由wan1 - wan5相连，24口与上级路由lan口相连
        # 17口与24口同属于vlan24，18-vlan18，19-vlan19，20-vlan20，21-vlan21

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 增加vlan 25/26/27/28/29/30
        tn.read_until(b'UTT(config)##')
        tn.write(b'vlan 17' + b'\n')
        tn.read_until(b'UTT(config-vlan17)#')
        tn.write(b'vlan 18' + b'\n')
        tn.read_until(b'UTT(config-vlan18)#')
        tn.write(b'vlan 19' + b'\n')
        tn.read_until(b'UTT(config-vlan19)#')
        tn.write(b'vlan 20' + b'\n')
        tn.read_until(b'UTT(config-vlan20)#')
        tn.write(b'vlan 21' + b'\n')
        tn.read_until(b'UTT(config-vlan21)#')
        tn.write(b'vlan 24' + b'\n')
        tn.read_until(b'UTT(config-vlan24)#')
        tn.write(b'interface vlan 30' + b'\n')
        tn.read_until(b'UTT(config-if-vlan30)#')
        # 设置vlan30虚接口地址，与config以及changeStaticIP3_34duan.bat 网段一致
        tn.write(b'ip address 192.168.30.254 255.255.255.0' + b'\n')
        tn.write(b'exit' + b'\n')
        # 9口与15口通(9口与1-14、16-26口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/9' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/9)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/9)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/8,0/10-0/14,0/16-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/9)#')
        tn.write(b'exit' + b'\n')
        # 10口 (10口与所有端口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/10' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/9,0/11-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'exit' + b'\n')
        # 11口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/11' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/10,0/12-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'exit' + b'\n')
        # 12口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/12' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/11,0/13-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'exit' + b'\n')
        # 13口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/13' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/13)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/13)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/12,0/14-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/13)#')
        tn.write(b'exit' + b'\n')
        # 14口 14与AP1-8，pc 19 通
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/14' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/14)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/14)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/9-0/13,0/15-0/18,0/20-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/14)#')
        tn.write(b'exit' + b'\n')
        # 15口 与9号口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/15)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/15)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/8,0/10-0/14,0/16-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/15)#')
        tn.write(b'exit' + b'\n')
        # 17口与AP1-8/14口通(19口与9-13、15-26口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/17' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/17)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/17)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/9-0/13,0/15-0/16,0/18,0/20-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/17)#')
        tn.write(b'exit' + b'\n')
        # 19口与AP1-8/14/17口通(19口与9-13、15-16、18、19-26口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/19' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/9-0/13,0/15-0/16,0/18,0/20-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g9 = 'Gi 0/9 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
             'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g10 = 'Gi 0/10 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g11 = 'Gi 0/11 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g12 = 'Gi 0/12 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g13 = 'Gi 0/13 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g14 = 'Gi 0/14 : Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 Gi 0/15 Gi 0/16 Gi 0/18 Gi 0/20 Gi 0/21 ' \
              'Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26 '
        g15 = 'Gi 0/15 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g17 = 'Gi 0/17 : Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 Gi 0/15 Gi 0/16 Gi 0/18 Gi 0/20 Gi 0/21 ' \
              'Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26 '
        g19 = 'Gi 0/19 : Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 Gi 0/15 Gi 0/16 Gi 0/18 Gi 0/20 Gi 0/21 ' \
              'Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26 '
        Interface = [g9,g10,g11,g12,g13,g14,g15,g17,g19]
        if all(t in result1 for t in Interface):
            logger.info(u'交换机vlan接口 初始化完成')
        else:
            logger.info(u'Interface: %s' % Interface)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'交换机vlan接口 初始化异常')
        tn.close()

    def test_changeWAN2(self):
        u'''调整wan2 与上联口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，15口与上级路由lan口相连
        #设置wan2 与 上联口 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 10口与14口通(9口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离15口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/10' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g9 = 'Gi 0/9 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
             'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g10 = 'Gi 0/10 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g11 = 'Gi 0/11 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g12 = 'Gi 0/12 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g13 = 'Gi 0/13 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g15 = 'Gi 0/15 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        Interface = [g9, g10, g11, g12, g13, g15]
        if all(t in result1 for t in Interface):
            logger.info(u'交换机changeWAN2 完成')
        else:
            logger.info(u'Interface: %s' % Interface)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整wan2与上联口 互通异常')
        tn.close()

        logger.info(u'调整wan2 与上联口 互通 完成')

    def test_changeWAN3(self):
        u'''调整wan2\wan3 与上联口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，14口与上级路由lan口相连
        # 设置wan2\wan3 与 上联口 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 10口与14口通(9口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/10' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'exit' + b'\n')
        # 11口与14口通(11口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/11' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g9 = 'Gi 0/9 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
             'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g10 = 'Gi 0/10 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g11 = 'Gi 0/11 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g12 = 'Gi 0/12 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/13 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g13 = 'Gi 0/13 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g15 = 'Gi 0/15 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        Interface = [g9, g10, g11, g12, g13, g15]
        if all(t in result1 for t in Interface):
            logger.info(u'交换机changeWAN3 完成')
        else:
            logger.info(u'Interface: %s' % Interface)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整wan3 与上联口 互通异常')
        tn.close()

        logger.info(u'调整wan3 与上联口 互通 完成')

    def test_changeWAN4(self):
        u'''调整wan2/wan3/wan4 与上联口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，14口与上级路由lan口相连
        # 设置wan2/wan3/wan4 与 上联口 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 10口与14口通(9口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/10' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'exit' + b'\n')
        # 11口与14口通(11口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/11' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'exit' + b'\n')
        # 12口与14口通(12口与1-13、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/12' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g9 = 'Gi 0/9 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
             'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g10 = 'Gi 0/10 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g11 = 'Gi 0/11 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g12 = 'Gi 0/12 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g13 = 'Gi 0/13 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 ' \
              'Gi 0/14 Gi 0/15 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g15 = 'Gi 0/15 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        Interface = [g9, g10, g11, g12, g13, g15]
        if all(t in result1 for t in Interface):
            logger.info(u'交换机changeWAN4 完成')
        else:
            logger.info(u'Interface: %s' % Interface)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整wan4 与上联口互通异常')
        tn.close()
        logger.info(u'调整wan4 与上联口 互通完成')

    def test_changeWAN5(self):
        u'''调整wan2\wan3\wan4\wan5 与上联口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，14口与上级路由lan口相连
        # 设置wan2\wan3\wan4\wan5 与 上联口 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 10口与14口通(9口与1-9、11-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/10' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/10)#')
        tn.write(b'exit' + b'\n')
        # 11口与14口通(11口与1-10、12-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/11' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/11)#')
        tn.write(b'exit' + b'\n')
        # 12口与14口通(12口与1-11、13-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/12' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/12)#')
        tn.write(b'exit' + b'\n')
        # 13口与14口通(13口与1-12、15-26口隔离) #在初始化的基础上修改 不隔离14口
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/13' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/13)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/15' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/13)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g9 = 'Gi 0/9 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
             'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g10 = 'Gi 0/10 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g11 = 'Gi 0/11 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g12 = 'Gi 0/12 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g13 = 'Gi 0/13 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        g15 = 'Gi 0/15 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/19 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'
        Interface = [g9, g10, g11, g12, g13, g15]
        if all(t in result1 for t in Interface):
            logger.info(u'交换机changeWAN5 完成')
        else:
            logger.info(u'Interface: %s' % Interface)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整wan5 与上联口互通异常')
        tn.close()

        logger.info(u'调整wan5 与上联口 互通完成')

    def test_LanToWan(self):
        u'''调整PC接线口 与上联口/wan1口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，14口与上级路由lan口相连，19口与测试pc相连
        # 设置19口 与 上联口/wan1 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 19口与9\15口通(19口与1-8、10-14、16-26口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/19' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/1-0/8,0/10-0/14,0/16-0/18,0/20-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g19 = 'Gi 0/19 : Gi 0/1 Gi 0/2 Gi 0/3 Gi 0/4 Gi 0/5 Gi 0/6 Gi 0/7 Gi 0/8 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 ' \
              'Gi 0/14 Gi 0/16 Gi 0/17 Gi 0/18 Gi 0/20 Gi 0/21 Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26'

        if g19 in result1:
            logger.info(u'调整PC接线口 与上联口/wan1口 互通完成')
        else:
            logger.info(u'g19: %s' % g19)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整PC接线口 与上联口/wan1口 互通异常')
        tn.close()
        logger.info(u'设置14口与 上联口/wan1口 完成')

    def test_WanToLan(self):
        u'''PC口改回与lan口 互通'''
        ##交换机9、10、11、12、13分别与被测路由wan1 - wan5相连，14口与上级路由lan口相连，19口与测试pc相连
        # 设置19口 与 lan口 通

        # telnet交换机
        hostip = gettelnet('switchURL')
        port = gettelnet('switchport')
        password = bytes(gettelnet('switchPwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'UTT>')
        tn.write(b'enable' + b"\n")
        tn.read_until(b'password:')
        tn.write(password + b"\n")
        tn.read_until(b'UTT#')
        tn.write(b'configure terminal' + b'\n')
        # 19口与AP1-8/14/17口通(19口与9-13、15-16、18、19-26口隔离)
        tn.read_until(b'UTT(config)#')
        tn.write(b'interface gigabitEthernet 0/19' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'no isolate-port interface gigabitEthernet 0/1-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'isolate-port interface gigabitEthernet 0/9-0/13,0/15-0/16,0/18,0/20-0/26' + b'\n')
        tn.read_until(b'UTT(config-if-gigaEthernet-0/19)#')
        tn.write(b'end' + b'\n')

        # 输出结果，判断
        tn.read_until(b'UTT#')
        tn.write(b'show isolate-port' + b'\n')
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        print('result1', result1)
        g19 = 'Gi 0/19 : Gi 0/9 Gi 0/10 Gi 0/11 Gi 0/12 Gi 0/13 Gi 0/15 Gi 0/16 Gi 0/18 Gi 0/20 Gi 0/21 ' \
              'Gi 0/22 Gi 0/23 Gi 0/24 Gi 0/25 Gi 0/26 '

        if g19 in result1:
            logger.info(u'调整PC接线口 与上联口/wan1口 互通完成')
        else:
            logger.info(u'g19: %s' % g19)
            logger.info(u'result1: %s' % result1)
            raise Exception(u'调整PC接线口 与上联口/wan1口 互通异常')
        tn.close()
        logger.info(u'pc口改回与lan口 互通 完成')

    def tearDown(self):
        print('sendMail over')

if __name__=='__main__':
    unittest.main()

