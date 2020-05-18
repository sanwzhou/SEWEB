#! -*-conding:utf-8 -*-
#@Time: 2019/1/2 0002 17:26
#@swzhou
'''
双线路接入：
固定+固定IP接入
双固定IP接入时的线路切换：主、备份线路
固定IP+PPPOE拨号上网
PPPOE+PPPOE接入上网以及线路切换
'''

import time
import unittest
import telnetlib
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,ElementNotVisibleException,ElementNotInteractableException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.swconfig import swconfig
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,gettelnet,getweb
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'NetworkConfig_001_2WAN').getlog()

class Config_2WAN(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        #进入网络配置-外网配置
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # pass

    def test_000_getReady(self):
        u'''更改wan口数量 以及设置wan2与上联口互通'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        #1、 动态wan口，调整wan口数量
        wan_config.click_GlobalConfig()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            wan_config.find_PortNumber()
        except ElementNotVisibleException:
            logger.info(u'页面没有wan口数量调整，不支持动态WAN口')
        except ElementNotInteractableException:
            logger.info(u'页面没有wan口数量调整，不支持动态WAN口')
        else:
            selPortNumber = wan_config.selelement_byName(wan_config.selPortNumber)
            Select(selPortNumber).select_by_value('2')
            time.sleep(2)
            try:
                wan_config.find_cfm_ok()
            except NoSuchElementException:
                logger.info(u'WAN口数量已为2')
            else:
                time.sleep(30)
                i = 0
                while i < 20:
                    now_url = str(self.driver.current_url)
                    # print(now_url,i)
                    if '/noAuth/login.html' not in now_url:  # 如果不同
                        time.sleep(5)
                    else:
                        break
                    i += 1
                else:
                    raise Exception('更改设备wan口数量后未正常启动')
        self.driver.quit()
        #2 调整wan2 与上联口互通
        swconfig.test_changeWAN2(self)
        logger.info('test_000_getReady passed')

    def test_001_static(self):
        u'''固定+固定IP接入'''
        # 获取2条外线的链接类型
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        linetype = getAssertText('DHCPline')
        ConnectState = getAssertText('ConnectState')
        line1_type = wan_config.getText_byXpath(wan_config.line1Type)
        line2_type = wan_config.getText_byXpath(wan_config.line2Type)
        # 先改为动态接入，得到正确的IP地址及网关地址
        # WAN1
        if str(line1_type) != linetype:
            wan_config.click_line1edit()
            time.sleep(1)
            access_mode = wan_config.selelement_byName(wan_config.connectionType)
            Select(access_mode).select_by_value('DHCP')
            wan_config.click_save()
            time.sleep(10)  # 修改接口后 可能会回到登录页面 所以关闭，再打开
            self.driver.quit()
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            wan_config = NetworkConfig_wanpage(self.driver, self.url)
            wan_config.click_NetworkConfig()
            time.sleep(0.5)
            wan_config.click_WANconfig()
            time.sleep(1)
        else:
            print('wan1 动态接入')
        if str(line2_type) != linetype:
            wan_config.click_line2edit()
            time.sleep(1)
            access_mode = wan_config.selelement_byName(wan_config.connectionType)
            Select(access_mode).select_by_value('DHCP')
            wan_config.click_save()
            time.sleep(10)  # 修改接口后 可能会回到登录页面 所以关闭，再打开
            self.driver.quit()
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            wan_config = NetworkConfig_wanpage(self.driver, self.url)
            wan_config.click_NetworkConfig()
            time.sleep(0.5)
            wan_config.click_WANconfig()
            time.sleep(1)
        else:
            print('wan2 动态接入')
        #断言
        n = 0
        while n < 30:
            wan_config.click_refresh()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            print(str(list_connectState1), str(list_connectState2))
            list_connectState = [str(list_connectState1), str(list_connectState2)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in  list_connectState):
                print('WAN口均已获取到地址', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未获取到地址')

        #获取两个wan口IP、网关、mac
        WAN1_ip = wan_config.getText_byXpath(wan_config.line1IP)
        WAN2_ip = wan_config.getText_byXpath(wan_config.line2IP)
        # print('WAN1_ip=',WAN1_ip)
        WAN1_gw = wan_config.getText_byXpath(wan_config.line1gw)
        WAN2_gw = wan_config.getText_byXpath(wan_config.line2gw)
        # print('WAN1_gw=',WAN1_gw)
        WAN1_dns = wan_config.getText_byXpath(wan_config.line1Dns)
        WAN2_dns = wan_config.getText_byXpath(wan_config.line2Dns)
        # print('WAN1_dns=',WAN1_dns)
        line1_mac = str(wan_config.getText_byXpath(wan_config.line1Mac))
        # print('WAN1_dns=',line1_mac)
        line2_mac = str((wan_config.getText_byXpath(wan_config.line2Mac)))
        # print('WAN1_dns=',line2_mac)
        # self.driver.quit()

        # 改为固定接入
        # 将wan1口的IP/网关/dns 拿来输入
        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('STATIC')
        time.sleep(1)
        wan_config.input_staticIp(WAN1_ip)
        wan_config.input_staticGateway(WAN1_gw)
        wan_config.input_staticPriDns(WAN1_dns)
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        # WAN2
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line2edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('STATIC')
        time.sleep(1)
        wan_config.input_staticIp(WAN2_ip)
        wan_config.input_staticGateway(WAN2_gw)
        wan_config.input_staticPriDns(WAN2_dns)
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 断言
        n = 0
        while n < 30:
            wan_config.click_refresh_s()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            print(str(list_connectState1), str(list_connectState2))
            list_connectState = [str(list_connectState1), str(list_connectState2)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in list_connectState):
                print('WAN口均已连接', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未已连接')

        #处理wan口的mac地址
        #字母变大写
        line1_mac1=line1_mac.upper()
        line2_mac1 = line2_mac.upper()
        #加冒号
        line1_mac2=line1_mac1[0:2]+':'+line1_mac1[2:4]+':'+line1_mac1[4:6]+':'+line1_mac1[6:8]+':'+line1_mac1[8:10]+':'+line1_mac1[10:]
        line2_mac2=line2_mac1[0:2]+':'+line2_mac1[2:4]+':'+line2_mac1[4:6]+':'+line2_mac1[6:8]+':'+line2_mac1[8:10]+':'+line2_mac1[10:]
        print(line1_mac2,line2_mac2)

        #telnet获取接口名称及确认默认路由
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ifconfig | grep eth' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        #获取WAN口对应接口名称
        result1 = result[3:-9]
        # print(result1)
        result2 = result1.split(r'\r\n')
        print('result2:',result2)

        for i in range(len(result2)):
            if line1_mac2 in result2[i]:
                result2_num = (result2[i])
                # print(result2[i])
                line1_Interface_name = result2_num.split()[0]
                print(line1_Interface_name)
            if line2_mac2 in result2[i]:
                result2_num = (result2[i])
                # print(result2[i])
                line2_Interface_name = result2_num.split()[0]
                print(line2_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')
        #确认默认路由情况
        tn.write(b'ip route' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[2:-7]
        print('result1',result1)
        result2 = result1.split(r'\r\n')
        print('result2',result2)

        wan1route = 'dev '+ line1_Interface_name + ' weight '
        wan2route = 'dev ' + line2_Interface_name + ' weight '
        print('wan1route:',wan1route,'wan2route:',wan2route)

        for i in range(len(result2)):
            if wan1route in result2[i]:
                wan1route_status=not None
                print('wan1路由在')
            if wan2route in result2[i]:
                wan2route_status=not None
                print('wan2路由在')
        if wan1route_status ==None:
            raise Exception('wan1默认路由不存在')
        if wan2route_status ==None:
            raise Exception('wan2默认路由不存在')

        tn.close()  # tn.write('exit\n')
        self.driver.quit()
        logger.info('test_001_static passed')

    def test_002_backupLineSW(self):
        u'''双固定IP接入时的线路切换：主、备份线路'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        #1、获取wan1、wan2 网关及mac
        line1_mac = str(wan_config.getText_byXpath(wan_config.line1Mac))
        # print('WAN1_dns=',line1_mac)
        line2_mac = str(wan_config.getText_byXpath(wan_config.line2Mac))
        # print('WAN1_dns=',line2_mac)
        # 处理wan口的mac地址
        # 字母变大写
        line1_mac1 = line1_mac.upper()
        line2_mac1 = line2_mac.upper()
        # 加冒号
        line1_mac2 = line1_mac1[0:2] + ':' + line1_mac1[2:4] + ':' + line1_mac1[4:6] + ':' + line1_mac1[
                                                                                             6:8] + ':' + line1_mac1[
                                                                                                          8:10] + ':' + line1_mac1[
                                                                                                                        10:]
        line2_mac2 = line2_mac1[0:2] + ':' + line2_mac1[2:4] + ':' + line2_mac1[4:6] + ':' + line2_mac1[
                                                                                             6:8] + ':' + line2_mac1[
                                                                                                          8:10] + ':' + line2_mac1[
                                                                                                                        10:]
        print(line1_mac2, line2_mac2)

        #WAN1改为备份线路
        wan_config.click_line1edit()
        time.sleep(1)
        line_type = wan_config.selelement_byXpath(wan_config.line_type)
        Select(line_type).select_by_value('0')#1为主 0为备份
        wan_config.click_save()
        time.sleep(10)
        n = 0
        while n < 20:
            ping = pingTestIP()
            if ping != 'Y':
                time.sleep(1)
                n += 1
            else:
                break
        self.driver.quit()

        # telnet获取接口名称及确认默认路由（wan1备份应该只剩下wan2默认路由）
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ifconfig | grep eth' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN口对应接口名称
        result1 = result[3:-9]
        # print(result1)
        result2 = result1.split(r'\r\n')
        print('result2:', result2)

        for i in range(len(result2)):
            if line1_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2[i])
                line1_Interface_name = result2_num.split()[0]
                print(line1_Interface_name)
            if line2_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2[i])
                line2_Interface_name = result2_num.split()[0]
                print(line2_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')
        # 确认默认路由情况
        roure1 = bytes(('ip route | grep "%s"') % line2_Interface_name, encoding="utf8")
        tn.write(roure1 + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[2:-7]
        print('result1', result1)
        result2 = result1.split(r'\r\n')
        print('result2', result2)
        #wan1已备份，只剩wan2路由，这里只判断wan2的
        wan2route = 'dev ' + line2_Interface_name
        print('wan2route:', wan2route)

        for i in range(len(result2)):
            if 'default' in result2[i] and wan2route in result2[i]:
                wan2route_status=not None
                print('wan2路由在')
        if wan2route_status ==None:
            raise Exception('wan2默认路由显示有误')
        #单线路默认路由变为：default via 192.168.11.1 dev eth2.3 equalize 不再有weight值
        # (高通没有equalize)：default via 192.168.12.1 dev eth0.3
        #多线mtk
        # default equalize
        #    nexthop via 192.168.32.1  dev eth2.2 weight 1
        #    nexthop via 192.168.200.1  dev eth2.3 weight 1
        # 多线高通
        # default
        #    nexthop via 192.168.11.1  dev eth0.2 weight 1
        #    nexthop via 192.168.11.1  dev eth0.3 weight 1

        tn.close()  # tn.write('exit\n')

        #2、设置线路检测地址，验证线路切换
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        wan_config = NetworkConfig_wanpage(self.driver, self.url)

        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        #配置线路检测 检测3s 检测 3次，地址为223.5.5.5
        wan_config.click_GlobalConfig()
        time.sleep(1)
        wan_config.input_KeepLive1('3')
        wan_config.input_RetryTimes1('3')
        sel1 = wan_config.selelement_byName(wan_config.PriAddrType1)
        Select(sel1).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP1('223.5.5.5')

        wan_config.input_KeepLive2('3')
        wan_config.input_RetryTimes2('3')
        sel2 = wan_config.selelement_byName(wan_config.PriAddrType2)
        Select(sel2).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP2('1.2.3.4')#WAN2配一个ping不通的地址，测试线路切换
        wan_config.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wan_config.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wan_config.getAttribute_byClass(wan_config.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'线路检测保存 异常')
                    raise Exception(u'线路检测保存 异常')
                break
        else:
            raise Exception(u'线路检测保存 未弹出提示框')

        #切换标签页判断配置正确
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_GlobalConfig()
        time.sleep(1)
        KeepLive2 = str(wan_config.getAttribute_byName(wan_config.KeepLive2v,'value'))
        RetryTimes2 = str(wan_config.getAttribute_byName(wan_config.RetryTimes2v,'value'))
        DestIP2 = str(wan_config.getAttribute_byName(wan_config.DestIP2v,'value'))
        self.assertEqual(KeepLive2,'3',msg='wan2检测间隔与设置不一致')
        self.assertEqual(RetryTimes2, '3', msg='wan2检测次数与设置不一致')
        self.assertEqual(DestIP2, '1.2.3.4', msg='wan2检测地址与设置不一致')

        # 确认默认路由情况
        # 单线路默认路由变为：default via 192.168.11.1 dev eth2.2 equalize 不再有weight值
        wan1route1 = 'dev ' + line1_Interface_name
        print('wan1route:', wan1route1)
        roure1 = bytes(('ip route | grep "%s"') % line1_Interface_name, encoding="utf8")

        time.sleep(10)  # 等待检测，路由切换
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            tn.write(roure1 + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            # print('result:', result)
            result4 = result[1:]
            # print('result4', result4)
            result5 = result4.replace('\r\n', ' ')
            print('result5', result5)
            tn.close()
            # wan2、wan3检测不通，这里判断仅wan1在
            if  'default' in result5 and wan1route1 in result5:
                print('wan1路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan1route1: %s' % wan1route1)
            logger.info(u'result5: %s' % result5)
            raise Exception('wan1默认路由显示有误')

        #3、将wan2检测目标改正确，线路、路由切换回来
        wan_config.input_DestIP2('223.5.5.5') # WAN2检测地址改可ping通，测试线路切换
        wan_config.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wan_config.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wan_config.getAttribute_byClass(wan_config.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'线路检测保存 异常')
                    raise Exception(u'线路检测保存 异常')
                break
        else:
            raise Exception(u'线路检测保存 未弹出提示框')
        # 切换标签页判断配置正确
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_GlobalConfig()
        time.sleep(1)
        DestIP2 = str(wan_config.getAttribute_byName(wan_config.DestIP2v,'value'))
        self.assertEqual(DestIP2, '223.5.5.5', msg='wan2检测地址与设置不一致')

        time.sleep(20)  # 等待检测，路由切换
        # 确认默认路由情况（wan2检测地址通，默认路由应切换成wan2）
        # 单线路默认路由变为：default via 192.168.11.1 dev eth2.2 equalize 不再有weight值
        wan2route1 = 'dev ' + line2_Interface_name
        print('wan2route1:', wan2route1)
        roure1 = bytes(('ip route | grep "%s"') % wan2route1, encoding="utf8")
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            tn.write(roure1 + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            # print('result:', result)
            result4 = result[1:]
            # print('result4', result4)
            result5 = result4.replace('\r\n',' ')
            print('result5', result5)
            # wan2、wan3检测不通，这里只判断wan1的
            tn.close()
            if 'default' in result5 and wan2route1 in result5:
                print('wan2路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan2route1: %s' % wan2route1)
            logger.info(u'result5: %s' % result5)
            raise Exception('wan2默认路由显示有误')

        #4、wan1口改回主线路
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line1edit()
        time.sleep(1)
        line_type = wan_config.selelement_byXpath(wan_config.line_type)
        Select(line_type).select_by_value('1')  # 1为主 0为备份
        wan_config.click_save()
        time.sleep(10)  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        self.driver.quit()
        
        # telnet获取接口名称及确认默认路由
        wan1route_2 = 'dev ' + line1_Interface_name + ' weight '
        wan2route_2 = 'dev ' + line2_Interface_name + ' weight '
        print('wan1route_2:', wan1route_2, 'wan2route_2:', wan2route_2)
        time.sleep(10)
        # 获取接口名称
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            tn.read_until(b'#')
            # 确认默认路由情况
            tn.write(b'ip route' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result9 = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            # print('result9:', result9)
            # 获取WAN1对应接口名称
            result10 = result9[1:]
            # print('result10', result10)
            result11 = result10.replace('\r\n',' ')
            print('result11', result11)
            tn.close()
            if (wan1route_2 in result11) and (wan2route_2 in result11):
                print('wan1/wan2路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan1route_2: %s' % wan1route_2)
            logger.info(u'wan2route_2: %s' % wan2route_2)
            logger.info(u'result11 %s' % result11)
            raise Exception('wan1/wan2默认路由显示有误')

        logger.info('test_002_backupLineSW passed')

    def test_003_static_PPPoE(self):
        u'''固定+PPPoE 接入'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        ConnectState = getAssertText('ConnectState')
        # WAN1改成pppoe
        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('111')
        wan_config.input_pppoePass('111')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开

        login.loginWeb(self)  # admin账号登录
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        self.driver.implicitly_wait(10)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        #断言
        n = 0
        while n < 30:
            wan_config.click_refresh()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            print(str(list_connectState1), str(list_connectState2))
            list_connectState = [str(list_connectState1), str(list_connectState2)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in list_connectState):
                print('WAN口均已连接', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未已连接')
        #获取两个wan口IP、mac，pppoe接口通过IP判断接口名，固定通过mac地址判断接口名
        line1_ip=str(wan_config.getText_byXpath(wan_config.line1IP))
        print('line1_ip:',line1_ip)
        line2_mac = str(wan_config.getText_byXpath(wan_config.line2Mac))
        # print('WAN1_dns=',line2_mac)
        self.driver.quit()

        #处理wan口的mac地址
        #字母变大写
        line2_mac1 = line2_mac.upper()
        #加冒号
        line2_mac2=line2_mac1[0:2]+':'+line2_mac1[2:4]+':'+line2_mac1[4:6]+':'+line2_mac1[6:8]+':'+line2_mac1[8:10]+':'+line2_mac1[10:]
        print(line2_mac2)

        #telnet获取接口名称及确认默认路由
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding = "utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password  + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ifconfig | grep eth' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        #获取WAN口对应接口名称
        result1 = result[3:-9]
        # print(result1)
        result2 = result1.split(r'\r\n')
        print('result2:',result2)

        for i in range(len(result2)):
            if line2_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2[i])
                line2_Interface_name = result2_num.split()[0]
                print(line2_Interface_name)
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')

        # 通过IP获取wan1ppp接口名称 以及确认默认路由情况
        tn.write(b'ip route' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[2:-7]
        print('result1', result1)
        result2 = result1.split(r'\r\n')
        print('result2', result2)

        for x in range(len(result2)):
            if line1_ip in result2[x]:
                result2_num1 = (result2[x])
                print(result2_num1)
                line1_Interface_name = result2_num1.split()[2]
                print(line1_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')

        #确认默认路由情况
        wan1route='nexthop dev '+line1_Interface_name+' weight '
        wan2route = 'dev ' + line2_Interface_name + ' weight '
        print('wan1route:',wan1route,'wan2route:',wan2route)

        for i in range(len(result2)):
            if wan1route in result2[i]:
                wan1route_status=not None
                print('wan1路由在')
            if wan2route in result2[i]:
                wan2route_status=not None
                print('wan2路由在')
        if wan1route_status ==None:
            raise Exception('wan1默认路由不存在')
        if wan2route_status ==None:
            raise Exception('wan2默认路由不存在')
        tn.close()  # tn.write('exit\n')
        logger.info('test_003_static_PPPoE passed')

    def test_004_PPPoEsw(self):
        u'''PPPOE+PPPOE接入上网以及线路切换'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        ConnectState = getAssertText('ConnectState')
        #1、 WAN2口改为pppoe接入
        wan_config.click_line2edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('222')# 输入上层网关配置的PPPoE账号密码
        wan_config.input_pppoePass('222')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 断言
        n = 0
        while n < 30:
            wan_config.click_refresh()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            print(str(list_connectState1), str(list_connectState2))
            list_connectState = [str(list_connectState1), str(list_connectState2)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in list_connectState):
                print('WAN口均已连接', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未连接')
        # 获取两个wan口IP、mac，pppoe接口通过IP判断接口名，固定通过mac地址判断接口名
        line1_ip = str(wan_config.getText_byXpath(wan_config.line1IP))
        # print('line1_ip:', line1_ip)
        line2_ip = str(wan_config.getText_byXpath(wan_config.line2IP))
        # print('line2_ip:', line2_ip)

        time.sleep(10)  # 等待wan2路由生成

        # telnet获取接口名称及确认默认路由
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        # 获取接口名称
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 通过IP获取wan1ppp接口名称 以及确认默认路由情况
        tn.write(b'ip route' + b'\n')
        # 输出结果，判断
        time.sleep(1)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 获取WAN1对应接口名称
        result1 = result[2:-7]
        print('result1', result1)
        result2 = result1.split(r'\r\n')
        print('result2', result2)

        for x in range(len(result2)):
            if line1_ip in result2[x]:
                result2_num1 = (result2[x])
                print(result2_num1)
                line1_Interface_name = result2_num1.split()[2]
                print(line1_Interface_name)
            if line2_ip in result2[x]:
                result2_num1 = (result2[x])
                print(result2_num1)
                line2_Interface_name = result2_num1.split()[2]
                print(line2_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')

        # 确认默认路由情况
        wan1route = 'nexthop dev ' + line1_Interface_name + ' weight '
        wan2route = 'nexthop dev ' + line2_Interface_name + ' weight '
        print('wan1route:', wan1route, 'wan2route:', wan2route)

        for i in range(len(result2)):
            if wan1route in result2[i]:
                wan1route_status = not None
                print('wan1路由在')
            if wan2route in result2[i]:
                wan2route_status = not None
                print('wan2路由在')
        if wan1route_status == None:
            raise Exception('wan1默认路由不存在')
        if wan2route_status == None:
            raise Exception('wan2默认路由不存在')
        tn.close()  # tn.write('exit\n')
        self.driver.quit()

        # 2、设置线路检测地址，验证线路切换
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # 配置线路检测 检测3s 检测 3次，地址为223.5.5.5
        wan_config.click_GlobalConfig()
        time.sleep(1)
        wan_config.input_KeepLive1('3')
        wan_config.input_RetryTimes1('3')
        sel1 = wan_config.selelement_byName(wan_config.PriAddrType1)
        Select(sel1).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP1('223.5.5.5')

        wan_config.input_KeepLive2('3')
        wan_config.input_RetryTimes2('3')
        sel2 = wan_config.selelement_byName(wan_config.PriAddrType2)
        Select(sel2).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP2('1.2.3.4')  # WAN2配一个ping不通的地址，测试线路切换
        wan_config.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wan_config.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wan_config.getAttribute_byClass(wan_config.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'线路检测保存 异常')
                    raise Exception(u'线路检测保存 异常')
                break
        else:
            raise Exception(u'线路检测保存 未弹出提示框')
        # 切换标签页判断配置正确
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_GlobalConfig()
        time.sleep(1)
        KeepLive2 = str(wan_config.getAttribute_byName(wan_config.KeepLive2v, 'value'))
        RetryTimes2 = str(wan_config.getAttribute_byName(wan_config.RetryTimes2v, 'value'))
        DestIP2 = str(wan_config.getAttribute_byName(wan_config.DestIP2v, 'value'))
        self.assertEqual(KeepLive2, '3', msg='wan2检测间隔与设置不一致')
        self.assertEqual(RetryTimes2, '3', msg='wan2检测次数与设置不一致')
        self.assertEqual(DestIP2, '1.2.3.4', msg='wan2检测地址与设置不一致')

        # telnet确认默认路由（wan2检测地址不通，默认路由应切换成wan1）
        # wan2检测不通，这里只判断wan1的
        # 单线路默认路由变为ru：default dev ppp0 equalize  不再有weight值
        # (高通没有equalize)：default via 192.168.12.1 dev eth0.3
        wan1route1 = 'default dev ' + line1_Interface_name
        print('wan1route:', wan1route1)
        roure1 = bytes(('ip route | grep "%s"') % line1_Interface_name, encoding="utf8")
        time.sleep(10)  # 等待检测，路由切换
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 确认默认路由情况
            tn.write(roure1 + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result3 = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            # print('result3:', result3)
            # 获取WAN1对应接口名称
            result4 = result3[1:]
            # print('result4', result4)
            result5 = result4.replace('\r\n',' ')
            # print('result5', result2)
            tn.close()
            if 'default' in result5 and wan1route1 in result5:
                print('wan1路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan1route1: %s' % wan1route1)
            logger.info(u'result5 %s' % result5)
            raise Exception('wan1默认路由显示有误')

        # 3、将wan2检测目标改正确，线路、路由切换回来
        wan_config.input_DestIP2('223.5.5.5')  # WAN2检测地址改可ping通，测试线路切换
        wan_config.click_save()
        time.sleep(2)
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wan_config.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wan_config.getAttribute_byClass(wan_config.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'线路检测保存 异常')
                    raise Exception(u'线路检测保存 异常')
                break
        else:
            raise Exception(u'线路检测保存 未弹出提示框')
        # 切换标签页判断配置正确
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_GlobalConfig()
        time.sleep(1)
        DestIP2 = str(wan_config.getAttribute_byName(wan_config.DestIP2v, 'value'))
        self.assertEqual(DestIP2, '223.5.5.5', msg='wan2检测地址与设置不一致')

        # 确认默认路由情况（wan2检测地址通，默认路由应切换成wan2）
        wan1route2 = 'nexthop dev ' + line1_Interface_name + ' weight '
        wan2route2 = 'nexthop dev ' + line2_Interface_name + ' weight '
        print('wan1route:', wan1route, 'wan2route:', wan2route)
        time.sleep(10)  # 等待检测，路由切换
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 确认默认路由情况
            tn.write(b'ip route' + b'\n')
            # 输出结果，判断
            time.sleep(1)
            result6 = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            # print('result6:', result6)
            # 获取WAN1对应接口名称
            result7 = result6[1:]
            # print('result7', result7)
            result8 = result7.replace('\r\n',' ')
            # print('result8', result8)
            tn.close()
            if (wan1route2 in result8) and (wan2route2 in result8):
                print('wan1/wan2路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan1route_2: %s' % wan1route2)
            logger.info(u'wan2route_2: %s' % wan2route2)
            logger.info(u'result8 %s' % result8)
            raise Exception('wan1/wan2默认路由显示有误')

        #取消线路检测
        wan_config.click_GlobalConfig()
        time.sleep(1)
        wan_config.input_KeepLive1('0')
        wan_config.input_KeepLive2('0')
        wan_config.click_save()
        # 等待弹窗提示成功
        i = 0
        while i < 80:
            try:
                self.driver.implicitly_wait(1)
                wan_config.find_tipsshowin()
            except NoSuchElementException:
                time.sleep(1)
                i = i + 1
                print(i)
            else:
                tips = str(wan_config.getAttribute_byClass(wan_config.tipsshowin, 'tip-sign'))
                print(tips, i)
                if tips != 'success':
                    CapPic(self.driver)
                    logger.info(u'线路检测保存 异常')
                    raise Exception(u'线路检测保存 异常')
                break
        else:
            raise Exception(u'线路检测保存 未弹出提示框')
        # 切换标签页判断配置正确
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_GlobalConfig()
        time.sleep(1)
        KeepLive1 = str(wan_config.getAttribute_byName(wan_config.KeepLive1v, 'value'))
        KeepLive2 = str(wan_config.getAttribute_byName(wan_config.KeepLive2v, 'value'))
        self.assertEqual(KeepLive1, '0', msg='wan1检测间隔不为0')
        self.assertEqual(KeepLive2, '0', msg='wan2检测间隔不为0')
        # WAN1改回动态接入，得到正确的IP地址及网关地址
        wan_config.click_WANconfig()
        time.sleep(1)
        # WAN1
        wan_config.click_line1edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('DHCP')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()
        logger.info('test_004_PPPoEsw passed')

    def test_005_initSwPort(self):
        u'''初始化交换机接口vlan'''
        self.driver.quit()
        swconfig.test_initSwPort(self)
        logger.info('test_005_initSwPort passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

