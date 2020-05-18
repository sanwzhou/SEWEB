# host = '192.168.1.1'
# host1 = str(host).split(r'.')
# host2 = host1[0] + '.' + host1[1] + '.' + host1[2] +'.'
#
# print(host2)

#过滤掉中文和带空格的
# zhmodel = re.compile(u'[^\u4e00-\u9fa5]')  # 检查非中文
# ftpFile2 = []
# for i in ftpFile:
#     i = i[2:]
#     if ' ' not in i:
#         if zhmodel.search(i):
#             x = i
#             ftpFile2.append(x)

# import re
# i1 = ['11','aa','中1','1中','a中','中a','中']
# i2 = ['11','aa','中1','1中','a中','中a','中']
# a = re.compile(u'[\u4e00-\u9fa5]')
# for i in i1:
#     print('123:,',i)
#
#     if a.search(i):
#         a1 = a.search(i)
#         print('1:',a1)
#
#         i2.remove(i)
# print(i1)
# print(i2)

# a = 'nv640Ev1.5.0-130918'
# b = 'nvA655Wv3.0.0-200116-142208'
# c = 'TL-BWR-21v3.2.1-200304-171146'
#
# list = [a,b,c]
# for aa in list:
# #     i = 0
# #     for x in aa:
# #         if x == '-':
# #             i +=1
# #     print(i)
#
#     num = 0
#     ver= ''
#     v_split = aa.split(r'-')
#     print(v_split)
#     if len(v_split) == 2:
#         ver = v_split[0] + '-' +v_split[1]
#     else:
#         while num < len(v_split) -1:
#             ver += v_split[num] + '-'
#             num +=1
#         else:
#             print(ver)
#             ver = ver[:-1]
#     print(ver)


# import time
# timeStamp = 1381419600
# timeArray = time.localtime(timeStamp)
# otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# print(otherStyleTime)

aa = "abc"
bb = ["a","b","c"]

if any(b in aa for b in bb):
    print('1')