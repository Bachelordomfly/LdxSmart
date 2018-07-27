# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.pages.getCargo_page import getCargo
from selenium.webdriver.support import expected_conditions as EC
from model.common import log
from model.pages.inputBill_page import subInput
from model.pages.inputCheck_page import check
from pymongo import MongoClient

'''
project:
日本单自动选择配送服务检查
前提:收件国家地区为日本
产品默认配送服务为黑猫宅急便：不修改配送服务
产品默认配送服务非黑猫宅急便：
    航空服务：
        东京方向 ：是佐川超标货，则改为西浓混载，不是则佐川
        大阪方向 ：是黑猫超标货，则改为西浓混载，不是则YGX
        其他或无 ：超标货检查
佐川超标件：三边之和大于250cm或单件超过45KG或货物类型为其它

黑猫超标件：单件超过25KG或存在某一件三边之和大于160cm或货物类型为其它
'''

class input_distributeService(unittest.TestCase):

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
        self.inputCheck = check()
        self.mylog = log.log()

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

    def Cargo(self, product):
        #   进入收货页面收货(一票一件), 单号取当日时间
        self.waybillNo = time.strftime("%Y%m%d%H%M%S", time.localtime())
        # customer_name = "S-SHAPER CO LTD"
        # customer_code = "SZXALMY"
        cargo = "文件"
        # service = "CQ1122"
        weight = "2"
        pieces = "1"
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

    def InputBill(self, zipcode):
        #   进入输单页面完成输单
        sender_tel = "18146615611"
        receiver_tel = "13162558525"
        self.inputBill.enter(self.driver)
        self.inputBill.waybill_enter(self.driver, self.waybillNo)
        self.inputBill.sender_tel_enter(self.driver, sender_tel)
        self.inputBill.receiver_tel_enter(self.driver, receiver_tel)
        self.inputBill.zipcode_enter(self.driver, zipcode)
        self.inputBill.save_click(self.driver)
        if EC.alert_is_present()(self.driver):
            print u'输单未保存成功,测试停止'
            self.mylog.info(u'收货未保存成功,测试停止')
            self.driver.quit()
        else:
            if self.service_is_correct(self.waybillNo):
                print self.waybillNo+u'输单配送服务选择正确'
                self.mylog.info(self.waybillNo+u'输单配送服务选择正确')
            else:
                print self.waybillNo+u'输单配送服务选择错误'
                self.mylog.info(self.waybillNo+u'输单配送服务选择错误')

    def service_is_correct(self, waybill):
        client = MongoClient('192.168.1.168', 27017, connect=False)
        db = client.LdxSmart
        collection = db.packageItem
        account_info = db.accountInfo
        product_info = db.productInfo
        service_item = db.serviceItem
        package_item_detail = db.packageItemDetail
        try:
            #   获取该单号的配送服务和航空服务
            waybill_id = collection.find_one({'waybill_no': waybill})['_id']
            distribute_service_id = account_info.find_one({'waybill_id': waybill_id})['distribution_service']
            distribute_service_name = service_item.find_one({'_id': distribute_service_id})['name']
            flight_service_id = account_info.find_one({'waybill_id': waybill_id})['flight_service']
            flight_service_name = service_item.find_one({'_id': flight_service_id})['name']

            #   获取该单号的长宽高重量
            length = package_item_detail.find_one({'waybill_id': waybill_id})['delivery_length']
            width = package_item_detail.find_one({'waybill_id': waybill_id})['delivery_width']
            height = package_item_detail.find_one({'waybill_id': waybill_id})['delivery_height']
            weight = package_item_detail.find_one({'waybill_id': waybill_id})['delivery_weight']
            sum_length = length + width + height

            #   获取货物类型
            cargo_type = collection.find_one({'waybill_no': waybill})['cargo_type']

            #   数据库已保存的配送服务
            product_id = collection.find_one({'waybill_no': waybill})['product_id']
            default_distribute_service_id = product_info.find_one({'_id': product_id})['default_distribution_service']
            default_distribute_service_name = service_item.find_one({'_id': default_distribute_service_id})['name']

            #   配送服务为黑猫宅急便,不修改配送服务
            if default_distribute_service_name == u'黑猫宅急便' :
                self.correct_service_name = u'黑猫宅急便'

                if distribute_service_name == default_distribute_service_name:
                    return True
                else:
                    return False
            #   配送服务不为黑猫宅急便,且航空服务为东京方向,若是佐川超标件则改为西浓混载,否则改为佐川
            elif flight_service_name == u'东京方向':
                #   判断是否为佐川超标货
                if sum_length > 250 or weight > 45 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'
                    if distribute_service_name == u'西浓混载':
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = u'佐川'
                    if distribute_service_name == u'佐川':
                        return True
                    else:
                        return False
            #   配送服务不为黑猫宅急便,且航空服务为大阪方向,若是黑猫超标件则改为西浓混载,否则改为YGX
            elif flight_service_name == u'大阪方向':
                #   判断是否为黑猫超标件
                if sum_length > 160 or weight > 25 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'

                    if distribute_service_name == u'西浓混载':
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = u'YGX'

                    if distribute_service_name == u'YGX':
                        return True
                    else:
                        return False
            #   配送服务不为黑猫宅急便,且航空服务不为东京方向或大阪方向,若是黑猫超标件则改为西浓混载,否则不修改配送服务
            else:
                #   判断是否为黑猫超标件
                if sum_length > 160 or weight > 25 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'

                    if distribute_service_name == u'西浓混载':
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = default_distribute_service_name

                    if distribute_service_name == default_distribute_service_name:
                        return True
                    else:
                        return False

        except Exception as e:
            print e

    def LoginAgain(self, name, passwd):
        #   退出登陆,并使用其他站点用户重新登陆
        self.login_page.again_login(name, passwd)

    def test01(self):
        self.Login()
        product = ["日本今发明至", "日本今发后至商业件"]
        for p in product:
            zipcode = ["0700000", "0900000", "6000000", "8000000", "0500000"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i)
                self.LoginAgain(self.name, self.passwd)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()

