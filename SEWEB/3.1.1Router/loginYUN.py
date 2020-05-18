from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import random

driver = webdriver.Chrome()

def move_to_gap(tracks):
    driver.get("http://47.97.110.84/")
    driver.maximize_window()
    driver.find_element_by_name('user').send_keys('18225516235')
    driver.find_element_by_name('password').send_keys('utt.123456')


    # 找到滑块span
    need_move_span = driver.find_element_by_xpath('//*[@id="slider"]/div[4]')
    # 模拟按住鼠标左键
    ActionChains(driver).click_and_hold(need_move_span).perform()
    for x in tracks: # 模拟人的拖动轨迹
        print(x)
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=random.randint(1,3)).perform()
    time.sleep(1)
    ActionChains(driver).release().perform() # 释放左键

    driver.find_element_by_id('btn').click()
    time.sleep(2)
    nowurl = driver.current_url
    if 'index.html' in nowurl:
        print('登录成功')
    else:
        raise Exception('未登录成功')


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
      a = 1000 # 加速运动
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


if __name__ == '__main__':
  move_to_gap(get_track(350))