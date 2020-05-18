#! -*-conding:utf-8 -*-
#@Time: 2019/3/15 0015 16:32
#@swzhou
'''
日志服务器，开启日志 可以抓到数据 by VPN 备用 当前未启用改case
'''

import os
import time
import socket
import unittest
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import gettelnet,getweb,getpath,getAssertText
from common.loginRoute import login
from common.call_FireFox import call_Firefox
from pages.sysConfig_005_syslogPage import syslogPage
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
logger = LogGen(Logger = 'sysConfig_010_syslogServer').getlog()
tmppath = os.path.dirname(os.path.abspath('.')) + '/tmp/'

class syslogServer(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        # pass

    def test_syslog(self):
        u'''日志服务器'''
        pcNetworkID = getweb('pcNetworkID')
        wiresharkpath = getpath('wiresharkpath')
        host = gettelnet('host')

        #0、清理tmp下的syslog.pcapng\log文件
        call_Firefox.del_syslog_log(self)
        #1、开启syslog server
        pcaddr = socket.gethostbyname(socket.getfqdn(socket.gethostname()))
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        syslog = syslogPage(self.driver,self.url)
        syslog.click_sysConfig()
        time.sleep(0.5)
        syslog.click_Syslog()
        time.sleep(1)
        syslog.click_SyslogServer()
        time.sleep(1)
        syslog.click_syslogEn()
        syslog.input_ServerIp(pcaddr)
        syslog.input_ServerPort('514')
        syslog.click_save()
        time.sleep(1)
        syslogEs = syslog.getAttribute_byXpath(syslog.syslogEs,'checked')
        self.assertEqual(syslogEs,'true',msg = 'syslog服务器启用失败')

        #2、新建一条vpn 使生成syslog
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
        pptpl2tp.click_add()
        time.sleep(2)
        pptpl2tp.click_workMode2()
        pptpl2tp.click_workModepptp()
        pptpl2tp.input_TunNames('testS')
        pptpl2tp.input_TunNamesIP('11.2.3.4')
        pptpl2tp.input_userNames('test')
        pptpl2tp.input_password('test')
        pptpl2tp.input_remoteInIp('11.2.3.4')
        pptpl2tp.input_remoteInIPMask('255.255.255.0')
        pptpl2tp.click_save()
        time.sleep(0.5)

        # 3、调用wireshark 开启抓包，必须要抓到包之后才会进行下一步，因此放在设置vpn之后，通过抓下一次的log
        packetfile = tmppath + 'syslogtest.pcapng'
        dir = wiresharkpath[0:2]
        getpacket = ('tshark -i%s -f "udp port 514" -w %s -c 2' % (pcNetworkID, packetfile))
        os.system('%s && cd %s && %s' % (dir,wiresharkpath, getpacket))

        #4、读取抓包显示 并存为log文件
        logfile = tmppath + 'syslogtest.log'
        savepacket = ('tshark -r %s -T fields -e "ip.src" -e ip.dst -Y "syslog" > %s ' % (packetfile,logfile))
        os.system('%s && cd %s && %s' % (dir,wiresharkpath,savepacket))

        #5、读取判断syslog生效
        with open(logfile, 'r') as file_to_read:
            while True:
                lines = file_to_read.readline()  # 整行读取数据
                print(lines)
                if not lines:
                    break
                if host + pcaddr in lines:
                    print(u'验证通过')
        #删除vpn 关闭syslog
        nodata = getAssertText('nodata')
        # 删除VPN
        pptpl2tp = pptpL2tpPage(self.driver, self.url)
        pptpl2tp.click_pptpL2tp()
        time.sleep(1)
        pptpl2tp.click_selall()
        time.sleep(0.2)
        pptpl2tp.click_delall()
        time.sleep(1)
        pptpl2tp.click_ok()
        time.sleep(2)
        list_nodata = pptpl2tp.getText_byXpath(pptpl2tp.list_nodata)
        if list_nodata == nodata:
            logger.info(u'VPN 已删除')
        else:
            CapPic(self.driver)
            logger.info(u'VPN删除失败')
            raise Exception(u'VPN删除失败')
        syslog = syslogPage(self.driver, self.url)
        syslog.click_sysConfig()
        time.sleep(0.5)
        syslog.click_Syslog()
        time.sleep(1)
        syslog.click_SyslogServer()
        time.sleep(1)
        syslog.click_syslogC()
        syslog.click_save()
        time.sleep(1)
        syslogCs = syslog.getAttribute_byXpath(syslog.SyslogCs, 'checked')
        self.assertEqual(syslogCs, 'true', msg='syslog服务器关闭失败')

        self.driver.quit()
        logger.info('test_reboot1 passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
