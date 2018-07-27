# coding:utf-8
import unittest
from selenium import webdriver
from model.pages.login_page import loginIn
import time
from model.pages.getCargo_page import getCargo
from selenium.webdriver.support import expected_conditions as EC
from model.common import log
from model.pages.inputBill_page import subInput
from pymongo import MongoClient
import requests


'''
project:
分拣码检查(除台湾)
被检查的配送服务为:YGX、黑猫、一洋、佐川
1、使用上海用户登陆
2、进入收货页面收货
3、进入输单页面输单保存
'''

class input_deliveryCode(unittest.TestCase):

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
        cargo = "文件"
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
            self.mylog.info(u'收货成功')
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
            print u'输单未保存成功'
            self.mylog.info(u'输单未保存成功')
            self.driver.quit()
        else:
            if self.delivery_is_error(zipcode) == 0:
                self.mylog.info(self.waybillNo+u'分拣码获取错误')
                print u'分拣码获取错误'
            if self.delivery_is_error(zipcode) == 1:
                self.mylog.info(self.waybillNo+u'分拣码获取正确')
                print u'分拣码获取正确'
            else:
                self.mylog.info(self.waybillNo+u'台湾分拣码不做校验')
                print u'台湾分拣码不做校验'

    #   检查输单后的分拣码是否正确
    def delivery_is_error(self, zipcode):
        client = MongoClient('192.168.1.168', 27017, connect=False)  # 防止出现no servers found yet错误
        db = client.LdxSmart
        package_item = db.packageItem
        account_info = db.accountInfo
        service_item = db.serviceItem
        delivery_info = db.deliveryInfo
        vendor = db.vendor
        # 当前已保存的分拣码
        now_code = package_item.find_one({'waybill_no': self.waybillNo})['branch_code']

        # 正确的分拣码
        waybill_id = package_item.find_one({'waybill_no': self.waybillNo})['_id']
        distribution_service = account_info.find_one({'waybill_id': waybill_id})['distribution_service']
        vendor_id = service_item.find_one({'_id': distribution_service})['vendor_id']
        delivery_code = delivery_info.find_one({'vendor_id': vendor_id, 'zipcode': zipcode})['delivery_code']

        # 如果供应商为YGX,则分拣码取后五位
        vendor_name = vendor.find_one({'_id': vendor_id})['name']
        if vendor_name == u'YGX国际黑猫':
            code = delivery_code[-6:]
            if now_code == code:
                self.mylog.info(self.waybillNo+u'YGX分拣码获取正确')
                print self.waybillNo+u'YGX分拣码获取正确'
                return 1
            else:
                return 0
        elif vendor_name == u'老黑猫':
            code = delivery_code[-6:]
            if now_code == code:
                self.mylog.info(self.waybillNo+u'老黑猫分拣码获取正确')
                print self.waybillNo+u'老黑猫分拣码获取正确'
                return 1
            else:
                return 0
        elif vendor_name == u'佐川':
            code = delivery_code
            if now_code == code:
                self.mylog.info(self.waybillNo+u'佐川分拣码获取正确')
                print self.waybillNo+u'佐川分拣码获取正确'
                return 1
            else:
                return 0
        elif vendor_name == u'一洋配送':
            count = len(zipcode)
            if count == 6:
                zcode = zipcode[-6:-3]+u'-'+zipcode[-3:]
                url = 'http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=' + str(zcode)
                html = requests.get(url)
                t = html.text
                strlist = t.split('|')
                tip = []
                for value in strlist:  # 循环输出列表值
                    tip.append(value)
                if now_code == tip[2]:
                    self.mylog.info(self.waybillNo + u'一洋分拣码获取正确')
                    print self.waybillNo+u'一洋分拣码获取正确'
                    return 1
                else:
                    return 0
            elif count == 5:
                url = 'http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=' + str(zipcode)
                html = requests.get(url)
                t = html.text
                strlist = t.split('|')
                tip = []
                for value in strlist:  # 循环输出列表值
                    tip.append(value)
                if now_code == tip[2]:
                    self.mylog.info(self.waybillNo + u'一洋分拣码获取正确')
                    print self.waybillNo+u'一洋分拣码获取正确'
                    return 1
                else:
                    return 0
        else:
            self.mylog.info(self.waybillNo + vendor_name + u'台湾分拣码不做校验')
            print self.waybillNo+u'台湾分拣码不做校验'
            return 2

    def LoginAgain(self, name, passwd):
        #   退出登陆,并使用其他站点用户重新登陆
        self.login_page.again_login(name, passwd)

    def test01(self):
        self.Login()
        # 日本线分拣码检查
        product1 = ["日本今发明至", "日本今发后至商业件"]
        for p in product1:
            zipcode = ["0700000", "0900000", "6000000", "8000000", "0500000"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i)
                self.LoginAgain(self.name, self.passwd)
        # 韩国线分拣码检查
        product2 = ["LDX韩国专线", "韩国海运"]
        for p in product2:
            zipcode = ["100021", "30101", "38615", "44692", "28156"]
            for i in zipcode:
                self.Cargo(p)
                self.InputBill(i)
                self.LoginAgain(self.name, self.passwd)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()

