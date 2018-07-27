# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.pages.getCargo_page import getCargo
from selenium.webdriver.support import expected_conditions as EC
from model.common import log
from model.pages.inputBill_page import subInput

'''
project:
输单页弹出框检查
'''

class input_arlert(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.url = 'http://192.168.1.79:8080'
        self.name = 'SZCR'
        self.passwd = '123456'
        self.title = u'用户登录_EXSOFT'
        self.login_page = loginIn(self.driver, self.url, self.title)
        self.cusCode = u'HQ082'
        self.cusName = u'HQ082_name'
        self.mylog = log.log()
        self.gc = getCargo()
        self.waybillNo = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.inputBill = subInput()

    def Login(self):
        # 使用深圳站点用户登陆
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

    def Cargo(self):
        #   进入收货页面收货(一票一件), 单号取当日时间
        customer_name = "S-SHAPER CO LTD"
        customer_code = "SZXALMY"
        product = "日本今发明至"
        cargo = "文件"
        service = "CQ1122"
        weight = "2"
        self.gc.enter(self.driver)
        self.gc.cus_name_enter(self.driver, customer_name)
        self.gc.cus_code_enter(self.driver, customer_code)
        self.gc.waybillNo_enter(self.driver, self.waybillNo)
        self.gc.product_select(self.driver, product)
        self.gc.cargotype_select(self.driver, cargo)
        self.gc.flightService_select(self.driver, service)
        self.gc.weight_write(self.driver, weight)
        self.gc.save_click(self.driver)
        if EC.alert_is_present()(self.driver):
            print u'收货未成功,测试停止'
            self.driver.quit()

    def InputBill(self):
        #   进入输单页面完成输单
        sender_tel = "4865094"
        receiver_tel = "0354335650"
        self.inputBill.enter(self.driver)
        self.inputBill.waybill_enter(self.driver, self.waybillNo)
        self.inputBill.sender_tel_enter(self.driver, sender_tel)
        self.inputBill.receiver_tel_enter(self.driver, receiver_tel)
        self.inputBill.save_click(self.driver)
        self.alert_ispresent()

    def alert_ispresent(self):
        try:
            sender_tel = ["4865094", "59522106543", "6184256", "75589602460"]
            receiver_tel = ["0354335650", "8049827182", "9031603221", "HASHIMOTO KOUICHI"]
            customer_code = "SZXALMY"
            tip1 = u'客户不存在'
            tip2 = u'信息不可为空'
            index = -1
            # arr_len = 0
            if len(sender_tel) > len(receiver_tel):
                arr_len = len(receiver_tel)
            else:
                arr_len = len(sender_tel)
            # 如果弹框存在，则执行以下代码
            while EC.alert_is_present()(self.driver):
                result = EC.alert_is_present()(self.driver)
                if tip1 in result.text:
                    # 弹出框显示tip1
                    result.accept()  # 关闭弹出框
                    self.inputBill.customerCode_loc(self.driver, customer_code)  # 修改客户代码
                    self.inputBill.save_click(self.driver)  # 再进行保存

                elif tip2 in result.text:
                    # 弹出框显示tip2
                    index += 1
                    if index == arr_len:
                        print('都不符合条件，异常情况')
                        return
                    else:
                        result.accept()  # 关闭弹出框
                        sender_tel = sender_tel[index]
                        receiver_tel = receiver_tel[index]

                        self.inputBill.sender_tel_enter(self.driver, sender_tel)  # 修改发件人电话
                        self.inputBill.receiver_tel_enter(self.driver, receiver_tel)  # 修改收件人电话
                        self.inputBill.save_click(self.driver)  # 再进行保存
            # 弹框不存在
            print(u'输单成功')
        except Exception as e:
            print e

    def test01(self):
        self.Login()
        self.Cargo()
        self.InputBill()

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
