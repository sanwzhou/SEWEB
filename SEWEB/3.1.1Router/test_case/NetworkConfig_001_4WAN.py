#! -*-conding:utf-8 -*-
#@Time: 2019/1/10 0010 13:33
#@swzhou
'''
功能说明
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
from common.ReadConfig import getAssertText,gettelnet,getweb
from pages.NetConfig_001_WANpage import NetworkConfig_wanpage
logger = LogGen(Logger = 'NetworkConfig_001_4WAN').getlog()

class Config_4WAN(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        # 进入网络配置-外网配置
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        # pass

    def test_000_getReady(self):
        u'''更改wan口数量 以及设置wan4与上联口互通'''
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
            Select(selPortNumber).select_by_value('4')
            time.sleep(2)
            try:
                wan_config.find_cfm_ok()
            except NoSuchElementException:
                logger.info(u'WAN口数量已为4')
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
        #2 调整wan4 与上联口互通
        swconfig.test_changeWAN4(self)
        logger.info('test_000_getReady passed')

    def test_001_static(self):
        u'''四条线路固定IP地址接入'''
        # 获取4条外线的链接类型
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        linetype = getAssertText('DHCPline')
        ConnectState = getAssertText('ConnectState')
        line1_type = wan_config.getText_byXpath(wan_config.line1Type)
        line2_type = wan_config.getText_byXpath(wan_config.line2Type)
        line3_type = wan_config.getText_byXpath(wan_config.line3Type)
        line4_type = wan_config.getText_byXpath(wan_config.line4Type)
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
        if str(line3_type) != linetype:
            wan_config.click_line3edit()
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
            print('wan3 动态接入')
        if str(line4_type) != linetype:
            wan_config.click_line4edit()
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
            print('wan4 动态接入')

        # 断言
        n = 0
        while n < 30:
            wan_config.click_refresh()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            list_connectState3 = wan_config.getText_byXpath(wan_config.connectState3)
            list_connectState4 = wan_config.getText_byXpath(wan_config.connectState4)
            print(str(list_connectState1), str(list_connectState2), str(list_connectState3), str(list_connectState4))
            list_connectState = [str(list_connectState1), str(list_connectState2), str(list_connectState3),
                                 str(list_connectState4)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in  list_connectState):
                print('WAN口均已获取到地址', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未获取到地址')

        # 获取4个wan口IP、网关、mac
        WAN1_ip = wan_config.getText_byXpath(wan_config.line1IP)
        WAN2_ip = wan_config.getText_byXpath(wan_config.line2IP)
        WAN3_ip = wan_config.getText_byXpath(wan_config.line3IP)
        WAN4_ip = wan_config.getText_byXpath(wan_config.line4IP)
        # print('WAN1_ip=',WAN1_ip,'WAN2_ip=',WAN2_ip,'WAN3_ip=',WAN3_ip,'WAN4_ip=',WAN4_ip)
        WAN1_gw = wan_config.getText_byXpath(wan_config.line1gw)
        WAN2_gw = wan_config.getText_byXpath(wan_config.line2gw)
        WAN3_gw = wan_config.getText_byXpath(wan_config.line3gw)
        WAN4_gw = wan_config.getText_byXpath(wan_config.line4gw)
        # print('WAN1_gw=',WAN1_gw)
        WAN1_dns = wan_config.getText_byXpath(wan_config.line1Dns)
        WAN2_dns = wan_config.getText_byXpath(wan_config.line2Dns)
        WAN3_dns = wan_config.getText_byXpath(wan_config.line3Dns)
        WAN4_dns = wan_config.getText_byXpath(wan_config.line4Dns)
        # print('WAN1_dns=',WAN1_dns)
        line1_mac = str(wan_config.getText_byXpath(wan_config.line1Mac))
        # print('WAN1_dns=',line1_mac)
        line2_mac = str((wan_config.getText_byXpath(wan_config.line2Mac)))
        # print('WAN1_dns=',line2_mac)
        line3_mac = str((wan_config.getText_byXpath(wan_config.line3Mac)))
        # print('WAN1_dns=',line3_mac)
        line4_mac = str((wan_config.getText_byXpath(wan_config.line4Mac)))
        # print('WAN1_dns=',line3_mac)
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
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        # WAN3
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line3edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('STATIC')
        time.sleep(1)
        wan_config.input_staticIp(WAN3_ip)
        wan_config.input_staticGateway(WAN3_gw)
        wan_config.input_staticPriDns(WAN3_dns)
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        # WAN4
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line4edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('STATIC')
        time.sleep(1)
        wan_config.input_staticIp(WAN4_ip)
        wan_config.input_staticGateway(WAN4_gw)
        wan_config.input_staticPriDns(WAN4_dns)
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
            wan_config.click_refresh_s()
            time.sleep(1)
            list_connectState1 = wan_config.getText_byXpath(wan_config.connectState1)
            list_connectState2 = wan_config.getText_byXpath(wan_config.connectState2)
            list_connectState3 = wan_config.getText_byXpath(wan_config.connectState3)
            list_connectState4 = wan_config.getText_byXpath(wan_config.connectState4)
            print(str(list_connectState1), str(list_connectState2), str(list_connectState3), str(list_connectState4))
            list_connectState = [str(list_connectState1), str(list_connectState2), str(list_connectState3),
                                 str(list_connectState4)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in list_connectState):
                print('WAN口均已连接', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未连接')

        # 处理wan口的mac地址
        # 字母变大写
        line1_mac1 = line1_mac.upper()
        line2_mac1 = line2_mac.upper()
        line3_mac1 = line3_mac.upper()
        line4_mac1 = line4_mac.upper()
        # 加冒号
        line1_mac2 = line1_mac1[0:2] + ':' + line1_mac1[2:4] + ':' + line1_mac1[4:6] + ':' + line1_mac1[
                                                                                             6:8] + ':' + line1_mac1[
                                                                                                          8:10] + ':' + line1_mac1[
                                                                                                                        10:]
        line2_mac2 = line2_mac1[0:2] + ':' + line2_mac1[2:4] + ':' + line2_mac1[4:6] + ':' + line2_mac1[
                                                                                             6:8] + ':' + line2_mac1[
                                                                                                          8:10] + ':' + line2_mac1[
                                                                                                                        10:]
        line3_mac2 = line3_mac1[0:2] + ':' + line3_mac1[2:4] + ':' + line3_mac1[4:6] + ':' + line3_mac1[
                                                                                             6:8] + ':' + line3_mac1[
                                                                                                          8:10] + ':' + line3_mac1[
                                                                                                                        10:]
        line4_mac2 = line4_mac1[0:2] + ':' + line4_mac1[2:4] + ':' + line4_mac1[4:6] + ':' + line4_mac1[
                                                                                             6:8] + ':' + line4_mac1[
                                                                                                          8:10] + ':' + line4_mac1[
                                                                                                                        10:]
        print(line1_mac2, line2_mac2, line3_mac2, line4_mac2)

        # telnet获取接口名称及确认默认路由
        # 获取接口名称
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
                print(result2_num)
                line1_Interface_name = result2_num.split()[0]
                print(line1_Interface_name)
            if line2_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2_num)
                line2_Interface_name = result2_num.split()[0]
                print(line2_Interface_name)
            if line3_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2_num)
                line3_Interface_name = result2_num.split()[0]
                print(line3_Interface_name)
            if line4_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2_num)
                line4_Interface_name = result2_num.split()[0]
                print(line4_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')
        if line3_Interface_name == None:
            raise Exception('获取wan3口对应接口名称失败')
        if line4_Interface_name == None:
            raise Exception('获取wan4口对应接口名称失败')
        # 确认默认路由情况
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

        wan1route = 'dev ' + line1_Interface_name + ' weight '
        wan2route = 'dev ' + line2_Interface_name + ' weight '
        wan3route = 'dev ' + line3_Interface_name + ' weight '
        wan4route = 'dev ' + line4_Interface_name + ' weight '
        print('wan1route:', wan1route, 'wan2route:', wan2route, 'wan3route:', wan3route, 'wan4route:', wan4route)

        for i in range(len(result2)):
            if wan1route in result2[i]:
                wan1route_status = not None
                print('wan1路由在')
            if wan2route in result2[i]:
                wan2route_status = not None
                print('wan2路由在')
            if wan3route in result2[i]:
                wan3route_status = not None
                print('wan3路由在')
            if wan4route in result2[i]:
                wan4route_status = not None
                print('wan4路由在')
        if wan1route_status == None:
            raise Exception('wan1默认路由不存在')
        if wan2route_status == None:
            raise Exception('wan2默认路由不存在')
        if wan3route_status == None:
            raise Exception('wan3默认路由不存在')
        if wan4route_status == None:
            raise Exception('wan4默认路由不存在')
        tn.close()  # tn.write('exit\n')
        self.driver.quit()
        logger.info('test_001_static passed')

    def test_002_staticSW(self):
        u'''四条线路固定接入线路切换'''
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 1、获取wan mac
        line1_mac = str(wan_config.getText_byXpath(wan_config.line1Mac))
        line2_mac = str(wan_config.getText_byXpath(wan_config.line2Mac))
        line3_mac = str(wan_config.getText_byXpath(wan_config.line3Mac))
        line4_mac = str(wan_config.getText_byXpath(wan_config.line4Mac))
        # 处理wan口的mac地址
        # 字母变大写
        line1_mac1 = line1_mac.upper()
        line2_mac1 = line2_mac.upper()
        line3_mac1 = line3_mac.upper()
        line4_mac1 = line4_mac.upper()
        # 加冒号
        line1_mac2 = line1_mac1[0:2] + ':' + line1_mac1[2:4] + ':' + line1_mac1[4:6] + ':' + line1_mac1[
                                                                                             6:8] + ':' + line1_mac1[
                                                                                                          8:10] + ':' + line1_mac1[
                                                                                                                        10:]
        line2_mac2 = line2_mac1[0:2] + ':' + line2_mac1[2:4] + ':' + line2_mac1[4:6] + ':' + line2_mac1[
                                                                                             6:8] + ':' + line2_mac1[
                                                                                                          8:10] + ':' + line2_mac1[
                                                                                                                        10:]
        line3_mac2 = line3_mac1[0:2] + ':' + line3_mac1[2:4] + ':' + line3_mac1[4:6] + ':' + line3_mac1[
                                                                                             6:8] + ':' + line3_mac1[
                                                                                                          8:10] + ':' + line3_mac1[
                                                                                                                        10:]
        line4_mac2 = line4_mac1[0:2] + ':' + line4_mac1[2:4] + ':' + line4_mac1[4:6] + ':' + line4_mac1[
                                                                                             6:8] + ':' + line4_mac1[
                                                                                                          8:10] + ':' + line4_mac1[
                                                                                                                        10:]
        print(line1_mac2, line2_mac2, line3_mac2, line4_mac2)
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

        wan_config.input_KeepLive3('3')
        wan_config.input_RetryTimes3('3')
        sel3 = wan_config.selelement_byName(wan_config.PriAddrType3)
        Select(sel3).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP3('1.2.3.5')  # WAN3配一个ping不通的地址，测试线路切换

        wan_config.input_KeepLive4('3')
        wan_config.input_RetryTimes4('3')
        sel4 = wan_config.selelement_byName(wan_config.PriAddrType4)
        Select(sel4).select_by_value('others')
        time.sleep(0.5)
        wan_config.input_DestIP4('1.2.3.6')  # WAN4配一个ping不通的地址，测试线路切换
        wan_config.click_save()
        time.sleep(1)
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
        KeepLive4 = str(wan_config.getAttribute_byName(wan_config.KeepLive4v,'value'))
        RetryTimes4 = str(wan_config.getAttribute_byName(wan_config.RetryTimes4v,'value'))
        DestIP4 = str(wan_config.getAttribute_byName(wan_config.DestIP4v,'value'))
        self.assertEqual(KeepLive4, '3', msg='wan4检测间隔与设置不一致')
        self.assertEqual(RetryTimes4, '3', msg='wan4检测次数与设置不一致')
        self.assertEqual(DestIP4, '1.2.3.6', msg='wan4检测地址与设置不一致')

        # telnet获取接口名称及确认默认路由（wan2/wan3检测不通，应只剩下wan1默认路由）
        # 获取接口名称
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
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
            if line3_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2[i])
                line3_Interface_name = result2_num.split()[0]
                print(line3_Interface_name)
            if line4_mac2 in result2[i]:
                result2_num = (result2[i])
                print(result2[i])
                line4_Interface_name = result2_num.split()[0]
                print(line4_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')
        if line3_Interface_name == None:
            raise Exception('获取wan3口对应接口名称失败')
        if line4_Interface_name == None:
            raise Exception('获取wan4口对应接口名称失败')

        time.sleep(10)  # 等待检测，路由切换
        # 确认默认路由情况
        # 单线路默认路由变为：default via 192.168.11.1 dev eth2.2 equalize 不再有weight值
        wan1route1 = 'dev ' + line1_Interface_name
        print('wan1route:', wan1route1)
        roure1 = bytes(('ip route | grep "%s"') % line1_Interface_name, encoding="utf8")
        x = 0
        while x < 60:
            tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
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
            # print('result5', result5)
            # wan2、wan3检测不通，这里只判断wan1的
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
            logger.info(u'result5: %s' % result5)
            raise Exception('wan1默认路由显示有误')

        # 3、将wan2\wan3检测目标改正确，线路、路由切换回来
        wan_config.input_DestIP2('223.5.5.5')  # WAN2检测地址改可ping通，测试线路切换
        wan_config.input_DestIP3('223.5.5.5')  # WAN3检测地址改可ping通，测试线路切换
        wan_config.input_DestIP4('223.5.5.5')  # WAN4检测地址改可ping通，测试线路切换
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
        DestIP4 = str(wan_config.getAttribute_byName(wan_config.DestIP4v, 'value'))
        self.assertEqual(DestIP4, '223.5.5.5', msg='wan4检测地址与设置不一致')

        # telnet获取接口名称及确认默认路由 检测通应该恢复4条默认路由
        wan1route_2 = 'dev ' + line1_Interface_name + ' weight '
        wan2route_2 = 'dev ' + line2_Interface_name + ' weight '
        wan3route_2 = 'dev ' + line3_Interface_name + ' weight '
        wan4route_2 = 'dev ' + line3_Interface_name + ' weight '
        print('wan1route_2:', wan1route_2, 'wan2route_2:', wan2route_2, 'wan3route_2:', wan3route_2, 'wan4route_2:',
              wan4route_2)
        time.sleep(10)  # 等待检测，路由切换
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
            result10 = result9[1:]
            # print('result10', result10)
            result11 = result10.replace('\r\n',' ')
            # print('result11', result11)
            tn.close()
            if (wan1route_2 and wan2route_2 and wan3route_2 and wan4route_2) in result11:
                print('wan1/wan2/wan3/wan4路由在')
                break
            else:
                print(x)
                time.sleep(2)
                x += 1
        else:
            logger.info(u'wan1route_2: %s' % wan1route_2)
            logger.info(u'wan2route_2: %s' % wan2route_2)
            logger.info(u'wan3route_2: %s' % wan3route_2)
            logger.info(u'wan4route_2: %s' % wan4route_4)
            logger.info(u'result11 %s' % result11)
            raise Exception('wan1/wan2/wan3/wan4默认路由显示有误')

        self.driver.quit()
        logger.info('test_002_staticSW passed')

    def test_003_4PPPoE(self):
        u'''四条线路PPPOE拨入'''
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
        # WAN2口改为pppoe接入
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
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('222')  # 输入上层网关配置的PPPoE账号密码
        wan_config.input_pppoePass('222')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        # WAN3口改为pppoe接入
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line3edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('333')  # 输入上层网关配置的PPPoE账号密码
        wan_config.input_pppoePass('333')
        wan_config.click_save()
        time.sleep(10)
        self.driver.quit()  # 修改接口后 可能会回到登录页面 所以关闭，再打开
        # WAN4口改为pppoe接入
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        wan_config = NetworkConfig_wanpage(self.driver, self.url)
        # 进入网络配置-外网配置
        wan_config.click_NetworkConfig()
        time.sleep(0.5)
        wan_config.click_WANconfig()
        time.sleep(1)
        wan_config.click_line4edit()
        time.sleep(1)
        access_mode = wan_config.selelement_byName(wan_config.connectionType)
        Select(access_mode).select_by_value('PPPOE')
        time.sleep(1)
        wan_config.input_pppoeUser('444')  # 输入上层网关配置的PPPoE账号密码
        wan_config.input_pppoePass('444')
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
            list_connectState3 = wan_config.getText_byXpath(wan_config.connectState3)
            list_connectState4 = wan_config.getText_byXpath(wan_config.connectState4)
            print(str(list_connectState1), str(list_connectState2), str(list_connectState3), str(list_connectState4))
            list_connectState = [str(list_connectState1), str(list_connectState2), str(list_connectState3),
                                 str(list_connectState4)]
            # 动态接入 未获取到地址/wan口线未接入 都是未连接
            if all(t == ConnectState for t in list_connectState):
                print('WAN口均已连接', n)
                break
            else:
                time.sleep(2)
                n += 1
        else:
            raise Exception('WAN口未连接')
        time.sleep(2)

        # 获取两个wan口IP、mac，pppoe接口通过IP判断接口名，固定通过mac地址判断接口名
        line1_ip = str(wan_config.getText_byXpath(wan_config.line1IP))
        # print('line1_ip:', line1_ip)
        line2_ip = str(wan_config.getText_byXpath(wan_config.line2IP))
        # print('line2_ip:', line2_ip)
        line3_ip = str(wan_config.getText_byXpath(wan_config.line3IP))
        line4_ip = str(wan_config.getText_byXpath(wan_config.line4IP))
        time.sleep(3)
        # telnet获取接口名称及确认默认路由
        # 获取接口名称
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 通过IP获取wan ppp接口名称 以及确认默认路由情况
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
            if line3_ip in result2[x]:
                result2_num1 = (result2[x])
                print(result2_num1)
                line3_Interface_name = result2_num1.split()[2]
                print(line3_Interface_name)
            if line4_ip in result2[x]:
                result2_num1 = (result2[x])
                print(result2_num1)
                line4_Interface_name = result2_num1.split()[2]
                print(line4_Interface_name)
        if line1_Interface_name == None:
            raise Exception('获取wan1口对应接口名称失败')
        if line2_Interface_name == None:
            raise Exception('获取wan2口对应接口名称失败')
        if line3_Interface_name == None:
            raise Exception('获取wan3口对应接口名称失败')
        if line4_Interface_name == None:
            raise Exception('获取wan4口对应接口名称失败')

        # 确认默认路由情况
        wan1route = 'nexthop dev ' + line1_Interface_name + ' weight '
        wan2route = 'nexthop dev ' + line2_Interface_name + ' weight '
        wan3route = 'nexthop dev ' + line3_Interface_name + ' weight '
        wan4route = 'nexthop dev ' + line4_Interface_name + ' weight '
        print('wan1route:', wan1route, 'wan2route:', wan2route, 'wan3route:', wan3route, 'wan4route:', wan4route)

        for i in range(len(result2)):
            if wan1route in result2[i]:
                wan1route_status = not None
                print('wan1路由在')
            if wan2route in result2[i]:
                wan2route_status = not None
                print('wan2路由在')
            if wan3route in result2[i]:
                wan3route_status = not None
                print('wan3路由在')
            if wan4route in result2[i]:
                wan4route_status = not None
                print('wan4路由在')
        if wan1route_status == None:
            raise Exception('wan1默认路由不存在')
        if wan2route_status == None:
            raise Exception('wan2默认路由不存在')
        if wan3route_status == None:
            raise Exception('wan3默认路由不存在')
        if wan4route_status == None:
            raise Exception('wan4默认路由不存在')

        tn.close()  # tn.write('exit\n')

        print(u'四条线路PPPOE拨入 验证通过')

        # 取消线路检测
        wan_config.click_GlobalConfig()
        time.sleep(1)
        wan_config.input_KeepLive1('0')
        wan_config.input_KeepLive2('0')
        wan_config.input_KeepLive3('0')
        wan_config.input_KeepLive4('0')
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
        KeepLive1 = str(wan_config.getAttribute_byName(wan_config.KeepLive1v, 'value'))
        KeepLive2 = str(wan_config.getAttribute_byName(wan_config.KeepLive2v, 'value'))
        KeepLive3 = str(wan_config.getAttribute_byName(wan_config.KeepLive3v, 'value'))
        KeepLive4 = str(wan_config.getAttribute_byName(wan_config.KeepLive4v, 'value'))
        self.assertEqual(KeepLive1, '0', msg='wan1检测间隔不为0')
        self.assertEqual(KeepLive2, '0', msg='wan2检测间隔不为0')
        self.assertEqual(KeepLive3, '0', msg='wan3检测间隔不为0')
        self.assertEqual(KeepLive4, '0', msg='wan4检测间隔不为0')
        # wan1改回动态接入，得到正确的IP地址及网关地址
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
        logger.info('test_003_4PPPoE passed')

    def test_004_initSwPort(self):
        u'''初始化交换机接口vlan'''
        self.driver.quit()
        swconfig.test_initSwPort(self)
        logger.info('test_004_initSwPort passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
