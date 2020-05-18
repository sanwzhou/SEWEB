#! -*-conding:utf-8 -*-
#@Time: 2019/1/16 0016 16:17
#@swzhou
'''
禁止IP段的爱奇艺应用，在该IP段内的设备无法打开爱奇艺网站
'''



import time
import unittest
import os.path
import socket
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText
from common.loginRoute import login
from pages.actionManage_001_actionManagePage import actionManagePage
logger = LogGen(Logger = 'actionManage_003_actionManage').getlog()
batpath = os.path.dirname(os.path.abspath('.')) + '/script/'
DomainFilterNotice = getAssertText('DomainFilterNotice')

class iqiyiFilter(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_iqiyiFilter(self):
        u'''行为管理 控制IP段 过滤爱奇艺'''
        iqiyi = getAssertText('iqiyi')
        iqiyi2 = getAssertText('iqiyi2')
        baidutitle = getAssertText('baidutitle')

        # 获取本机ip 默认有线地址，有线断开会显示无线
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))

        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        actionManage = actionManagePage(self.driver,self.url)
        #配置行为管理
        actionManage.click_BehaviorManagement()
        time.sleep(0.5)
        actionManage.click_BehaviorManagement2()
        time.sleep(1)
        actionManage.click_add()
        time.sleep(1)
        actionManage.input_ruleName('iqiyi')
        actionManage.click_users()
        time.sleep(1)
        #选择IP段 用自身IP
        actionManage.click_userip()
        time.sleep(1)
        actionManage.input_starip(pcaddr)
        actionManage.input_endip(pcaddr)
        actionManage.click_saveW1()
        time.sleep(1)
        actionManage.click_servers()
        time.sleep(1)
        actionManage.input_searchText(iqiyi)
        actionManage.click_search()
        time.sleep(1)
        actionManage.click_appSearchRes()
        actionManage.click_saveW2()
        time.sleep(1)
        actionManage.click_save()
        time.sleep(1)
        #开启行为管理
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens,'checktype')  # checktype 0未开启，1开启
        if checkOpenS =='0':
            actionManage.click_checkOpen()
            time.sleep(2)
        print('行为管理 已添加')
        #断言
        list_server = str(actionManage.getText_byXpath(actionManage.list_server))
        self.assertEqual(list_server , iqiyi2, msg='过滤内容不为"爱奇艺PPS"')
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens,'checktype') #checktype 0未开启，1开启
        self.assertEqual(checkOpenS,'1',msg='行为管理 未开启')
        self.driver.quit()

        #尝试访问爱奇艺 应不可以
        time.sleep(5)
        self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.set_page_load_timeout(10)  # selenium超时设置/等待时间过长自动停止
        # 清除浏览器cookies
        cookies = self.driver.get_cookies()
        print(f"main: cookies = {cookies}")
        self.driver.delete_all_cookies()
        # 因为被过滤，会打不开网站，命令执行后会一直处于命令执行中，最后报超时错误，默认超时300s
        # selenium.common.exceptions.TimeoutException: Message: timeout
        # 配合上文 set_page_load_timeout(10)设置等待超时时间，这里等待10s，判断报超时错误则正常，否则失败
        try:
            self.driver.get('http://www.iqiyi.com/')
        except TimeoutException:
            print('爱奇艺禁止 验证成功')
        else:
            raise Exception('爱奇艺禁止失败')
        #尝试访问官网 应可以
        self.driver.get('http://www.baidu.com')
        title2 = self.driver.title
        print(title2)
        self.assertEqual(title2, baidutitle, msg='认证后 不能打开网页')
        self.driver.quit()

        logger.info('test_iqiyiFilter passed')

    def tearDown(self):
        # 关闭行为管理，删除禁止策略
        nodata = getAssertText('nodata')
        login.loginWeb(self)  # admin账号登录
        self.driver.implicitly_wait(10)
        actionManage = actionManagePage(self.driver, self.url)
        # 配置行为管理
        actionManage.click_BehaviorManagement()
        time.sleep(0.5)
        actionManage.click_BehaviorManagement2()
        time.sleep(1)
        actionManage.click_checkOpen()
        time.sleep(1)
        checkOpenS = actionManage.getAttribute_byId(actionManage.checkOpens, 'checktype')  # checktype 0未开启，1开启
        self.assertEqual(checkOpenS, '0', msg='行为管理 未关闭')
        print('行为管理 已关闭')
        actionManage.click_delete()
        time.sleep(1)
        actionManage.click_ok()
        time.sleep(1)
        # 断言
        listnodata = str(actionManage.getText_byXpath(actionManage.listnodata))
        self.assertEqual(listnodata, nodata, msg='策略删除失败')
        print('策略已删除')
        self.driver.quit()

        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()

