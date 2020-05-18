#! -*-conding:utf-8 -*-
#@Time: 2019/1/11 0011 17:31
#@swzhou
'''
组织架构 新增 编辑 删除 组
'''

import time
import unittest
import os.path
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.organization_edit import organization_group
from pages.Organization_001_Memberspage import OrganizationMembersPage
logger = LogGen(Logger = 'Members_001_Groups').getlog()

class MembersGroups(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_groupAdd(self):
        u'''组织架构 - 新增组'''
        organization_group.import_empty_template(self)#判断是否有组织架构，有则清空

        organization_group.group_add(self)  # 新增组

        logger.info('test_001_groupAdd passed')

    def test_002_groupEdit(self):
        u'''组织架构 - 编辑组'''
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        group = OrganizationMembersPage(self.driver, self.url)
        # 打开用户管理 - 组织成员
        group.click_UserManage()
        time.sleep(0.5)
        group.click_userGroup()
        time.sleep(1)
        group.click_list_groupName_c()
        time.sleep(0.5)
        group.click_editBtnnewTree1()
        time.sleep(1)
        group.input_groupName('changed')
        group.click_save()
        time.sleep(2)
        # 断言 增加的组名称是否相同：相同代表验证通过
        group.click_userGroup()  # 再点击下“组织成员”，架构树会展开
        time.sleep(1)
        add_groupName = str(group.getText_byID(group.list_groupName1))
        self.assertEqual(add_groupName, 'changed', msg='编辑组出错')
        self.driver.quit()
        logger.info('test_002_groupEdit passed')

    def test_003_groupDelete(self):
        u'''组织架构 - 删除组'''
        organization_group.group_delete(self)  # 删除组
        logger.info('test_003_groupDelete passed')

    def test_004_group_importMAXgroup(self):
        u'''组织架构 - 最大组'''
        tempUser = getAssertText('tempUser')
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
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
        #调用autoIt脚本上传组的cvs文件
        if tempUser == '临时用户':
            autoItScript = batpath + 'SE_organizationalimport_groupCn.exe'
        elif tempUser == 'Temp':
            autoItScript = batpath + 'SE_organizationalimport_groupEn.exe'
        os.system(autoItScript)  # 注意脚本所在路径不要太复杂，比如下划线；autoIt内没关系
        time.sleep(2)
        group.click_save()
        time.sleep(5)

        # # 断言 通过临时用户的ID，D525和j1800是128，510G是64，可能还有32
        # self.dr.find_element_by_link_text('临时用户').click()

        groupID = group.getAttribute_byLink(tempUser,'id')
        print(groupID)

        logger.info('最大组ID为%s' % groupID)
        Num=['newTree_32_a','newTree_64_a','newTree_128_a']
        self.assertIn(groupID,Num,msg='临时用户组 ID不对，导入组出错')
        self.driver.quit()
        logger.info('test_004_group_importMAXgroup passed')

    def test_005_import_emptyTemplate(self): #清空组织架构
        u'''组织架构 - 判断组织架构不为空则导入空组织架构模板(清空组织架构)'''
        organization_group.import_empty_template(self)  # 调用判断 有组织架构清空

        logger.info('test_005_import_emptyTemplate passed')


    def tearDown(self):
        print('Members_Groups over')

if __name__=='__main__':
    unittest.main()

