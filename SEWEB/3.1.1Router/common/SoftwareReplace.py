#! -*-conding:utf-8 -*-
#@Time: 2019/4/25 0025 11:03
#@swzhou
'''
telnet更换软件
'''

import time
import socket
import telnetlib
import subprocess
import win32process

from common.GetRouteCPU import getCPUmodel
from common.ReadConfig import getweb,gettelnet,getpath,getParameter
from common.LogGen import LogGen
from common.pingTest import pingTestIP
from common.swNumC import IFlicense
logger = LogGen(Logger= 'SoftwareReplace').getlog()

def softwareReplac(version = getweb('ReplaceVersion1')):
    # ReplaceVersion1 = getweb('ReplaceVersion1')
    hostip = gettelnet('host')
    port = gettelnet('port')
    licenseSN = getweb('licenseSN')
    username = bytes(getweb('User'), encoding="utf8")
    password = bytes(getweb('Passwd'), encoding="utf8")
    pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
    CPUmodel = getCPUmodel()
    license = IFlicense(version)
    # print(license)

    # 打开tftp32.exe,
    # 注意：tftp32打开后的目录是由 由哪个脚本执行 所在的路径决定
    # 直接运行该脚本，则tftp32的目录是‘test_003_udp69’所在的‘D:\python\SEWEB\3.1.1Router\test_case\Port_mapping’
    # 由all_test.py或者ProductModel_test.py调用执行，则目录为‘D:\python\SEWEB\3.1.1Router\run’
    # 因此 需把握好 对应目录中包含上传的文件，此脚本设定上传的文件为'tftpd32.exe'
    handle = win32process.CreateProcess(r"D:\python\SEWEB\3.1.1Router\test_case\tftpd32.exe", '', None,
                                        None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                        win32process.STARTUPINFO())  # 打开tftp32.exe，获得其句柄
    time.sleep(2)
    if CPUmodel == 'X86':
        if '.img' not in version:
            raise Exception(u'X86设备需要 img文件')
    elif '.bin' not in version:
        version = version + '.bin'
    VersionCmd = bytes(('tftp -gr ' + version + ' ' +pcaddr + ' 69'), encoding='utf8')

    tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(VersionCmd + b'\n')
    tn.read_until(b'#')
    if CPUmodel == 'MTK' or CPUmodel == 'Qualcomm':
        mtdwriteCmd = bytes(('mtd_write write ' + version + ' Kernel'), encoding='utf8')
        tn.write(mtdwriteCmd + b'\n')
        tn.read_until(b'#')
    elif CPUmodel == 'P1010':
        mtdCmd = bytes(('tftp -gr mtd_write_p1010 ' + pcaddr + ' 69'), encoding='utf8')
        tn.write(mtdCmd + b'\n')
        tn.write(b'chmod 777 mtd_write_p1010' + b'\n')
        tn.read_until(b'#')
        mtdwriteCmd = bytes(('./mtd_write_p1010 write ' + version + ' Kernel'), encoding='utf8')
        tn.write(mtdwriteCmd + b'\n')
        tn.read_until(b'#')
    elif CPUmodel == 'X86':
        writeCmd = bytes(('dd if=' + version + ' of=/dev/sda'), encoding='utf8')
        tn.write(writeCmd + b'\n')
        tn.read_until(b'#')
    tn.write(b'ls' + b'\n')
    tn.read_until(b'#')
    #如果支持license 重置license分区且修改序列号为 licenseSN
    if license == '1':
        mtdwriteCmd = bytes(('tftp -gr license ' + pcaddr + ' 69'), encoding='utf8')
        tn.write(mtdwriteCmd + b'\n')
        tn.read_until(b'#')
        tn.write(b'dd if=license of=/dev/sda3' + b'\n')
        tn.read_until(b'#')
        mtdwriteCmd = bytes(('tftp -gr uttsn_x86_new ' + pcaddr + ' 69'), encoding='utf8')
        tn.write(mtdwriteCmd + b'\n')
        tn.read_until(b'#')
        tn.write(b'chmod 777 uttsn_x86_new' + b'\n')
        tn.read_until(b'#')
        mtdwriteCmd = bytes(('./uttsn_x86_new ' + licenseSN), encoding='utf8')
        tn.write(mtdwriteCmd + b'\n')
        tn.read_until(b'#')
    tn.write(b'reboot' + b'\n')
    time.sleep(40)

    win32process.TerminateProcess(handle[0], 0)  # 关闭tftp32，注意脚本执行前关闭所有的tftp32进程 否则不能关闭会报错

    i = 0
    while i < 30:
        p = pingTestIP()
        if p == 'N':
            time.sleep(1)
            print(i)
            i += 1
        else:
            time.sleep(10)  # 多等待10s
            break

    else:
        logger.info(u'telnet更换软件后无法ping通 设备')
        raise Exception(u'telnet更换软件后无法ping通 设备')


#
# softwareReplac('ER742GV3v3.1.4-190827-133649.bin')
