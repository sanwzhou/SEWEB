#! -*-conding:utf-8 -*-
#@Time: 2019/2/13 0013 17:16
#@swzhou
'''
出厂信息:登录IP/域名、账号、密码
'''

import unittest
from common.LogGen import LogGen
from common.initTestPC import initTestPC
from test_case.sysConfig_008_configuration import configuration
logger = LogGen(Logger = 'Parameter_010_DefaultInfo').getlog()

class DefaultInfo(unittest.TestCase):

    def setUp(self):
        logger.info('setUp start')

    def test_resertFirstLogin(self):
        u'''验证出厂信息：登录IP/域名、账号、密码'''
        configuration.test_002_Resert(self)
        logger.info('test_resertFirstLogin passed')

    def tearDown(self):
        # self.dr.close()
        logger.info('准备工作已完成，开始测试')
        logger.info('tearDown over')
        logger.info('%s' % ('=' * 50))

if __name__=='__main__':
    unittest.main()