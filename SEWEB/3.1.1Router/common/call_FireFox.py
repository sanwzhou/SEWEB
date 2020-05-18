#! -*-conding:utf-8 -*-
#@Time: 2018/12/29 0029 10:58
#@swzhou
'''
调用火狐浏览器登录设备，指定下载路径等  这里使用火狐浏览器，chrome导出配置时候会提示"损坏计算机"，需要手动点击
'''

import time
import unittest
import os.path
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb
from pages.Loginpage import LoginPage
logger = LogGen(Logger = 'Call_FireFox').getlog()

class call_Firefox(unittest.TestCase):

    def setUp(self):
        print('call_Firefox start')

    def Firefox_login_web(self):
        u'''配置备份'''
         # 配置备份(因为chrome配置导出提示'损害计算机'问题，这里使用Firefox导出配置文件)
        # Firedownpath = r'%s' %getpath('Firedownpath')
        # Firefoxpath = getpath('tempfilepath')
        self.url = getweb('RouteUrl')
        self.user = getweb('User')
        self.passwd = getweb('Passwd')
        #设置Firefox的Profile
        profile = webdriver.FirefoxProfile()
        #指定下载路径
        profile.set_preference('browser.download.dir',r'D:\python\SEWEB\3.1.1Router\tmp')
        #设置成 2 表示使用自定义下载路径；设置成 0 表示下载到桌面；设置成 1 表示下载到默认路径
        profile.set_preference('browser.download.folderList', 2)
        #在开始下载时是否显示下载管理器
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        #对所给出文件类型不再弹出框进行询问
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
            #登录web
        #引用设置的Profile
        self.driver=webdriver.Firefox(firefox_profile=profile)
        # self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        now_url = self.driver.current_url
        if 'https://' in str(now_url):
            time.sleep(3)
        login_page = LoginPage(self.driver, self.url)
        login_page.input_username(self.user)
        login_page.input_password(self.passwd)
        login_page.click_login()
        time.sleep(3)
        try:
            self.driver.implicitly_wait(1)
            login_page.find_passwd1()
        except NoSuchElementException:
            pass
        else:
            login_page.input_passwd1(self.passwd)
            login_page.input_passwd2(self.passwd)
            login_page.click_cfm()
            # 加个判断 某些型号等待时间长（6550G）
            time.sleep(1)
            x = 0
            while x < 15:
                now_url = str(self.driver.current_url)
                print(now_url, x)
                if '/noAuth/login.html' not in now_url:  # 如果不同
                    time.sleep(2)
                else:
                    break
                x += 1
            login_page.input_username(self.user)
            login_page.input_password(self.passwd)
            login_page.click_login()
            time.sleep(3)
        self.driver.implicitly_wait(10)
        #断言url变更
        url = self.driver.current_url
        try:
            self.assertIn('/index.html', url, msg='未登陆成功')
        except AssertionError:
            CapPic(self.driver)
            logger.info(u"未登录成功")
            raise Exception('未登陆成功')
        print('Firefox_login_web success')

    def del_config_xml(self):
        #删除配置文件路径中的 xml文件
        config_xml = getAssertText('config_xml')
        config_xml3 = getAssertText('config_xml3')
        path_xml = os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path_xml)
        files_xml = os.listdir(r'%s' % path_xml) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        for filename_xml in files_xml:
            portion_xml = os.path.splitext(filename_xml) #splitext()用于返回 文件名和扩展名 元组
            # print(portion_xml)
            if config_xml in portion_xml[0] : #如果文件名包含"系统配置20"
                if portion_xml[1] == '.xml':  #后缀是 .xml
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_xml  =(r'%s' % path_xml) +filename_xml
                    os.remove(filenamedir_xml)
            if config_xml3 in portion_xml[0] : #如果文件名包含"系统配置3333"
                if portion_xml[1] == '.xml':  #后缀是 .xml
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_xml  =(r'%s' % path_xml) +filename_xml
                    os.remove(filenamedir_xml)

    def del_organization_csv(self):
        #删除组织成员路径中的 csv文件
        organization_csv = getAssertText('organization_csv')
        organization_csv3 = getAssertText('organization_csv3')
        path_cvs = os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path_cvs)
        files_cvs = os.listdir(r'%s' % path_cvs) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        for filename_cvs in files_cvs:
            portion_cvs = os.path.splitext(filename_cvs) #splitext()用于返回 文件名和扩展名 元组
            # print(portion_cvs)
            if organization_csv  in portion_cvs[0]: #如果文件名包含"组织成员20"
                if portion_cvs[1] == '.csv':  #后缀是 .csv
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_cvs  =(r'%s' % path_cvs) +filename_cvs
                    os.remove(filenamedir_cvs)
            if organization_csv3 in portion_cvs[0]: #如果文件名包含“组织成员3333”
                if portion_cvs[1] == '.csv':  #后缀是 .csv
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_cvs  =(r'%s' % path_cvs) +filename_cvs
                    os.remove(filenamedir_cvs)

    def del_flowWatch_csv(self):
        #删除流量监控路径中的 csv文件
        flowWatch_csv = getAssertText('flowWatch_csv')
        flowWatch_csv3 = getAssertText('flowWatch_csv3')
        path_cvs = os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path_cvs)
        files_cvs = os.listdir(r'%s' % path_cvs) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        for filename_cvs in files_cvs:
            portion_cvs = os.path.splitext(filename_cvs) #splitext()用于返回 文件名和扩展名 元组
            # print(portion_cvs)
            if flowWatch_csv  in portion_cvs[0]: #如果文件名包含"流量监控20"
                if portion_cvs[1] == '.csv':  #后缀是 .csv
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_cvs  =(r'%s' % path_cvs) +filename_cvs
                    os.remove(filenamedir_cvs)
            if flowWatch_csv3 in portion_cvs[0]: #如果文件名包含“流量监控3333”
                if portion_cvs[1] == '.csv':  #后缀是 .csv
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_cvs  =(r'%s' % path_cvs) +filename_cvs
                    os.remove(filenamedir_cvs)

    def del_apconfig_gz(self):
        #删除AP配置文件路径中的 gz文件
        apconfig_gz = getAssertText('apconfig_gz')
        apconfig_gz3 = getAssertText('apconfig_gz3')
        path_gz = os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path_gz)
        files_gz = os.listdir(r'%s' % path_gz) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        for filename_gz in files_gz:
            portion_gz = os.path.splitext(filename_gz) #splitext()用于返回 文件名和扩展名 元组
            # print(portion_cvs)
            if apconfig_gz in portion_gz[0]: #如果文件名包含"apUpdateConf_20"
                if portion_gz[1] == '.gz':  #后缀是 .gz
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_gz  =(r'%s' % path_gz) +filename_gz
                    os.remove(filenamedir_gz)
            if apconfig_gz3 in portion_gz[0]: #如果文件名包含"apUpdateConf3333"
                if portion_gz[1] == '.gz':  #后缀是 .gz
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir_gz =(r'%s' % path_gz) +filename_gz
                    os.remove(filenamedir_gz)

    def del_syslog_log(self):
        #删除syslog抓包文件 pcapng\log文件,配合sysConfig_010_syslogServer 使用
        path_log = os.path.dirname(os.path.abspath('.')) + '/tmp/' #配置文件存放（下载）路径
        sys.path.append(r'%s' % path_log)
        files_log = os.listdir(r'%s' % path_log) #os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        for filename_log in files_log:
            portion_log = os.path.splitext(filename_log) #splitext()用于返回 文件名和扩展名 元组
            # print(portion_cvs)
            if 'syslogtest' in portion_log[0]: #如果文件名包含"syslogtest"
                if portion_log[1] == '.pcapng':  #后缀是 .pcapng
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filename_log  =(r'%s' % path_log) + filename_log
                    os.remove(filename_log)
            if 'syslogtest' in portion_log[0]: #如果文件名包含"syslogtest"
                if portion_log[1] == '.log':  #后缀是 .log
                    #重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filename_log = (r'%s' % path_log) + filename_log
                    os.remove(filename_log)


    def tearDown(self):
        print('call_Firefox over')

