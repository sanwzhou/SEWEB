#! -*-conding:utf-8 -*-
#@Time: 2019/5/14 0014 12:05
#@swzhou
'''
ping
'''

import os
from common.ReadConfig import getweb

def pingTestIP(dst = getweb('RouteUrl')[7:]):

    p = os.popen("ping -w 2 -n 2 " + dst)
    line = p.read()

    # print(str(line))
    # print(str(line).split("\n"))
    sss = (str(line).split("\n"))
    sss = [x for x in sss if x != '']
    # print(sss)
    if len(sss) >= 5 and 'TTL=' in sss[2]:  # dns无法解析 会直接返回找不到主机名
        Result = 'Y'
    else:
        Result = 'N'

    p.close()
    return Result

# print(pingTestIP('12.2.2.2'))
# print(pingTestIP('www.baidu.com'))

