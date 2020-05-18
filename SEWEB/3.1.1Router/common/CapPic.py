#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 16:21
#@swzhou
'''
截图,放在 pictrue目录下
'''
from selenium import webdriver
import time
import os
from common.ReadConfig import getweb

def CapPic(driver):
    SoftVersion1 = getweb('SoftVersion1')
    pt = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
    picname = os.path.dirname(os.path.abspath('.')) + '/picture/' + SoftVersion1 +'_' + pt +'.png'
    driver.get_screenshot_as_file(picname)


#CapPic(driver=webdriver.Chrome())
