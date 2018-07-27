# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.pages.getCargo_page import getCargo
from selenium.webdriver.support import expected_conditions as EC
from model.common import log
from model.pages.inputBill_page import subInput

class input_order(unittest.TestCase):

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
        self.inputBill = subInput()
        self.mylog = log.log()

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

    def Cargo(self, product):
        #   进入收货页面收货(一票一件), 单号取当日时间
        self.waybillNo = time.strftime("%Y%m%d%H%M%S", time.localtime())
        cargo = "包裹"
        weight = "2"
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

    def InputBill(self, zipcode, country):
        #   进入输单页面完成输单
        sender_tel = "18146615611"
        receiver_tel = "13162558525"
        self.inputBill.enter(self.driver)
        self.inputBill.waybill_enter(self.driver, self.waybillNo)
        self.inputBill.sender_tel_enter(self.driver, sender_tel)
        self.inputBill.receiver_tel_enter(self.driver, receiver_tel)
        self.inputBill.receiver_country_select(self.driver, country)
        self.inputBill.zipcode_enter(self.driver, zipcode)
        self.inputBill.save_click(self.driver)
        if EC.alert_is_present()(self.driver):
            self.mylog.info(u'收货未保存成功,测试停止')
            self.driver.quit()
        else:

            if self.inputBill.delivery_is_error(zipcode, self.waybillNo) == 0:
                self.mylog.info(self.waybillNo + u'分拣码获取错误')
            elif self.inputBill.delivery_is_error(zipcode, self.waybillNo) == 1:
                self.mylog.info(self.waybillNo + u'分拣码获取正确')
            else:
                self.mylog.info(self.waybillNo + u'台湾分拣码不做校验')

            if country == u'日本':
                if self.inputBill.service_is_correct(self.waybillNo):
                    self.mylog.info(self.waybillNo + u'输单配送服务选择正确')
                else:
                    self.mylog.info(self.waybillNo + u'输单配送服务选择错误')
            else:
                self.mylog.info(self.waybillNo + u'韩国线不校验配送服务')

    def LoginAgain(self, name, passwd):
        #   退出登陆,并使用其他站点用户重新登陆
        self.login_page.again_login(name, passwd)

    def test_destribute_service(self):
        #   输单自动分拣逻辑查验
        self.Login()
        country = u'日本'
        product = ["日本今发明至", "日本今发后至商业件"]
        for p in product:
            zipcode = ["0700000", "0900000", "6000000", "8000000", "0500000"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i, country)
                self.LoginAgain(self.name, self.passwd)

    def test_delivery_code(self):
        self.Login()
        # 日本线分拣码检查
        product1 = ["日本今发明至", "日本今发后至商业件"]
        for p in product1:
            country = u'日本'
            zipcode = ["0700000", "0900000", "6000000", "8000000", "0500000"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i, country)
                self.LoginAgain(self.name, self.passwd)
        # 韩国线分拣码检查
        product2 = ["LDX韩国专线", "韩国海运"]
        for p in product2:
            country = u'韩国'
            zipcode = ["100021", "30101", "38615", "44692", "28156"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i, country)
                self.LoginAgain(self.name, self.passwd)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
