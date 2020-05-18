#! -*-conding:utf-8 -*-
#@Time: 2019/4/11 0011 16:44
#@swzhou
'''
从路由器后台判断设备CPU型号
'''

import time
import telnetlib
from common.ReadConfig import gettelnet,getweb

def getCPUmodel():
    host = gettelnet('host')
    port = gettelnet('port')
    username = bytes(getweb('User'), encoding="utf8")
    password = bytes(getweb('Passwd'), encoding="utf8")

    tn = telnetlib.Telnet(host=host, port=port,timeout=10)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    # 输入登录用户名
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(b"cat /proc/cpuinfo" + b'\n')
    # 输出结果，判断
    time.sleep(1)
    result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    print('result:', result)
    # 判断
    if "system type             : MT762" in result:
        CPUmodel = 'MTK'
    elif "model name      : Intel" in result:
        CPUmodel ='X86'
    elif "platform        : P1010" in result:
        CPUmodel ='P1010'
    elif "system type             : Qualcomm" in result:
        CPUmodel ='Qualcomm'
    else:
        raise Exception('平台判断出错')
    tn.close()  # tn.write('exit\n')

    return CPUmodel

# print(getCPUmodel())