# coding:utf-8
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import select
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC


class szpackage(object):
    menu1_loc = (By.PARTIAL_LINK_TEXT, '出口')
    menu2_loc = (By.LINK_TEXT, 'SZ航空打包')
    mawb_loc = (By.ID, '26ba3fed-5556-4300-8596-8cb937292dba')          # 主单号
    flight_loc = (By.ID, '26fd6b30-5f1d-4a94-9511-24e3118e1aad')        # 航班选择
    flight_no_loc = (By.ID, '071414b7-2747-4981-978f-d7eead23761c')     # 航班号
    departure_port_loc = (By.ID, '171da0c9-833b-4fbb-9ce9-600c4e901d28')  # 始发港
    destination_port_loc = (By.ID, '9e522506-fbd6-4358-956c-616835a44693')  # 目的港
    mawb_remark_loc = (By.ID, '229a88b1-5513-415c-8106-b0178036ac35')   # 主单备注
    auto_mark_loc = (By.ID, '96c48840-f056-48ff-b648-1cffb3e2f15f')     # 自动袋号
    sub_waybill_loc = (By.ID, 'ee5b47f5-0286-4194-9ddd-e91bfcd50a48')   # 子单号
    waybill_loc = (By.ID, '86ec7e77-9997-4535-ad3d-6e0ca947051a')       # 运单号
    mawb_weight_loc = (By.ID, 'd9a0141f-d368-4dc0-82bc-8654508657f5')   # 主单重量
    mawb_volume_loc = (By.ID, '92b04d17-97e4-4de3-9814-32b92835b4f1')   # 主单体积
    mawb_ticket_loc = (By.ID, '88bcec38-4e46-4330-9c44-3a3c24f5308d')   # 主单票数
    mawb_pieces_loc = (By.ID, '85c3a520-5c0a-4a2e-9d76-17bc1d16fdaa')   # 主单件数
    mawb_bag_loc = (By.ID, '43623670-d06c-4b82-93bd-942747c18dbf')      # 主单袋数
    weight_total = (By.ID, '6bcb9ee9-48ae-410f-aad6-a17ab06a5005')      # 重量合计
    pieces_total = (By.ID, '42bed7e6-64fa-4076-ab6e-81fcd5a31025')      # 件数合计

    def enter(self, driver):
        try:
            driver.find_element(*self.menu1_loc).click()
        except Exception as e:
            print e
        time.sleep(3)
        try:
            driver.find_element(*self.menu2_loc).click()
        except Exception as e:
            print e
        time.sleep(5)

    def mawb_enter(self, driver, mawb):
        try:
            driver.find_element(*self.mawb_loc).send_keys(mawb)
            driver.find_element(*self.mawb_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(3)

    def flight_select(self, driver, flight_no):
        try:
            select.Select(driver.find_element(*self.flight_loc)).select_by_visible_text(flight_no)
        except Exception as e:
            print e
        time.sleep(3)
        #   检查航空编号、始发港、目的港是否已自动填入值
        try:
            flight_no = driver.find_element(*self.flight_no_loc).get_attribute('value')
            departure_port = driver.find_element(*self.departure_port_loc).get_attribute('value')
            destination_port = driver.find_element(*self.destination_port_loc).get_attribute('value')
            if flight_no != u'' and departure_port != u'' and destination_port != u'':
                print u'航班选择正常'
            else:
                return
        except Exception as e:
            print e
        time.sleep(3)

    def automatic_bag_select(self, driver):
        try:
            driver.find_element(*self.auto_mark_loc).click()
        except Exception as e:
            print e
        time.sleep(3)

    def subWaybill_input(self, driver, waybill):
        client = MongoClient('192.168.1.79', 27017, connect=False)
        db = client.LdxSmart
        collection = db.packageItem
        package_item_detail = db.packageItemDetail
        waybill_id = collection.find_one({'waybill_no': waybill})['_id']
        sub_waybillNo = package_item_detail.find_one({'waybill_id': waybill_id})['sub_waybillNo']
        try:
            driver.find_element(*self.sub_waybill_loc).send_keys(sub_waybillNo)
            driver.find_element(*self.sub_waybill_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(3)
        while EC.alert_is_present()(driver):
            result = EC.alert_is_present()(driver)
            print result.text
            result.accept()

    def waybill_input(self, driver, waybill):
        try:
            driver.find_element(*self.waybill_loc).send_keys(waybill)
            driver.find_element(*self.waybill_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(3)









