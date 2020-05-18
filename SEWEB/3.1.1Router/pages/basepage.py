#! -*-conding:utf-8 -*-
#@Time: 2018/11/28 0028 16:54
#@swzhou
'''
查找元素及输入数据两个子函数
'''

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.CapPic import CapPic
from common.LogGen import LogGen
logger = LogGen(Logger = 'BasePage').getlog()

class BasePage(object):
    def __init__(self,driver,url):
        self.driver = driver
        self.url = url

    def find_element(self,*loc):
        try:
            WebDriverWait(self.driver,10).until(EC.visibility_of_all_elements_located(loc))
            return self.driver.find_element(*loc)
        except:
            CapPic(self.driver)
            logger.info(u"%s 页面中未能找到 %s 元素" % (self,loc))
            self.driver.quit()

    def exist_element(self,*loc):
        return self.driver.find_element(*loc)


    def send_keys(self,loc,vaule,clear_first = True,click_first=True):
        try:
            loc = getattr(self,"%s" % loc)
            if clear_first:
                self.find_element(*loc).click()
            if click_first:
                self.find_element(*loc).clear()
                self.find_element(*loc).send_keys(vaule)
        except AttributeError:
            CapPic(self.driver)
            logger.info(u"%s 页面中未能找到 %s 元素" % (self,loc))
            self.driver.quit()

    def getText_byXpath(self,location,quit=1):
        try:
            return self.driver.find_element_by_xpath(location).text
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getText_byID(self,location,quit=1):
        try:
            return self.driver.find_element_by_id(location).text
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getText_byClass(self,location,quit=1):
        try:
            return self.driver.find_element_by_class_name(location).text
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getText_byName(self,location,quit=1):
        try:
            return self.driver.find_element_by_name(location).text
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def selelement_byName(self,location,quit=1):
        try:
            return self.driver.find_element_by_name(location)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def selelement_byXpath(self,location,quit=1):
        try:
            return self.driver.find_element_by_xpath(location)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def selelement_byID(self,location,quit=1):
        try:
            return self.driver.find_element_by_id(location)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getAttribute_byLink(self,location,attribute,quit=1):
        try:
            return self.driver.find_element_by_link_text(location).get_attribute(attribute)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getAttribute_byName(self,location,attribute,quit=1):
        try:
            return self.driver.find_element_by_name(location).get_attribute(attribute)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getAttribute_byXpath(self,location,attribute,quit=1):
        try:
            return self.driver.find_element_by_xpath(location).get_attribute(attribute)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getAttribute_byId(self,location,attribute,quit=1):
        try:
            return self.driver.find_element_by_id(location).get_attribute(attribute)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()

    def getAttribute_byClass(self,location,attribute,quit=1):
        try:
            return self.driver.find_element_by_class_name(location).get_attribute(attribute)
        except:
            print(u"%s 页面中未能找到 %s 元素" % (self,location))
            if quit ==1:
                self.driver.quit()


    # def find_Noelement(self,*loc):
    #     try:
    #         WebDriverWait(self.driver, 3)
    #         self.find_element(loc)
    #
    #         # WebDriverWait(self.driver,3).until(EC.invisibility_of_element(loc))
    #         # return self.driver.find_element(*loc)
    #         # print (self.driver.find_element(*loc))
    #     except NoSuchElementException:
    #         # CapPic(self.driver)
    #         # logger.info(u"%s 页面中未能找到 %s 元素" % (self.loc))
    #         return  1
    #     else:
    #         return 2




