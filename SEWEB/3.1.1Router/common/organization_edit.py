#! -*-conding:utf-8 -*-
#@Time: 2018/12/28 0028 14:35
#@swzhou
'''
组织架构 新增 编辑 删除 组
'''

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import time
import unittest
import os.path
import socket


from common.LogGen import LogGen
logger = LogGen(Logger = 'organization_edit').getlog()
from common.CapPic import CapPic
from common.ReadConfig import getpath,getAssertText
from common.loginRoute import login
from pages.Organization_001_Memberspage import OrganizationMembersPage
from pages.basepage import BasePage

class organization_group(unittest.TestCase):

    def setUp(self):
        print('organizational_group start')
        # pass

    def group_add(self):
        u'''组织架构 - 新增组'''
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        organization = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        organization.click_UserManage()
        time.sleep(0.5)
        organization.click_userGroup()
        time.sleep(1)
        organization.click_addBtnNewTree1()
        time.sleep(1)
        organization.input_groupName('SelfComputerTest')
        organization.click_save()
        time.sleep(2)
        # 断言 增加的组名称是否相同：相同代表验证通过
        organization.click_userGroup() #再点击下“组织成员”，架构树会展开
        time.sleep(1)
        add_group_name=str(organization.getText_byID(organization.list_groupName1))
        self.assertEqual(add_group_name,'SelfComputerTest',msg='新增组出错')
        self.driver.quit()
        print('组织架构 - 新增组 验证成功')

    def group_delete(self):
        u'''组织架构 - 删除组'''
        nodata = getAssertText('nodata')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        organization = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        organization.click_UserManage()
        time.sleep(0.5)
        organization.click_userGroup()
        time.sleep(1)
        organization.click_list_groupName_c()
        organization.click_delBtnNewTree1()
        time.sleep(1)
        organization.click_ok()
        time.sleep(2)
        # 断言 成员列表中"暂无数据"：代表验证通过
        time.sleep(1)
        organization.click_list_Rootgroup_c()
        time.sleep(1)
        tips = str(organization.getText_byXpath(organization.listTips))
        self.assertEqual(tips, nodata, msg='删除组出错')
        self.driver.quit()
        print('组织架构 - 删除组 验证成功')

    def import_empty_template(self): #主要用于为其他引用组织架构时候清空组织架构
        u'''组织架构 - 判断组织架构不为空则导入空组织架构模板(清空组织架构)'''
        nodata = getAssertText('nodata')
        tempUser = getAssertText('tempUser')
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
        login.loginWeb2(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        organization = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        organization.click_UserManage()
        time.sleep(0.5)
        organization.click_userGroup()
        time.sleep(1)
        #先确认 仅ip/mac绑定、仅mac绑定 关闭
        organization.click_globalconfig()
        time.sleep(1)
        IPMACb_Cs = str(organization.getAttribute_byXpath(organization.IPMACb_Cs, 'checked'))
        Macb_Cs = str(organization.getAttribute_byXpath(organization.MACb_Cs, 'checked'))
        if IPMACb_Cs != 'true' or Macb_Cs != 'true':
            organization.click_IPMACb_C()
            time.sleep(0.5)
            organization.click_MACb_C()
            time.sleep(0.5)
            organization.click_saveAllSetting()
            time.sleep(3)
        IPMACb_Cs = str(organization.getAttribute_byXpath(organization.IPMACb_Cs, 'checked'))
        self.assertEqual(IPMACb_Cs, 'true', msg='"仅IP/MAC绑定用户能上网" 关闭出错')
        print('"仅IP/MAC绑定用户能上网" 关闭')
        Macb_Cs = str(organization.getAttribute_byXpath(organization.MACb_Cs, 'checked'))
        self.assertEqual(Macb_Cs, 'true', msg='"仅MAC绑定用户能上网" 关闭出错')
        print('"仅MAC绑定用户能上网" 关闭')

        organization.click_list_Rootgroup_c()
        time.sleep(1)
        groupID = organization.getAttribute_byLink(organization.groupID,attribute='id')

        # groupID = self.driver.find_element_by_link_text('临时用户').get_attribute('id')
        print('groupID:',groupID)  #空则为 “newTree_32_a”

        if str(groupID) == 'newTree_2_a':
            print('组织架构为空')
        else:
            organization.click_download()
            time.sleep(1)
            organization.click_chooseFile()
            if nodata == '暂无数据':
                filepath = batpath + 'SE_organizationalImport_emptyCn.exe'
            elif nodata == 'No data':
                filepath = batpath + 'SE_organizationalImport_emptyEn.exe'
            elif nodata == '暫無數據':
                filepath = batpath + 'SE_organizationalImport_emptyT.exe'
            #调用autoIt脚本上传组的cvs文件
            os.system(filepath)  # 注意脚本所在路径不要太复杂，比如下划线；autoIt内没关系
            time.sleep(2)
            organization.click_save()
            time.sleep(5)

            # 断言 成员列表中"暂无数据"：代表Root组中没有组
            organization.click_list_Rootgroup_c()
            time.sleep(1)
            listTips = organization.getText_byXpath(organization.listTips)
            self.assertEqual(str(listTips), nodata, msg='删除成功')

            # 断言 newTree_2_span id为临时用户：代表没有其他组
            groupText = str(organization.getText_byID(organization.list_groupName1))
            print('groupText:',groupText)
            self.assertEqual(groupText, tempUser, msg='"临时用户组"id 不为2')
            time.sleep(1)
        self.driver.quit()
        print('组织架构为空/导入空组织架构 成功')

    def add_user(self):
        u'''新增组织架构组 及 当前PC的用户'''
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        organization = OrganizationMembersPage(self.driver, self.url)

        # 打开用户管理 - 组织成员
        organization.click_UserManage()
        time.sleep(0.5)
        organization.click_userGroup()
        time.sleep(1)

        #普通用户
        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
         # 新增用户 仅IP 设置的为本机IP
        organization.click_addBtnNewTree1()
        time.sleep(1)
        organization.input_groupName('SelfComputerTest')
        organization.click_save()
        time.sleep(1)
        organization.click_addUser()
        time.sleep(1)
        organization.input_UserName('SelfComputer')
        organization.input_normalIP(pcaddr)
        organization.click_save()
        time.sleep(2)

        # 断言 增加的IP与实际IP相同：代表验证通过
        organization.click_userGroup()  #再点击下“组织成员”，架构树会展开
        time.sleep(0.5)
        organization.click_list_groupName_c()
        time.sleep(1)
        listAddIP = str(organization.getText_byXpath(organization.listAddIP))
        self.assertEqual(listAddIP,pcaddr,msg='新增 普通用户出错')
        self.driver.quit()
        print('组织架构 - 新增普通用户 成功')


    def tearDown(self):
        print('organizational_group over')

if __name__=='__main__':
    unittest.main()
