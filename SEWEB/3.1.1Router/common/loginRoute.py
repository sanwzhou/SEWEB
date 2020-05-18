#! -*-conding:utf-8 -*-
#@Time: 2018/12/10 0010 9:32
#@swzhou
'''
登录路由器WEB页面 /注销登录
'''

import os
import sys
import socket
import time
import unittest
import telnetlib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getweb,getAssertText
from pages.Loginpage import LoginPage
logger = LogGen(Logger = 'loginRoute').getlog()
RouteUrl = getweb('RouteUrl')
BrowerMode = getweb('BrowerMode')
# licensefile = os.path.dirname(os.path.abspath('.')) + '/script/licensefile/'


class login(unittest.TestCase):

    def setUp(self):
        print('login start')
        # self.url = getweb('RouteUrl')
        # print(self.url)
        # self.user = getweb('User')
        # self.passwd = getweb('Passwd')
        # self.driver = webdriver.Chrome()
        # self.driver.maximize_window()
        # self.driver.implicitly_wait(10)
        # self.driver.get(self.url)

    def loginWeb(self):
        self.url = getweb('RouteUrl')
        self.user = getweb('User')
        self.passwd = getweb('Passwd')
        if BrowerMode == '0':
            # 使用无界模式
            chrome_opt = Options()
            chrome_opt.add_argument('--headless')
            chrome_opt.add_argument('--diaable-gpu')
            self.driver = webdriver.Chrome(options=chrome_opt)
            self.driver.set_window_size(1920, 1080)
        else:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            if BrowerMode == '0':  # 暂时https 无法使用chrome无界模式登录，调用判断 使用有界模式登录
                self.driver.quit()
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.driver.get(self.url)
                time.sleep(1)
                nowUrl = self.driver.current_url
            else:
                time.sleep(3)

        login_page = LoginPage(self.driver, self.url)
        try:
            login_page.find_username()
        except NoSuchElementException:
            try:#https模式 浏览器提示证书不对 url正确，无法进入页面，需要点击"高级"-下一步
                login_page.find_details_button()
            except NoSuchElementException: #非 证书问题
                CapPic(self.driver)
                logger.info(u'无法打开设备界面')
                logger.info(u'当前浏览器rul:%s' % nowUrl)
                raise Exception(u'无法打开设备界面')
            else:
                login_page.click_details_button()
                time.sleep(1)
                login_page.click_proceed_link()
                time.sleep(3)

        login_page.input_username(self.user)
        login_page.input_password(self.passwd)
        login_page.click_login()
        time.sleep(3)

        #电子授权
        # try:
        #     self.driver.implicitly_wait(1)
        #     login_page.flid_chooseFile()
        # except NoSuchElementException:
        #     pass
        # else:
        #     # telnet获取接口名称及确认默认路由
        #     licenseSN = getweb('licenseSN')
        #     hostip = gettelnet('host')
        #     port = gettelnet('port')
        #     username = bytes(getweb('User'), encoding="utf8")
        #     password = bytes(getweb('Passwd'), encoding="utf8")
        #     # 判断SN
        #     tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        #     tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        #     tn.read_until(b'login:')
        #     tn.write(username + b"\n")
        #     tn.read_until(b'Password:')
        #     tn.write(password + b"\n")
        #     # 登录完毕后执行命令
        #     tn.read_until(b'#')
        #     tn.write(b'uttcli get_uttsn' + b'\n')
        #     # 输出结果，判断
        #     time.sleep(1)
        #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        #     print('-------------------输出结果------------------------')
        #     # 命令执行结果
        #     print('result:', result)
        #     # 获取WAN口对应接口名称
        #     sn = result.split(r'\r\n')[1][:-3]
        #     print(sn)
        #     if sn != licenseSN:
        #         raise Exception('设备的序列号 不为licenseSN值，license文件不能导入')
        #     tn.close()
        #     # 判断SN
        #     tn = telnetlib.Telnet(host=hostip, port=port, timeout=10)
        #     tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        #     tn.read_until(b'login:')
        #     tn.write(username + b"\n")
        #     tn.read_until(b'Password:')
        #     tn.write(password + b"\n")
        #     # 登录完毕后执行命令
        #     tn.read_until(b'#')
        #     tn.write(b"uname -a" + b'\n')
        #     # 输出结果，判断
        #     time.sleep(1)
        #     result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        #     print('-------------------输出结果------------------------')
        #     # 命令执行结果
        #     print('result:', result)
        #     # 获取WAN口对应接口名称
        #     model = result.split(r'\r\n')[1].split(r' ')[4]
        #     print(model)
        #
        #     sys.path.append(r'%s' % licensefile)
        #     files_lic = os.listdir(r'%s' % licensefile)  # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        #     for filename_lic in files_lic:
        #         portion_lic = os.path.splitext(filename_lic)  # splitext()用于返回 文件名和扩展名 元组
        #         # print(portion_xml)
        #         if model in portion_lic[0] and '-1-1' in portion_lic[0]:  # 如果文件名包含 当前设备型号 且 选择第一个license
        #             if portion_lic[1] == '.lic':  # 后缀是 .xml
        #                 # 重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
        #                 licensefilenow = (r'%s' % licensefile) + filename_lic
        #
        #     self.driver.find_element_by_xpath(login_page.updatesoftware).send_keys(licensefilenow)
        #     time.sleep(1)
        #     login_page.click_innerput()
        #     time.sleep(2)
        #     login_page.click_ok()
        #     time.sleep(1)
        # 判断恢复出厂后输入账号密码
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
        # 判断是否有弹出兼容模式提示框
        try:
            self.driver.implicitly_wait(1)
            login_page.find_no()
            time.sleep(2)
            logger.info(u'已取消开启兼容模式开关')
        except NoSuchElementException:
            pass
        self.driver.implicitly_wait(10)
        # 断言url变更
        url = self.driver.current_url
        try:
            self.assertIn('/index.html', url, msg='未登陆成功')
        except AssertionError:
            CapPic(self.driver)
            logger.info(u"未登录成功")
            raise Exception('未登陆成功')
        print('login_web success')

    def loginWeb2(self):
        #使用有界模式 调用autoIt等脚本不能使用无界模式
        self.url = getweb('RouteUrl')
        self.user = getweb('User')
        self.passwd = getweb('Passwd')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            time.sleep(3)
        time.sleep(1)
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
        # 判断是否有弹出兼容模式提示框
        try:
            self.driver.implicitly_wait(1)
            login_page.find_no()
            time.sleep(2)
            logger.info(u'已取消开启兼容模式开关')
        except NoSuchElementException:
            pass
        self.driver.implicitly_wait(10)
        # 断言url变更
        url = self.driver.current_url
        try:
            self.assertIn('/index.html', url, msg='未登陆成功')
        except AssertionError:
            CapPic(self.driver)
            logger.info(u"未登录成功")
            raise Exception('未登陆成功')
        print('login_web success')

    def logoutWeb(self):
        login_page = LoginPage(self.driver, self.url)
        login_page.click_logout()
        time.sleep(1)
        # 断言用户名按钮（username）元素不为空：代表注销成功
        self.assertIsNotNone(login_page.username)
        print('logout_web success')

    def test_unableLoginWeb(self,username='admin1',password='admin'):
        #用于修改账号密码后，验证无法登录
        self.username = username
        self.password = password

        self.url = getweb('RouteUrl')
        # self.user = getweb('User')
        # self.passwd = getweb('Passwd')
        if BrowerMode == '0':
            # 使用无界模式
            chrome_opt = Options()
            chrome_opt.add_argument('--headless')
            chrome_opt.add_argument('--diaable-gpu')
            self.driver = webdriver.Chrome(options=chrome_opt)
        else:
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            if BrowerMode == '0':  # 暂时https 无法使用chrome无界模式登录，调用判断 使用有界模式登录
                self.driver.quit()
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.driver.get(self.url)
                time.sleep(1)
                nowUrl = self.driver.current_url
            else:
                time.sleep(3)

        login_page = LoginPage(self.driver, self.url)
        try:
            login_page.find_username()
        except NoSuchElementException:
            try:#https模式 浏览器提示证书不对 url正确，无法进入页面，需要点击"高级"-下一步
                login_page.find_details_button()
            except NoSuchElementException: #非 证书问题
                CapPic(self.driver)
                logger.info(u'无法打开设备界面')
                logger.info(u'当前浏览器rul:%s' % nowUrl)
                raise Exception(u'无法打开设备界面')
            else:
                login_page.click_details_button()
                time.sleep(1)
                login_page.click_proceed_link()
                time.sleep(3)

        login_page.input_username(username)
        login_page.input_password(password)
        login_page.click_login()
        time.sleep(0.5)
        # 断言登录告警信息（warning-msg）元素不为空：代表确实无法登录
        self.assertIsNotNone(login_page.warning_msg)

        try:
            self.assertIsNotNone(login_page.warning_msg)
        except AssertionError:
            CapPic(self.driver)
            logger.info(u"输入错误密码 未提示告警信息")
            raise Exception('输入错误密码 未提示告警信息')
        print(username,password,'unable_login')

    def test_enableLoginWeb(self,url=RouteUrl,username='admin',password='admin'):
        # 用于新增账号密码后，验证登录
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        self.username = username
        self.password = password
        #使用无界模式
        if BrowerMode == '0':
            # 使用无界模式
            chrome_opt = Options()
            chrome_opt.add_argument('--headless')
            chrome_opt.add_argument('--diaable-gpu')
            self.driver = webdriver.Chrome(options=chrome_opt)
        else:
            self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            if BrowerMode == '0':  # 暂时https 无法使用chrome无界模式登录，调用判断 使用有界模式登录
                self.driver.quit()
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.driver.get(self.url)
                time.sleep(1)
                nowUrl = self.driver.current_url
            else:
                time.sleep(3)

        login_page = LoginPage(self.driver, self.url)
        try:
            login_page.find_username()
        except NoSuchElementException:
            try:#https模式 浏览器提示证书不对 url正确，无法进入页面，需要点击"高级"-下一步
                login_page.find_details_button()
            except NoSuchElementException: #非 证书问题
                CapPic(self.driver)
                logger.info(u'无法打开设备界面')
                logger.info(u'当前浏览器rul:%s' % nowUrl)
                logger.info(u'当前IP地址：%s' % pcaddr)
                raise Exception(u'无法打开设备界面')
            else:
                login_page.click_details_button()
                time.sleep(1)
                login_page.click_proceed_link()
                time.sleep(3)

        login_page.input_username(username)
        login_page.input_password(password)
        login_page.click_login()
        time.sleep(3)
        #判断恢复出厂后输入账号密码
        try:
            self.driver.implicitly_wait(1)
            login_page.find_passwd1()
        except NoSuchElementException:
            pass
        else:
            login_page.input_passwd1(username)
            login_page.input_passwd2(password)
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
            login_page.input_username(username)
            login_page.input_password(password)
            login_page.click_login()
            time.sleep(3)
        # 判断是否有弹出兼容模式提示框
        try:
            self.driver.implicitly_wait(1)
            login_page.find_no()
            time.sleep(2)
            logger.info(u'已取消开启兼容模式开关')
        except NoSuchElementException:
            pass

        self.driver.implicitly_wait(10)
        # 断言url变更
        url = self.driver.current_url
        try:
            self.assertIn('/index.html', url, msg='未登陆成功')
        except AssertionError:
            CapPic(self.driver)
            logger.info(u"未登录成功")
            raise Exception('未登陆成功')
        print('login_web success')
    def tearDown(self):
        print('login over')

if __name__=='__main__':
    unittest.main()

