# coding:utf-8
from selenium.webdriver.common.by import By
import time
from pymongo import MongoClient
from selenium.webdriver.support import select
from selenium.webdriver.common.keys import Keys


class sort(object):

    menu1_loc = (By.PARTIAL_LINK_TEXT, '出口')
    menu2_loc = (By.LINK_TEXT, '分拣')
    #   应当选择的配送服务名称
    correct_service_name = u''
    service_loc = (By.ID, 'cc525272-1db6-4a74-af71-882b5fcd2878')
    send_loc = (By.ID, '86156150-856f-4c4f-98e9-7b9d14b40a40')

    #   打开页面
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
        time.sleep(8)

    #   判断配送服务是否正确
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

    #   选择正确的配送服务
    def service_select(self, driver, waybill):

        judge = self.service_is_correct(waybill)
        if judge:
            print u'配送服务正确,不用重新分拣'
            return
        else:
            #   选择正确的配送服务
            try:
                select.Select(driver.find_element(*self.service_loc)).select_by_visible_text(*self.correct_service_name)
            except Exception as e:
                print e
            time.sleep(3)
            #   点击批量确认
            try:
                driver.find_element(*self.send_loc).send_keys(Keys.ENTER)
            except Exception as e:
                print e
            time.sleep(3)
