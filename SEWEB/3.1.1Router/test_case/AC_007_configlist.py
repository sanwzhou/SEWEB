#! -*-conding:utf-8 -*-
#@Time: 2019/2/1 0001 14:27
#@swzhou
'''
AP配置文件列表：
列表显示、导入导出、删除、
重启恢复安测，配置文件不丢失
'''

import time
import unittest
import os
import os.path
import sys
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.call_FireFox import call_Firefox
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.AC_001_NetNamePage import netNamePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from test_case.sysConfig_009_Reboot import Reboot
from test_case.sysConfig_008_configuration import configuration
logger = LogGen(Logger = 'AC_007_configlist').getlog()


class Configlist(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        os.system('taskkill /im "tftpd32.exe" /F')
        # pass

    def test_000_makeconfig(self):
        u'''对AP进行操作，谨防AP恢复后没有配置文件生成'''
        # 在恢复出厂后 未对V1 AP操作 会没有V1对应AP的配置文件生成（主要是针对v1 AP ，这里直接修改设备名称）
        # 003中 重启和恢复出厂有引用test_001_configlist 所以单独出来，不放在001中
        OnlineA = getAssertText('OnlineA')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        configlist = deviceMgmtPage(self.driver,self.url)
        configlist.click_wirelessExtension()
        time.sleep(0.5)
        configlist.click_deviceMgmt()
        time.sleep(1)
        x = 0
        while x < 100:
            configlist.click_refreshtable()
            time.sleep(1)
            list_status1 = configlist.getText_byXpath(configlist.list_status1)
            list_status2 = configlist.getText_byXpath(configlist.list_status2)
            list_status3 = configlist.getText_byXpath(configlist.list_status3)
            list_status4 = configlist.getText_byXpath(configlist.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(configlist.getAttribute_byXpath(configlist.list_channel1, 'data-local'))
                channel2 = str(configlist.getAttribute_byXpath(configlist.list_channel2, 'data-local'))
                channel3 = str(configlist.getAttribute_byXpath(configlist.list_channel3, 'data-local'))
                channel4 = str(configlist.getAttribute_byXpath(configlist.list_channel4, 'data-local'))
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
            raise Exception('AP  未能同步2.4G无线接口')
        #操作AP 修改AP名称
        configlist.click_list_name1()
        time.sleep(0.5)
        configlist.input_list_namein1('1')
        time.sleep(0.5)
        configlist.click_list_nameS1()
        time.sleep(8)
        name_save1 = str(configlist.getAttribute_byXpath(configlist.list_name1s, 'data-local'))
        self.assertEqual(name_save1, '1', msg='V2 AP1名称修改出错')
        configlist.click_list_name2()
        time.sleep(0.5)
        configlist.input_list_namein2('1')
        time.sleep(0.5)
        configlist.click_list_nameS2()
        time.sleep(8)
        name_save2 = str(configlist.getAttribute_byXpath(configlist.list_name2s, 'data-local'))
        self.assertEqual(name_save2, '1', msg='V2 AP1名称修改出错')
        configlist.click_list_name3()
        time.sleep(0.5)
        configlist.input_list_namein3('1')
        time.sleep(0.5)
        configlist.click_list_nameS3()
        time.sleep(8)
        name_save3 = str(configlist.getAttribute_byXpath(configlist.list_name3s, 'data-local'))
        self.assertEqual(name_save3, '1', msg='V1 AP1名称修改出错')
        configlist.click_list_name4()
        time.sleep(0.5)
        configlist.input_list_namein4('1')
        time.sleep(0.5)
        configlist.click_list_nameS4()
        time.sleep(8)
        name_save4 = str(configlist.getAttribute_byXpath(configlist.list_name4s, 'data-local'))
        self.assertEqual(name_save4, '1', msg='V1 AP2名称修改出错')
        time.sleep(5) #等待AP的配置文件生成
        self.driver.quit()
        logger.info('test_000_makeconfig passed')

    def test_001_configlist(self):
        u'''配置文件列表显示'''
        OnlineA = getAssertText('OnlineA')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        netname = netNamePage(self.driver, self.url)
        netname.click_wirelessExtension()
        time.sleep(0.5)
        netname.click_netName()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(3)
            netname.find_ok()
        except NoSuchElementException:
            pass
        else:
            print('打开无线扩展，等待AP上线')
            time.sleep(5)
            ManageProtocol = netname.getAttribute_byId(netname.ManageProtocolss, 'checktype')
            if ManageProtocol == '0':  # 1为打开 0为关闭 开启兼容模式
                netname.click_ManageProtocols()
            print('打开兼容模式，等待AP上线')
            time.sleep(70)
        self.driver.implicitly_wait(10)
        configlist = deviceMgmtPage(self.driver,self.url)
        configlist.click_deviceMgmt()
        time.sleep(5)
        # 确认在线AP序列号，确认配置文件列表中包含有对应ap的配置文件
        # 先确认AP在线
        x = 0
        while x < 100:
            configlist.click_refreshtable()
            time.sleep(1)
            list_status1 = configlist.getText_byXpath(configlist.list_status1)
            list_status2 = configlist.getText_byXpath(configlist.list_status2)
            list_status3 = configlist.getText_byXpath(configlist.list_status3)
            list_status4 = configlist.getText_byXpath(configlist.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(configlist.getAttribute_byXpath(configlist.list_channel1, 'data-local'))
                channel2 = str(configlist.getAttribute_byXpath(configlist.list_channel2, 'data-local'))
                channel3 = str(configlist.getAttribute_byXpath(configlist.list_channel3, 'data-local'))
                channel4 = str(configlist.getAttribute_byXpath(configlist.list_channel4, 'data-local'))
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
            raise Exception('AP  未能同步2.4G无线接口')
        #确认AP序列号
        APseq1 = configlist.getText_byXpath(configlist.list_seq1)
        APseq2 = configlist.getText_byXpath(configlist.list_seq2)
        APseq3 = configlist.getText_byXpath(configlist.list_seq3)
        APseq4 = configlist.getText_byXpath(configlist.list_seq4)
        APModel1 = configlist.getText_byXpath(configlist.list_modes1)
        APModel2 = configlist.getText_byXpath(configlist.list_modes2)
        APmodel3 = configlist.getText_byXpath(configlist.list_modes3)
        APModel4 = configlist.getText_byXpath(configlist.list_modes4)
        configlist.click_backupconfig()
        time.sleep(1)
        configlist.input_searchBack(APseq1)
        configlist.click_searchBackb()
        time.sleep(1)
        try:
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum,APseq1,msg='seqnum1 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel1, msg='model1 型号不一致')
            configlist.input_searchBack(APseq2)
            configlist.click_searchBackb()
            time.sleep(1)
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq2, msg='seqnum2 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel2, msg='model2 型号不一致')
        except NoSuchElementException:
            logger.info(u'v2AP配置文件不存在')
            CapPic(self.driver)
            raise Exception(u'v2AP配置文件不存在')
        configlist.input_searchBack(APseq3)
        configlist.click_searchBackb()
        time.sleep(1)
        try:
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq3, msg='seqnum3 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APmodel3, msg='model3 型号不一致')
            configlist.input_searchBack(APseq4)
            configlist.click_searchBackb()
            time.sleep(1)
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq4, msg='seqnum4 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel4, msg='mode4 型号不一致')
        except NoSuchElementException:
            logger.info(u'v1AP配置文件不存在')
            CapPic(self.driver)
            raise Exception(u'v1AP配置文件不存在')
        self.driver.quit()
        logger.info('test_001_configlist passed')

    def test_002_configOperation(self):
        u'''配置文件导入、删除、导出'''
        apconfig_gz = getAssertText('apconfig_gz')
        apconfig_gz3 = getAssertText('apconfig_gz3')
        path_gz = os.path.dirname(os.path.abspath('.')) + '/tmp/'
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
        nodata = getAssertText('nodata')
        # 先删除AP配置文件路径中的 apUpdateConf开头 的gz文件
        call_Firefox.del_apconfig_gz(self)
        # 调用Firefox 导出组织架构
        call_Firefox.Firefox_login_web(self)
        self.driver.implicitly_wait(10)
        device = deviceMgmtPage(self.driver,self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        # 配置文件列表中 4个在线AP的配置信息
        APseq1 = device.getText_byXpath(device.list_seq1)
        APseq2 = device.getText_byXpath(device.list_seq2)
        APseq3 = device.getText_byXpath(device.list_seq3)
        APseq4 = device.getText_byXpath(device.list_seq4)
        APModel1 = device.getText_byXpath(device.list_modes1)
        APModel2 = device.getText_byXpath(device.list_modes2)
        APmodel3 = device.getText_byXpath(device.list_modes3)
        APModel4 = device.getText_byXpath(device.list_modes4)
        configlist = deviceMgmtPage(self.driver,self.url)
        configlist.click_backupconfig()
        time.sleep(1)
        # 导出AP配置
        configlist.click_backup()
        time.sleep(1)
        configlist.click_ok()
        time.sleep(2)

        # 进行配置文件命名修改
        sys.path.append(r'%s' % path_gz)
        files = os.listdir(r'%s' % path_gz)  # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        # 通过文件名称判断 修改为指定的文件名
        for filename in files:
            portion = os.path.splitext(filename)  # splitext()用于返回 文件名和扩展名 元组
            # print(portion2)
            if apconfig_gz in str(portion[0]):  # 如果文件名种包含"组织成员20"
                if portion[1] == '.gz':  # 如果后缀是 .gz
                    newname = apconfig_gz3 + '.gz'
                    # 重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir = (r'%s' % path_gz) + filename
                    newnamedir = (r'%s' % path_gz) + newname
                    # 修改文件名称（与autoIt上传脚本中上传的文件名称一致）
                    os.rename(filenamedir, newnamedir)
        # print(newname)
        self.driver.quit()
        print('AP配置 - 备份 验证成功')
        #删除AP配置
        login.loginWeb2(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        configlist = deviceMgmtPage(self.driver, self.url)
        configlist.click_wirelessExtension()
        time.sleep(0.5)
        configlist.click_deviceMgmt()
        time.sleep(1)
        configlist.click_backupconfig()
        time.sleep(1)
        # 全选 删除AP配置
        while 1 > 0:
            configlist.click_selall_b()
            time.sleep(0.2)
            configlist.click_allDelete()
            time.sleep(1)
            configlist.click_ok()
            time.sleep(3)
            try:
                self.driver.implicitly_wait(2)
                configlist.find_listback_nodata()
            except NoSuchElementException:
                print('AP配置未删除完 继续删除')
            else:
                tips = str(configlist.getText_byXpath(configlist.listback_nodata))
                self.assertEqual(tips,nodata,msg='AP配置删除后列表提示信息有误')
                break
        self.driver.implicitly_wait(10)
        print('AP配置 删除验证通过')
        time.sleep(2)
        #导入AP配置
        configlist.click_uploadBackup()
        time.sleep(1)
        configlist.click_chooseFile()
        time.sleep(1)
        # 调用autoIt脚本上传组的cvs文件
        os.system('%s' % (batpath + 'SE_APconfig_import.exe'))
        time.sleep(2)
        configlist.click_demo_id()
        time.sleep(3)
        configlist.input_searchBack(APseq1)
        configlist.click_searchBackb()
        time.sleep(1)
        try:
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum,APseq1,msg='seqnum1 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel1, msg='model1 型号不一致')
            configlist.input_searchBack(APseq2)
            configlist.click_searchBackb()
            time.sleep(1)
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq2, msg='seqnum2 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel2, msg='model2 型号不一致')
        except NoSuchElementException:
            logger.info(u'v2AP配置文件不存在')
            CapPic(self.driver)
            raise Exception(u'v2AP配置文件不存在')
        configlist.input_searchBack(APseq3)
        configlist.click_searchBackb()
        time.sleep(1)
        try:
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq3, msg='seqnum3 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APmodel3, msg='model3 型号不一致')
            configlist.input_searchBack(APseq4)
            configlist.click_searchBackb()
            time.sleep(1)
            list_seqnum = str(configlist.getText_byXpath(configlist.bconfigseq1))
            self.assertEqual(list_seqnum, APseq4, msg='seqnum4 序列号不一致')
            list_model = str(configlist.getText_byXpath(configlist.bconfigmodel1))
            self.assertEqual(list_model, APModel4, msg='mode4 型号不一致')
        except NoSuchElementException:
            logger.info(u'v1AP配置文件不存在')
            CapPic(self.driver)
            raise Exception(u'v1AP配置文件不存在')
        print('导入AP配置正常')
        self.driver.quit()
        logger.info('test_002_configOperation passed')

    def test_003_rebootAC(self):
        u'''重启、恢复AC，配置文件不丢失'''

        #调用重启
        Reboot.test_reboot1(self)
        print('AC重启，等待AP上线')
        time.sleep(30)
        #调用001验证 AP配置
        Configlist.test_001_configlist(self)

        #调用恢复出厂
        configuration.test_002_Resert(self)
        # 调用001验证 AP配置
        Configlist.test_001_configlist(self)
        logger.info('test_003_rebootAC passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
