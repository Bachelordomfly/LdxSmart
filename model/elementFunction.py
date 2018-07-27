#-*- coding: UTF-8 -*-
import time
from selenium.webdriver.support import select
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class elementFunction(object):

    #清空输入框,根据name定位发送文本
    def send_element_by_name(self, driver, name, key):
        driver.find_element_by_name(name).clear()
        return driver.find_element_by_name(name).send_keys(key)

    #清空输入框,根据value定位发送文本
    def send_element_by_value(self, driver, value, key):
        driver.find_element_by_value(value).clear()
        return driver.find_element_by_value(value).send_keys(key)

    #清空输入框,根据xpath定位发送文本
    def send_element_by_xpath(self, driver, xpath, key):
        driver.find_element_by_xpath(xpath).clear()
        return driver.find_element_by_xpath(xpath).send_keys(key)

    #清空输入框,根据css定位发送文本
    def send_element_by_css(self, driver, css, key):
        driver.find_element_by_css_selector(css).clear()
        return driver.find_element_by_css_selector(css).send_keys(key)

    #清空输入框,根据id定位发送文本
    def send_element_by_id(self, driver, id, key):

        driver.find_element_by_id(id).clear()
        return driver.find_element_by_id(id).send_keys(key)

    # def clear_element_by_name(self,driver,name):
    #     return driver.find_element_by_name(name).clear()

    # def clear_element_by_value(self,driver,value):
    #     return driver.find_element_by_name(value).clear()

    # def clear_element_by_id(self,driver,id):
    #     return driver.find_element_by_id(id).clear()

    # def clear_element_by_xpath(self,driver,xpath):
    #     return driver.find_element_by_name(xpath).clear()

    # def clear_element_by_css(self,driver,css):
    #     return driver.find_element_by_css_selector(css).clear()

    # 根据name定位点击
    def click_element_by_name(self, driver, name):
        return driver.find_element_by_name(name).click()

    # 根据value定位点击
    def click_element_by_value(self, driver, value):
        return driver.find_element_by_name(value).click()

    # 根据id定位点击
    def click_element_by_id(self, driver, id):
        return driver.find_element_by_id(id).click()

    # 根据xpath定位点击
    def click_element_by_xpath(self, driver, xpath):
        return driver.find_element_by_name(xpath).click()

    # 根据css定位点击
    def click_element_by_css(self, driver, css):
        return driver.find_element_by_css_selector(css).click()
