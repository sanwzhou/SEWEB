#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 16:27
#@swzhou
'''
脚本执行过程中日志记录 info
'''
import logging
import os
import time

from common.ReadConfig import getweb

class LogGen(object):

    def __init__(self,Logger):
        SoftVersion1 = getweb('SoftVersion1')

        self.Logger = logging.getLogger(Logger)
        self.Logger.setLevel(logging.INFO)
        #创建写入文件 Handler
        lt = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
        logname = os.path.dirname(os.path.abspath('.')) + '/logs/' + SoftVersion1 + '_' + lt + '.log'
        fileh = logging.FileHandler(logname) #FileHandler 写入文件
        fileh.setLevel(logging.INFO)
        #创建 输入到控制台 的Handler
        consoleh = logging.StreamHandler() #StreamHandler 输出到控制台
        consoleh.setLevel(logging.INFO)
        #定义 输出格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileh.setFormatter(formatter)
        consoleh.setFormatter(formatter)
        #给loger添加 Handler
        self.Logger.addHandler(fileh)
        self.Logger.addHandler(consoleh)

    def getlog(self):
        return self.Logger


# #测试
# logger = LogGen(Logger = 'LoginPage').getlog()
# logger.info('this is info message')



