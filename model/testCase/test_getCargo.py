# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.pages.getCargo_page import getCargo
from selenium.webdriver.support import expected_conditions as EC
from model.common import log
import random

class get_cargo(unittest.TestCase):

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
        self.gc = getCargo()
        self.waybillNo = u''
        self.mylog = log.log()
        self.cargo_page = getCargo()

    def Login(self):
        # 使用上海站点用户登陆
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

    #   件数回车自动生成子单号输入框检查
    def test_auto_pieces(self):
        self.Login()
        self.cargo_page.enter(self.driver)
        pieces = random.randint(0, 300)
        self.cargo_page.pieces_enter(self.driver, pieces)
        if EC.alert_is_present()(self.driver):
            if pieces > 200 and EC.alert_is_present()(self.driver).text == u'件数的值必须大于等于0小于等于200':
                self.mylog.info(u'件数'+pieces+u'大于200')
            else:
                self.mylog.error(u'pieces'+pieces+u'回车异常' + self.driver.current_url)
        else:
            if self.cargo_page.get_table_row(self.driver) == pieces:
                self.mylog.info(u'件数回车正常'+self.driver.current_url)
            else:
                self.mylog.error(u'pieces'+pieces+u'回车异常' + self.driver.current_url)

    # 自动复制最后一行的重量、长、宽、高功能检查
    def test_copy_attribute(self):
        self.Login()

    #   运费计算检查
    def test_freight_caculate(self):
        self.Login()
        self.gc.enter(self.driver)
        self.waybillNo = time.strftime("%Y%m%d%H%M%S", time.localtime())
        product = random.randint(0, 19)
        cargo = random.randint(0, 3)
        weight = str(random.uniform(0, 50))

        self.gc.enter(self.driver)
        self.gc.cus_name_enter(self.driver, self.cusName)
        self.gc.cus_code_enter(self.driver, self.cusCode)
        self.gc.waybillNo_enter(self.driver, self.waybillNo)
        self.gc.product_select(self.driver, product)
        self.gc.cargotype_select(self.driver, cargo)
        self.gc.weight_write(self.driver, weight)
        self.gc.save_click(self.driver)
        if EC.alert_is_present()(self.driver):
            print u'收货未保存成功,测试停止'
            self.mylog.info(u'收货未保存成功,测试停止')
            self.driver.quit()
        else:
            print u'收货成功'
            if self.gc.freight_caculate(self.waybillNo):
                self.mylog.info(self.waybillNo + u'运费计算正确')
            else:
                self.mylog.error(self.waybillNo + u'运费计算错误')

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()

