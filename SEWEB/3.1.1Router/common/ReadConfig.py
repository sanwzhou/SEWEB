#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 16:13
#@swzhou
'''
读取config.ini配置
'''

import configparser
import os

configfile = '/config/config.ini'
# configfile = '/config/configE.ini'
# configfile = '/config/configT.ini'

def getweb(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('web',name)
    return NameValue

def gettelnet(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('telnet',name)
    return NameValue

def getpath(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('path',name)
    return NameValue

def getAssertText(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('AssertText',name)
    return NameValue

def getMenu(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('Menu',name)
    return NameValue

def getParameter(name):
    cf = configparser.ConfigParser()
    cfpath = os.path.dirname(os.path.abspath('.')) + configfile
    cf.read(cfpath,encoding='utf8')
    NameValue = cf.get('parameter',name)
    return NameValue

# print(ReadConfig.getweb('BrowerName'))
# print(ReadConfig.gettelnet('host'))
# print(ReadConfig.getweb('SoftVersion1'))
