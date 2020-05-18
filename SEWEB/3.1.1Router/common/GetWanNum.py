#! -*-conding:utf-8 -*-
#@Time: 2019/4/26 0026 13:51
#@swzhou
'''
从参数中获取wan口数量
'''

from common.ReadConfig import getweb,getParameter
from common.GetExcelValue import getExcelValue


def getWanNum():

    portTateWANp = getParameter('portTateWANp')
    portTateWANp = getExcelValue(parameter=portTateWANp)

    if '默认' in portTateWANp:
        if '-' in portTateWANp:
            wanNum1 = int(portTateWANp.split(r'-')[0])
            wanNum2 = int(portTateWANp.split(r'-')[1][0])
            if wanNum1 > wanNum2:
                wanNum = wanNum1
            else:
                wanNum = wanNum2
        elif '/' in portTateWANp:
            wanNum1 = int(portTateWANp.split(r'/')[0])
            wanNum2 = int(portTateWANp.split(r'/')[1][0])
            if wanNum1 > wanNum2:
                wanNum = wanNum1
            else:
                wanNum = wanNum2
    else:
        wanNum = int(portTateWANp[0])

    return wanNum

# print(getWanNum())