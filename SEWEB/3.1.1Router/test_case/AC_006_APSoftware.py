#! -*-conding:utf-8 -*-
#@Time: 2019/1/31 0031 17:36
#@swzhou
'''
AP软件管理
'''

import time
import unittest
import os
import os.path
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getAssertText,getweb
from common.loginRoute import login
from common.pingTest import pingTestIP
from pages.AC_005_APSoftwarePage import APSoftwarePage
from pages.AC_002_deviceMgmtPage import deviceMgmtPage
from pages.sysConfig_003_MaintenancePage import MaintenancePage
logger = LogGen(Logger = 'AC_006_APSoftware').getlog()


class APSoftware(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        os.system('taskkill /im "tftpd32.exe" /F')
        #谨防007 重启AC报错，提示失败 但设备已在重启导致无法登录路由
        i = 0
        while i < 50:
            ping = pingTestIP()
            if ping == 'Y':
                time.sleep(2)
                break
            else:
                time.sleep(1)
                i +=1
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        time.sleep(0.5)
        # pass

    def test_001_ManualUpgrade(self):
        u'''手动升级'''
        v2APname = getweb('v2APname')
        v2APoldversion = getweb('v2APoldversion')
        v2APnewversion = getweb('v2APnewversion')
        v1APname = getweb('v1APname')
        v1APoldversion = getweb('v1APoldversion')
        v1APnewversion = getweb('v1APnewversion')
        WillReboottips = getAssertText('WillReboottips')
        OnlineA = getAssertText('OnlineA')
        tmppath = os.path.dirname(os.path.abspath('.')) + '/script/'
        batpath = os.path.dirname(os.path.abspath('.')) + '/script/'

        #等待AP上线
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
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
        time.sleep(10)
        #先将WA3000N & WA2520N 单独页面降级
        device.input_search(v2APname)
        device.click_searchB()
        time.sleep(1)
        v2_ip1 = str(device.getText_byXpath(device.list_IP1))
        passurl_v2 = 'http://admin:admin@' + v2_ip1 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        pathv2 = tmppath + v2APoldversion + '.bin'
        device.input_search(v1APname)
        device.click_searchB()
        time.sleep(1)
        v1_ip4 = str(device.getText_byXpath(device.list_IP1))
        passurl_v1 = 'http://admin:admin@' + v1_ip4 + '/SoftwareUpdate.asp'  # 在URL里面直接加入用户名和密码
        pathv1 = tmppath + v1APoldversion + '.bin'

        # V2降级
        # 新开一个窗口，通过执行js来新开一个窗口
        js = 'window.open("%s");' %passurl_v2
        self.driver.execute_script(js)
        route_handles=self.driver.current_window_handle
        # print('route_handles:',route_handles)  # 输出当前窗口句柄（路由）
        all_handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        # print(all_handles)  # 输出句柄集合

        for handle in all_handles:  # 切换窗口（切换到v2）
            if handle != route_handles:
                print('switch to '), handle
                self.driver.switch_to_window(handle)
                v2_handles = self.driver.current_window_handle
                # print('v2_handles:',v2_handles)  # 输出当前窗口句柄（v2）
                break
        try:
            self.driver.get(passurl_v2)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            print('passurl_v2:',passurl_v2)
            raise Exception('v2 AP1登录失败')
        else:
            apsoftware = APSoftwarePage(self.driver,self.url)
            apsoftware.input_updatesoftware(pathv2)
            time.sleep(1)
            apsoftware.click_uttupdate()
            time.sleep(1)
            self.driver.switch_to.alert.accept()  # 接受警告框
            time.sleep(25)
        # V1降级
        # 再新开一个窗口，通过执行js来新开一个窗口
        js1 = 'window.open("%s");' % passurl_v1
        self.driver.execute_script(js1)
        all_handles2 = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        # print(all_handles2)  # 输出句柄集合

        for handle in all_handles2:  # 切换窗口（切换到v1）
            if handle != route_handles :
                print('switch to '), handle
                self.driver.switch_to_window(handle)
                v1_handles = self.driver.current_window_handle
                # print('v1_handles:', v1_handles)  # 输出当前窗口句柄（v1）
                break
        try:
            self.driver.get(passurl_v1)
            self.driver.set_page_load_timeout(5)  # selenium超时设置/等待时间过长自动停止
        except TimeoutException:
            print('passurl_v1:',passurl_v1)
            raise Exception('v1 AP2登录失败')
        else:
            apsoftware = APSoftwarePage(self.driver, self.url)
            apsoftware.input_updatesoftware(pathv1)
            time.sleep(1)
            apsoftware.click_uttupdate()
            time.sleep(1)
            self.driver.switch_to.alert.accept()  # 接受警告框
            time.sleep(30)
        #web降级后，等待AP上线
        self.driver.switch_to_window(route_handles)
        # 将路由器重启掉（降级后可能会存在mac22不同 导致有同个设备多个离线记录，D525重启很快 放AP后面）
        reboot = MaintenancePage(self.driver, self.url)
        reboot.click_headerReboot()
        time.sleep(1)
        reboot.click_ok()
        time.sleep(2)
        tips = str(reboot.getText_byClass(reboot.u_tim_str))
        self.assertEqual(tips, WillReboottips, msg='点击页面上方重启 操作失败')
        # 等待路由器重启
        i = 0
        while i < 20:
            now_url = str(self.driver.current_url)
            # print(now_url,i)
            if '/noAuth/login.html' not in now_url:  # 如果不同
                time.sleep(5)
            else:
                break
            i += 1
        self.driver.quit()
        # all_handles = self.driver.window_handles  # 获取当前窗口句柄集合（列表类型）
        # # print(all_handles)  # 输出句柄集合
        # for handle in all_handles:
        #     self.driver.switch_to_window(handle)
        #     self.driver.quit()
        time.sleep(2)
        login.loginWeb2(self)
        self.driver.implicitly_wait(10)
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(50)
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
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

        #手动升级
        apsoftware = APSoftwarePage(self.driver, self.url)
        apsoftware.click_APsoftware()
        time.sleep(1)
        # v1手动升级
        apsoftware.input_serach(v1APname)
        apsoftware.click_serachB()
        time.sleep(1)
        v1_version = str(apsoftware.getText_byXpath(apsoftware.list_version1))
        v1APoldversio2 = v1APoldversion[-12:]  # 截取版本号及日期 如：2.6.4-171110
        self.assertIn(v1APoldversio2, v1_version, msg='v1版本 web页面降级失败')
        apsoftware.click_list_sel1()
        time.sleep(0.2)
        apsoftware.click_upDataLocal()
        time.sleep(2)
        apsoftware.click_chooseFile()
        time.sleep(1)
        # 调用autoIt脚本上传AP版本
        os.system('%s' % (batpath + 'SE_APupdate_WA3000N.exe'))
        time.sleep(2)
        apsoftware.click_demo_upgrade()
        time.sleep(5)
        try:
            self.driver.implicitly_wait(2)
            apsoftware.find_ok()
        except NoSuchElementException:
            pass
        else:
            time.sleep(3)
        time.sleep(8)
        self.driver.implicitly_wait(10)
        # v2手动升级
        apsoftware.input_serach(v2APname)
        apsoftware.click_serachB()
        time.sleep(1)
        v2_version = str(apsoftware.getText_byXpath(apsoftware.list_version1))
        v2APoldversio2 = v2APoldversion[-12:] #截取版本号及日期 如：2.6.4-171110
        self.assertIn(v2APoldversio2,v2_version, msg='v2版本 web页面降级失败')
        apsoftware.click_list_sel1()
        time.sleep(0.2)
        apsoftware.click_upDataLocal()
        time.sleep(2)
        apsoftware.click_chooseFile()
        time.sleep(1)
        # 调用autoIt脚本上传AP版本
        os.system('%s' % (batpath + 'SE_APupdate_WA2520N.exe'))
        time.sleep(2)
        apsoftware.click_demo_upgrade()
        time.sleep(5)
        try:
            self.driver.implicitly_wait(2)
            apsoftware.find_ok()
        except NoSuchElementException:
            pass
        else:
            time.sleep(3)
        self.driver.implicitly_wait(10)


        #已手动升级，切换到设备管理 等待AP上线
        time.sleep(100)
        self.driver.quit()
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        time.sleep(0.5)
        print('AP升级中，等待AP上线...')
        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
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
        #切换回软件管理 确认AP升级后版本
        apsoftware = APSoftwarePage(self.driver, self.url)
        apsoftware.click_APsoftware()
        time.sleep(1)
        apsoftware.input_serach(v2APname)
        apsoftware.click_serachB()
        time.sleep(1)
        v2_version = str(apsoftware.getText_byXpath(apsoftware.list_version1))
        v2APversion2 = v2APnewversion[-12:]  # 截取版本号及日期 如：2.6.4-171110
        self.assertIn(v2APversion2, v2_version, msg='v2版本 手动升级失败')
        apsoftware.input_serach(v1APname)
        apsoftware.click_serachB()
        time.sleep(1)
        v1_version = str(apsoftware.getText_byXpath(apsoftware.list_version1))
        v1APversion2 = v1APnewversion[-12:]  # 截取版本号及日期 如：2.6.4-171110
        self.assertIn(v1APversion2, v1_version, msg='v1版本 手动升级失败')
        self.driver.quit()
        logger.info('test_001_ManualUpgrade passed')

    def test_002_autoUpodate(self):
        u'''自动更新：批量3个按钮提示正常，批量更新'''
        CapPic(self.driver)
        noAPupdateA = getAssertText('noAPupdateA')
        v1APname = getweb('v1APname')
        v1APnewversion = getweb('v1APnewversion')
        APexecStatus1 = getAssertText('APexecStatus1')
        APexecStatus2 = getAssertText('APexecStatus2')
        APexecStatus3 = getAssertText('APexecStatus3')
        OnlineA = getAssertText('OnlineA')
        OfflineA = getAssertText('OfflineA')

        device = deviceMgmtPage(self.driver, self.url)
        device.click_wirelessExtension()
        time.sleep(0.5)
        device.click_deviceMgmt()
        time.sleep(1)
        x = 0
        while x < 100:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            list_status2 = device.getText_byXpath(device.list_status2)
            list_status3 = device.getText_byXpath(device.list_status3)
            list_status4 = device.getText_byXpath(device.list_status4)
            print(list_status1, list_status2, list_status3, list_status4, x)
            if list_status1 == OnlineA and list_status2 == OnlineA and list_status3 == OnlineA and list_status4 == OnlineA:
                print('4台AP均在线', x)
                channel1 = str(device.getAttribute_byXpath(device.list_channel1, 'data-local'))
                channel2 = str(device.getAttribute_byXpath(device.list_channel2, 'data-local'))
                channel3 = str(device.getAttribute_byXpath(device.list_channel3, 'data-local'))
                channel4 = str(device.getAttribute_byXpath(device.list_channel4, 'data-local'))
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
        time.sleep(5)
        apsoftware = APSoftwarePage(self.driver, self.url)
        apsoftware.click_APsoftware()
        time.sleep(1)
        # #全选
        # apsoftware.click_list_selall()
        apsoftware.click_list_sel1()
        apsoftware.click_list_sel3()
        time.sleep(0.5)
        apsoftware.click_checkUpdata() # 检测更新
        time.sleep(3)
        #点一个没有检测到更新的
        apsoftware.click_list_updata1()
        time.sleep(1)
        tips=str(apsoftware.getText_byClass(apsoftware.tipsshowin))
        self.assertEqual(tips,noAPupdateA ,msg='更新 按钮异常')
        #自动更新
        apsoftware.click_list_selall()
        time.sleep(0.5)
        apsoftware.click_upData()
        time.sleep(25)
        apsoftware.input_serach(v1APname)
        apsoftware.click_serachB()
        time.sleep(1)
        list_status1 = apsoftware.getText_byXpath(apsoftware.list_status1)

        execStatus = [APexecStatus1,APexecStatus2,APexecStatus3]
        if list_status1 in execStatus:
            pass
        else:
            CapPic(self.driver)
            logger.info(u'点击自动更新 AP更新状态不对')
            print('list_status1:',list_status1)
            raise Exception('点击自动更新 AP更新状态不对')
        time.sleep(30)
        i = 0
        while i < 40 :
            list_status1 = apsoftware.getText_byXpath(apsoftware.list_status1)
            if list_status1 != '检测更新':
                # print(list_status1,i)
                time.sleep(3)
                i = i + 1
            else:
                print('自动更新 已升级成功',i)
                break
        device = deviceMgmtPage(self.driver, self.url)
        device.click_deviceMgmt()
        time.sleep(1)
        device.input_search(v1APname)
        device.click_searchB()
        time.sleep(1)
        i = 0
        while i < 30:
            device.click_refreshtable()
            time.sleep(1)
            list_status1 = device.getText_byXpath(device.list_status1)
            try:
                self.driver.implicitly_wait(3)
                device.find_list_status2()
            except NoSuchElementException:
                time.sleep(3)
                i = i +1
            else:
                self.driver.implicitly_wait(10)
                list_status2 = device.getText_byXpath(device.list_status2)
                print(list_status1, list_status2, i)
                if list_status1 == OnlineA or list_status2 == OnlineA:
                    print('v1 AP已上线', i)
                    break
                else:
                    time.sleep(3)
                i = i + 1
        else:
            raise Exception('v1 AP 未上线')

        #清除离线AP（ap升级后mac变为fc 会有两条记录 清除掉另一个）
        if list_status1 == OfflineA:
            device.click_list_sel1()
        elif list_status2 == OfflineA:
            device.click_list_sel2()
        device.click_clearOutlineAP()
        time.sleep(1)
        x = 0
        while x < 60:
            device.click_refreshtable()
            time.sleep(1.5)
            list_status1 = device.getText_byXpath(device.list_status1)
            # print(list_status1, x)
            if list_status1 == OnlineA:
                print('v1 AP已上线', x)
                ip1 = str(device.getText_byXpath(device.list_IP1))
                # print('ip1=', ip1,  x)
                if ip1 != '192.168.1.253':
                    print('v1 信息已同步', x)
                    break
                else:
                    time.sleep(3)
            else:
                time.sleep(3)
            x = x + 1
        else:
            raise Exception('v1 信息未能同步')

        apsoftware = APSoftwarePage(self.driver, self.url)
        apsoftware.click_APsoftware()
        time.sleep(1)
        apsoftware.input_serach(v1APname)
        apsoftware.click_serachB()
        time.sleep(1)
        v1_version = str(apsoftware.getText_byXpath(apsoftware.list_version1))
        v1APversion2 = v1APnewversion[-12:]
        if v1APversion2 not in v1_version:
            print('AP版本确认正常')
        else:
            raise Exception('AP升级后 版本依旧与升级前一致')
        self.driver.quit()
        logger.info('test_002_autoUpodate passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()
