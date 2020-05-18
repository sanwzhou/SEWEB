#! -*-conding:utf-8 -*-
#@Time: 2019/9/5 0005 16:47
#@swzhou
'''
艾泰云 登录
'''


import random
import time
import unittest
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from common.LogGen import LogGen
from common.CapPic import CapPic
from common.ReadConfig import getweb
from pages.LoginYunPage import LoginYunPage
logger = LogGen(Logger = 'loginYun').getlog()
BrowerMode = getweb('BrowerMode')


def get_track(distance):
  '''
  拿到移动轨迹，模仿人的滑动行为，先匀加速后匀减速
  匀变速运动基本公式：
  ①v=v0+at
  ②s=v0t+(1/2)at²
  ③v²-v0²=2as

  :param distance: 需要移动的距离
  :return: 存放每0.2秒移动的距离
  '''
  # 初速度
  v=0
  # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
  t=0.1
  # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
  tracks=[]
  # 当前的位移
  current=0
  # 到达mid值开始减速
  mid=distance * 4/5

  distance += 10 # 先滑过一点，最后再反着滑动回来

  while current < distance:
    if current < mid:
      # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
      a = 2000 # 加速运动
    else:
      a = -3 # 减速运动

    # 初速度
    v0 = v
    # 0.2秒时间内的位移
    s = v0*t+0.5*a*(t**2)
    # 当前的位置
    current += s
    # 添加到轨迹列表
    tracks.append(round(s))

    # 速度已经达到v,该速度作为下次的初速度
    v= v0+a*t

  # 反着滑动到大概准确位置
  for i in range(3):
    tracks.append(-2)
  for i in range(4):
    tracks.append(-1)
  return tracks

class loginYun(unittest.TestCase):

    def setUp(self):
        print('login start')

    def loginYunWeb(self,tracks=get_track(350)):

        self.url = 'http://' + getweb('cloudURL')
        self.user = getweb('cloundC')
        self.passwd = getweb('cloundP')
        if BrowerMode == '0':
            # 使用无界模式
            chrome_opt = Options()
            chrome_opt.add_argument('--headless')
            chrome_opt.add_argument('--diaable-gpu')
            self.driver = webdriver.Chrome(options=chrome_opt)
            self.driver.set_window_size(1920, 1080)
        else:
            self.driver = webdriver.Chrome()
            self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            time.sleep(3)
        login_page = LoginYunPage(self.driver, self.url)
        try: #暂时https 无法使用chrome无界模式登录，调用判断 使用有界模式登录
            login_page.input_username(self.user)
        except AttributeError:
            nowUrl = self.driver.current_url
            exUrl = 'https://' + getweb('cloudURL')
            if BrowerMode == '0' and nowUrl == exUrl:
                self.driver.quit()
                self.driver = webdriver.Chrome()
                self.driver.maximize_window()
                self.driver.implicitly_wait(10)
                self.driver.get(self.url)
                time.sleep(1)
                nowUrl = self.driver.current_url
                if 'https' in nowUrl:
                    time.sleep(3)
                time.sleep(1)
                login_page = LoginYunPage(self.driver, self.url)
                login_page.input_username(self.user)
            else:
                CapPic(self.driver)
                logger.info(u'无法打开设备界面')
                logger.info(u'当前浏览器rul:%s' % nowUrl)
                raise Exception(u'无法打开设备界面')
        login_page.input_password(self.passwd)
        need_move_span = self.driver.find_element_by_xpath('//*[@id="slider"]/div[4]') #调用的回报错 直接定位
        ActionChains(self.driver).click_and_hold(need_move_span).perform()
        for x in tracks:  # 模拟人的拖动轨迹
            # print(x)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=random.randint(1, 3)).perform()
        time.sleep(1)
        ActionChains(self.driver).release().perform()  # 释放左键

        login_page.click_login()
        time.sleep(1)
        nowurl = self.driver.current_url
        if 'index.html' in nowurl:
            print('登录成功')
        else:
            raise Exception('未登录成功')


        print('login_web success')

    def test_loginYunWeb2(self,tracks=get_track(350)):
        #使用有界模式 调用autoIt等脚本不能使用无界模式
        self.url = 'http://' + getweb('cloudURL')
        self.user = getweb('cloundC')
        self.passwd = getweb('cloundP')
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(1)
        nowUrl = self.driver.current_url
        if 'https' in nowUrl:
            time.sleep(3)
        time.sleep(1)
        login_page = LoginYunPage(self.driver, self.url)
        login_page.input_username(self.user)
        login_page.input_password(self.passwd)
        need_move_span = self.driver.find_element_by_xpath('//*[@id="slider"]/div[4]')  # 调用的回报错 直接定位
        ActionChains(self.driver).click_and_hold(need_move_span).perform()
        for x in tracks:  # 模拟人的拖动轨迹
            # print(x)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=random.randint(1, 3)).perform()
        time.sleep(1)
        ActionChains(self.driver).release().perform()  # 释放左键

        login_page.click_login()
        time.sleep(1)
        nowurl = self.driver.current_url
        if 'index.html' in nowurl:
            print('登录成功')
        else:
            raise Exception('未登录成功')
        print('login_web success')


    def tearDown(self):
        print('login over')

if __name__=='__main__':
    unittest.main()

