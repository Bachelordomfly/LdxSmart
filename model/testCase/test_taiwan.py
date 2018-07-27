# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.common import log
from model.pages.twinput_page import taiwan_page

class taiwan(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url = 'http://192.168.1.79:8080'
        self.name = 'SHTEST'
        self.passwd = '123456'
        self.title = u'用户登录_EXSOFT'
        self.login_page = loginIn(self.driver, self.url, self.title)
        self.cusCode = u'HQ082'
        self.cusName = u'HQ082_name'
        self.mylog = log.log()
        self.taiwan_page = taiwan_page()

    def Login(self):
        try:
            self.driver.get(self.url)
            self.driver.maximize_window()
            # 通过断言输入的title是否在当前title中
            assert self.title in self.driver.title, u'title not same'
        except Exception as e:
            self.mylog.error(u'未能正确打开页面:' + self.url)
            print e
        self.login_page.input_name(self.name)
        self.login_page.input_passwd(self.passwd)
        self.login_page.click_submit()
        time.sleep(3)

    def test_taiwan_input(self):
        self.Login()
        self.taiwan_page.enter(self.driver)
        self.taiwan_page.cus_name_enter(self.driver, self.cusName)
        self.taiwan_page.cus_code_enter(self.driver, self.cusCode)
        self.taiwan_page.template_select(self.driver, u'台湾线预录单（尺寸）')
        self.taiwan_page.excel_creat()
        self.taiwan_page.file_upload(self.driver, 'new_TWtest.xls')

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
