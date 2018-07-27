# coding:utf-8
__author__ = 'helen'
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
from time import sleep
from model.common import log

'''
project:Ldxsmart登陆页面测试
'''


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url = 'http://192.168.1.79:8080'
        self.name = 'SHTEST'
        self.passwd = 'KD12345678'
        self.title = u'用户登录_EXSOFT'
        self.login_page = loginIn(self.driver, self.url, self.title)
        self.mylog = log.log()
        print "start"


    def test01(self):
        u'''登陆'''
        try:
            try:
                self.driver.get(self.url)
                self.driver.maximize_window()
                # 通过断言输入的title是否在当前title中
                assert self.title in self.driver.title, 'title not same'
            except:
                self.mylog.error(u'未能正确打开页面:' + self.url)
            self.login_page.input_name(self.name)
            self.login_page.input_passwd(self.passwd)
            self.login_page.click_submit()
            sleep(2)
            self.login_page.img_screenshot(u'登陆成功')
        except Exception as e:
            self.login_page.img_screenshot(u'登陆失败')
            raise e
        print "login"

    def test02(self):
        self.driver.find_element_by_link_text('输单').click()
        print "cargo"

    def tearDown(self):
        print "end"
        self.driver.close()

if __name__ == '__main__':
    unittest.main()

