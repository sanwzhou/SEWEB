#! -*-conding:utf-8 -*-
#@Time: 2019/1/12 0012 15:24
#@swzhou
'''
仅绑定用户上网  仅IP/MAC绑定用户、仅MAC绑定用户,
更换电脑需要注意 修改绑定的mac地址
'''
import subprocess
import time
import unittest
import os.path
import socket
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.pingTest import pingTestIP
from common.ReadConfig import getAssertText,getweb
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_001_Memberspage import OrganizationMembersPage
logger = LogGen(Logger = 'Members_003_binding').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
PcMac = getweb('PcMac')
savesucess = getAssertText('savesucess')


class onlyBinding(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_IPMACBinding(self):
        u'''仅IP/MAC绑定用户 上网'''
        organization_group.import_empty_template(self)  # 判断是否有组织架构，有则清空

        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

        #先创建用户组
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_addBtnNewTree1()
        time.sleep(1)
        group.input_groupName('bangdingTest')
        group.click_save()
        time.sleep(2)
        group.click_userGroup()
        time.sleep(1)
        list_groupName1 = str(group.getText_byID(group.list_groupName1))
        self.assertEqual(list_groupName1, 'bangdingTest', msg='新增组出错')
        print('组织架构 - 新增组完成')

        group.click_addUser()
        time.sleep(1)
        group.input_UserName('bangdingTest')
        group.click_IPMACb()
        time.sleep(1)
        group.input_normalIPMac_IP(pcaddr)
        group.input_normalIPMac_Mac(PcMac)
        group.click_save()
        time.sleep(2)
        group.click_list_groupName_c()
        time.sleep(1)
        listAddIP = group.getText_byXpath(group.listAddIP)
        self.assertEqual(listAddIP,pcaddr,msg='新增 用户IP出错')
        listAddMAC = group.getText_byXpath(group.listAddMAC)
        self.assertEqual(listAddMAC,PcMac, msg='新增 用户MAC出错')
        print('组织架构 - 新增用户完成')

        # 判断联网 ，不能上网则报错
        p = pingTestIP('223.5.5.5')
        if p == 'N':
            raise Exception('connect failed.')

        #开启"仅IP/MAC绑定用户能上网"
        group.click_globalconfig()
        time.sleep(1)
        group.click_IPMACb_E()
        time.sleep(0.5)
        group.click_saveAllSetting()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        tips = str(group.getText_byClass(group.tips))
        time.sleep(1)
        self.assertEqual(tips, savesucess, msg='"仅IP/MAC绑定用户能上网" 开启出错')
        print('"仅IP/MAC绑定用户能上网" 开启')
        # 判断联网 ，不能上网则报错
        pingTestIP('www.baidu.com') #避免失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')

        # 修改MAC为 非绑定的MAC地址
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMac.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            # raise Exception('未获取到地址1')
            # 开启绑定情况下 仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')

        # 判断联网 ,测试该项改完mac之后前几个包有可能可以ping通，为避免判断失误，加一个缓冲
        pingTestIP('www.baidu.com') #避免失误
        pingTestIP('www.163.com') #避免失误

        #判断联网 ,非绑定用户应该不能上网
        time.sleep(3)
        p = pingTestIP('114.114.114.114')
        if p == 'Y':
            raise Exception('非绑定用户依旧可以上网')
        time.sleep(1)
        #将mac改回
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            # raise Exception('未获取到地址1')
            # 开启绑定情况下 仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')
        # 判断联网 ，不能上网则报错
        pingTestIP('www.baidu.com') #避免失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')
        logger.info('test_001_IPMACBinding passed')

    def test_002_MAC_binding(self):
        u'''仅MAC绑定用户 上网'''
        organization_group.import_empty_template(self)  # 判断是否有组织架构，有则清空

        # 增加绑定mac用户
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_addBtnNewTree1()
        time.sleep(1)
        group.input_groupName('bangdingTest')
        group.click_save()
        time.sleep(2)
        # 断言 增加的组名称是否相同：相同代表验证通过
        group.click_userGroup()  # 再点击下“组织成员”，架构树会展开
        time.sleep(1)
        list_groupName1 = str(group.getText_byID(group.list_groupName1))
        self.assertEqual(list_groupName1, 'bangdingTest', msg='新增组出错')
        print('组织架构 - 新增组完成')
        time.sleep(1)
        group.click_addUser()
        time.sleep(1)
        group.input_UserName('bangdingTest2')
        group.click_MACb()
        time.sleep(0.5)
        group.input_normalMac(PcMac)
        group.click_save()
        time.sleep(2)
        # 断言 增加的MAC与实际MAC相同：代表验证通过
        group.click_list_groupName_c()
        time.sleep(1)
        listAddMAC = group.getText_byXpath(group.listAddMAC)
        self.assertEqual(listAddMAC, PcMac, msg='新增 用户MAC出错')
        print('组织架构 - 新增绑定MAC用户 成功')
        # 判断联网 ，不能上网则报错
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')

        # 开启"仅MAC绑定用户能上网"
        group.click_globalconfig()
        time.sleep(1)
        group.click_MACb_E()
        time.sleep(0.5)
        group.click_saveAllSetting()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        tips = str(group.getText_byClass(group.tips))
        time.sleep(1)
        self.assertEqual(tips, savesucess, msg='"仅IP/MAC绑定用户能上网" 开启出错')
        print('"仅IP/MAC绑定用户能上网" 开启')
        # 判断联网 ，不能上网则报错
        pingTestIP('www.baidu.com') #避免失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')

        # 修改MAC为 非绑定的MAC地址
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMac.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功1', n)
                break
        else:
            # raise Exception('未获取到地址1')
            # 开启绑定情况下 仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')

        # 判断联网 ,测试该项改完mac之后前几个包有可能可以ping通，为避免判断失误，加一个缓冲
        pingTestIP('www.baidu.com') #避免失误
        pingTestIP('www.163.com') #避免失误
        time.sleep(3)
        # 判断联网 ,非绑定用户应该不能上网
        p = pingTestIP('www.sina.com.cn')
        if p == 'Y':
            raise Exception('非绑定用户依旧可以上网')

        time.sleep(1)
        # 将mac改回
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            raise Exception('未获取到地址1')

        # 判断联网 ，不能上网则报错
        pingTestIP('www.baidu.com') #避免失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')
        logger.info('test_002_MAC_binding passed')

    def tearDown(self):
        time.sleep(1)
        # 将mac改回
        # 调用bat脚本
        os.system('%s' % (batpath + 'changeMacToBack.bat'))
        time.sleep(5)
        n = 0
        while n < 30:
            # 获取本机ip 默认有线地址，有线断开会显示无线
            pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
            print(pcaddr_new, n)
            if '192.168.' not in str(pcaddr_new):
                time.sleep(2)
                n += 1
            else:
                print('IP地址已自动获取成功', n)
                break
        else:
            # raise Exception('未获取到地址1')
            # 开启绑定情况下 仅更改mac 可能会获取不到地址
            os.system('%s' % (batpath + 'ipconfig_release.bat'))
            time.sleep(5)
            os.system('%s' % (batpath + 'ipconfig_renew.bat'))
            time.sleep(5)
            i = 0
            while i < 30:
                # 获取本机ip 默认有线地址，有线断开会显示无线
                pcaddr_new = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
                print(pcaddr_new, i)
                if '192.168.' not in str(pcaddr_new):
                    time.sleep(2)
                    i += 1
                else:
                    print('IP地址已自动获取成功2', i)
                    break
            else:
                raise Exception('未获取到地址2')
        time.sleep(2)
        # 判断联网 ，不能上网则报错
        pingTestIP('www.baidu.com') #避免失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            raise Exception('connect failed.')
        nodata = getAssertText('nodata')
        # 关闭"IP/MAC绑定用户能上网"
        group = OrganizationMembersPage(self.driver, self.url)
        group.click_globalconfig()
        time.sleep(1)
        group.click_IPMACb_C()
        time.sleep(0.5)
        group.click_MACb_C()
        time.sleep(0.5)
        group.click_saveAllSetting()
        time.sleep(2)
        IPMACb_Cs = str(group.getAttribute_byXpath(group.IPMACb_Cs,'checked'))
        self.assertEqual(IPMACb_Cs, 'true', msg='"仅IP/MAC绑定用户能上网" 关闭出错')
        print('"仅IP/MAC绑定用户能上网" 关闭')
        Macb_Cs = str(group.getAttribute_byXpath(group.MACb_Cs,'checked'))
        self.assertEqual(Macb_Cs, 'true', msg='"仅MAC绑定用户能上网" 关闭出错')
        print('"仅MAC绑定用户能上网" 关闭')
        # 删除用户组
        group.click_list_groupName_c()
        time.sleep(1)
        group.click_delBtnNewTree1()
        time.sleep(1)
        group.click_ok()
        time.sleep(1)
        # 断言 成员列表中"暂无数据"：代表Root组中没有组
        group.click_list_Rootgroup_c()
        time.sleep(1)
        listtips = group.getText_byXpath(group.listTips)
        self.assertEqual(str(listtips),nodata, msg='删除成功')
        print('已删除用户组及绑定用户')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

