#! -*-conding:utf-8 -*-
#@Time: 2019/2/28 0028 10:29
#@swzhou
'''
交换机设置 端口vlan相关
命令适用于 3552Fv1
#交换机1-2 接v1 AP vlan1000，3-4 接v2 AP vlan1999
#7口上联lan vlan7
#8口server PC  vlan1
#11-12口测试PC  vlan1
#路由器组1-6，默认vlan分别为各自接口号
#13 - 18 为测试路由器组1 分别接 wan1 -wan5 、lan1
# 19 - 24 为测试路由器组2 分别接 wan1 -wan5 、lan1  mtk2 /-L
# 25 - 30 为测试路由器组3 分别接 wan1 -wan5 、lan1   高通
# 31 - 36 为测试路由器组4 分别接 wan1 -wan5 、lan1 p1010
# 37 - 42 为测试路由器组5 分别接 wan1 -wan5 、lan1 D525
# 43 - 48 为测试路由器组6 分别接 wan1 -wan5 、lan1 j1800 / 6550G
'''

import telnetlib
import unittest
import time
from common.ReadConfig import gettelnet
from common.swNumC import swNum1,swNum2
from common.LogGen import LogGen
logger = LogGen(Logger = 'switchconfig').getlog()
hostip = gettelnet('switchURL')
hostip2 = gettelnet('switchURL2')
port = gettelnet('switchport')
username = bytes(gettelnet('switchUser'), encoding="utf8")
password = bytes(gettelnet('switchPwd'), encoding="utf8")


def test_initSwPortNext():
    u'''初始化交换机接口vlan 下个型号'''
    # 交换机1-2 接v1 AP vlan1000，3-4 接v2 AP vlan1999
    # 7口上联lan vlan7
    # 8口server PC  vlan1
    # 11-12口测试PC  vlan1
    # 路由器组1-6，默认vlan分别为各自接口号
    # 13 - 18 为测试路由器组1 分别接 wan1 -wan5 、lan1
    # 19 - 24 为测试路由器组2 分别接 wan1 -wan5 、lan1
    # 25 - 30 为测试路由器组3 分别接 wan1 -wan5 、lan1   高通
    # 31 - 36 为测试路由器组4 分别接 wan1 -wan5 、lan1 p1010
    # 37 - 42 为测试路由器组5 分别接 wan1 -wan5 、lan1 D525
    # 43 - 48 为测试路由器组6 分别接 wan1 -wan5 、lan1 j1800 / 6550G
    # 获取路由器组号后，将 wan1口 和 7口上联lan口互通，设置vlan为7；lan口 允许vlan1、1000、1999
    swNum = swNum1()  # 获取下个设备wan/lan接口号

    # telnet交换机
    tn = telnetlib.Telnet(host=hostip, port=port)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")

    # 1、增加vlan 7/1000/1999 以及对应接口vlan
    tn.read_until(b'ST3552F#')
    tn.write(b'config' + b'\n')
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'vlan 13-48,1000,1999,7' + b'\n')
    tn.read_until(b'ST3552F(config)#')

    # 2、设置vlan7虚接口地址，与config以及changeStaticIP3_34duan.bat 网段一致
    tn.write(b'interface vlan 7' + b'\n')
    tn.read_until(b'ST3552F(config-if-vlan7)#')
    tn.write(b'ip address 192.168.34.254 255.255.255.0' + b'\n')
    tn.write(b'exit' + b'\n')

    # 3、分别设置7口、13-48口的接口号vlan;8、11、12为vlan1
    # 7口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/7' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    tn.write(b'switchport access vlan 7' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    tn.write(b'exit' + b'\n')
    # 8、11、12口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/8;11-12' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport access vlan 1' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'exit' + b'\n')
    # 13口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/13' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    tn.write(b'switchport access vlan 13' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    tn.write(b'exit' + b'\n')
    # 14口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/14' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    tn.write(b'switchport access vlan 14' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    tn.write(b'exit' + b'\n')
    # 15口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/15' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    tn.write(b'switchport access vlan 15' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    tn.write(b'exit' + b'\n')
    # 16口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/16' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    tn.write(b'switchport access vlan 16' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    tn.write(b'exit' + b'\n')
    # 17口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/17' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    tn.write(b'switchport access vlan 17' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    tn.write(b'exit' + b'\n')
    # 18口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/18' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    tn.write(b'switchport access vlan 18' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    tn.write(b'exit' + b'\n')
    # 19口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/19' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    tn.write(b'switchport access vlan 19' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    tn.write(b'exit' + b'\n')
    # 20口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/20' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    tn.write(b'switchport access vlan 20' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    tn.write(b'exit' + b'\n')
    # 21口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/21' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    tn.write(b'switchport access vlan 21' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    tn.write(b'exit' + b'\n')
    # 22口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/22' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    tn.write(b'switchport access vlan 22' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    tn.write(b'exit' + b'\n')
    # 23口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/23' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    tn.write(b'switchport access vlan 23' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    tn.write(b'exit' + b'\n')
    # 24口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/24' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    tn.write(b'switchport access vlan 24' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    tn.write(b'exit' + b'\n')
    # 25口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/25' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    tn.write(b'switchport access vlan 25' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    tn.write(b'exit' + b'\n')
    # 26口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/26' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    tn.write(b'switchport access vlan 26' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    tn.write(b'exit' + b'\n')
    # 27口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/27' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    tn.write(b'switchport access vlan 27' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    tn.write(b'exit' + b'\n')
    # 28口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/28' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    tn.write(b'switchport access vlan 28' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    tn.write(b'exit' + b'\n')
    # 29口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/29' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    tn.write(b'switchport access vlan 29' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    tn.write(b'exit' + b'\n')
    # 30口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/30' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    tn.write(b'switchport access vlan 30' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    tn.write(b'exit' + b'\n')
    # 31口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/31' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    tn.write(b'switchport access vlan 31' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    tn.write(b'exit' + b'\n')
    # 32口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/32' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    tn.write(b'switchport access vlan 32' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    tn.write(b'exit' + b'\n')
    # 33口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/33' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    tn.write(b'switchport access vlan 33' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    tn.write(b'exit' + b'\n')
    # 34口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/34' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    tn.write(b'switchport access vlan 34' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    tn.write(b'exit' + b'\n')
    # 35口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/35' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    tn.write(b'switchport access vlan 35' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    tn.write(b'exit' + b'\n')
    # 36口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/36' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    tn.write(b'switchport access vlan 36' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    tn.write(b'exit' + b'\n')
    # 37口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/37' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    tn.write(b'switchport access vlan 37' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    tn.write(b'exit' + b'\n')
    # 38口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/38' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    tn.write(b'switchport access vlan 38' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    tn.write(b'exit' + b'\n')
    # 39口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/39' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    tn.write(b'switchport access vlan 39' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    tn.write(b'exit' + b'\n')
    # 40口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/40' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    tn.write(b'switchport access vlan 40' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    tn.write(b'exit' + b'\n')
    # 41口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/41' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    tn.write(b'switchport access vlan 41' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    tn.write(b'exit' + b'\n')
    # 42口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/42' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    tn.write(b'switchport access vlan 42' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    tn.write(b'exit' + b'\n')
    # 43口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/43' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    tn.write(b'switchport access vlan 43' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    tn.write(b'exit' + b'\n')
    # 44口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/44' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    tn.write(b'switchport access vlan 44' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    tn.write(b'exit' + b'\n')
    # 45口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/45' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    tn.write(b'switchport access vlan 45' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    tn.write(b'exit' + b'\n')
    # 46口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/46' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    tn.write(b'switchport access vlan 46' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    tn.write(b'exit' + b'\n')
    # 47口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/47' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    tn.write(b'switchport access vlan 47' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    tn.write(b'exit' + b'\n')
    # 48口
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/48' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    tn.write(b'switchport access vlan 48' + b'\n')
    tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    tn.write(b'exit' + b'\n')

    # 4、 1-4 接AP设置为trunk 允许 vlan1，1000，1999
    tn.read_until(b'ST3552F(config)#')
    tn.write(b'interface ethernet 1/0/1-4' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport mode trunk' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'exit' + b'\n')

    # 5、判断wan1口、lan1口 接线口
    # wan1口设置为和上联口7口相连，
    wan1num = swNum[:2]
    cmd = 'interface ethernet 1/0/' + wan1num + ';7'
    cmd = bytes(cmd, encoding='utf8')
    tn.read_until(b'ST3552F(config)#')
    tn.write(cmd + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport mode access' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'switchport access vlan 7' + b'\n')
    tn.read_until(b'ST3552F(config-if-port-range)#')
    tn.write(b'exit' + b'\n')
    # lan1口设置为vlan1
    lan1num = swNum[-2:]
    cmd = 'interface ethernet 1/0/' + lan1num
    cmd = bytes(cmd, encoding='utf8')
    cmd2 = 'ST3552F(config-if-ethernet1/0/%s)#' % lan1num
    cmd2 = bytes(cmd2, encoding='utf8')
    tn.read_until(b'ST3552F(config)#')
    tn.write(cmd + b'\n')
    tn.read_until(cmd2)
    tn.write(b'switchport mode trunk' + b'\n')
    tn.read_until(cmd2)
    tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
    tn.read_until(cmd2)
    tn.write(b'end' + b'\n')
    # 输出结果，判断
    # 26
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

    # vlan1
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
    if 'Ethernet1/0/1' and 'Ethernet1/0/2' and ('Ethernet1/0/%s' % lan1num) in result1:
        print('port 1/2/lan in vlan 1')
    else:
        logger.info(u'result1: %s' % result1)
        logger.info(u'port 1 or 2 or lan1num not in vlan 1')
        raise Exception(u'port 1 or 2 or lan1num not in vlan 1')
    tn.close()
    # vlan7
    tn = telnetlib.Telnet(host=hostip, port=port)
    tn.set_debuglevel(5)
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'ST3552F#')
    tn.write(b'show vlan id 7' + b'\n')
    time.sleep(0.5)
    result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    print('result:', result)
    # 获取WAN1对应接口名称
    result1 = result[1:]
    # print('result1', result1)
    if 'Ethernet1/0/7' and ('Ethernet1/0/%s' % wan1num) in result1:
        print('port 7/lan in vlan 1')
    else:
        logger.info(u'result1: %s' % result1)
        logger.info(u'port 7 or wan1num not in vlan 1')
        raise Exception(u'port 7 or wan1num not in vlan 1')
    tn.close()
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
    if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
        print('port 1/2/lan1num in vlan 1000')
    else:
        logger.info(u'result1: %s' % result1)
        logger.info(u'port 1 or 2 or lan1num not in vlan 1000')
        raise Exception(u'port 1 or 2 or lan1num not in vlan 1000')
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
    result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    print('result:', result)
    # 获取WAN1对应接口名称
    result1 = result[1:]
    # print('result1', result1)
    if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
        print('port 1/2/lan1num in vlan 1999')
    else:
        logger.info(u'result1: %s' % result1)
        logger.info(u'port 1 or 2 or lan1num not in vlan 1999')
        raise Exception(u'port 1 or 2 or lan1num not in vlan 1999')

    tn.close()
    logger.info(u'交换机vlan接口 初始化完成')

class swconfig(unittest.TestCase):

    def setUp(self):
        print('switchconfig start')
        # pass

    # def test_initSwPortNext2(self):
    #     u'''初始化交换机接口vlan 下个型号'''
    #     #交换机1-2 接v1 AP vlan1000，3-4 接v2 AP vlan1999
    #     #7口上联lan vlan7
    #     #8口server PC  vlan1
    #     #11-12口测试PC  vlan1
    #     #路由器组1-6，默认vlan分别为各自接口号
    #     #13 - 18 为测试路由器组1 分别接 wan1 -wan5 、lan1
    #     # 19 - 24 为测试路由器组2 分别接 wan1 -wan5 、lan1
    #     # 25 - 30 为测试路由器组3 分别接 wan1 -wan5 、lan1   高通
    #     # 31 - 36 为测试路由器组4 分别接 wan1 -wan5 、lan1 p1010
    #     # 37 - 42 为测试路由器组5 分别接 wan1 -wan5 、lan1 D525
    #     # 43 - 48 为测试路由器组6 分别接 wan1 -wan5 、lan1 j1800 / 6550G
    #     #获取路由器组号后，将 wan1口 和 7口上联lan口互通，设置vlan为7；lan口 允许vlan1、1000、1999
    #     swNum = swNum1() #获取下个设备wan/lan接口号
    #
    #     # telnet交换机
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #
    #     # 1、增加vlan 7/1000/1999 以及对应接口vlan
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'config' + b'\n')
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'vlan 13-48,1000,1999,7' + b'\n')
    #     tn.read_until(b'ST3552F(config)#')
    #
    #     # 2、设置vlan7虚接口地址，与config以及changeStaticIP3_34duan.bat 网段一致
    #     tn.write(b'interface vlan 7' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-vlan7)#')
    #     tn.write(b'ip address 192.168.34.254 255.255.255.0' + b'\n')
    #     tn.write(b'exit' + b'\n')
    #
    #     # 3、分别设置7口、13-48口的接口号vlan;8、11、12为vlan1
    #     # 7口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/7' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    #     tn.write(b'switchport access vlan 7' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
    #     tn.write(b'exit' + b'\n')
    #     #8、11、12口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/8;11-12' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport access vlan 1' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'exit' + b'\n')
    #     # 13口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/13' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    #     tn.write(b'switchport access vlan 13' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
    #     tn.write(b'exit' + b'\n')
    #     # 14口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/14' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    #     tn.write(b'switchport access vlan 14' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
    #     tn.write(b'exit' + b'\n')
    #     # 15口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/15' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    #     tn.write(b'switchport access vlan 15' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
    #     tn.write(b'exit' + b'\n')
    #     # 16口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/16' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    #     tn.write(b'switchport access vlan 16' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
    #     tn.write(b'exit' + b'\n')
    #     # 17口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/17' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    #     tn.write(b'switchport access vlan 17' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
    #     tn.write(b'exit' + b'\n')
    #     # 18口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/18' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    #     tn.write(b'switchport access vlan 18' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
    #     tn.write(b'exit' + b'\n')
    #     # 19口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/19' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    #     tn.write(b'switchport access vlan 19' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
    #     tn.write(b'exit' + b'\n')
    #     # 20口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/20' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    #     tn.write(b'switchport access vlan 20' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
    #     tn.write(b'exit' + b'\n')
    #     # 21口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/21' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    #     tn.write(b'switchport access vlan 21' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
    #     tn.write(b'exit' + b'\n')
    #     # 22口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/22' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    #     tn.write(b'switchport access vlan 22' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
    #     tn.write(b'exit' + b'\n')
    #     # 23口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/23' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    #     tn.write(b'switchport access vlan 23' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
    #     tn.write(b'exit' + b'\n')
    #     # 24口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/24' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    #     tn.write(b'switchport access vlan 24' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
    #     tn.write(b'exit' + b'\n')
    #     # 25口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/25' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    #     tn.write(b'switchport access vlan 25' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
    #     tn.write(b'exit' + b'\n')
    #     # 26口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/26' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    #     tn.write(b'switchport access vlan 26' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
    #     tn.write(b'exit' + b'\n')
    #     # 27口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/27' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    #     tn.write(b'switchport access vlan 27' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
    #     tn.write(b'exit' + b'\n')
    #     # 28口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/28' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    #     tn.write(b'switchport access vlan 28' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
    #     tn.write(b'exit' + b'\n')
    #     # 29口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/29' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    #     tn.write(b'switchport access vlan 29' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
    #     tn.write(b'exit' + b'\n')
    #     # 30口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/30' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    #     tn.write(b'switchport access vlan 30' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
    #     tn.write(b'exit' + b'\n')
    #     # 31口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/31' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    #     tn.write(b'switchport access vlan 31' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
    #     tn.write(b'exit' + b'\n')
    #     # 32口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/32' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    #     tn.write(b'switchport access vlan 32' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
    #     tn.write(b'exit' + b'\n')
    #     # 33口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/33' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    #     tn.write(b'switchport access vlan 33' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
    #     tn.write(b'exit' + b'\n')
    #     # 34口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/34' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    #     tn.write(b'switchport access vlan 34' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
    #     tn.write(b'exit' + b'\n')
    #     # 35口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/35' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    #     tn.write(b'switchport access vlan 35' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
    #     tn.write(b'exit' + b'\n')
    #     # 36口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/36' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    #     tn.write(b'switchport access vlan 36' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
    #     tn.write(b'exit' + b'\n')
    #     # 37口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/37' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    #     tn.write(b'switchport access vlan 37' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
    #     tn.write(b'exit' + b'\n')
    #     # 38口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/38' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    #     tn.write(b'switchport access vlan 38' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
    #     tn.write(b'exit' + b'\n')
    #     # 39口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/39' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    #     tn.write(b'switchport access vlan 39' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
    #     tn.write(b'exit' + b'\n')
    #     # 40口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/40' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    #     tn.write(b'switchport access vlan 40' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
    #     tn.write(b'exit' + b'\n')
    #     # 41口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/41' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    #     tn.write(b'switchport access vlan 41' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
    #     tn.write(b'exit' + b'\n')
    #     # 42口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/42' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    #     tn.write(b'switchport access vlan 42' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
    #     tn.write(b'exit' + b'\n')
    #     # 43口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/43' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    #     tn.write(b'switchport access vlan 43' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
    #     tn.write(b'exit' + b'\n')
    #     # 44口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/44' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    #     tn.write(b'switchport access vlan 44' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
    #     tn.write(b'exit' + b'\n')
    #     # 45口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/45' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    #     tn.write(b'switchport access vlan 45' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
    #     tn.write(b'exit' + b'\n')
    #     # 46口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/46' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    #     tn.write(b'switchport access vlan 46' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
    #     tn.write(b'exit' + b'\n')
    #     # 47口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/47' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    #     tn.write(b'switchport access vlan 47' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
    #     tn.write(b'exit' + b'\n')
    #     # 48口
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/48' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    #     tn.write(b'switchport access vlan 48' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
    #     tn.write(b'exit' + b'\n')
    #
    #     # 4、 1-4 接AP设置为trunk 允许 vlan1，1000，1999
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(b'interface ethernet 1/0/1-4' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport mode trunk' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'exit' + b'\n')
    #
    #     #5、判断wan1口、lan1口 接线口
    #     #wan1口设置为和上联口7口相连，
    #     wan1num = swNum[:2]
    #     cmd = 'interface ethernet 1/0/' + wan1num + ';7'
    #     cmd = bytes(cmd,encoding='utf8')
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(cmd + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport mode access' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'switchport access vlan 7' + b'\n')
    #     tn.read_until(b'ST3552F(config-if-port-range)#')
    #     tn.write(b'exit' + b'\n')
    #     # lan1口设置为vlan1
    #     lan1num = swNum[-2:]
    #     cmd = 'interface ethernet 1/0/' + lan1num
    #     cmd = bytes(cmd, encoding='utf8')
    #     cmd2 = 'ST3552F(config-if-ethernet1/0/%s)#' % lan1num
    #     cmd2 = bytes(cmd2, encoding='utf8')
    #     tn.read_until(b'ST3552F(config)#')
    #     tn.write(cmd + b'\n')
    #     tn.read_until(cmd2)
    #     tn.write(b'switchport mode trunk' + b'\n')
    #     tn.read_until(cmd2)
    #     tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
    #     tn.read_until(cmd2)
    #     tn.write(b'end' + b'\n')
    #     # 输出结果，判断
    #     #26
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 26' + b'\n')
    #     time.sleep(1)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/26' in result1:
    #         print('port 26 in vlan 26')
    #     else:
    #         logger.info(u'result1: %s' % result1)
    #         logger.info(u'port 26 not in vlan 26')
    #         raise Exception(u'port 26 not in vlan 26')
    #     tn.close()
    #     # 27
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #     # 登录完毕后执行命令
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 27' + b'\n')
    #     time.sleep(0.5)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/27' in result1:
    #         print('port 27 in vlan 27')
    #     else:
    #         logger.info(u'result2: %s' % result1)
    #         logger.info(u'port 27 not in vlan 27')
    #         raise Exception(u'port 27 not in vlan 27')
    #     tn.close()
    #
    #     # vlan1
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #     # 登录完毕后执行命令
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 1' + b'\n')
    #     time.sleep(0.5)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/1' and 'Ethernet1/0/2' and ('Ethernet1/0/%s' % lan1num) in result1:
    #         print('port 1/2/lan in vlan 1')
    #     else:
    #         logger.info(u'result1: %s' % result1)
    #         logger.info(u'port 1 or 2 or lan1num not in vlan 1')
    #         raise Exception(u'port 1 or 2 or lan1num not in vlan 1')
    #     tn.close()
    #     # vlan7
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #     # 登录完毕后执行命令
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 7' + b'\n')
    #     time.sleep(0.5)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/7' and ('Ethernet1/0/%s' % wan1num) in result1:
    #         print('port 7/lan in vlan 1')
    #     else:
    #         logger.info(u'result1: %s' % result1)
    #         logger.info(u'port 7 or wan1num not in vlan 1')
    #         raise Exception(u'port 7 or wan1num not in vlan 1')
    #     tn.close()
    #     # 1000
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #     # 登录完毕后执行命令
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 1000' + b'\n')
    #     time.sleep(0.5)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
    #         print('port 1/2/lan1num in vlan 1000')
    #     else:
    #         logger.info(u'result1: %s' % result1)
    #         logger.info(u'port 1 or 2 or lan1num not in vlan 1000')
    #         raise Exception(u'port 1 or 2 or lan1num not in vlan 1000')
    #     tn.close()
    #     # 1999
    #     tn = telnetlib.Telnet(host=hostip, port=port)
    #     tn.set_debuglevel(5)
    #     tn.read_until(b'login:')
    #     tn.write(username + b"\n")
    #     tn.read_until(b'Password:')
    #     tn.write(password + b"\n")
    #     # 登录完毕后执行命令
    #     tn.read_until(b'ST3552F#')
    #     tn.write(b'show vlan id 1999' + b'\n')
    #     time.sleep(0.5)
    #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    #     print('-------------------输出结果------------------------')
    #     # 命令执行结果
    #     print('result:', result)
    #     # 获取WAN1对应接口名称
    #     result1 = result[1:]
    #     # print('result1', result1)
    #     if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
    #         print('port 1/2/lan1num in vlan 1999')
    #     else:
    #         logger.info(u'result1: %s' % result1)
    #         logger.info(u'port 1 or 2 or lan1num not in vlan 1999')
    #         raise Exception(u'port 1 or 2 or lan1num not in vlan 1999')
    #
    #     tn.close()
    #     logger.info(u'交换机vlan接口 初始化完成')

    def test_initSwPort(self):
        u'''初始化交换机接口vlan 当前型号'''
        #交换机1、3 接v1 AP vlan1000，2、4 接v2 AP vlan1999
        #7口上联lan vlan7
        #8口server PC  vlan1
        #11-12口测试PC  vlan1
        #路由器组1-6，默认vlan分别为各自接口号
        #13 - 18 为测试路由器组1 分别接 wan1 -wan5 、lan1
        # 19 - 24 为测试路由器组2 分别接 wan1 -wan5 、lan1
        # 25 - 30 为测试路由器组3 分别接 wan1 -wan5 、lan1   高通
        # 31 - 36 为测试路由器组4 分别接 wan1 -wan5 、lan1 p1010
        # 37 - 42 为测试路由器组5 分别接 wan1 -wan5 、lan1 D525
        # 43 - 48 为测试路由器组6 分别接 wan1 -wan5 、lan1 j1800 / 6550G
        #获取路由器组号后，将 wan1口 和 7口上联lan口互通，设置vlan为7；lan口 允许vlan1、1000、1999
        swNum = swNum2() #获取当前设备wan/lan接口号
        print('123:',swNum)
        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")

        # 1、增加vlan 7/1000/1999 以及对应接口vlan
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'vlan 13-48,1000,1999,7' + b'\n')
        tn.read_until(b'ST3552F(config)#')

        # 2、设置vlan7虚接口地址，与config以及changeStaticIP3_34duan.bat 网段一致
        tn.write(b'interface vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-vlan7)#')
        tn.write(b'ip address 192.168.34.254 255.255.255.0' + b'\n')
        tn.write(b'exit' + b'\n')

        # 3、分别设置7口、13-48口的接口号vlan;8、11、12为vlan1
        # 7口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/7' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/7)#')
        tn.write(b'exit' + b'\n')
        #8、11、12口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/8;11-12' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 1' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        # 13口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/13' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
        tn.write(b'switchport access vlan 13' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/13)#')
        tn.write(b'exit' + b'\n')
        # 14口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/14' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
        tn.write(b'switchport access vlan 14' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/14)#')
        tn.write(b'exit' + b'\n')
        # 15口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/15' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
        tn.write(b'switchport access vlan 15' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/15)#')
        tn.write(b'exit' + b'\n')
        # 16口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/16' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
        tn.write(b'switchport access vlan 16' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/16)#')
        tn.write(b'exit' + b'\n')
        # 17口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/17' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
        tn.write(b'switchport access vlan 17' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/17)#')
        tn.write(b'exit' + b'\n')
        # 18口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/18' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
        tn.write(b'switchport access vlan 18' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/18)#')
        tn.write(b'exit' + b'\n')
        # 19口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/19' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
        tn.write(b'switchport access vlan 19' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/19)#')
        tn.write(b'exit' + b'\n')
        # 20口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/20' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
        tn.write(b'switchport access vlan 20' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/20)#')
        tn.write(b'exit' + b'\n')
        # 21口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/21' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
        tn.write(b'switchport access vlan 21' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/21)#')
        tn.write(b'exit' + b'\n')
        # 22口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/22' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
        tn.write(b'switchport access vlan 22' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/22)#')
        tn.write(b'exit' + b'\n')
        # 23口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/23' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
        tn.write(b'switchport access vlan 23' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/23)#')
        tn.write(b'exit' + b'\n')
        # 24口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/24' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
        tn.write(b'switchport access vlan 24' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/24)#')
        tn.write(b'exit' + b'\n')
        # 25口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/25' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
        tn.write(b'switchport access vlan 25' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/25)#')
        tn.write(b'exit' + b'\n')
        # 26口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'switchport access vlan 26' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/26)#')
        tn.write(b'exit' + b'\n')
        # 27口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'switchport access vlan 27' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/27)#')
        tn.write(b'exit' + b'\n')
        # 28口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'switchport access vlan 28' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/28)#')
        tn.write(b'exit' + b'\n')
        # 29口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/29' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'switchport access vlan 29' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/29)#')
        tn.write(b'exit' + b'\n')
        # 30口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/30' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
        tn.write(b'switchport access vlan 30' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/30)#')
        tn.write(b'exit' + b'\n')
        # 31口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/31' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
        tn.write(b'switchport access vlan 31' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/31)#')
        tn.write(b'exit' + b'\n')
        # 32口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/32' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
        tn.write(b'switchport access vlan 32' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/32)#')
        tn.write(b'exit' + b'\n')
        # 33口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/33' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
        tn.write(b'switchport access vlan 33' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/33)#')
        tn.write(b'exit' + b'\n')
        # 34口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
        tn.write(b'switchport access vlan 34' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/34)#')
        tn.write(b'exit' + b'\n')
        # 35口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/35' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
        tn.write(b'switchport access vlan 35' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/35)#')
        tn.write(b'exit' + b'\n')
        # 36口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/36' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
        tn.write(b'switchport access vlan 36' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/36)#')
        tn.write(b'exit' + b'\n')
        # 37口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/37' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
        tn.write(b'switchport access vlan 37' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/37)#')
        tn.write(b'exit' + b'\n')
        # 38口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/38' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
        tn.write(b'switchport access vlan 38' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/38)#')
        tn.write(b'exit' + b'\n')
        # 39口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/39' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
        tn.write(b'switchport access vlan 39' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/39)#')
        tn.write(b'exit' + b'\n')
        # 40口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/40' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
        tn.write(b'switchport access vlan 40' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/40)#')
        tn.write(b'exit' + b'\n')
        # 41口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/41' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
        tn.write(b'switchport access vlan 41' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/41)#')
        tn.write(b'exit' + b'\n')
        # 42口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/42' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
        tn.write(b'switchport access vlan 42' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/42)#')
        tn.write(b'exit' + b'\n')
        # 43口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/43' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
        tn.write(b'switchport access vlan 43' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/43)#')
        tn.write(b'exit' + b'\n')
        # 44口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/44' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
        tn.write(b'switchport access vlan 44' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/44)#')
        tn.write(b'exit' + b'\n')
        # 45口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/45' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
        tn.write(b'switchport access vlan 45' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/45)#')
        tn.write(b'exit' + b'\n')
        # 46口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/46' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
        tn.write(b'switchport access vlan 46' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/46)#')
        tn.write(b'exit' + b'\n')
        # 47口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/47' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
        tn.write(b'switchport access vlan 47' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/47)#')
        tn.write(b'exit' + b'\n')
        # 48口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/48' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
        tn.write(b'switchport access vlan 48' + b'\n')
        tn.read_until(b'ST3552F(config-if-ethernet1/0/48)#')
        tn.write(b'exit' + b'\n')

        # 4、 1-4 接AP设置为trunk 允许 vlan1，1000，1999
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/1-4' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode trunk' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')

        #5、判断wan1口、lan1口 接线口
        #wan1口设置为和上联口7口相连，
        wan1num = swNum[:2]
        cmd = 'interface ethernet 1/0/' + wan1num + ';7'
        cmd = bytes(cmd,encoding='utf8')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        # lan1口设置为vlan1
        lan1num = swNum[-2:]
        cmd = 'interface ethernet 1/0/' + lan1num
        cmd = bytes(cmd, encoding='utf8')
        cmd2 = 'ST3552F(config-if-ethernet1/0/%s)#' % lan1num
        cmd2 = bytes(cmd2, encoding='utf8')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(cmd2)
        tn.write(b'switchport mode trunk' + b'\n')
        tn.read_until(cmd2)
        tn.write(b'switchport trunk allowed vlan 1,1000,1999' + b'\n')
        tn.read_until(cmd2)
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

        # vlan1
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
        if 'Ethernet1/0/1' and 'Ethernet1/0/2' and ('Ethernet1/0/%s' % lan1num) in result1:
            print('port 1/2/lan in vlan 1')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 1 or 2 or lan1num not in vlan 1')
            raise Exception(u'port 1 or 2 or lan1num not in vlan 1')
        tn.close()
        # vlan7
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'show vlan id 7' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/7' and ('Ethernet1/0/%s' % wan1num) in result1:
            print('port 7/lan in vlan 1')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 7 or wan1num not in vlan 1')
            raise Exception(u'port 7 or wan1num not in vlan 1')
        tn.close()
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
        if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
            print('port 1/2/lan1num in vlan 1000')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 1 or 2 or lan1num not in vlan 1000')
            raise Exception(u'port 1 or 2 or lan1num not in vlan 1000')
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
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        if 'Ethernet1/0/1(T)' and 'Ethernet1/0/2(T)' and ('Ethernet1/0/%s' % lan1num) in result1:
            print('port 1/2/lan1num in vlan 1999')
        else:
            logger.info(u'result1: %s' % result1)
            logger.info(u'port 1 or 2 or lan1num not in vlan 1999')
            raise Exception(u'port 1 or 2 or lan1num not in vlan 1999')

        tn.close()
        logger.info(u'交换机vlan接口 初始化完成')

    def test_changeWAN2(self):
        u'''调整wan2 与上联口 互通'''
        #通过swNum2判断 归属于组几，同时调整wan1、wan2与上联口互通
        #设置wan1wan2 与 上联口 同属于vlan7

        swNum = swNum2()  # 获取当前设备wan/lan接口号

        # 判断wan1口、wan2口 接线口
        #wan1wan2口设置为和上联口7口相连
        wan1num = swNum[:2]
        wan2num = swNum[2:4]
        cmd = 'interface ethernet 1/0/' + wan1num + '-' +wan2num
        cmd = bytes(cmd, encoding='utf8')
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 7' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/%s' % wan1num,'Ethernet1/0/%s' % wan2num,'Ethernet1/0/7']
        for x in inter:
            if x in result1:
                print('port wan1/wan2/7 in vlan 7')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port wan1/wan2/7 in vlan7')
                raise Exception(u'port wan1/wan2/7 not in vlan 7')
        tn.close()
        logger.info(u'调整wan2 与上联口 互通 完成')

    def test_changeWAN3(self):
        u'''调整wan1\wan2\wan3 与上联口 互通'''
        #通过swNum2判断 归属于组几，同时调整wan1、wan2、wan3与上联口互通
        #设置wan1wan2 \wan3 与 上联口 同属于vlan7

        swNum = swNum2()  # 获取当前设备wan/lan接口号

        wan1num = swNum[:2]
        wan2num = swNum[2:4]
        wan3num = swNum[4:6]
        cmd = 'interface ethernet 1/0/' + wan1num + '-' + wan3num
        cmd = bytes(cmd, encoding='utf8')
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 7' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/%s' % wan1num, 'Ethernet1/0/%s' % wan2num,'Ethernet1/0/%s' % wan3num, 'Ethernet1/0/7']
        for x in inter:
            if x in result1:
                print('port wan1/wan2/wan3/7 in vlan 7')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port wan1/wan2/wan3/7 in vlan7')
                raise Exception(u'port wan1/wan2/wan3/7 not in vlan 7')
        tn.close()
        logger.info(u'调整wan3 与上联口 互通 完成')

    def test_changeWAN4(self):
        u'''调整wan2/wan3/wan4 与上联口 互通'''
        # 通过swNum2判断 归属于组几，同时调整wan1、wan2、wan3\wan4与上联口互通
        # 设置wan1wan2 \wan3\wan4 与 上联口 同属于vlan7

        swNum = swNum2()  # 获取当前设备wan/lan接口号

        wan1num = swNum[:2]
        wan2num = swNum[2:4]
        wan3num = swNum[4:6]
        wan4num = swNum[6:8]
        cmd = 'interface ethernet 1/0/' + wan1num + '-' + wan4num
        cmd = bytes(cmd, encoding='utf8')
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 7' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/%s' % wan1num, 'Ethernet1/0/%s' % wan2num, 'Ethernet1/0/%s' % wan3num,
                 'Ethernet1/0/%s' % wan4num, 'Ethernet1/0/7']
        for x in inter:
            if x in result1:
                print('port wan1/wan2/wan3/wan4/7 in vlan 7')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port wan1/wan2/wan3/wan4/7 in vlan7')
                raise Exception(u'port wan1/wan2/wan3/wan4/7 not in vlan 7')
        tn.close()
        logger.info(u'调整wan4 与上联口 互通 完成')

    def test_changeWAN5(self):
        u'''调整wan2\wan3\wan4\wan5 与上联口 互通'''
        # 通过swNum2判断 归属于组几，同时调整wan1、wan2、wan3\wan4\wan5与上联口互通
        # 设置wan1wan2 \wan3\wan4\wan5 与 上联口 同属于vlan7

        swNum = swNum2()  # 获取当前设备wan/lan接口号

        wan1num = swNum[:2]
        wan2num = swNum[2:4]
        wan3num = swNum[4:6]
        wan4num = swNum[6:8]
        wan5num = swNum[8:10]
        cmd = 'interface ethernet 1/0/' + wan1num + '-' + wan5num
        cmd = bytes(cmd, encoding='utf8')
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(b'config' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(cmd + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'show vlan id 7' + b'\n')
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[1:]
        # print('result1', result1)
        inter = ['Ethernet1/0/%s' % wan1num, 'Ethernet1/0/%s' % wan2num, 'Ethernet1/0/%s' % wan3num,
                 'Ethernet1/0/%s' % wan4num, 'Ethernet1/0/%s' % wan5num,'Ethernet1/0/7']
        for x in inter:
            if x in result1:
                print('port wan1/wan2/wan3/wan4/wan5/7 in vlan 7')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port wan1/wan2/wan3/wan4/wan5/7 in vlan7')
                raise Exception(u'port wan1/wan2/wan3/wan4/wan5/7 not in vlan 7')
        tn.close()
        logger.info(u'调整wan5 与上联口 互通 完成')

    def test_LanToWan(self):
        u'''调整PC接线口 与上联口/wan1口 互通'''
        # 交换机11、12口接测试pc
        # 设置11/12口与 上联口/wan1口 同属于vlan7

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
        tn.write(b'interface ethernet 1/0/11-12' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 7' + b'\n')
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
        logger.info(u'设置11、12口与 上联口/wan1口 完成')

    def test_WanToLan(self):
        u'''PC口改回与lan口 互通'''
        # 交换机11、12口与pc口相连
        # 设置11、12改回没有vlan，lanToWan之后，需要交换机上设置7vlan的虚接口才能再登录

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
        # 11 - 12口
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/11-12' + b'\n')
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

        swNum = swNum2()  # 获取当前设备wan/lan接口号
        lan1num = swNum[10:]
        cmd = 'show interface ethernet 1/0/' + lan1num
        cmd = bytes(cmd, encoding='utf8')
        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(cmd + b'\n')
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

        swNum = swNum2()  # 获取当前设备wan/lan接口号
        wan1num = swNum[:2]
        cmd = 'show interface ethernet 1/0/' + wan1num
        cmd = bytes(cmd, encoding='utf8')
        # telnet交换机
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'ST3552F#')
        tn.write(cmd + b'\n')
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
        # 1、2 为一组v1、v2 AP，改为Acess vlan1000
        # 3、4 为一组v1、v2 AP，改为Acess vlan1999

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
        # 1-1 接AP,改为trunk vlan 1000
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/1-2' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport mode access' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'switchport access vlan 1000' + b'\n')
        tn.read_until(b'ST3552F(config-if-port-range)#')
        tn.write(b'exit' + b'\n')
        # 3-4 接AP,改为trunk vlan 1999
        tn.read_until(b'ST3552F(config)#')
        tn.write(b'interface ethernet 1/0/3-4' + b'\n')
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
        inter = ['Ethernet1/0/1', 'Ethernet1/0/2']
        for x in inter:
            if x in result1:
                print('port 1/2 in vlan 1000')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 1/2 not in vlan 1000')
                raise Exception(u'port 1/2 not in vlan 1000')
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
        inter = ['Ethernet1/0/3', 'Ethernet1/0/4']
        for x in inter:
            if x in result1:
                print('port 3/4 in vlan 1999')
            else:
                logger.info(u'result1: %s' % result1)
                logger.info(u'port 3/4 not in vlan 1999')
                raise Exception(u'port 3/4 not in vlan 1999')
        tn.close()


    def tearDown(self):
        print('swconfig over')

# if __name__=='__main__':
#     unittest.main()


# test_initSwPortNext()