#! -*-conding:utf-8 -*-
#@Time: 2019/1/12 0012 11:22
#@swzhou
'''
组织架构 成员列表管理
'''

import time
import unittest
import os.path
import socket
import sys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.select import Select
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.organization_edit import organization_group
from common.call_FireFox import call_Firefox
from pages.Organization_001_Memberspage import OrganizationMembersPage
from pages.Organization_003_userAuthpage import Organization_userAuthPage
logger = LogGen(Logger = 'Members_002_members').getlog()


class Members(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_add_user(self):
        u'''组织架构 - 新增成员'''
        organization_group.import_empty_template(self)  # 调用判断 有组织架构清空

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)

        #普通用户
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
         # 新增用户 仅IP 设置的为本机IP
        group.click_addBtnNewTree1()
        time.sleep(1)
        group.input_groupName('SelfComputerTest')
        group.click_save()
        time.sleep(1)
        group.click_addUser()
        time.sleep(1)
        group.input_UserName('SelfComputer1')
        group.input_normalIP(pcaddr)
        group.click_save()
        time.sleep(2)

        # 断言 增加的IP与实际IP相同：代表验证通过
        group.click_userGroup()
        group.click_list_groupName_c()
        time.sleep(1)
        listAddIP=str(group.getText_byXpath(group.listAddIP))
        self.assertEqual(listAddIP,pcaddr,msg='新增 普通用户出错')
        print('组织架构 - 新增普通用户 验证成功')

        # 再新建一个组
        time.sleep(1)
        group.click_addBtnNewTree1()
        time.sleep(1)
        group.input_groupName('SelfComputerTest2')
        group.click_save()
        time.sleep(2)

        #用户认证页面 判断是否支持web认证
        webauth = 1 #预设web和pppoe认证为1，支持
        PPPoEAuth = 1
        auth = Organization_userAuthPage(self.driver, self.url)
        auth.click_userAuth()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            auth.find_WebAuthC()
        except ElementNotVisibleException:
            webauth = 0
        try:
            auth.find_pppoeAuthC()
        except ElementNotVisibleException:
            PPPoEAuth = 0

        self.driver.implicitly_wait(10)
        group.click_userGroup()
        time.sleep(1)
        if webauth == 1:
            # 新增web认证用户（部分型号不支持web认证）
            group.click_addUser()
            time.sleep(1)
            group.input_UserName('webtest1')
            group.click_authuser()
            time.sleep(1)
            sel = group.selelement_byName(group.authType)
            Select(sel).select_by_value('Web')
            time.sleep(1)
            group.input_authAccount('webtest1')
            group.input_authPassword('webtest1')
            group.click_save()
            time.sleep(2)
            # 断言 添加的账号 认证方式和认证账号 是否正常
            group.click_list_groupName_c()
            time.sleep(1)
            list_authType = group.getText_byXpath(group.list_authType)
            list_authAccount = group.getText_byXpath(group.list_authAccount)
            self.assertEqual(str(list_authType), 'Web', msg='认证方式显示不为“Web”')
            self.assertEqual(str(list_authAccount), 'webtest1', msg='认证账号不为“webtest1”')

        if PPPoEAuth == 1:
            #新增pppoe用户（部分型号不支持PPPoE server，目前支持web认证的都支持pppoe server）
            group.click_addUser()
            time.sleep(1)
            group.input_UserName('zpppoetest1')
            group.click_authuser()
            time.sleep(1)
            sel = group.selelement_byName(group.authType)
            Select(sel).select_by_value('PPPoE')
            time.sleep(0.5)
            group.input_authAccount('pppoetest1')
            group.input_authPassword('pppoetest1')
            group.click_save()
            time.sleep(2)
            #断言
            group.click_list_groupName_c()
            time.sleep(1)
            #pppoe账号排序默认在web账号之前的第二行，这里还是判断第二行的信息
            list_authType = group.getText_byXpath(group.list_authType)
            list_authAccount = group.getText_byXpath(group.list_authAccount)
            self.assertEqual(str(list_authType), 'PPPoE', msg='认证方式显示不为“PPPoE”')
            self.assertEqual(str(list_authAccount), 'pppoetest1', msg='认证账号不为“pppoetest1”')
            print('组织架构 - 新增PPPoE用户 验证成功')

        self.driver.quit()
        logger.info('test_001_add_user passed')

    def test_002_operation_member(self):
        u'''对成员进行操作：移动、编辑、删除'''
        nodata = getAssertText('nodata')
        ScanTipsA = getAssertText('ScanTipsA')

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)

        #移动 上一个def中的账号到 新建组 SelfComputerTest2 中
        group.click_list_groupName_c()
        time.sleep(2)
        group.input_search('SelfComputer1')
        time.sleep(0.5)
        group.click_searchB()
        time.sleep(1)
        group.click_checklist()
        time.sleep(0.5)
        group.click_moveUserTo()
        time.sleep(1)
        selgroup = group.selelement_byName(group.selmoveUserTo)
        Select(selgroup).select_by_value('3') #组中的值是数字，这里选择'SelfComputerTest2'
        group.click_save()
        time.sleep(1)
        # 断言 添加的账号 名称和组 是否正常
        group.click_list_groupName2()
        time.sleep(2)
        list_authAccount2 = group.getText_byXpath(group.list_authAccount2)
        self.assertEqual(str(list_authAccount2), 'SelfComputer1', msg='账号不为“SelfComputer”')
        list_authgroup2 = group.getText_byXpath(group.list_authgroup2)
        self.assertEqual(str(list_authgroup2), 'SelfComputerTest2', msg='SelfComputer 账号移动失败')

        #编辑 成员
        # 修改SelfComputer账号用户名为 ‘SelfComputer2’
        group.click_list_groupName2()
        time.sleep(2)
        group.click_edituser1()
        time.sleep(1)
        group.input_UserName('SelfComputer2')
        group.click_save()
        time.sleep(1)
        # 断言 编辑的账号 用户名是否为 ‘webtest2’
        group.click_list_groupName2()
        time.sleep(1)
        changedusername = group.getText_byXpath(group.changedusername)
        self.assertEqual(str(changedusername), 'SelfComputer2', msg='用户名 修改失败')

        # 删除 成员账号
        group.click_list_groupName2()
        time.sleep(2)
        group.click_deluser1()
        time.sleep(1)
        group.click_ok()
        time.sleep(1)
        # 断言 删除后 列表显示“暂无数据”
        group.click_list_groupName2()
        time.sleep(1)
        listtips = group.getText_byXpath(group.listTips)
        self.assertEqual(str(listtips), nodata, msg='删除失败')

        # 扫描
        group.click_allScan()
        time.sleep(1)
        group.click_allScan1()
        time.sleep(2)
        ScanTips = group.getText_byClass(group.ScanTips)
        self.assertEqual(str(ScanTips), ScanTipsA,msg='扫描出错')
        time.sleep(20)
        Scanlist = group.getText_byXpath(group.Scanlist)
        self.assertIsNotNone(Scanlist,msg='扫描出错')
        self.driver.quit()
        logger.info('test_002_operation_member passed')

    def test_003_import_export(self):
        u'''组织架构 - 导入导出'''
        organization_csv = getAssertText('organization_csv')
        organization_csv3 = getAssertText('organization_csv3')
        tempUser = getAssertText('tempUser')
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
        #先删除组织成员路径中 "组织成员20""织成员3333"开头的 csv文件
        call_Firefox.del_organization_csv(self)
        #调用Firefox 导出组织架构
        call_Firefox.Firefox_login_web(self)
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        #导出组织架构
        group.click_outload()
        time.sleep(1)

        # 进行配置文件命名修改
        path=os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path)
        files = os.listdir(r'%s' % path) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        #通过文件名称判断 修改为指定的文件名
        for filename in files:
            portion = os.path.splitext(filename) #splitext()用于返回 文件名和扩展名 元组
            # print(portion2)
            if organization_csv in str(portion[0]): #如果文件名种包含"组织成员20"
                if portion[1] == '.csv':  #如果后缀是 .xml
                    newname = organization_csv3+'.csv'
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir=(r'%s' % path) +filename
                    newnamedir=(r'%s' % path) +newname
                    #修改文件名称（与autoIt上传脚本中上传的文件名称一致）
                    os.rename(filenamedir,newnamedir)
        print('组织架构 - 导出 验证成功')

        #更改下组织架构
        time.sleep(1)
        group.click_addBtnNewTree1()
        time.sleep(1)
        group.input_groupName('SelfComputerTest3')
        time.sleep(0.5)
        group.click_save()
        time.sleep(2)
        self.driver.quit()

        #导入 刚导出的 修改配置之前 的组织架构
        login.loginWeb2(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_download()
        time.sleep(1)
        group.click_chooseFile()
        time.sleep(1)
        # 调用autoIt脚本上传组的cvs文件
        if organization_csv == '组织成员20':
            autoItScript = batpath + 'SE_organizationalimport_groupNewCn.exe'
        if organization_csv == 'Groupmembers20':
            autoItScript = batpath + 'SE_organizationalimport_groupNewEn.exe'
        os.system('%s' % autoItScript)
        time.sleep(2)
        group.click_save()
        time.sleep(5)
        # 断言 组只有4个：代表验证通过
        time.sleep(1)
        groupId = str(group.getText_byID(group. list_groupName3))
        print(groupId)
        self.assertEqual(groupId,tempUser, msg='"临时用户组"id 不为4,导入组织架构有误')

        #删除 组织成员3333.csv 文件
        call_Firefox.del_organization_csv(self)
        self.driver.quit()
        print('组织架构 - 导入 验证成功')

        #导入空组织架构 以 清空
        organization_group.import_empty_template(self)  # 判断是否有组织架构，有则清空

        logger.info('test_003_import_export passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()