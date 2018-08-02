# coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import select
from pymongo import MongoClient
import requests

class subInput(object):

    #   收货输单页页面元素及方法

    waybill_loc = (By.ID, '821c5dc7-da26-4334-9e05-25f708cd81be')          # 单号
    submit_loc = (By.ID, '0e5691db-9146-42b2-99d6-92d42fd7d19f')           # 保存
    menu1_loc = (By.PARTIAL_LINK_TEXT, '收货段')                            # 页面
    menu2_loc = (By.LINK_TEXT, '输单')
    senderTel_loc = (By.ID, '18049887-a8d4-4565-8d2d-ae7716bdcabf')        # 发件人电话
    sender_loc = (By.ID, '5e795861-80be-4372-b5a6-1ab9376b65af')           # 发件联系人
    receiveTel_loc = (By.ID, '3ed3974f-9b08-436b-ab9e-e4aa5af3255e')       # 收件人电话
    receiver_loc = (By.ID, '3ed3974f-9b08-436b-ab9e-e4aa5af3255e')         # 收件联系人
    rezipcode_loc = (By.ID, '579dcd71-e837-4298-aa37-b59ded929156')        # 收件邮编
    addGoods_loc = (By.ID, 'ded37947-3b50-4ea0-930d-56b6e02b6572Add')      # 添加商品信息
    customerCode_loc = (By.ID, '584fcce3-a6fd-4eeb-b27e-9a95c0ddf35d')     # 客户代码
    customerName_loc = (By.ID, '87f8dc80-fe3e-4240-9f3d-3845b3872ca4')     # 客户名称
    receiverCountry_loc = (By.ID, '12a3f4fe-5292-408a-a0be-47b7e97fd852')  # 收件国家地区
    product_loc = (By.ID, '8a8e5a2b-6fa8-457b-b2cb-5a8b10e71a7f')          # 产品

    # 打开页面
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
        time.sleep(3)

    # 输入单号,回车
    def waybill_enter(self, driver, waybill):
        try:
            driver.find_element(*self.waybill_loc).clear()
            driver.find_element(*self.waybill_loc).send_keys(waybill)
            driver.find_element(*self.waybill_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    # 选择产品
    def product_select(self, driver, product):
        try:
            select.Select(driver.find_element(*self.product_loc)).select_by_visible_text(product)
        except Exception as e:
            print e
        time.sleep(1)

    # 输入发件人电话,回车
    def sender_tel_enter(self, driver, tel):
        try:
            driver.find_element(*self.senderTel_loc).clear()
            driver.find_element(*self.senderTel_loc).send_keys(tel)
            driver.find_element(*self.senderTel_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    # 输入收件人电话,回车
    def receiver_tel_enter(self, driver, tel):
        try:
            driver.find_element(*self.receiver_loc).clear()
            driver.find_element(*self.receiver_loc).send_keys(tel)
            driver.find_element(*self.receiver_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    # 点击保存
    def save_click(self, driver):
        try:
            driver.find_element(*self.submit_loc).click()
        except Exception as e:
            print e
        time.sleep(3)

    # 填入客户代码
    def customer_code_enter(self, driver, code):
        try:
            driver.find_element(*self.customerCode_loc).clear()
            driver.find_element(*self.customerCode_loc).send_keys(code)
            driver.find_element(*self.customerCode_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    # 填入收件人邮编并回车
    def zipcode_enter(self, driver, zipcode):
        try:
            driver.find_element(*self.rezipcode_loc).clear()
            driver.find_element(*self.rezipcode_loc).send_keys(zipcode)
            driver.find_element(*self.rezipcode_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(4)

    # 选择收件人国家地区
    def receiver_country_select(self, driver, country):
        try:
            select.Select(driver.find_element(*self.receiverCountry_loc)).select_by_visible_text(country)
        except Exception as e:
            print e
        time.sleep(1)

    #   判断单号输入框是否为空
    def waybill_is_null(self, driver):
        value = driver.find_element(*self.waybill_loc).get_attribute('value')
        if value.strip():
            return True
        else:
            return False

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
    # 判断配送服务是否正确
    def service_is_correct(self, waybill):
        client = MongoClient('192.168.1.79', 27017, connect=False)
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
            distribute_service_name = service_item.find_one({'_id': distribute_service_id})['name']  # 单号已保存的配送服务
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

            #   产品的默认配送服务
            product_id = collection.find_one({'waybill_no': waybill})['product_id']
            default_distribute_service_id = product_info.find_one({'_id': product_id})['default_distribution_service']
            default_distribute_service_name = service_item.find_one({'_id': default_distribute_service_id})['name']

            #   配送服务为黑猫宅急便,不修改配送服务
            if default_distribute_service_name == u'黑猫宅急便' :
                self.correct_service_name = default_distribute_service_name    # 正确的配送服务
                if distribute_service_name == self.correct_service_name:
                    return True
                else:
                    return False
            #   配送服务不为黑猫宅急便,且航空服务为东京方向,若是佐川超标件则改为西浓混载,否则改为佐川
            elif flight_service_name == u'东京方向':
                #   判断是否为佐川超标货
                if sum_length > 250 or weight > 45 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'
                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = u'佐川'
                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False
            #   配送服务不为黑猫宅急便,且航空服务为大阪方向,若是黑猫超标件则改为西浓混载,否则改为YGX
            elif flight_service_name == u'大阪方向':
                #   判断是否为黑猫超标件
                if sum_length > 160 or weight > 25 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'

                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = u'YGX'

                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False
            #   配送服务不为黑猫宅急便,且航空服务不为东京方向或大阪方向,若是黑猫超标件则改为西浓混载,否则不修改配送服务
            else:
                #   判断是否为黑猫超标件
                if sum_length > 160 or weight > 25 or cargo_type == 3:
                    self.correct_service_name = u'西浓混载'

                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False
                else:
                    self.correct_service_name = default_distribute_service_name
                    if distribute_service_name == self.correct_service_name:
                        return True
                    else:
                        return False

        except Exception as e:
            print e

    '''
    project:
    供应商：

    ILyang：

    6位 邮编 包含 “-” 706-190	　
    http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=706-190	结果	(邮编|派送点名|派送点代码)
    5位 没有“-” 17039	　
    http://www.ilyanglogis.com/functionality/zip_search_code.asp?zipcd=17039

    YGX国际黑猫：根据邮编和供应商ID取出deliveryInfo表中对应的deliveryCode字段(取后六位)

    老黑猫：根据邮编和供应商ID取出deliveryInfo表中对应的deliveryCode字段(取后六位)

    佐川：根据邮编和供应商ID取出deliveryInfo表中对应的deliveryCode字段

    '''
    # 检查输单后的分拣码是否正确
    def delivery_is_error(self, zipcode, waybillNo):
        client = MongoClient('192.168.1.79', 27017, connect=False)  # 防止出现no servers found yet错误
        db = client.LdxSmart
        package_item = db.packageItem
        account_info = db.accountInfo
        service_item = db.serviceItem
        delivery_info = db.deliveryInfo
        vendor = db.vendor
        # 当前已保存的分拣码
        now_code = package_item.find_one({'waybill_no': waybillNo})['branch_code']

        # 正确的分拣码
        waybill_id = package_item.find_one({'waybill_no': waybillNo})['_id']
        distribution_service = account_info.find_one({'waybill_id': waybill_id})['distribution_service']
        vendor_id = service_item.find_one({'_id': distribution_service})['vendor_id']
        try:
            delivery_code = u''
            delivery_code = delivery_info.find_one({'vendor_id': vendor_id, 'zipcode': zipcode})['delivery_code']
        except Exception as e:
            print e

        # 如果供应商为YGX,则分拣码取后五位
        vendor_name = vendor.find_one({'_id': vendor_id})['name']
        if vendor_name == u'YGX国际黑猫':
            code = delivery_code[-6:]
            if now_code == code:
                print waybillNo+u'YGX分拣码获取正确'
                return 1
            else:
                return 0
        elif vendor_name == u'老黑猫':
            code = delivery_code[-6:]
            if now_code == code:
                print waybillNo+u'老黑猫分拣码获取正确'
                return 1
            else:
                return 0
        elif vendor_name == u'佐川':
            code = delivery_code
            if now_code == code:
                print waybillNo+u'佐川分拣码获取正确'
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
                    print waybillNo+u'一洋分拣码获取正确'
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
                    print waybillNo+u'一洋分拣码获取正确'
                    return 1
                else:
                    return 0
        else:
            print waybillNo+u'台湾分拣码不做校验'
            return 2




