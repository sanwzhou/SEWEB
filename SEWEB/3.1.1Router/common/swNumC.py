#! -*-conding:utf-8 -*-
#@Time: 2019/6/14 0014 13:35
#@swzhou
'''
判断设备的wan、lan对应的 交换机端口

'''
import time
import telnetlib
from configparser import NoOptionError

from common.ReadConfig import getweb,gettelnet
host = gettelnet('host')
port = gettelnet('port')
username = bytes(getweb('User'), encoding="utf8")
password = bytes(getweb('Passwd'), encoding="utf8")

mtk7620Llist = ['nv518GV2', 'ER742GV2', 'nv518GP', 'nv521GV3', 'ER745GV2', 'nv840GV3', 'nv810G', 'ER1500G',
                    'nv850G', 'nv1200GWV2', 'ER758GWV2','TL-BWR-21']
mtkOtherlist = ['nv510v5', 'nv510v6.1', 'ER741v2', 'ER741V3', 'ER741v3.1', 'nv510G', 'ER741G', 'nv520V4', 'nv520V5',
                'nv528GP', 'nv810V6', 'nv518GV3', 'ER742GV3', 'nv512Wv4', 'ER741Wv2', 'nv518WV5', 'nv518Wv4', 'ER748W','nv750Wv2',
                'ER742Wv2', 'nv1200W', 'ER758W', 'mv1200WV2','A908V3','nv512Wv4.2', 'nv810Gv2', 'ER1500GV2','nv510GV2','ER741GV2',
                'nvA655W']
QCAlist = ['512Wv5', 'ER741Wv3', '750Wv3', 'mv1200WV2', 'ER758Wv2', 'mv1250GW', 'ER762GW', 'mv1250GWv2']
p1010list = ['QV1210G', 'QV1220G', 'QV2620G', 'er1520G', 'QV3320Gv2', 'QV2610G', 'QV4220G', 'QV4240G', 'er5240G',
             'QV3640G', 'QV4840GV2.0', 'QVU3000', 'QVU4000', 'QVN800', 'QVNE1200V3.0', 'QVN1800V3.0','er5220G',
             'QV2620GS1', 'er1520GS1','QV4240GS1', 'er5240GS1', 'QV4220GS1', 'er5520GS1']
j1800list = ['lv4250G', 'ER5250G', 'lv4330Gv2', 'lv6530Gv5', 'ER5530Gv2']
# 支持license的j1800
j1800list2 = ['lv5830GV5', 'lv6830GV5', 'lvU5000V2', 'lvU6000V2', 'lvNE2200V4', 'lvNE4000V4', 'lvNE6000V5']
D525list = ['lv4330GV1', 'lv6530GV4', 'ER5530G', 'lv5830GV4', 'lv6830GV4', 'lvU5000V3', 'lvU6000V3',
            'lv2200V3', 'lv4000V3', 'lv6000V4']
i3list = ['lv6550G', 'ER5550G']

def swNum1():
    #下一个要升级的型号对应的lan/wan

    #1、判断当前路由器版本
    tn = telnetlib.Telnet(host=host, port=port)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    # 输入登录用户名
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(b"uname -a" + b'\n')
    # 输出结果，判断
    time.sleep(1)
    result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    # print('result:', result)
    nowVersion = result.split(r'\r\n')[1].split(r' ')[4]
    print(nowVersion)
    tn.close()  # tn.write('exit\n')
    #2、对比判断当前版本 是测试型号中的第几个
    n = 1
    while True:
        try:
            SoftVersion = getweb('SoftVersion' + str(n))
        except NoOptionError:
            raise Exception('未在config中找到对应版本')
        if nowVersion in SoftVersion:
            num = n + 1
            break
        else:
            n += 1
    print(n)
    SoftVersion = getweb('SoftVersion' + str(num))
    if 'v3.0.' in SoftVersion:
        SoftVersion1 = str(SoftVersion).split(r'v3.0.')[0]
    elif 'v3.1.' in SoftVersion:
        SoftVersion1 = str(SoftVersion).split(r'v3.1.')[0]
    elif 'v3.2.' in SoftVersion:
        SoftVersion1 = str(SoftVersion).split(r'v3.2.')[0]
    else:
        raise Exception('版本号超出当前设定')

    if SoftVersion1 in mtk7620Llist: #nv810Gv2为other、nv810G为-L,如果设备是nv810G可能会被误认为是oter，所以-l放前
        print('zu2')
        # Rport = [19, 20, 21, 22, 23, 24]
        return '192021222324'
    elif SoftVersion1 in mtkOtherlist:
        print('zu1')
        # Rport = [13, 14, 15, 16, 17, 18]
        return '131415161718'
    elif SoftVersion1 in QCAlist:
        print('zu3')
        # Rport = [25, 26, 27, 28, 29, 30]
        return '252627282930'
    elif SoftVersion1 in p1010list:
        print('zu4')
        # Rport = [31, 32, 33, 34, 35, 36]
        return '313233343536'
    elif SoftVersion1 in D525list:
        print('zu5')
        # Rport = [37, 38, 39, 40, 41, 42]
        return '373839404142'
    elif SoftVersion1 in j1800list or SoftVersion1 in j1800list2 or SoftVersion1 in i3list:
        print('zu6')
        # Rport = [43, 44, 45, 46, 47, 48]
        return '434445464748'
    else:
        raise Exception('未找到该型号对应的接口')

def swNum2():
    #当前型号对应的lan/wan

    #1、判断当前路由器版本
    tn = telnetlib.Telnet(host=host, port=port)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    # 输入登录用户名
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(b"uname -a" + b'\n')
    # 输出结果，判断
    time.sleep(1)
    result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    # print('result:', result)
    nowVersion = result.split(r'\r\n')[1].split(r' ')[4]
    print('nowVersion:',nowVersion)
    tn.close()  # tn.write('exit\n')

    if nowVersion in mtk7620Llist: #nv810Gv2为other、nv810G为-L,如果设备是nv810G可能会被误认为是oter，所以-l放前
        print('zu2')
        # Rport = [19, 20, 21, 22, 23, 24]
        return '192021222324'
    elif nowVersion in mtkOtherlist:
        print('zu1')
        # Rport = [13, 14, 15, 16, 17, 18]
        return '131415161718'
    elif nowVersion in QCAlist:
        print('zu3')
        # Rport = [25, 26, 27, 28, 29, 30]
        return '252627282930'
    elif nowVersion in p1010list:
        print('zu4')
        # Rport = [31, 32, 33, 34, 35, 36]
        return '313233343536'
    elif nowVersion in D525list:
        print('zu5')
        # Rport = [37, 38, 39, 40, 41, 42]
        return '373839404142'
    elif nowVersion in j1800list or nowVersion in j1800list2 or nowVersion in i3list:
        print('zu6')
        # Rport = [43, 44, 45, 46, 47, 48]
        return '434445464748'
    else:
        raise Exception('未找到该型号对应的接口')


def IFlicense(version):
    #判断下一个型号是否支持license

    # 支持license的j1800 j1800list2

    # #1、判断当前路由器版本
    # tn = telnetlib.Telnet(host=host, port=port)
    # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    # # 输入登录用户名
    # tn.read_until(b'login:')
    # tn.write(username + b"\n")
    # tn.read_until(b'Password:')
    # tn.write(password + b"\n")
    # # 登录完毕后执行命令
    # tn.read_until(b'#')
    # tn.write(b"uname -a" + b'\n')
    # # 输出结果，判断
    # time.sleep(1)
    # result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
    # print('-------------------输出结果------------------------')
    # # 命令执行结果
    # # print('result:', result)
    # nowVersion = result.split(r'\r\n')[1].split(r' ')[4]
    # print('nowVersion:',nowVersion)
    # tn.close()  # tn.write('exit\n')
    #
    # # 2、对比判断当前版本 是测试型号中的第几个
    # n = 1
    # while True:
    #     try:
    #         SoftVersion = getweb('SoftVersion' + str(n))
    #     except NoOptionError:
    #         raise Exception('未在config中找到对应版本')
    #     if nowVersion in SoftVersion:
    #         num = n + 1
    #         break
    #     else:
    #         n += 1
    # print(n)
    # SoftVersion = getweb('SoftVersion' + str(num))
    # SoftVersion1 = str(SoftVersion).split(r'v3.1.')[0]
    for  x in j1800list2:
        if x in version:
            print('支持license')
            # Rport = [43, 44, 45, 46, 47, 48]
            return '1'


# aaa=IFlicense()
# print(aaa)