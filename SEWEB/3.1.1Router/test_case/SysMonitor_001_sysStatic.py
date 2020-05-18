#! -*-conding:utf-8 -*-
#@Time: 2019/4/15 0015 13:51
#@swzhou
'''
系统状态页面
'''

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
import os
import sys
import csv
import time
import unittest
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getParameter
from common.call_FireFox import call_Firefox
from common.loginRoute import login
from common.GetExcelValue import getExcelValue
from pages.SysMonitor_001_sysStaticPage import sysStaticPage
from pages.SysMonitor_002_flowWatchPage import flowWatchpage
from pages.VPNconfig_IPsecPage import IPsecPage
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
logger = LogGen(Logger = 'SysMonitor_001_sysStatic').getlog()


class sysStatic(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_001_Modelcorrelation(self):
        u'''系统状态 型号相关'''
        vmodel = getExcelValue(getParameter('ProductmodelP'))
        print('性能参数中产品型号', vmodel)
        login.loginWeb(self)
        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)
        #系统负载 - 产品型号
        webmodel = (sysstatic.getText_byXpath(sysstatic.Model)).upper()
        print('页面产品型号',webmodel)

        if webmodel in vmodel:
            logger.info('产品型号 一致')
        elif webmodel.replace(' ','') in vmodel: #部分性能参数型号中未包含空格
            logger.info('产品型号 一致')
        elif 'HiPER' or '商睿' in vmodel:
            vmodel1 = '商睿 ' + vmodel.split(r' ')[1]
            vmodel2 = 'HIPER ' + vmodel.split(r' ')[1] #字母已切换大写
            # print(vmodel1,vmodel2)
            if webmodel in vmodel1 or webmodel in vmodel2:
                logger.info('产品型号 一致')
            else:
                print('页面产品型号', webmodel)
                print('性能参数中产品型号', vmodel)
                logger.info(u'软件页面产品型号 与性能参数显示不一致1')
                logger.info('页面产品型号',webmodel)
                logger.info('性能参数中产品型号',vmodel)
                CapPic(self.driver)
                raise Exception('软件页面产品型号 与性能参数显示不一致1')
        else:
            logger.info(u'软件页面产品型号 与性能参数显示不一致2')
            CapPic(self.driver)
            raise Exception('软件页面产品型号 与性能参数显示不一致2')
        if '硬件' in vmodel:
            hdVersion = 'V' + vmodel.split(r'V')[1][:-1]
        else:
            hdVersion = 'V1.0'
        print(hdVersion)
        wb_hdmodel = sysstatic.getText_byXpath(sysstatic.hdmodel)
        if wb_hdmodel == hdVersion:
            logger.info(u'硬件版本 与性能参数一致')
        else:
            logger.info(u'硬件版 与性能参数显示不一致')
            CapPic(self.driver)
            raise Exception('硬件版 与性能参数显示不一致')

        self.driver.quit()
        logger.info('test_001_Modelcorrelation passed')

    def test_001_AppFlowRanking(self):
        u'''今日应用流量排名 显示及跳转'''
        flowWatch_csv = getAssertText('flowWatch_csv')
        flowWatch_csv3 = getAssertText('flowWatch_csv3')
        path_csv = os.path.dirname(os.path.abspath('.')) + '/tmp/'

        # 先删除AP配置文件路径中的 流量监控开头 的csv文件
        call_Firefox.del_flowWatch_csv(self)

        call_Firefox.Firefox_login_web(self)
        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)
        #今日应用流量排名 跳转
        sysstatic.click_more1()
        time.sleep(2)
        url = self.driver.current_url
        if '#/system_watcher/traffic_watcher' in url:
            logger.info(u'今日应用流量排名 跳转到流量监控 验证正常')
        else:
            CapPic(self.driver)
            logger.info(u'今日应用流量排名 跳转到流量监控 验证异常')
            raise Exception(u'今日应用流量排名 跳转到流量监控 验证异常')
        flowWatch = flowWatchpage(self.driver,self.url)
        checkOpenS = flowWatch.getAttribute_byId(flowWatch.checkOpens, 'checktype')
        if checkOpenS != '1':
            flowWatch.click_checkOpen()
            time.sleep(3)
        checkOpenS = flowWatch.getAttribute_byId(flowWatch.checkOpens,'checktype')
        if checkOpenS == '1':
            logger.info(u'流量监控打开 正常')
        else:
            CapPic(self.driver)
            logger.info(u'流量监控打开 异常')
            raise Exception(u'流量监控打开 异常')
        selrefresh = flowWatch.selelement_byXpath(flowWatch.selrefresh)
        Select(selrefresh).select_by_value('manual')
        time.sleep(5)
        #判断导入csv文件可读
        # 1）获取列表 应用，并导出
        list_apply = []
        i = 0
        while i < 30:
            flowWatch.click_fresh()
            time.sleep(0.5)
            try:
                self.driver.implicitly_wait(2)
                list_apply1 = flowWatch.getText_byXpath(flowWatch.list_apply1)
            except NoSuchElementException:
                time.sleep(2)
                i += 1
            else:
                list_apply.append(list_apply1)
                break
            print(i)
        else:
            CapPic(self.driver)
            logger.info(u'流量监控未显示应用')
            raise Exception(u'流量监控未显示应用')
        try:
            list_apply2 = flowWatch.getText_byXpath(flowWatch.list_apply2)
            list_apply.append(list_apply2)
        except NoSuchElementException:
            pass
        else:
            try:
                list_apply3 = flowWatch.getText_byXpath(flowWatch.list_apply3)
                list_apply.append(list_apply3)
            except NoSuchElementException:
                pass
            else:
                try:
                    list_apply4 = flowWatch.getText_byXpath(flowWatch.list_apply4,quit=0)
                    list_apply.append(list_apply4)
                except NoSuchElementException:
                    pass
                else:
                    try:
                        list_apply5 = flowWatch.getText_byXpath(flowWatch.list_apply5,quit=0)
                        list_apply.append(list_apply5)
                    except NoSuchElementException:
                        pass
        flowWatch.click_export()
        time.sleep(2)

        # 2）进行配置文件命名修改，读取csv文件内容 并判断
        sys.path.append(r'%s' % path_csv)
        files = os.listdir(r'%s' % path_csv)  # os.listdir(path) 返回path指定的文件夹包含的文件或文件夹的名字的列表
        # 通过文件名称判断 修改为指定的文件名
        for filename in files:
            portion = os.path.splitext(filename)  # splitext()用于返回 文件名和扩展名 元组
            # print(portion2)
            if flowWatch_csv in str(portion[0]):  # 如果文件名种包含"流量监控20"
                if portion[1] == '.csv':  # 如果后缀是 .csv
                    newname = flowWatch_csv3 + '.csv'
                    # 重新组合文件名和后缀名，直接修改名称的话 程序和文件必须在一个目录下
                    filenamedir = (r'%s' % path_csv) + filename
                    newnamedir = (r'%s' % path_csv) + newname
                    os.rename(filenamedir, newnamedir)
        # print(newname)

        csv_apply = []
        csv_file1 = csv.reader(open(newnamedir, 'r', encoding='utf-8'))
        # print(csv_file)
        for stu in csv_file1:
            # print(stu)
            # a = str(stu)
            csv_apply.append(str(stu)[1:-1].split(", ")[1][1:-1])
        print(csv_apply)

        for x in csv_apply :
            if x in csv_apply:
                logger.info(u'流量监控 导出文件可读')
            else:
                logger.info(u'x:%s' % x)
                logger.info(u'csv_apply:' % csv_apply)
                logger.info(u'流量监控 导出文件不可读')

        checkOpenS = flowWatch.getAttribute_byId(flowWatch.checkOpens, 'checktype')
        if checkOpenS == '1':
            flowWatch.click_checkOpen()
            time.sleep(3)
        checkOpenS = flowWatch.getAttribute_byId(flowWatch.checkOpens, 'checktype')
        if checkOpenS == '0':
            logger.info(u'流量监控关闭 正常')
        else:
            CapPic(self.driver)
            logger.info(u'流量监控关闭 异常')
            raise Exception(u'流量监控关闭 异常')

        self.driver.back()
        sysstatic = sysStaticPage(self.driver, self.url)
        try:
            list_num = sysstatic.getText_byXpath(sysstatic.list_num)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'系统状态-今日应用流量排名 未显示数据')
        else:
            if list_num == '1':
                logger.info(u'系统状态-今日应用流量排名 显示数据验证通过 ')
            else:
                CapPic(self.driver)
                logger.info(u'系统状态-今日应用流量排名 显示数据 异常')
                raise Exception(u'系统状态-今日应用流量排名 显示数据 异常')

        self.driver.quit()
        logger.info('test_001_AppFlowRanking passed')

    def test_002_UserFlowRanking(self):
        u'''今日用户网络流量排名 显示及跳转'''
        login.loginWeb(self)
        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)

        sysstatic.click_more2()
        time.sleep(2)
        url = self.driver.current_url
        if '#/user_management/user_state' in url:
            logger.info(u'今日用户网络流量排名 跳转到用户状态 验证正常')
        else:
            CapPic(self.driver)
            logger.info(u'今日用户网络流量排名 跳转到用户状态 验证正常')
            raise Exception(u'今日用户网络流量排名 跳转到用户状态 验证正常')

        self.driver.back()
        sysstatic = sysStaticPage(self.driver, self.url)
        try:
            list_user = sysstatic.getText_byXpath(sysstatic.list_user)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'系统状态-今日用户网络流量排名 未显示数据')
            raise Exception(u'系统状态-今日用户网络流量排名 未显示数据')
        else:
            if 'Guest' in list_user:
                logger.info(u'系统状态-今日用户网络流量排名 显示数据验证通过 ')
            else:
                CapPic(self.driver)
                logger.info(u'系统状态-今日用户网络流量排名 显示数据 异常')
                raise Exception(u'系统状态-今日用户网络流量排名 显示数据 异常')

        self.driver.quit()
        logger.info('test_002_UserFlowRanking passed')

    def test_003_VPNStatus(self):
        u'''VPN状态 显示及跳转'''
        WillReboottips = getAssertText('WillReboottips')
        login.loginWeb(self)
        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_systemWatch()
        time.sleep(0.5)
        sysstatic.click_sysStatic()
        time.sleep(1)

        sysstatic.click_more3()
        time.sleep(2)
        url = self.driver.current_url
        if '#/VPN/IPSec' in url or '#/VPN/PPTP/L2TP' in url:
            logger.info(u'VPN状态 跳转到VPN配置 验证正常')
        else:
            CapPic(self.driver)
            logger.info(u'VPN状态 跳转到VPN配置 验证正常')
            raise Exception(u'VPN状态 跳转到VPN配置 验证正常')

        #配置VPN
        if '#/VPN/IPSec' in url:
            ipsec = IPsecPage(self.driver, self.url)
            # 操作删除 以访已有规则
            ipsec.click_selall()
            time.sleep(0.2)
            ipsec.click_delall()
            time.sleep(2)
            try:
                self.driver.implicitly_wait(2)
                ipsec.find_ok()
            except NoSuchElementException:
                try:
                    ipsec.find_tipsshowin()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(1)
                print('ipsec VPN列表为空')
            ipsec.click_add()
            time.sleep(1)
            ipsec.input_ids('test')
            ipsec.input_peer('123.5.3.6')
            ipsec.input_remoteAddr('123.5.3.6')
            # ipsec.input_remoteMask('255.255.255.0')
            ipsec.input_preshareKey('12345678')
            ipsec.click_save()
            time.sleep(2)
            try:  # 无线设备增加ac功能后 配置第一条ipsec时会提示重启
                ipsec.find_no()
            except NoSuchElementException:
                pass
            time.sleep(2)
        else:
            pptpl2tp = pptpL2tpPage(self.driver, self.url)
            # 操作删除 以访已有规则
            pptpl2tp.click_selall()
            time.sleep(0.2)
            pptpl2tp.click_delall()
            time.sleep(2)
            try:
                self.driver.implicitly_wait(2)
                pptpl2tp.find_ok()
            except NoSuchElementException:
                try:
                    pptpl2tp.find_tipsshowin()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(1)
                print('VPN隧道列表为空')
            pptpl2tp.click_add()
            time.sleep(1)
            pptpl2tp.click_workMode1()
            pptpl2tp.click_workModepptp()
            pptpl2tp.input_TunNames('test')
            seluserType = pptpl2tp.selelement_byName(pptpl2tp.seluserType)
            Select(seluserType).select_by_value('lantolan')
            pptpl2tp.input_userNames('test')
            pptpl2tp.input_password('test')
            pptpl2tp.input_remoteInIp('1.2.3.4')
            pptpl2tp.input_remoteInIPMask('255.255.255.0')
            pptpl2tp.click_saveS()
            time.sleep(2)

        sysstatic = sysStaticPage(self.driver, self.url)
        sysstatic.click_sysStatic()
        time.sleep(1)
        try:
            self.driver.implicitly_wait(2)
            list_name = sysstatic.getText_byXpath(sysstatic.list_name)
        except NoSuchElementException:
            CapPic(self.driver)
            logger.info(u'系统状态-VPN状态 未显示数据')
            raise Exception(u'系统状态-VPN状态 未显示数据')
        else:
            if list_name == 'test':
                logger.info(u'系统状态-VPN状态 显示数据验证通过 ')
            else:
                CapPic(self.driver)
                logger.info(u'系统状态-VPN状态 显示数据 异常')
                raise Exception(u'系统状态-VPN状态 显示数据 异常')

        # 删除VPN
        if '#/VPN/IPSec' in url:
            ipsec = IPsecPage(self.driver, self.url)
            ipsec.click_VPNConfig()
            time.sleep(0.5)
            ipsec.click_IPSec()
            time.sleep(1)
            # 操作删除 以访已有规则
            ipsec.click_selall()
            time.sleep(0.2)
            ipsec.click_delall()
            time.sleep(2)
            try:
                self.driver.implicitly_wait(2)
                ipsec.find_ok()
            except NoSuchElementException:
                try:
                    ipsec.find_tipsshowin()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(1)
                print('ipsec VPN列表为空')
        else:
            pptpl2tp = pptpL2tpPage(self.driver, self.url)
            pptpl2tp.click_VPNConfig()
            time.sleep(0.5)
            pptpl2tp.click_pptpL2tp()
            time.sleep(1)
            # 操作删除 以访已有规则
            pptpl2tp.click_selall()
            time.sleep(0.2)
            pptpl2tp.click_delall()
            time.sleep(2)
            try:
                self.driver.implicitly_wait(2)
                pptpl2tp.find_ok()
            except NoSuchElementException:
                try:
                    pptpl2tp.find_tipsshowin()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
            else:
                time.sleep(1)
                print('VPN隧道列表为空')

        self.driver.quit()
        logger.info('VPNStatus passed')

    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))


if __name__=='__main__':
    unittest.main()

