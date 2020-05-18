#! -*-conding:utf-8 -*-
#@Time: 2019/3/5 0005 15:55
#@swzhou
'''
负载均衡
'''

import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet,getweb
from common.loginRoute import login
from pages.AC_004_loadBalancingPage import loadBalancingPage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
logger = LogGen(Logger = 'AC_005_loadBalancing').getlog()

class loadBalancing(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # pass

    def test_001_open(self):
        u'''启用负载均衡'''
        v1APname = getweb('v1APname')
        OnlineA = getAssertText('OnlineA')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        device = deviceMgmtPage(self.driver, self.url)
        #1 查看未启用负载均衡
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        # 点击管理通讯协议，v2在上
        device.click_Priorityv2()
        time.sleep(1)
        # 先确认AP均上线
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
                print('channel1=', channel1, 'channel2=', channel2, 'channel3=', channel3, 'channel4=', channel4, x)
                if channel1 != '' and channel2 != '' and channel3 != '' and channel4 != '':
                    print('4台AP2.4G无线接口已同步', x)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            x = x + 1
        else:
            CapPic(self.driver)
            logger.info(u'AP  未能同步2.4G无线接口')
            raise Exception('AP  未能同步2.4G无线接口')
        #获取 wa3000N的IP
        device.input_search(v1APname)
        device.click_searchB()
        list_ip1 = device.getText_byXpath(device.list_IP1)
        #telnet
        tn = telnetlib.Telnet(host=list_ip1, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config | grep uttMaxStaNum' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if ("uttMaxStaNum:       0"  in result) or( "uttMaxStaNum:       32") in result:
            logger.info(u'负载均衡未开启 AP资源数正常')
        else:
            logger.info(u'负载均衡未开启 AP资源数异常')
            logger.info('result:', result)
            raise Exception('负载均衡未开启 AP资源数异常')
        tn.close()  # tn.write('exit\n')

        #2 开启负载均衡
        enableA = getAssertText('enableA')
        load = loadBalancingPage(self.driver, self.url)
        load.click_loadBalancing()
        time.sleep(1)
        load.click_add()
        time.sleep(1)
        load.input_loadBalanceNames('test')
        load.click_selAP1()
        load.click_toright()
        time.sleep(0.5)
        load.click_selAP1()
        load.click_toright()
        time.sleep(0.5)
        load.click_selAP1()
        load.click_toright()
        time.sleep(0.5)
        load.click_selAP1()
        load.click_toright()
        time.sleep(0.5)
        load.click_save()
        time.sleep(1)
        liststate = load.getText_byXpath(load.list_state)
        self.assertEqual(liststate,enableA,msg='AP负载均衡未启用')
        checkOpens = load.getAttribute_byId(load.checkOpens,'checktype') #1开启，0关闭
        self.assertEqual(checkOpens,'0',msg='负载均衡 开关默认未关闭')
        load.click_checkOpen()
        time.sleep(1)
        checkOpens = load.getAttribute_byId(load.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '1', msg='负载均衡 开启失败')
        time.sleep(10)

        tn = telnetlib.Telnet(host=list_ip1, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config | grep uttMaxStaNum' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if ("uttMaxStaNum:       0") not in result and ("uttMaxStaNum:       32") not in result:
            logger.info('负载均衡开启 AP资源数正常')
        else:
            logger.info('负载均衡开启 AP资源数异常')
            print('result:', result)
            logger.info('result:', result)
            raise Exception('负载均衡开启 AP资源数异常')
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_001_open passed')

    def test_002_close(self):
        u'''关闭负载均衡'''
        v1APname = getweb('v1APname')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        device.input_search(v1APname)
        device.click_searchB()
        list_ip1 = device.getText_byXpath(device.list_IP1)

        load = loadBalancingPage(self.driver, self.url)
        load.click_loadBalancing()
        time.sleep(1)
        load.click_checkOpen()
        time.sleep(1)
        checkOpens = load.getAttribute_byId(load.checkOpens, 'checktype')
        self.assertEqual(checkOpens, '0', msg='负载均衡 关闭失败')
        time.sleep(8)

        tn = telnetlib.Telnet(host=list_ip1, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'iwpriv ra0 get Config | grep uttMaxStaNum' + b'\n')  # 无线隔离
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        # print('result:', result)
        # 判断
        if "uttMaxStaNum:       32" in result:
            logger.info('负载均衡关闭 AP资源数正常')
        else:
            logger.info('负载均衡关闭 AP资源数异常')
            logger.info('result:', result)
            raise Exception('负载均衡关闭 AP资源数异常')
        tn.close()  # tn.write('exit\n')

        self.driver.quit()
        logger.info('test_002_close passed')



    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
