#! -*-conding:utf-8 -*-
#@Time: 2019/6/25 0025 18:37
#@swzhou
'''
license
'''

import os
import sys
import time
import telnetlib
import socket
import unittest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb,getpath
from common.loginRoute import login
from pages.Loginpage import LoginPage
from pages.sysConfig_003_MaintenancePage import MaintenancePage
logger = LogGen(Logger = 'sysConfig_011_license').getlog()
licensefile = os.path.dirname(os.path.abspath('.')) + '/script/licensefile/'

def getlicensefile():
    # telnet获取接口名称及确认默认路由
    licenseSN = getweb('licenseSN')
    hostip = gettelnet('host')
    port = gettelnet('port')
    username = bytes(getweb('User'), encoding="utf8")
    password = bytes(getweb('Passwd'), encoding="utf8")
    # 判断SN
    tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(b'uttcli get_uttsn' + b'\n')
    # 输出结果，判断
    time.sleep(1)
    result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    print('result:', result)
    # 获取WAN口对应接口名称
    sn = result.split(r'\r\n')[1][:-3]
    print(sn)
    if sn != licenseSN:
        raise Exception('设备的序列号 不为licenseSN值，license文件不能导入')
    tn.close()
    # 判断SN
    tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
    tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
    tn.read_until(b'login:')
    tn.write(username + b"\n")
    tn.read_until(b'Password:')
    tn.write(password + b"\n")
    # 登录完毕后执行命令
    tn.read_until(b'#')
    tn.write(b"uname -a" + b'\n')
    # 输出结果，判断
    time.sleep(1)
    result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
    print('-------------------输出结果------------------------')
    # 命令执行结果
    print('result:', result)
    # 获取WAN口对应接口名称
    model = result.split(r'\r\n')[1].split(r' ')[4][2:]
    print(model)

    sys.path.append(r'%s' % licensefile)
    files_lic = os.listdir(r'%s' % licensefile)  # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
    for filename_lic in files_lic:
        portion_lic = os.path.splitext(filename_lic)  # splitext()用于返回 文件名和扩展名 元组
        # print(portion_xml)
        if model in portion_lic[0] and '-1-1' in portion_lic[0]:  # 如果文件名包含 当前设备型号 且 选择第一个license
            if portion_lic[1] == '.lic':  # 后缀是 .xml
                # 重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                licensefilenow = (r'%s' % licensefile) + filename_lic
    return licensefilenow


class license(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_loginLicense(self):
        u'''登录页面的license'''

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        login_page = LoginPage(self.driver, self.url)
        try:
            self.driver.implicitly_wait(1)
            login_page.flid_chooseFile()
        except NoSuchElementException:
            pass
        else:
            # telnet获取接口名称及确认默认路由
            licenseSN = getweb('licenseSN')
            hostip = gettelnet('host')
            port = gettelnet('port')
            username = bytes(getweb('User'), encoding="utf8")
            password = bytes(getweb('Passwd'), encoding="utf8")
            # 判断SN
            tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'uttcli get_uttsn' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 获取WAN口对应接口名称
            sn = result.split(r'\r\n')[1][:-3]
            print(sn)
            if sn != licenseSN:
                raise Exception('设备的序列号 不为licenseSN值，license文件不能导入')
            tn.close()
            # 判断SN
            tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b"uname -a| awk '{print $5}'" + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 获取WAN口对应接口名称
            model = result.split(r'\r\n')[1][2:]
            print(model)

            sys.path.append(r'%s' % licensefile)
            files_lic = os.listdir(r'%s' % licensefile)  # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
            for filename_lic in files_lic:
                portion_lic = os.path.splitext(filename_lic)  # splitext()用于返回 文件名和扩展名 元组
                # print(portion_xml)
                if model in portion_lic[0] and '-1-1' in portion_lic[0]:  # 如果文件名包含 当前设备型号 且 选择第一个license
                    if portion_lic[1] == '.lic':  # 后缀是 .xml
                        # 重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                        licensefilenow = (r'%s' % licensefile) + filename_lic

            self.driver.find_element_by_xpath(login_page.updatesoftware).send_keys(licensefilenow)
            time.sleep(1)
            login_page.click_innerput()
            time.sleep(2)
            login_page.click_ok()
            time.sleep(1)


        self.driver.quit()
        logger.info('test_reboot1 passed')

    def test_002_license(self):
        u'''登录页面的license'''

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        maintenance = MaintenancePage(self.driver, self.url)
        maintenance.click_sysConfig()
        time.sleep(0.5)
        maintenance.click_Maintenance()
        time.sleep(1)
        maintenance.click_license()
        time.sleep(1)

        filename = ('//*[@id="iframe5"]/table/tbody/tr[6]/td[2]/input[2]')
        licensefilenow = getlicensefile()
        self.driver.find_element_by_xpath(filename).send_keys(licensefilenow)
        time.sleep(0.5)
        maintenance.click_innerput()
        time.sleep(100)




        self.driver.quit()
        logger.info('test_reboot1 passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
