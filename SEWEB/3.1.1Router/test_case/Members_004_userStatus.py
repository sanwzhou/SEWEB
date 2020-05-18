#! -*-conding:utf-8 -*-
#@Time: 2019/1/12 0012 17:11
#@swzhou
'''
仅绑定用户上网  仅IP/MAC绑定用户、仅MAC绑定用户,
更换电脑需要注意 修改绑定的mac地址
'''


import time
import unittest
import os.path
import socket
import subprocess
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,gettelnet
from common.pingTest import pingTestIP
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_001_Memberspage import OrganizationMembersPage
from pages.Organization_002_userStatuspage import Organization_userStatusPage
from pages.Organization_004_userBlackpage import Organization_userBlackPage
logger = LogGen(Logger = 'Members_004_binding').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
host = gettelnet('host')

class userStatus(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_userList(self):
        u'''用户状态 列表'''
        tempUser = getAssertText('tempUser')
        Minute = getAssertText('minute')
        Ban = getAssertText('Ban')
        #003中设置了ip/mac绑定上网，这里增加一个判断联网
        pingTestIP()  # 避免判断失误
        p = pingTestIP()
        if p == 'N':  # 如果不通
            # 1、改回DHCP， 调用bat脚本
            os.system('%s' % (batpath + 'changeDhcpIp.bat'))
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
                raise Exception('未获取到地址')
        pingTestIP('www.baidu.com') #避免判断失误
        p = pingTestIP('www.baidu.com')
        if p == 'N':
            # 1、将mac改回， 调用bat脚本
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
            #3、关闭"仅MAC绑定用户能上网" 关闭ip/mac绑定 以访003出错
            login.loginWeb(self)  # admin账号登录
            self.driver.implicitly_wait(10)
            group = OrganizationMembersPage(self.driver, self.url)
            # 打开用户管理 - 组织成员
            group.click_UserManage()
            time.sleep(0.5)
            group.click_userGroup()
            time.sleep(1)
            group = OrganizationMembersPage(self.driver, self.url)
            group.click_globalconfig()
            time.sleep(1)
            group.click_IPMACb_C()
            group.click_MACb_C()
            time.sleep(0.5)
            group.click_saveAllSetting()
            time.sleep(1)
            IPMACb_Cs = str(group.getAttribute_byXpath(group.IPMACb_Cs, 'checked'))
            self.assertEqual(IPMACb_Cs, 'true', msg='"仅IP/MAC绑定用户能上网" 关闭出错')
            print('"仅IP/MAC绑定用户能上网" 关闭')
            Macb_Cs = str(group.getAttribute_byXpath(group.MACb_Cs, 'checked'))
            self.assertEqual(Macb_Cs, 'true', msg='"仅MAC绑定用户能上网" 关闭出错')
            print('"仅MAC绑定用户能上网" 关闭')
            self.driver.quit()

        # 打开用户管理 - 用户状态
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        #定义页面显示元素变量
        ID = str(status.getText_byXpath(status.ID))
        username = str(status.getText_byXpath(status.username))
        group = str(status.getText_byXpath(status.group))
        VlanID = str(status.getText_byXpath(status.VlanID))
        IP = str(status.getText_byXpath(status.IP))
        mac = str(status.getText_byXpath(status.mac))
        authmode = str(status.getText_byXpath(status.authmode))
        online_time_length = str(status.getText_byXpath(status.online_time_length))
        Uploading_data = str(status.getText_byXpath(status.Uploading_data))
        Downing_data = str(status.getText_byXpath(status.Downing_data))
        Uploading_speed = str(status.getText_byXpath(status.Uploading_speed))
        Downing_speed = str(status.getText_byXpath(status.Downing_speed))
        edit = str(status.getText_byXpath(status.edit))

        # 断言 用户列表是否显示有误
        time.sleep(1)
        self.assertEqual(ID,'1',msg='ID出错')
        print('用户状态 - ID 验证成功')
        self.assertIsNotNone(username, msg='用户名 出错')
        print('用户状态 - 用户名 验证成功')
        self.assertEqual(group,tempUser,msg='所属组 出错') #脚本在最后会清空组织架构，所以脚本在一开始新建组，用户都是 临时用户
        print('用户状态 - 所属组 验证成功')
        self.assertIsNotNone(VlanID,msg='VLANID 出错')
        print('用户状态 - VLANID 验证成功')
        self.assertIn('192.168.', IP, msg='IP 出错') #lan口地址段
        print('用户状态 - IP 验证成功')
        self.assertEqual(len(mac),17, msg='mac 出错') #判断mac地址长度
        print('用户状态 - mac 验证成功')
        self.assertIsNotNone(authmode, msg='认证方式 出错')
        print('用户状态 - 认证方式 验证成功')
        self.assertIn(Minute, online_time_length, msg='在线时长 出错')  # 在线时长是否包含“分”
        print('用户状态 - 在线时长 验证成功')
        self.assertIsNotNone(Uploading_data, msg='上传数据 出错')
        print('用户状态 - 上传数据 验证成功')
        self.assertIsNotNone(Downing_data, msg='下载数据 出错')
        print('用户状态 - 下载数据 验证成功')
        self.assertIsNotNone(Uploading_speed, msg='上传速度 出错')
        print('用户状态 - 上传速度 验证成功')
        self.assertIsNotNone(Downing_speed, msg='下载速度 出错')
        print('用户状态 - 下载速度 验证成功')
        self.assertEqual(edit, Ban, msg='拉黑菜单显示 出错')
        print('用户状态 - 拉黑菜单显示 验证成功')
        self.driver.quit()
        logger.info('test_001_userList passed')

    def test_002_MovetoOther(self):
        u'''用户 ：移动到其他组'''
        organization_group.import_empty_template(self)  # 判断是否有组织架构，有则清空

        #新建组
        organization_group.group_add(self)

        #切回用户状态列表
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)
        #移动 列表中第一个 到 新建组'SelfComputerTest' 中
        #获取列表中第一个被移动的用户的IP
        list_IP1 = str(status.getText_byXpath(status.list_IP1))
        status.click_checkbox1()
        time.sleep(0.5)
        status.click_move()
        time.sleep(1)
        status.click_save()
        time.sleep(2)
        # 断言
        group = OrganizationMembersPage(self.driver, self.url)
        group.click_userGroup()
        time.sleep(1)
        group.click_list_groupName_c()
        time.sleep(2)
        listIP = str(group.getText_byXpath(group.listAddIP))
        self.assertEqual(listIP, list_IP1, msg='移动出错 IP不一致')
        authgroup = str(group.getText_byXpath(group.list_authgroup2))
        self.assertEqual(authgroup, 'SelfComputerTest', msg='移动出错 所属组 不一致')
        self.driver.quit()
        print('移动到其他组 验证成功')

        # 删除新建组'SelfComputerTest'，使在线用户回到临时用户组
        time.sleep(1)
        organization_group.group_delete(self)
        logger.info('test_002_MovetoOther passed')

    def test_003_movetoBlicklist(self):
        u'''用户 ：移动到黑名单'''
        nodata = getAssertText('nodata')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        status = Organization_userStatusPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        status.click_UserManage()
        time.sleep(0.5)
        status.click_userstatus()
        time.sleep(1)
        # 将页面刷新按钮改成“手动”
        sel = status.selelement_byXpath(status.selmanual)
        Select(sel).select_by_value('manual')
        time.sleep(1)
        status.click_refreshtable()
        time.sleep(1)

        #需要设备下有另一个终端（至少两个终端），因为不能拉黑自己并且用户状态的用户是在线的（注意用户与lan口在同网段才会在线）
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = str(socket.gethostbyname(socket.getfqdn(socket.gethostname())))
        #获取第一行第二行IP
        IP_line1 = str(status.getText_byXpath(status.list_IP1))
        IP_line2 = str(status.getText_byXpath(status.list_IP2))
        #判断选出非自身主机的IP
        if pcaddr == IP_line1:
            Selected_IP = IP_line2
        else:
            Selected_IP = IP_line1

        #右上角拉黑
        #在列表中搜索选中的IP
        status.input_search(Selected_IP)
        status.click_searchb()
        time.sleep(1)
        #选中列表中第一个拉黑，获取其mac地址
        status.click_listCheckbox1()
        Selected_MAC=status.getText_byXpath(status.Selected_MAC)
        status.click_addToBlackList()
        time.sleep(1)
        status.click_ok()
        time.sleep(2)
        # 断言 黑名单列表中的MAC和北移动的用户的mac
        blacklist = Organization_userBlackPage(self.driver,self.url)
        blacklist.click_blacklist()
        time.sleep(100)
        MAC_black = str(blacklist.getText_byXpath(blacklist.blicklist_mac))
        self.assertEqual(MAC_black,Selected_MAC, msg='黑名单移动出错 MAC不一致')
        print('移动到黑名单-右上角拉黑 验证成功')
        # 删除黑名单列表中的用户
        blacklist.click_delete()
        time.sleep(1)
        blacklist.click_ok()
        time.sleep(1)

        #用户列表 拉黑
        status.click_userstatus()
        time.sleep(1)
        # 在列表中搜索选中的IP
        status.input_search(Selected_IP)
        status.click_searchb()
        time.sleep(1)
        # 选中列表中第一个拉黑，获取其mac地址
        Selected_MAC = status.getText_byXpath(status.Selected_MAC)
        status.click_calldown()
        time.sleep(1)
        status.click_ok()
        time.sleep(2)
        # 断言 黑名单列表中的MAC和北移动的用户的mac
        blacklist.click_blacklist()
        time.sleep(1)
        MAC_black = str(blacklist.getText_byXpath(blacklist.blicklist_mac))
        self.assertEqual(MAC_black, Selected_MAC, msg='黑名单移动出错 MAC不一致')
        print('移动到黑名单-列表中拉黑 验证成功')
        # 删除黑名单列表中的用户
        blacklist.click_delete()
        time.sleep(1)
        blacklist.click_ok()
        time.sleep(1)
        list_tips=str(blacklist.getText_byXpath(blacklist.list_tips))
        self.assertEqual(list_tips,nodata,msg='黑名单删除失败')
        self.driver.quit()
        logger.info('test_003_movetoBlicklist passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()


