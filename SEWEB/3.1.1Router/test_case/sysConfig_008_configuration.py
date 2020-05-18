#! -*-conding:utf-8 -*-
#@Time: 2019/1/18 0018 16:51
#@swzhou
'''
配置管理：备份 和 导入测试  这里使用了火狐浏览器，chrome导出配置时候会提示"损坏计算机"，需要手动点击
'''
import sys
import time
import unittest
import os.path
import datetime
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from common.call_FireFox import call_Firefox
from pages.sysConfig_003_MaintenancePage import MaintenancePage
from pages.sysObj_timePlanPage import timePlanPage
logger = LogGen(Logger = 'sysConfig_008_configuration').getlog()


class configuration(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')

    def test_001_configbackup(self):
        u'''配置备份'''
         # 配置备份(因为chrome配置导出提示'损害计算机'问题，这里使用Firefox导出配置文件)
        # 先删除tmp路径中的xml文件
        call_Firefox.del_config_xml(self)
        
        # 添加一个当天的时间计划配置 后面用于验证配置导出正确（）
        call_Firefox.Firefox_login_web(self)
        self.driver.implicitly_wait(10)
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        # 操作删除 以访已有规则
        timePlan.click_selall()
        time.sleep(0.2)
        timePlan.click_delall()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            timePlan.find_ok()
        except NoSuchElementException:
            try:
                timePlan.find_tipsshowin()
                time.sleep(1)
            except NoSuchElementException:
                pass
        else:
            time.sleep(1)
            print('时间计划列表已删除')
        # 创建时间计划 新增时间计划的名称 命令为当前年月
        today = str(datetime.date.today())[:-3]  # 获取当前年月(以访测试过程正好隔天，仅取年份月份)
        timePlan.click_add()
        time.sleep(1)
        timePlan.input_TimeRangeName(today)
        timePlan.click_save()
        time.sleep(1)
        # 断言 开启提示信息是否有误
        list_name = str(timePlan.getText_byXpath(timePlan.listName))
        time.sleep(1)
        self.assertEqual(list_name, today, msg='时间段名 与配置的不一致')
        print('时间计划已添加')

        # 开始进行配置备份
        #进入系统配置-系统维护-配置管理
        config = MaintenancePage(self.driver, self.url)
        config.click_sysConfig()
        time.sleep(0.5)
        config.click_Maintenance()
        time.sleep(1)
        config.click_configuration()
        time.sleep(1)
        config.click_output()
        time.sleep(2)
        self.driver.quit()
        logger.info('test_001_configbackup passed')

    def test_002_Resert(self):
        u'''恢复出厂'''
        nodata = getAssertText('nodata')
        #用于恢复出厂并验证
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        config = MaintenancePage(self.driver, self.url)
        #进入系统配置-系统维护-配置管理
        config.click_sysConfig()
        time.sleep(0.5)
        config.click_Maintenance()
        time.sleep(1)
        config.click_configuration()
        time.sleep(1)
        config.click_restore()
        time.sleep(1)
        config.click_ok()
        time.sleep(1)
        config.click_ok() #确认重启
        time.sleep(30)
        i = 0
        while i < 30:
            now_url = str(self.driver.current_url)
            # print(now_url,i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        else:
            raise Exception('设备重启未正常启动')
        self.driver.quit()

        #登录验证是否恢复出厂成功（通过配置的 当天的时间计划）
        login.loginWeb(self) #admin账号登录
        self.driver.implicitly_wait(10)
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        list_nodata = timePlan.getText_byXpath(timePlan.listnodata)
        self.assertEqual(list_nodata,nodata,msg='配置恢复出厂成功')
        time.sleep(1)
        self.driver.quit()
        logger.info('test_002_Resert passed')

    def test_003_configIpmort(self):
        u'''导入配置'''
        nodata = getAssertText('nodata')
        config_xml = getAssertText('config_xml')
        config_xml3 = getAssertText('config_xml3')
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
        #先进行配置文件命名修改
        path = os.path.dirname(os.path.abspath('.')) + '/tmp/'  # 配置文件存放（下载）路径
        sys.path.append(r'%s' % path)
        files = os.listdir(r'%s' % path) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        #通过文件名称判断 修改为指定的文件名
        for filename in files:
            portion = os.path.splitext(filename) #splitext()用于返回 文件名和扩展名 元组
            # print(portion2)
            if config_xml in str(portion[0]): #如果文件名种包含"系统配置20"
                if portion[1] == '.xml':  #如果后缀是 .xml
                    newname = config_xml3 + '.xml'
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir = (r'%s' % path) +filename
                    newnamedir = (r'%s' % path) +newname
                    #修改文件名称（与autoIt上传脚本中上传的文件名称一致）
                    os.rename(filenamedir,newnamedir)

        #导入配置 验证
        login.loginWeb2(self)
        self.driver.implicitly_wait(10)
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
        if config_xml3 == '系统配置3333':
            autoItScript = batpath + 'SE_config_importCn.exe'
        if config_xml3 == 'Systemconfig3333':
            autoItScript = batpath + 'SE_config_importEn.exe'
        os.system('%s' % autoItScript)

        #点击导入
        config.click_innerput()
        time.sleep(1)
        config.click_ok()
        time.sleep(2)
        #取消重启
        config.click_no()
        time.sleep(1)
        #验证导入配置是否成功（通过配置的 今天时间计划）
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        today = str(datetime.date.today())[:-3]  # 获取当前年月(以访测试过程正好隔天，仅取年份月份)
        list_name = str(timePlan.getText_byXpath(timePlan.listName))
        self.assertEqual(list_name,today,msg='配置导入失败')
        time.sleep(1)
        # 删除时间计划
        timePlan = timePlanPage(self.driver, self.url)
        timePlan.click_sysObj()
        time.sleep(0.5)
        timePlan.click_timePlan()
        time.sleep(1)
        timePlan.click_delete()
        time.sleep(1)
        timePlan.click_ok()
        time.sleep(1)
        # 断言
        listtips2 = str(timePlan.getText_byXpath(timePlan.listnodata))
        self.assertEqual(listtips2, nodata, msg='时间计划删除失败')
        print('时间计划已删除')
        self.driver.quit()

        # 删除tmp路径中的xml文件
        call_Firefox.del_config_xml(self)
        logger.info('test_003_configIpmort passed')

    def tearDown(self):
        # self.driver.quit()
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
