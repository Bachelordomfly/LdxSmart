# coding:utf-8
from selenium.webdriver.common.by import By
from model.common.base_page import BasePage
import time

class loginIn(BasePage):
    # 定位器
    name_loc = (By.NAME, 'name')
    passwd_loc = (By.NAME, 'password')
    submit_loc = (By.CSS_SELECTOR, '.btn.btn-primary')
    #退出登陆
    loginout_xpath = (By.XPATH, '/html/body/div[1]/div[1]/div/div[3]/ul/li[3]')
    loginout_css = (By.CSS_SELECTOR, '.icon-logout')

    #   打开页面
    def open(self):
        self._open(self, self.url, self.title)

    #   输入用户名
    def input_name(self, name):
        self.find_element(*self.name_loc).send_keys(name)

    #   输入密码
    def input_passwd(self,passwd):
        self.find_element(*self.passwd_loc).send_keys(passwd)

    #   点击登陆按钮
    def click_submit(self):
        self.find_element(*self.submit_loc).click()

    #   重新登录
    def again_login(self, name, passwd):
        try:
            self.find_element(*self.loginout_xpath).click()
            time.sleep(3)
            self.input_name(name)
            self.input_passwd(passwd)
            self.click_submit()
        except Exception as e:
            print e
            print "重新登录失败"
        time.sleep(5)
        print "重新登录成功"







