#! -*-conding:utf-8 -*-
#@Time: 2019/3/23 0023 15:47
#@swzhou
'''
导入配置文件，核对参数
'''

import os
import sys
import time
import unittest
import telnetlib
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getParameter,gettelnet,getweb
from common.GetExcelValue import getExcelValue
from common.GetRouteCPU import getCPUmodel
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from pages.sysObj_timePlanPage import timePlanPage
from pages.NetConfig_005_RouteConfigPage import RouteConfigPage
from pages.PortMapping_002_staticMappingPage import staticMappingPage
from pages.PortMapping_003_natRulePage import natRulePage
from pages.Firewall_001_ACLPage import AccessControlPage
from pages.sysObj_AddressGroupPage import AddressGroupPage
from pages.actionManage_001_actionManagePage import actionManagePage
from pages.actionManage_003_WhiteListPage import WhiteListPage
from pages.actionManage_002_DomainFilterPage import DomainFilterPage
from pages.TrafficManagement_002_BWManagementPage import BWManagementPage
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
from pages.Organization_001_Memberspage import OrganizationMembersPage
from pages.Organization_003_userAuthpage import Organization_userAuthPage
from pages.Organization_004_userBlackpage import Organization_userBlackPage
from pages.AC_004_loadBalancingPage import loadBalancingPage
from pages.AC_001_NetNamePage import netNamePage
from selenium.common.exceptions import NoSuchElementException
logger = LogGen(Logger = 'Parameter_100_Parameter').getlog()
list1_name = '//*[@id="1"]/div/div/div[1]/table/tbody/tr[%s]/td[2]/span' #list中第一行的第二列
list2_name = '//*[@id="2"]/div/div/div[1]/table/tbody/tr[%s]/td[2]/span' #list中第一行的第二列
list_type = str('//*[@id="1"]/div/div/div[1]/table/tbody/tr[%s]/td[3]/span') #QQ白名单用到，第一行第三列
list_num = str('//*[@id="1"]/table/tbody/tr[8]/td[2]/select/option[%s]') #域名过滤用到，域名列表

class Parameter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # pass

    def test_000_configIpmort(self):
        u'''导入基本满配置'''
        self.driver.quit()
        login.loginWeb2(self)
        self.driver.implicitly_wait(10)
        scriptpath = os.path.dirname(os.path.abspath('.')) + '/script/'
        #导入配置 验证
        config = MaintenancePage(self.driver, self.url)
        # 进入系统配置-系统维护-配置管理
        config.click_sysConfig()
        time.sleep(0.5)
        config.click_Maintenance()
        time.sleep(1)
        config.click_configuration()
        time.sleep(1)
        # 选中'选择文件' #这里没有取消"导入前恢复出厂设置"按钮
        config.click_chooseFile()
        time.sleep(1)
        #调用autoIt脚本上传组的xml文件
        autoItScript = scriptpath + 'SE_allconfig_import.exe'
        os.system('%s' % autoItScript)
        time.sleep(2)
        #点击导入
        config.click_innerput()
        time.sleep(1)
        config.click_ok()
        time.sleep(8)
        #取消重启
        config.click_no()
        time.sleep(1)
        #验证导入配置是否成功（通过配置的 今天时间计划）
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        list_name5 = timePlan.getText_byXpath(timePlan.list_name5)
        if list_name5 == '5':
            logger.info(u'all配置导入完成')
        else:
            CapPic(self.driver)
            logger.info(u'all配置导入异常')
            raise Exception(u'all配置导入异常')
        self.driver.quit()
        logger.info('test_000_configIpmort passed')

    def test_000_deviceParameter(self):
        u'''检查硬件参数'''
        natsessionP = getParameter('natsessionP')
        memoryP = getParameter('memoryP')
        valueN = getExcelValue(natsessionP)
        valueM = getExcelValue(memoryP)

        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        # #1\natsession
        # tn = telnetlib.Telnet(host=hostip, port=port)
        # tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # # 输入登录用户名
        # tn.read_until(b'login:')
        # tn.write(username + b"\n")
        # tn.read_until(b'Password:')
        # tn.write(password + b"\n")
        # # 登录完毕后执行命令
        # tn.read_until(b'#')
        # tn.write(b'cat /proc/sys/net/netfilter/nf_conntrack_max' + b'\n')
        # # 输出结果，判断
        # time.sleep(0.5)
        # result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        # print('-------------------输出结果------------------------')
        # # 命令执行结果
        # print('result:', result)
        # result_list = result.split(r'\r\n')
        # # 判断
        # # print(result_list)
        # if str(valueN) == (result_list[1]):
        #     print('NATsession 与参数一致')
        # else:
        #     logger.info(u'value:', valueN)
        #     logger.info(u'result_list[1]:', (result_list[1]))
        #     raise Exception('NATsession 与参数不一致')  # 如果没有则报错
        # tn.close()  # tn.write('exit\n')
        #2、内存
        tn = telnetlib.Telnet(host=hostip, port=port)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'free' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        result_list = result.split(r'\r\n')
        # 判断
        # print(result_list)
        result_list = (result_list[2]).split(r' ')
        # print(result_list)
        result_list = [x for x in result_list if x!=''] #去除空字符 ''
        # print(result_list)
        print('result_list[1]:',result_list[1]) #取总内存值
        if str(valueM)[:2] == (result_list[1][0:2]): #前两位相等
            print('内存 与参数一致')
        elif 'G' in str(valueM): #大设备 如6550G 内存参数表为 2G
            # print(str(valueM)[0])
            # print((result_list[1][0:2]))
            if str(valueM)[0] == str(int(result_list[1][0:2]) + 1)[0]:
                print('内存 与参数一致')
            else:
                logger.info(u'str(valueM)[0]', str(valueM)[0])
                logger.info(u'str(int(result_list[1][0:2]) + 1)', str(int(result_list[1][0:2]) + 1))
                raise Exception('内存 与参数不一致')
        else:
            logger.info(u'str(valueM)[:2]:',str(valueM)[:2])
            logger.info(u'(result_list[1])', (result_list[1]))
            raise Exception('内存 与参数不一致')
        tn.close()  # tn.write('exit\n')
        self.driver.quit()
        logger.info('test_000_configIpmort passed')

    def test_001_route(self):
        u'''查询静态路由&策略路由 条目'''
        #1、静态路由
        staticRp = getParameter('staticRp')
        print('1:',getExcelValue(staticRp))
        value = int(getExcelValue(staticRp))
        print('value:',value,type(value))
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        routeconfig = RouteConfigPage(self.driver, self.url)
        routeconfig.click_NetworkConfig()
        time.sleep(0.5)
        routeconfig.click_Routeconfig()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(routeconfig.getAttribute_byXpath(routeconfig.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'静态路由最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'静态路由最大页数显示异常')
            raise Exception(u'静态路由最大页数显示异常')
        #2）查参数最大条目是否显示
        routeconfig.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = routeconfig.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'静态路由未达到最大条目数')
            raise Exception(u'静态路由未达到最大条目数')
        else:
            logger.info(u'静态路由可以达到最大条目数')
        #3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = routeconfig.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'静态路由未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'静态路由超过最大条目数')
            raise Exception(u'静态路由超过最大条目数')

        # 2、策略路由
        policyP = getParameter('policyP')
        Support = getExcelValue(policyP)
        if Support != '×':
            value = int(getExcelValue(policyP))
            # print('value:',value)
            value1 = value + 1
            value2 = str(value)[:-1]
            if str(value)[-1:] != '0': #参数值不为整10，则需要+1
                value2 = int(value2) + 1

            routeconfig = RouteConfigPage(self.driver, self.url)
            routeconfig.click_PolicyRoute()
            time.sleep(1)
            # 1）查看页数
            maxpagenums = str(routeconfig.getAttribute_byXpath(routeconfig.maxpagenums2, 'max'))
            print(maxpagenums, value2)
            if maxpagenums == str(value2):
                logger.info(u'策略路由最大页数显示正常')
            else:
                CapPic(self.driver)
                logger.info(u'策略路由最大页数显示异常')
                raise Exception(u'策略路由最大页数显示异常')
            # 2）查参数最大条目是否显示
            routeconfig.click_pageend2()
            time.sleep(1)
            list_name1 = (list2_name % value)
            # print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = routeconfig.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'策略路由未达到最大条目数')
                raise Exception(u'策略路由未达到最大条目数')
            else:
                logger.info(u'策略路由可以达到最大条目数')
            # 3）查比参数值多1 是否找不到
            list_name2 = (list2_name % value1)
            # print(list_name2)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = routeconfig.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                logger.info(u'策略路由未超过最大条目数')
            else:
                CapPic(self.driver)
                logger.info(u'策略路由超过最大条目数')
                raise Exception(u'策略路由超过最大条目数')
        self.driver.quit()
        logger.info('test_001_route passed')

    def test_002_nat(self):
        u'''查询静态映射&NAT规则 条目'''
        #1、静态映射
        staticMapP = getParameter('staticMapP')
        value = int(getExcelValue(staticMapP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        ststicmap = staticMappingPage(self.driver, self.url)
        ststicmap.click_NetworkConfig()
        time.sleep(0.5)
        ststicmap.click_portMapping()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(ststicmap.getAttribute_byXpath(ststicmap.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'静态映射最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'静态映射最大页数显示异常')
            raise Exception(u'静态映射最大页数显示异常')
        #2）查参数最大条目是否显示
        ststicmap.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = ststicmap.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'静态映射未达到最大条目数')
            raise Exception(u'静态映射未达到最大条目数')
        else:
            logger.info(u'静态映射可以达到最大条目数')
        #3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = ststicmap.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'静态映射未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'静态映射超过最大条目数')
            raise Exception(u'静态映射超过最大条目数')

        # 2、NAT规则
        natRuleP = getParameter('natRuleP')
        value = int(getExcelValue(natRuleP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0': #参数值不为整10，则需要+1
            value2 = int(value2) + 1

        natRule = natRulePage(self.driver, self.url)
        natRule.click_natRule()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(natRule.getAttribute_byXpath(natRule.maxpagenums1, 'max'))
        print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'NAT规则最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'NAT规则最大页数显示异常')
            raise Exception(u'NAT规则最大页数显示异常')
        # 2）查参数最大条目是否显示
        natRule.click_pageend1()
        time.sleep(1)
        list_name1 = (list2_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = natRule.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'NAT规则未达到最大条目数')
            raise Exception(u'NAT规则未达到最大条目数')
        else:
            logger.info(u'NAT规则可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list2_name % value1)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = natRule.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'NAT规则未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'NAT规则超过最大条目数')
            raise Exception(u'NAT规则超过最大条目数')
        self.driver.quit()
        logger.info('test_002_nat')

    def test_003_FireWall(self):
        u'''查询访问控制 条目'''

        FirewallP = getParameter('FirewallP')
        value = int(getExcelValue(FirewallP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        firewall = AccessControlPage(self.driver, self.url)
        firewall.click_FireWall()
        time.sleep(0.5)
        firewall.click_AccessControl()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(firewall.getAttribute_byXpath(firewall.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'访问控制最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'访问控制最大页数显示异常')
            raise Exception(u'访问控制最大页数显示异常')
        # 2）查参数最大条目是否显示
        firewall.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = firewall.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'访问控制未达到最大条目数')
            raise Exception(u'访问控制未达到最大条目数')
        else:
            logger.info(u'访问控制可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = firewall.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'访问控制未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'访问控制超过最大条目数')
            raise Exception(u'访问控制超过最大条目数')
        self.driver.quit()
        logger.info('test_003_FireWall passed')

    def test_004_address(self):
        u'''查询地址组 条目'''

        addGroupP = getParameter('addGroupP')
        value = int(getExcelValue(addGroupP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        addressgroup = AddressGroupPage(self.driver, self.url)
        addressgroup.click_sysObj()
        time.sleep(0.5)
        addressgroup.click_AddressGroup()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(addressgroup.getAttribute_byXpath(addressgroup.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'地址组最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'地址组最大页数显示异常')
            raise Exception(u'地址组最大页数显示异常')
        # 2）查参数最大条目是否显示
        addressgroup.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = addressgroup.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'地址组未达到最大条目数')
            raise Exception(u'地址组未达到最大条目数')
        else:
            logger.info(u'地址组可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = addressgroup.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'地址组未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'地址组超过最大条目数')
            raise Exception(u'地址组超过最大条目数')
        self.driver.quit()
        logger.info('test_004_address passed')

    def test_005_timePlan(self):
        u'''查询时间组 条目'''

        timePlanP = getParameter('timePlanP')
        value = int(getExcelValue(timePlanP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(timePlan.getAttribute_byXpath(timePlan.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'时间组最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'时间组最大页数显示异常')
            raise Exception(u'时间组最大页数显示异常')
        # 2）查参数最大条目是否显示
        timePlan.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = timePlan.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'时间组未达到最大条目数')
            raise Exception(u'时间组未达到最大条目数')
        else:
            logger.info(u'时间组可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = timePlan.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'时间组未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'时间组超过最大条目数')
            raise Exception(u'时间组超过最大条目数')
        self.driver.quit()
        logger.info('test_005_timePlan passed')

    def test_006_actionManage(self):
        u'''查询行为管理 条目'''

        actionMp = getParameter('actionMp')
        value = int(getExcelValue(actionMp))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        actionManage = actionManagePage(self.driver, self.url)
        actionManage.click_BehaviorManagement()
        time.sleep(0.5)
        actionManage.click_BehaviorManagement2()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(actionManage.getAttribute_byXpath(actionManage.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'行为管理最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'行为管理最大页数显示异常')
            raise Exception(u'行为管理最大页数显示异常')
        # 2）查参数最大条目是否显示
        actionManage.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = actionManage.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'行为管理未达到最大条目数')
            raise Exception(u'行为管理未达到最大条目数')
        else:
            logger.info(u'行为管理可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = actionManage.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'行为管理未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'行为管理超过最大条目数')
            raise Exception(u'行为管理超过最大条目数')
        self.driver.quit()
        logger.info('test_006_actionManage passed')

    def test_007_QQali(self):
        u'''查询QQ、阿里旺旺白名单 条目'''

        QQnumP = getParameter('QQnumP')
        alinumP = getParameter('alinumP')
        valueQ = int(getExcelValue(QQnumP))
        valueA = int(getExcelValue(alinumP))
        # print('value:',value)
        value2 = str(valueQ + valueA)[:-1] #QQ\阿里旺旺在一个页面
        if str(valueQ + valueA)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        whitelist = WhiteListPage(self.driver, self.url)
        whitelist.click_BehaviorManagement()
        time.sleep(0.5)
        whitelist.click_Whitelist()
        time.sleep(3)
        # 1）查看页数
        maxpagenums = str(whitelist.getAttribute_byXpath(whitelist.maxpagenums1, 'max'))
        print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'白名单最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'白名单最大页数显示异常')
            raise Exception(u'白名单最大页数显示异常')
        # 2）查QQ参数最大条目是否显示
        if str(valueQ)[-1:] != '0':
            valueQ1 = str(valueQ)[:-1]
        else:
            valueQ1 = int(str(valueQ)[:-1]) - 1
        whitelist.input_maxpagenums(valueQ1)
        whitelist.click_next()
        time.sleep(3)
        list_name1 = (list1_name % valueQ)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = whitelist.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'QQ白名单未达到最大条目数')
            raise Exception(u'QQ白名单未达到最大条目数')
        else:
            logger.info(u'行为管理可以达到最大条目数')
        # 3）查比QQ参数值多1 是否找不到
        list_type1 = (list_type % valueQ1)
        # print(list_type1)
        if list_type1 != 'QQ': #超过QQ白名单之后应该是阿里旺旺
            logger.info(u'QQ白名单未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'QQ白名单超过最大条目数')
            raise Exception(u'QQ白名单超过最大条目数')

        # 2）查阿里旺旺参数最大条目是否显示
        whitelist.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % (valueQ + valueA))
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = whitelist.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'行为管理未达到最大条目数')
            raise Exception(u'行为管理未达到最大条目数')
        else:
            logger.info(u'行为管理可以达到最大条目数')
        # 3）查比最多参数值多1 是否找不到
        list_name1 = (list1_name % (valueQ + valueA + 1))
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = whitelist.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'行为管理未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'行为管理超过最大条目数')
            raise Exception(u'行为管理超过最大条目数')
        self.driver.quit()
        logger.info('test_007_QQali passed')

    def test_008_DomainFiltering(self):
        u'''查询域名过滤 条目'''

        DomainFilerP = getParameter('DomainFilerP')
        value = int(getExcelValue(DomainFilerP))
        # print('value:',value)
        value1 = value + 1

        domainfilter = DomainFilterPage(self.driver, self.url)
        domainfilter.click_BehaviorManagement()
        time.sleep(0.5)
        domainfilter.click_DomainFilter()
        time.sleep(1)

        # 1）查参数最大条目是否显示
        list_num1 = (list_num % value)
        # print(list_num1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = domainfilter.getText_byXpath(list_num1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'域名过滤未达到最大条目数')
            raise Exception(u'域名过滤未达到最大条目数')
        else:
            logger.info(u'行为管理可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_num1 = (list_num % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = domainfilter.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'域名过滤未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'域名过滤超过最大条目数')
            raise Exception(u'域名过滤超过最大条目数')
        self.driver.quit()
        logger.info('test_008_DomainFiltering passed')

    def test_009_bandwidth(self):
        u'''查询流量管理 条目'''
        cpumodel = getCPUmodel()
        actionMp = getParameter('actionMp')
        valueA = int(getExcelValue(actionMp))
        FlowruleP = getParameter('FlowruleP')
        valueF = int(getExcelValue(FlowruleP))
        if cpumodel =="MTK" or cpumodel =="Qualcomm":
            value = valueA + valueF #mtk设备中流量管理条目 是流量管理条目与行为管理条目之和
        else:
            value = valueF #p1010数量即流量管理条目数
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        bandwidth = BWManagementPage(self.driver, self.url)
        bandwidth.click_Qos()
        time.sleep(0.5)
        bandwidth.click_TrafficManagement()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(bandwidth.getAttribute_byXpath(bandwidth.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'流量管理最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'流量管理最大页数显示异常')
            raise Exception(u'流量管理最大页数显示异常')
        # 2）查参数最大条目是否显示
        bandwidth.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = bandwidth.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'流量管理未达到最大条目数')
            raise Exception(u'流量管理未达到最大条目数')
        else:
            logger.info(u'流量管理可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = bandwidth.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'流量管理未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'流量管理超过最大条目数')
            raise Exception(u'流量管理超过最大条目数')
        self.driver.quit()
        logger.info('test_009_bandwidth passed')

    def test_010_VPNnum(self):
        u'''查询VPN隧道数 条目'''
        # 参数中的VPN条目数为pptp+l2tp+IPsec总和,
        # 而设备中pptp server/pptp client/l2tp server/l2tp client/ipsec各存一份总条目数(参数中的)
        # 这里导入的配置文件中pptp/l2tp 仅包含l2tp server的配置
        vpnNumP = getParameter('vpnNumP')
        value = getExcelValue(vpnNumP)
        print(value)
        if value != '×':
            logger.info(u'参数 VPN隧道数不为空')
            # print('value:',value) #参数表格式为 8条/8条 或者100/100
            value_list = value.split(r'/')
            if '条' in value_list[0]:
                value0 = (value_list[0][:-1])
            else:
                value0 = (value_list[0])
            # print('value0:',value)
            if len(value0) == 1:  # 判断是否是个位数
                value1 = int(value0) + 1
                value2 = 1
            else:
                value = (value0[:-1])
                value1 = int(value0) + 1
                value2 = str(value)
                # print('value2:',value2)
                # print('len(value2):',len(value2))
                if value0[-1:] != '0':  # 参数值不为整10，则需要+1
                    value2 = int(value2) + 1
                else:
                    value2 = value2

            pptpl2tp = pptpL2tpPage(self.driver, self.url)
            pptpl2tp.click_VPNConfig()
            time.sleep(0.5)
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            # 1）查看页数
            maxpagenums = str(pptpl2tp.getAttribute_byXpath(pptpl2tp.maxpagenums1, 'max'))
            print(maxpagenums, value2)
            if maxpagenums == str(value2):
                logger.info(u'vpn最大页数显示正常')
            else:
                CapPic(self.driver)
                logger.info(u'vpn最大页数显示异常')
                raise Exception(u'vpn最大页数显示异常')
            # 2）查参数最大条目是否显示
            pptpl2tp.click_pageend1()
            time.sleep(1)
            list_name1 = (list1_name % value0)
            # print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = pptpl2tp.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'vpn未达到最大条目数')
                raise Exception(u'vpn未达到最大条目数')
            else:
                logger.info(u'vpn可以达到最大条目数')
            # 3）查比参数值多1 是否找不到
            list_name1 = (list1_name % value1)
            print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = pptpl2tp.getText_byXpath(list_name1)
                print('list_name1:', list_name1)
            except NoSuchElementException:
                logger.info(u'vpn未超过最大条目数')
            else:
                CapPic(self.driver)
                logger.info(u'vpn超过最大条目数')
                raise Exception(u'vpn超过最大条目数')
            self.driver.quit()
            # 4)查VPN并发数
            value = (value_list[1][:-1])
            valuenum = 'vpn session num =' + value
            hostip = gettelnet('host')
            port = gettelnet('port')
            username = bytes(getweb('User'), encoding="utf8")
            password = bytes(getweb('Passwd'), encoding="utf8")
            # 1\natsession
            tn = telnetlib.Telnet(host=hostip, port=port)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'vpnHandle print' + b'\n')
            # 输出结果，判断
            time.sleep(0.5)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            # 判断
            if valuenum in (result):
                print('VPN并发数 与参数一致')
            else:
                logger.info(u'valuenum:', valuenum)
                logger.info(u'result:', result)
                raise Exception('VPN并发数 与参数不一致')  # 如果没有则报错
            tn.close()  # tn.write('exit\n')
        else:
            logger.info(u'参数 VPN隧道数为空')
        logger.info('test_010_VPNnum passed')

    def test_011_userNum(self):
        u'''查询用户数 条目'''

        userNumP = getParameter('userNumP')
        value = int(getExcelValue(userNumP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        group = OrganizationMembersPage(self.driver, self.url)
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_list_groupName_c()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(group.getAttribute_byXpath(group.maxpagenums2, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'用户数最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'用户数最大页数显示异常')
            raise Exception(u'用户数最大页数显示异常')
        # 2）查参数最大条目是否显示
        group.click_pageend2()
        time.sleep(1)
        list_name1 = (list2_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = group.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'用户数未达到最大条目数')
            raise Exception(u'用户数未达到最大条目数')
        else:
            logger.info(u'用户数可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list2_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = group.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'用户数未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'用户数超过最大条目数')
            raise Exception(u'用户数超过最大条目数')
        self.driver.quit()
        logger.info('test_011_userNum passed')

    def test_012_IPMACbinding(self):
        u'''查询IP/MAC绑定 条目'''

        ipmac = getParameter('ipmac')
        value = int(getExcelValue(ipmac))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        group = OrganizationMembersPage(self.driver, self.url)
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_list_groupName_c()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(group.getAttribute_byXpath(group.maxpagenums2, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'IP/MAC绑定最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'IP/MAC绑定最大页数显示异常')
            raise Exception(u'IP/MAC绑定最大页数显示异常')
        # 2）查参数最大条目是否显示
        group.click_pageend2()
        time.sleep(1)
        list_name1 = (list2_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = group.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'IP/MAC绑定未达到最大条目数')
            raise Exception(u'IP/MAC绑定未达到最大条目数')
        else:
            logger.info(u'IP/MAC绑定可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list2_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = group.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'IP/MAC绑定未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'IP/MAC绑定超过最大条目数')
            raise Exception(u'IP/MAC绑定超过最大条目数')
        self.driver.quit()
        logger.info('test_012_IPMACbinding passed')

    def test_013_PPPoE(self):
        u'''查询PPPoEserver 条目'''

        pppoeSp = getParameter('pppoeSp')
        value = getExcelValue(pppoeSp)
        # print('value:',value)
        if value != '×': #判断是否支持PPPoE
            logger.info(u'参数支持PPPoE')
            value_list = value.split(r'/')
            value = (value_list[0])
            value1 = int(value_list[0]) + 1
            value2 = str(value_list[0])[:-1]
            if str(value_list[0])[-1:] != '0':  # 参数值不为整10，则需要+1
                value2 = int(value2) + 1

            group = OrganizationMembersPage(self.driver, self.url)
            group.click_UserManage()
            time.sleep(0.5)
            group.click_userGroup()
            time.sleep(1)
            group.click_list_groupName2()
            time.sleep(1)
            # 1）查看页数
            maxpagenums = str(group.getAttribute_byXpath(group.maxpagenums2, 'max'))
            # print(maxpagenums, value2)
            if maxpagenums == str(value2):
                logger.info(u'用户数最大页数显示正常')
            else:
                CapPic(self.driver)
                logger.info(u'用户数最大页数显示异常')
                raise Exception(u'用户数最大页数显示异常')
            # 2）查参数最大条目是否显示
            group.click_pageend2()
            time.sleep(1)
            list_name1 = (list2_name % value)
            print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = group.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'用户数未达到最大条目数')
                raise Exception(u'用户数未达到最大条目数')
            else:
                logger.info(u'用户数可以达到最大条目数')
            # 3）查比参数值多1 是否找不到
            list_name1 = (list2_name % value1)
            print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = group.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                logger.info(u'用户数未超过最大条目数')
            else:
                CapPic(self.driver)
                logger.info(u'用户数超过最大条目数')
                raise Exception(u'用户数超过最大条目数')

            pppoeauth = Organization_userAuthPage(self.driver, self.url)
            # 打开用户管理 - 用户认证
            pppoeauth.click_userAuth()
            time.sleep(1)
            pppoeauth.click_PPPoEConfig()
            time.sleep(2)
            ipcount = pppoeauth.getAttribute_byName(pppoeauth.ipcount,'value')
            print('1:',ipcount,'2:',value_list[0])
            if ipcount == value_list[0]:
                logger.info(u'PPPoE总地址池数参数匹配')
            else:
                CapPic(self.driver)
                logger.info(u'PPPoE总地址池数参数不匹配')
                raise Exception(u'PPPoE总地址池数参数不匹配')
            smaxconv = pppoeauth.getAttribute_byName(pppoeauth.smaxconvs,'value')
            if smaxconv == value_list[1]:
                logger.info(u'PPPoE并发数数参数匹配')
            else:
                CapPic(self.driver)
                logger.info(u'PPPoE并发数参数不匹配')
                raise Exception(u'PPPoE并发数参数不匹配')
        elif value == '×':
            logger.info(u'参数不支持PPPoE')
            try:
                pppoeauth = Organization_userAuthPage(self.driver, self.url)
                pppoeauth.click_UserManage()
                time.sleep(0.5)
                pppoeauth.click_userAuth()
                time.sleep(1)
                self.driver.implicitly_wait(2)
                pppoeauth.click_PPPoEConfig()
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持PPPoE，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持PPPoE，与参数表不符')
                raise Exception(u'软件支持PPPoE，与参数表不符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：',value)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_011_userNum passed')

    def test_014_blacklist(self):
        u'''查询黑名单 条目'''

        BlacklistP = getParameter('BlacklistP')
        value = int(getExcelValue(BlacklistP))
        # print('value:',value)
        value1 = value + 1
        value2 = str(value)[:-1]
        if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            value2 = int(value2) + 1

        blacklist = Organization_userBlackPage(self.driver, self.url)
        blacklist.click_UserManage()
        time.sleep(0.5)
        blacklist.click_blacklist()
        time.sleep(1)
        # 1）查看页数
        maxpagenums = str(blacklist.getAttribute_byXpath(blacklist.maxpagenums1, 'max'))
        # print(maxpagenums, value2)
        if maxpagenums == str(value2):
            logger.info(u'黑名单最大页数显示正常')
        else:
            CapPic(self.driver)
            logger.info(u'黑名单最大页数显示异常')
            raise Exception(u'黑名单最大页数显示异常')
        # 2）查参数最大条目是否显示
        blacklist.click_pageend1()
        time.sleep(1)
        list_name1 = (list1_name % value)
        # print(list_name1)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = blacklist.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'黑名单未达到最大条目数')
            raise Exception(u'黑名单未达到最大条目数')
        else:
            logger.info(u'黑名单可以达到最大条目数')
        # 3）查比参数值多1 是否找不到
        list_name1 = (list1_name % value1)
        # print(list_name)
        try:
            self.driver.implicitly_wait(2)
            list_name1 = blacklist.getText_byXpath(list_name1)
            # print('list_name1:', list_name1)
        except NoSuchElementException:
            logger.info(u'用户数未超过最大条目数')
        else:
            CapPic(self.driver)
            logger.info(u'用户数超过最大条目数')
            raise Exception(u'用户数超过最大条目数')
        self.driver.quit()
        logger.info('test_014_blacklist passed')

    def test_015_maxAp(self):
        u'''查询AP管理 条目'''

        APnumP = getParameter('APnumP')
        value = getExcelValue(APnumP)
        # print('value:',value)
        if value != None and value != '×':  # 以访有些参数表里未包含ac相关数据
            logger.info(u'参数支持AP管理')
            value = int(value)
            hostip = gettelnet('host')
            port = gettelnet('port')
            username = bytes(getweb('User'), encoding="utf8")
            password = bytes(getweb('Passwd'), encoding="utf8")
            tn = telnetlib.Telnet(host=hostip, port=port)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'uttcli getbynm apScan apScanf maxAp' + b'\n')
            # 输出结果，判断
            time.sleep(0.5)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            result_list = result.split(r'\r\n')
            # 判断
            if str(value) == (result_list[1])[:-3]:
                print('AP管理数量 与参数一致')
            else:
                logger.info(u'value:',value)
                logger.info(u'(result_list[1])[:-3]:',(result_list[1])[:-3])
                raise Exception('AP管理数量 与参数不一致')  # 如果没有则报错
            tn.close()  # tn.write('exit\n')
        else:
            logger.info(u'参数不支持AP管理')
            try:
                netname = netNamePage(self.driver, self.url)
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展，与参数表不符')
                raise Exception(u'软件支持无线扩展，与参数表不符')

        self.driver.quit()
        logger.info('test_014_blacklist passed')

    def test_016_loadBalance(self):
        u'''查询负载均衡组 条目'''

        RoamP = getParameter('RoamP')
        value = getExcelValue(RoamP)
        # print('value:',value)
        if value != None and value != '×':  # 以访有些参数表里未包含ac相关数据
            logger.info(u'参数支持AP管理')
            value = value[4:]
            value1 = int(value) + 1
            value2 = str(value)
            if len(value2) != 1:  # 判断是否是个位数
                if value2[-1:] != '0':  # 参数值不为整10，则需要+1
                    value2 = int(value2[:-1]) + 1
                else:
                    value2 = value2[:-1]
            else:
                value2 = 1

            load = loadBalancingPage(self.driver, self.url)
            load.click_wirelessExtension()
            time.sleep(0.5)
            load.click_loadBalancing()
            time.sleep(1)
            # 1）查看页数
            maxpagenums = str(load.getAttribute_byXpath(load.maxpagenums1, 'max'))
            # print(maxpagenums, value2)
            if maxpagenums == str(value2):
                logger.info(u'负载均衡组最大页数显示正常')
            else:
                CapPic(self.driver)
                logger.info(u'负载均衡组最大页数显示异常')
                raise Exception(u'负载均衡组最大页数显示异常')
            # 2）查参数最大条目是否显示
            load.click_pageend1()
            time.sleep(1)
            list_name1 = (list1_name % value)
            # print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = load.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'负载均衡组未达到最大条目数')
                raise Exception(u'负载均衡组未达到最大条目数')
            else:
                logger.info(u'负载均衡组可以达到最大条目数')
            # 3）查比参数值多1 是否找不到
            list_name1 = (list1_name % value1)
            # print(list_name)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = load.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                logger.info(u'负载均衡组未超过最大条目数')
            else:
                CapPic(self.driver)
                logger.info(u'负载均衡组超过最大条目数')
                raise Exception(u'负载均衡组超过最大条目数')
        else:
            logger.info(u'参数不支持AP管理')
            try:
                netname = netNamePage(self.driver, self.url)
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展，与参数表不符')
                raise Exception(u'软件支持无线扩展，与参数表不符')
        self.driver.quit()
        logger.info('test_016_loadBalance')

    def test_017_ssidNum(self):
        u'''查询SSID 条目'''

        #参数表ssid数量有误，这里仅取参数判断是否支持，AP管理数取后台值
        APnumP = getParameter('APnumP')
        # print(APnumP)
        value = getExcelValue(APnumP)
        # print('value:',value)
        if value != None and value != '×':  # 以访有些参数表里未包含ac相关数据
            logger.info(u'参数支持AP管理')
            value = int(value)
            # value1 = value + 1
            # value2 = str(value)[:-1]
            # if str(value)[-1:] != '0':  # 参数值不为整10，则需要+1
            #     value2 = int(value2) + 1
            #取Ap后台管理数
            hostip = gettelnet('host')
            port = gettelnet('port')
            username = bytes(getweb('User'), encoding="utf8")
            password = bytes(getweb('Passwd'), encoding="utf8")
            tn = telnetlib.Telnet(host=hostip, port=port)
            tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
            # 输入登录用户名
            tn.read_until(b'login:')
            tn.write(username + b"\n")
            tn.read_until(b'Password:')
            tn.write(password + b"\n")
            # 登录完毕后执行命令
            tn.read_until(b'#')
            tn.write(b'uttcli getbynm apScan apScanf maxAp' + b'\n')
            # 输出结果，判断
            time.sleep(0.5)
            result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
            print('-------------------输出结果------------------------')
            # 命令执行结果
            print('result:', result)
            result_list = result.split(r'\r\n')
            value = (result_list[1])[:-3]
            # print('value:',value)
            value1 = int(value) + 1
            value2 = str(value)
            if len(value2) != 1:  # 判断是否是个位数
                if value2[-1:] != '0':  # 参数值不为整10，则需要+1
                    value2 = int(value2[:-1]) + 1
                else:
                    value2 = value2[:-1]
            else:
                value2 = 1

            netname = netNamePage(self.driver, self.url)
            netname.click_wirelessExtension()
            time.sleep(0.5)
            netname.click_netName()
            time.sleep(1)
            # 1）查看页数
            maxpagenums = str(netname.getAttribute_byXpath(netname.maxpagenums1, 'max'))
            # print(maxpagenums, value2)
            if maxpagenums == str(value2):
                logger.info(u'负载均衡组最大页数显示正常')
            else:
                CapPic(self.driver)
                logger.info(u'SSID页面最大页数显示异常')
                raise Exception(u'SSID页面最大页数显示异常')
            # 2）查参数最大条目是否显示
            netname.click_pageend1()
            time.sleep(1)
            list_name1 = (list1_name % value)
            # print(list_name1)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = netname.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'SSID未达到最大条目数')
                raise Exception(u'SSID未达到最大条目数')
            else:
                logger.info(u'SSID可以达到最大条目数')
            # 3）查比参数值多1 是否找不到
            list_name1 = (list1_name % value1)
            # print(list_name)
            try:
                self.driver.implicitly_wait(2)
                list_name1 = netname.getText_byXpath(list_name1)
                # print('list_name1:', list_name1)
            except NoSuchElementException:
                logger.info(u'SSID未超过最大条目数')
            else:
                CapPic(self.driver)
                logger.info(u'SSID超过最大条目数')
                raise Exception(u'SSID超过最大条目数')
        else:
            logger.info(u'参数不支持AP管理')
            try:
                netname = netNamePage(self.driver, self.url)
                self.driver.implicitly_wait(2)
                netname.click_wirelessExtension()
                time.sleep(0.5)
                netname.click_netName()
                time.sleep(1)
            except AttributeError or NoSuchElementException:
                logger.info(u'软件不支持无线扩展，与参数表相符')
            else:
                CapPic(self.driver)
                logger.info(u'软件支持无线扩展，与参数表不符')
                raise Exception(u'软件支持无线扩展，与参数表不符')
        self.driver.quit()
        logger.info('test_016_loadBalance')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
