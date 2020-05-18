#! -*-conding:utf-8 -*-
#@Time: 2019/2/22 0022 13:08
#@swzhou
'''
VPN
'''

import time
import unittest
from selenium.common.exceptions import NoSuchElementException
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.loginRoute import login
from common.ReadConfig import getAssertText,getParameter
from common.GetExcelValue import getExcelValue
from pages.VPNconfig_pptpL2tpPage import pptpL2tpPage
from pages.VPNconfig_IPsecPage import IPsecPage
from selenium.webdriver.support.select import Select
logger = LogGen(Logger = 'Parameter_022_VPNconfig').getlog()


class VPNconfig(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')
        login.loginWeb(self)
        self.driver.implicitly_wait(10)
        # pass

    def test_001_pptpL2tp(self):
        u'''PPTP/L2TP'''
        L2tpP = getParameter('L2tpP')
        pptpP = getParameter('pptpP')
        SupportL = getExcelValue(L2tpP)
        SupportP = getExcelValue(pptpP)
        pptpL2tp = pptpL2tpPage(self.driver, self.url)
        # print(SupportL,SupportP)
        if SupportL == '√' and SupportP == '√':
            logger.info(u'参数支持PPTP/L2TP')
            try:
                self.driver.implicitly_wait(2)
                pptpL2tp.click_VPNConfig()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持VPN配置,则不支持pptp/l2tp，与参数表不相符')
                raise Exception('不支持VPN配置,则不支持pptp/l2tp，与参数表不相符')
            else:
                time.sleep(0.5)
                try:
                    self.driver.implicitly_wait(2)
                    pptpL2tp.click_pptpL2tp()
                except NoSuchElementException:
                    CapPic(self.driver)
                    logger.info(u'不支持pptp/l2tp，与参数表不相符')
                    raise Exception('不支持pptp/l2tp，与参数表不相符')
                else:
                    logger.info(u'支持pptp/l2tp，与参数表相符')
                    time.sleep(1)
                    pptpL2tp.click_PPTPGlobalSet()
                    time.sleep(0.5)
                    selauthtypeP = pptpL2tp.selelement_byXpath(pptpL2tp.selauthtypeP)
                    Select(selauthtypeP).select_by_value('PAP')
                    time.sleep(0.2)
                    Select(selauthtypeP).select_by_value('MS-CHAPV2')
                    time.sleep(0.2)
                    Select(selauthtypeP).select_by_value('CHAP')
                    time.sleep(0.2)
                    Select(selauthtypeP).select_by_value('THRIN')
                    time.sleep(0.2)
                    pptpL2tp.click_pptpEncryS()
                    time.sleep(0.2)
                    pptpL2tp.click_l2tpGlobalSet()
                    time.sleep(0.5)
                    selauthtypeL = pptpL2tp.selelement_byXpath(pptpL2tp.selauthtypeL)
                    Select(selauthtypeL).select_by_value('PAP')
                    time.sleep(0.2)
                    Select(selauthtypeL).select_by_value('NONE')
                    time.sleep(0.2)
                    Select(selauthtypeL).select_by_value('CHAP')
                    time.sleep(0.2)
                    Select(selauthtypeL).select_by_value('EITHER')
                    time.sleep(0.2)

                    pptpL2tp.click_Tunnellist()
                    time.sleep(0.5)
                    pptpL2tp.click_add()
                    time.sleep(1)
                    #服务端
                    pptpL2tp.click_workMode1() #拨入
                    pptpL2tp.click_workModepptp()
                    seluserType = pptpL2tp.selelement_byName(pptpL2tp.seluserType)
                    Select(seluserType).select_by_value('mobile') #移动用户
                    time.sleep(0.5)
                    pptpL2tp.input_staticIPs('1.2.3.4') #固定IP地址
                    pptpL2tp.input_LanMac('1') #硬件特征码
                    Select(seluserType).select_by_value('lantolan')  # LAN到LAN
                    time.sleep(0.5)
                    pptpL2tp.input_staticIPs('1.2.3.4')  # 固定IP地址
                    pptpL2tp.click_workModel2tp()
                    seluserType = pptpL2tp.selelement_byName(pptpL2tp.seluserType)
                    Select(seluserType).select_by_value('mobile')  # 移动用户
                    time.sleep(0.5)
                    Select(seluserType).select_by_value('lantolan')  # LAN到LAN
                    time.sleep(0.5)
                    #客户端
                    pptpL2tp.click_workMode2() # 拨出
                    time.sleep(0.5)
                    pptpL2tp.click_workModepptp()
                    time.sleep(0.5)
                    pptpL2tp.click_natEn() #nat模式
                    pptpL2tp.click_pptpEncryC()
                    time.sleep(0.5)
                    selPPTP2AuthType = pptpL2tp.selelement_byName(pptpL2tp.PPTP2AuthType)
                    Select(selPPTP2AuthType).select_by_value('PAP')
                    time.sleep(0.2)
                    Select(selPPTP2AuthType).select_by_value('MS-CHAPV2')
                    time.sleep(0.2)
                    Select(selPPTP2AuthType).select_by_value('CHAP')
                    time.sleep(0.2)
                    Select(selPPTP2AuthType).select_by_value('THRIN')
                    time.sleep(0.2)
                    pptpL2tp.click_workModel2tp()
                    time.sleep(0.5)
                    pptpL2tp.click_natEn()  # nat模式
                    selL2TPAuthTypes = pptpL2tp.selelement_byName(pptpL2tp.L2TPAuthTypes)
                    Select(selL2TPAuthTypes).select_by_value('PAP')
                    time.sleep(0.2)
                    Select(selL2TPAuthTypes).select_by_value('NONE')
                    time.sleep(0.2)
                    Select(selL2TPAuthTypes).select_by_value('CHAP')
                    time.sleep(0.2)
                    Select(selL2TPAuthTypes).select_by_value('EITHER')
                    time.sleep(0.2)
        elif SupportL == '×' and SupportP == '×':
            logger.info(u'参数不支持PPTP/L2TP')
            try:
                self.driver.implicitly_wait(2)
                pptpL2tp.click_VPNConfig()
            except AttributeError:
                logger.info('不支持VPN配置,则不支持pptp/l2tp，与参数表相符')
            else:
                time.sleep(1)
                try:
                    pptpL2tp.click_pptpL2tp()
                except AttributeError:
                    logger.info('不支持pptp/l2tp，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'支持pptp/l2tp，与参数表不相符')
                    raise Exception('支持pptp/l2tp，与参数表不相符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', SupportL,SupportP)
            raise Exception(u'参数表读取异常')

        self.driver.quit()
        logger.info('test_001_vlanInterface passed')

    def test_002_IPsec(self):
        u'''IPsec（某些设备可能不支持）'''
        ipsecP = getParameter('ipsecP')
        Support = getExcelValue(ipsecP)
        ipsecpage = IPsecPage(self.driver,self.url)
        if Support == '√':
            logger.info(u'参数支持IPsec')
            try:
                self.driver.implicitly_wait(2)
                ipsecpage.click_VPNConfig()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持VPN配置,则不支持ipsec，与参数表不相符')
                raise Exception('不支持VPN配置,则不支持ipsec，与参数表不相符')
            else:
                time.sleep(0.5)
                try:
                    self.driver.implicitly_wait(2)
                    ipsecpage.click_IPSec()
                except NoSuchElementException:
                    CapPic(self.driver)
                    logger.info(u'不支持ipsec，与参数表不相符')
                    raise Exception('不支持ipsec，与参数表不相符')
                else:
                    logger.info(u'支持ipsec，与参数表相符')
                    time.sleep(1)
                    ipsecpage.click_add()
                    time.sleep(1)
                    #连接方式
                    selconnType = ipsecpage.selelement_byName(ipsecpage.connType)
                    Select(selconnType).select_by_value('2')
                    time.sleep(0.3)
                    Select(selconnType).select_by_value('3')
                    time.sleep(0.3)
                    Select(selconnType).select_by_value('1')
                    time.sleep(0.3)
                    #加密认证算法
                    seltransform = ipsecpage.selelement_byName(ipsecpage.transform)
                    Select(seltransform).select_by_value('100')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('110')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('120')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('210')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('220')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('300')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('400')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('510')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('310')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('320')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('410')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('420')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('510')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('520')
                    time.sleep(0.2)
                    Select(seltransform).select_by_value('200')
                    time.sleep(0.2)
                    ipsecpage.click_highChoosen()
                    time.sleep(1)
                    #协商模式
                    selnegMode = ipsecpage.selelement_byXpath(ipsecpage.negMode)
                    Select(selnegMode).select_by_value('Aggres')
                    time.sleep(0.2)
                    Select(selnegMode).select_by_value('Main')
                    time.sleep(0.2)
                    #加密认证算法1
                    selpolicy = ipsecpage.selelement_byXpath(ipsecpage.policy)
                    Select(selpolicy).select_by_value('213')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('222')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('223')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('112')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('113')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('122')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('123')
                    time.sleep(0.2)
                    Select(selpolicy).select_by_value('212')
                    time.sleep(0.2)
                    ipsecpage.click_anti_replay()
                    ipsecpage.click_dpdEn()
                    ipsecpage.click_nattEn()
                    time.sleep(0.2)
                    ipsecpage.input_HeartbeatInt('30')
                    ipsecpage.input_natPort('500')
                    ipsecpage.input_Keepalive('30')
        elif Support == '×':
            logger.info(u'参数不支持IPsec')
            try:
                self.driver.implicitly_wait(2)
                ipsecpage.click_VPNConfig()
            except AttributeError:
                logger.info('不支持VPN配置,则不支持ipsec，与参数表相符')
            else:
                time.sleep(1)
                try:
                    ipsecpage.click_IPSec()
                except AttributeError:
                    logger.info('不支持ipsec，与参数表相符')
                else:
                    CapPic(self.driver)
                    logger.info(u'支持ipsec，与参数表不相符')
                    raise Exception('支持ipsec，与参数表不相符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_002_IPsec passed')

    def test_003_IPSec_binding_pptp(self):
        u'''IPSec可以绑定在pptp虚接口（某些设备可能不支持）'''
        nodata = getAssertText('nodata')
        ibindingPp =getParameter('ibindingPp')
        Support = getExcelValue(ibindingPp)
        pptpL2tp = pptpL2tpPage(self.driver, self.url)
        #新增pptp
        if Support == '√':
            logger.info(u'参数支持IPSec可以绑定在pptp虚接口')
            try:
                self.driver.implicitly_wait(2)
                pptpL2tp.click_VPNConfig()
                time.sleep(0.5)
                pptpL2tp.click_pptpL2tp()
            except NoSuchElementException:
                CapPic(self.driver)
                logger.info(u'不支持VPN配置或不支持pptp/l2tp 则不能支持ipsec绑定pptp接口，与参数表不相符')
                raise Exception('不支持VPN配置或不支持pptp/l2tp 则不能支持ipsec绑定pptp接口，与参数表不相符')
            else:
                time.sleep(1)
                # 操作删除 以访已有规则
                pptpL2tp.click_selall()
                time.sleep(0.2)
                pptpL2tp.click_delall()
                time.sleep(2)
                try:
                    self.driver.implicitly_wait(2)
                    pptpL2tp.find_ok()
                except NoSuchElementException:
                    try:
                        pptpL2tp.find_tipsshowin()
                        time.sleep(1)
                    except NoSuchElementException:
                        pass
                else:
                    time.sleep(1)
                    print('VPN隧道列表为空')
                pptpL2tp.click_add()
                time.sleep(1)
                pptpL2tp.click_workMode1()# 拨入
                pptpL2tp.click_workModepptp()
                pptpL2tp.input_TunNames('test1')
                seluserType = pptpL2tp.selelement_byName(pptpL2tp.seluserType)
                Select(seluserType).select_by_value('mobile')  # 移动用户
                time.sleep(0.5)
                pptpL2tp.input_userNames('test1')
                pptpL2tp.input_password('test1')
                pptpL2tp.click_save()
                time.sleep(1)
                try:
                    self.driver.implicitly_wait(2)
                    #ipsec调用pptp接口
                    ipsecpage = IPsecPage(self.driver, self.url)
                    ipsecpage.click_IPSec()
                except NoSuchElementException:
                    CapPic(self.driver)
                    logger.info(u'不支持IPsec，与参数表不相符')
                    raise Exception('不支持IPsec，与参数表不相符')
                else:
                    logger.info(u'支持IPsec，与参数表相符')
                    time.sleep(1)
                    ipsecpage.click_add()
                    time.sleep(1)
                    sellocalBing = ipsecpage.selelement_byName(ipsecpage.localBind)
                    Select(sellocalBing).select_by_value('PPTPS_test1')
                    time.sleep(0.3)
                    #删除PPTP
                    pptpL2tp = pptpL2tpPage(self.driver, self.url)
                    pptpL2tp.click_pptpL2tp()
                    time.sleep(1)
                    pptpL2tp.click_delete1()
                    time.sleep(1)
                    pptpL2tp.click_ok()
                    time.sleep(1)
                    listnodata = str(pptpL2tp.getText_byXpath(pptpL2tp.list_nodata))
                    self.assertEqual(listnodata,nodata,msg='删除失败')
        elif Support == '×':
            logger.info(u'参数不支持IPSec可以绑定在pptp虚接口')
            try:
                self.driver.implicitly_wait(2)
                pptpL2tp.click_VPNConfig()
                time.sleep(0.5)
                pptpL2tp.click_pptpL2tp()
                time.sleep(0.5)
            except AttributeError:
                logger.info(u'不支持VPN配置或不支持pptp/l2tp 则不能支持ipsec绑定pptp接口，与参数表相符')
            else:
                time.sleep(1)
                # 操作删除 以访已有规则
                pptpL2tp.click_selall()
                time.sleep(0.2)
                pptpL2tp.click_delall()
                time.sleep(2)
                try:
                    self.driver.implicitly_wait(2)
                    pptpL2tp.find_ok()
                except NoSuchElementException:
                    try:
                        pptpL2tp.find_tipsshowin()
                        time.sleep(1)
                    except NoSuchElementException:
                        pass
                else:
                    time.sleep(1)
                    print('VPN隧道列表为空')
                pptpL2tp.click_add()
                time.sleep(1)
                pptpL2tp.click_workMode1()  # 拨入
                pptpL2tp.click_workModepptp()
                pptpL2tp.input_TunNames('test1')
                seluserType = pptpL2tp.selelement_byName(pptpL2tp.seluserType)
                Select(seluserType).select_by_value('mobile')  # 移动用户
                time.sleep(0.5)
                pptpL2tp.input_userNames('test1')
                pptpL2tp.input_password('test1')
                pptpL2tp.click_save()
                time.sleep(1)
                try:
                    self.driver.implicitly_wait(2)
                    # ipsec调用pptp接口
                    ipsecpage = IPsecPage(self.driver, self.url)
                    ipsecpage.click_IPSec()
                except NoSuchElementException:
                    logger.info('不支持ipsec则不支持绑定到pptp接口，与参数表相符')
                else:
                    try:
                        time.sleep(1)
                        ipsecpage.click_add()
                        time.sleep(1)
                        sellocalBing = ipsecpage.selelement_byName(ipsecpage.localBind)
                        Select(sellocalBing).select_by_value('PPTPS_test1')
                    except NoSuchElementException:
                        logger.info('不支持ipsec则不支持绑定到pptp接口，与参数表相符')
                    else:
                        CapPic(self.driver)
                        logger.info(u'支持ipsec则不支持绑定到pptp接口，与参数表不相符')
                        raise Exception('支持ipsec则不支持绑定到pptp接口，与参数表不相符')
        else:
            logger.info(u'参数表读取异常')
            logger.info(u'参数表读取值为：', Support)
            raise Exception(u'参数表读取异常')
        self.driver.quit()
        logger.info('test_003_IPSec_binding_pptp passed')


    def tearDown(self):
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()