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
from model.pages.exportWeigh_page import exportWeigh
from model.pages.sorting_page import sort
from model.pages.szPacking_page import szpackage
from model.pages.review_page import review
from model.pages.declare_page import declare
from model.pages.clearance_page import clearance_customs


'''
project:
2、进入收货页面收货(一票一件),单号取当日时间
3、进入输单页面完成输单
4、进入输单查验页面将该单发往上海站点
5、退出登陆
6、使用上海站点用户重新登陆
7、进入出口复重页面对上单进行复重
8、进入打单页面进行打单
9、进入出口货物分拣页面进行分拣
10、进入信息分拣页面修改配送服务
11、进入SH航空打包页面进行打包,发往日本
12、进入审单页面进行审单
13、进入报关页面进行报关
14、退出登陆
15、使用日本站点用户重新登陆
16、进入清关页面对该单清关
17、进入待配送列表页进行配送
18、进入配送状态维护页进行签收
'''

class operateOne(unittest.TestCase):

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
        self.inputCheck = check()
        self.exportWeigh = exportWeigh()
        self.sorting = sort()
        self.mawbNo = time.strftime("%Y%m%d", time.localtime())
        self.szpackage = szpackage()
        self.review = review()
        self.declare = declare()
        self.clearance = clearance_customs()

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
        pieces = "1"
        self.gc.enter(self.driver)
        self.gc.cus_name_enter(self.driver, customer_name)
        self.gc.cus_code_enter(self.driver, customer_code)
        self.gc.waybillNo_enter(self.driver, self.waybillNo)
        self.gc.product_select(self.driver, product)
        self.gc.cargotype_select(self.driver, cargo)
        self.gc.flightService_select(self.driver, service)
        self.gc.weight_write(self.driver, weight)
        self.gc.save_click(self.driver)

        try:
            # 判断是否有弹出框
            result = EC.alert_is_present()(self.driver)
            tip1 = u'客户不存在'
            tip2 = u'信息不可为空'
            tip3 = u'件数应大于0'
            while result:
                if tip2 in result.text:
                    result.accept()
                    # 查找哪个输入框没有值
                    if self.gc.name_is_null(self.driver):
                        self.mylog.error(u'客户名称为空')
                        # 修改客户名称,再次尝试保存
                        self.gc.cus_name_enter(self.driver, customer_name)
                        self.gc.save_click(self.driver)

                    if self.gc.product_is_null(self.driver):
                        self.mylog.error(u'产品为空')
                        # 修改产品,再次尝试保存
                        self.gc.product_select(self.driver, product)
                        self.gc.save_click(self.driver)

                    if self.gc.cargo_is_null(self.driver):
                        self.mylog.error(u'货物类型为空')
                        # 修改货物类型,再次尝试保存
                        self.gc.cargotype_select(self.driver, cargo)
                        self.gc.save_click(self.driver)

                    if self.gc.pieces_is_null(self.driver):
                        self.mylog.error(u'件数为空')
                        # 修改件数,再次尝试保存
                        self.gc.pieces_enter(self.driver, pieces)
                        self.gc.save_click(self.driver)

                    if self.gc.allweight_is_null(self.driver):
                        self.mylog.error(u'总重为空')
                        # 修改重量,再次尝试保存
                        self.gc.weight_write(self.driver, weight)
                        self.gc.save_click(self.driver)

                if tip1 in result.text:
                    result.accept()
                    # 客户选择
                    self.gc.cus_code_move(self.driver, customer_code)

                if tip3 in result.text:
                    result.accept()
                    # 修改件数,再尝试保存
                    self.gc.pieces_enter(self.driver, '1')
                    self.gc.save_click(self.driver)

            else:
                print u'收货成功'

        except Exception as ms:
            print ms
            self.mylog.error(u'收货失败')

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

    def InputCheck(self):
        #   进入输单查验页面将该单发往上海站点
        self.inputCheck.enter(self.driver)
        self.inputCheck.get_table_content(self.driver, self.waybillNo)
        time.sleep(2)
        self.inputCheck.site_select(self.driver, "上海虹桥口岸")
        self.inputCheck.send_click(self.driver)
        try:
            tip1 = u'是否将所选定的订单发送'
            tip2 = u'请选择站点'
            while EC.alert_is_present()(self.driver):  # 弹出框出现
                result = EC.alert_is_present()(self.driver)
                if tip1 in result.text:
                    result.accept()
                    time.sleep(2)
                elif tip2 in result.text:
                    result.accept()
                    self.inputCheck.site_select(self.driver, "上海虹桥口岸")
                    self.inputCheck.send_click(self.driver)
                else:
                    print result.text
                    result.accept()
                    return
        except Exception as e:
            print e

    def LoginAgain(self, name, passwd):
        #   退出登陆,并使用其他站点用户重新登陆
        self.login_page.again_login(name, passwd)

    def ExportWeigh(self):
        #   进入出口复重页面对该单进行复重
        self.exportWeigh.enter(self.driver)
        self.exportWeigh.waybill_enter(self.driver, self.waybillNo)
        self.exportWeigh.weight_change(self.driver)
        self.exportWeigh.length_change(self.driver)
        self.exportWeigh.width_change(self.driver)
        self.exportWeigh.height_change(self.driver)
        self.exportWeigh.save_click(self.driver)

    def Sorting(self):
        #   进入信息分拣页面对该单进行分拣
        self.sorting.enter(self.driver)
        self.sorting.service_select(self.driver, self.waybillNo)

    def SZPackage(self):
        #   进入深圳打包页面对该单进行打包
        self.szpackage.enter(self.driver)
        self.szpackage.mawb_enter(self.driver, self.mawbNo)
        self.szpackage.flight_select(self.driver, u'NH8515')
        self.szpackage.automatic_bag_select(self.driver)
        self.szpackage.subWaybill_input(self.driver, self.waybillNo)
        # self.szpackage.waybill_input(self.driver, self.waybillNo)

    def Review(self):
        #   进入出口审单页面确认该单
        self.review.enter(self.driver)
        self.review.get_table_content(self.driver, self.waybillNo)
        self.review.send_click(self.driver)

    def DeclareCustoms(self):
        self.declare.enter(self.driver)
        self.declare.get_table_content(self.driver, self.waybillNo)
        self.declare.send_click(self.driver)

    def ClearanceCustoms(self):
        self.clearance.enter(self.driver)
        self.clearance.get_table_content(self.driver, self.waybillNo)
        self.clearance.send_click(self.driver)

    def test01(self):
        self.Login()
        self.Cargo()
        self.InputBill()
        self.InputCheck()
        self.LoginAgain("SHTEST", "123456")
        self.ExportWeigh()
        self.Sorting()
        self.SZPackage()
        # self.Review()
        # self.DeclareCustoms()
        # self.LoginAgain("JPuser3", "123456")
        # self.ClearanceCustoms()

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()
