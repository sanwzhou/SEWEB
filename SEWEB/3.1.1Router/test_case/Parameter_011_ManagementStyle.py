#! -*-conding:utf-8 -*-
#@Time: 2019/2/13 0013 17:22
#@swzhou
'''
管理方式
'''
import telnetlib
import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb,gettelnet,getParameter
from common.loginRoute import login
from common.GetExcelValue import getExcelValue
from pages.sysConfig_001_ManagementPolicyPage import ManagementPolicyPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_011_ManagementStyle').getlog()

class ManagementStyle(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        # 进入系统配置-网管策略
        accessStrategy.click_sysConfig()
        time.sleep(0.5)
        accessStrategy.click_ManagementPolicy()
        time.sleep(1)
        # pass

    def test_001_WEB_login(self):
        u'''WEB登录:HTTP/HTTPS'''
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.click_AccessPolicy()
        time.sleep(1)
        login_mode1 = accessStrategy.getAttribute_byXpath(accessStrategy.httpwebEns,'data-control-src')
        login_mode2 = accessStrategy.getAttribute_byXpath(accessStrategy.httpswebEns,'data-control-src')
        self.assertEqual(login_mode1,'HTTP',msg='模式不为"HTTP"')
        self.assertEqual(login_mode2, 'HTTPS', msg='模式不为"HTTPs"')
        self.driver.quit()
        logger.info('test_001_WEB_login passed')

    def test_002_admin(self):
        u'''多级用户管理:读写/读'''
        roleA = getAssertText('roleA')
        User = getweb('User')
        administrator = ManagementPolicyPage(self.driver, self.url)
        default = str(administrator.getText_byXpath(administrator.defaultAcc))
        defaultRole = str(administrator.getText_byXpath(administrator.defaultRole))
        self.assertEqual(default, User, msg='账号不为"admin"')
        self.assertEqual(defaultRole, roleA, msg='admin权限不为"读写"')

        # 查看新增账号的权限
        administrator.click_add()
        time.sleep(1)
        administrator.input_username('test')
        administrator.input_passwd1('test')
        administrator.input_passwd2('test')
        # 设置权限变量，选择 读写 权限
        selrole = administrator.selelement_byName(administrator.role)
        Select(selrole).select_by_value('adm')
        Select(selrole).select_by_value('viewer')
        self.driver.quit()
        logger.info('test_002_admin passed')

    def test_003_WEBUI(self):
        u'''WEB UI超时/登录错误次数/惩罚时间'''
        sessionLifep = getParameter('sessionLifep')
        passwdErrNumP = getParameter('passwdErrNumP')
        loginSpanP = getParameter('loginSpanP')
        print(getExcelValue(sessionLifep))
        sessionLifep = getExcelValue(sessionLifep)[:2]
        passwdErrNumP = str(getExcelValue(passwdErrNumP))[:2]
        loginSpanP = getExcelValue(loginSpanP)[:2]
        accessStrategy = ManagementPolicyPage(self.driver, self.url)
        accessStrategy.click_AccessPolicy()
        time.sleep(1)
        sessionLife =str(accessStrategy.getAttribute_byName(accessStrategy.sessionLife1,'value'))
        passwdErrNum = str(accessStrategy.getAttribute_byName(accessStrategy.passwdErrNum1,'value'))
        loginSpan = str(accessStrategy.getAttribute_byName(accessStrategy.loginSpan1,'value'))
        self.assertEqual(sessionLife, sessionLifep, msg='WEBUI超时默认值与参数不符')
        self.assertEqual(passwdErrNum, passwdErrNumP, msg='登录错误次数值与参数不符')
        self.assertEqual(loginSpan, loginSpanP, msg='惩罚时间默认值与参数不符')
        self.driver.quit()
        logger.info('test_003_WEBUI passed')

    def test_004_accesscontrol_Language(self):
        u'''设备访问控制/WEB语言'''
        accesscontrol = ManagementPolicyPage(self.driver, self.url)
        accesscontrol.click_lanAccessControl()
        time.sleep(1)
        switch =str(accesscontrol.getAttribute_byXpath(accesscontrol.innerAccessControlCs,'checked'))
        self.assertEqual(switch, 'true', msg='内网访问控制默认未关闭')

        languageA = getAssertText('languageA')
        language = ManagementPolicyPage(self.driver, self.url)
        language.click_Language()
        time.sleep(1)
        languageText = str(language.getText_byXpath(language.languageText))
        self.assertEqual(languageText, languageA, msg='语言 显示字符异常')

        self.driver.quit()
        logger.info('test_004_accesscontrol_Language passed')

    def test_005_telnet(self):
        u'''命令行登录：telnet（内部）'''

        # 连接Telnet服务器
        hostip = gettelnet('host')
        port = gettelnet('port')
        username = bytes(getweb('User'), encoding="utf8")
        password = bytes(getweb('Passwd'), encoding="utf8")
        tn = telnetlib.Telnet(host=hostip, port=port,timeout=10)
        tn.set_debuglevel(5)  # 级别越高输出的调试信息越多，并没有看出区别
        # 输入登录用户名
        tn.read_until(b'login:')
        tn.write(username + b"\n")
        tn.read_until(b'Password:')
        tn.write(password + b"\n")
        # 登录完毕后执行命令
        tn.read_until(b'#')
        tn.write(b'ps | grep telnetd | grep -v grep' + b'\n')
        # 输出结果，判断
        time.sleep(0.5)
        result = str(tn.read_very_eager())  # 执行多条命令时只会存最后一条命令的结果
        print('-------------------输出结果------------------------')
        # 命令执行结果
        print('result:', result)
        # 判断
        if ("telnetd -b %s " % hostip) in result:
            print('telnetd默认未仅对lan口开放 验证成功')
        else:
            raise Exception('telnetd默认未仅对lan口开放 验证失败')  # 如果没有则报错
        tn.close()  # tn.write('exit\n')
        self.driver.quit()
        logger.info('test_005_telnet passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
