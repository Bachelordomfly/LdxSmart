# coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select
from selenium.webdriver.support.wait import WebDriverWait
from pymongo import MongoClient
import math

class getCargo():
    # 定位器
    customerCode_loc = (By.ID, 'be9c632f-c631-4987-8d6b-0470100349e1')
    customerName_loc = (By.XPATH, '//*[@id="fba0128d-2891-4ae9-9a94-af626174983c"]')
    customerTip_loc = (By.XPATH, 'html/body/div[3]/ul/li[1]')
    product_loc = (By.ID, '26fb2293-6d35-4e00-8cdd-68d9a37655c7')
    cargoType_loc = (By.ID, '29868025-9473-411a-b1a1-af2614ab6c96')
    waybillNo_loc = (By.ID, 'a33a890d-5626-4379-83c1-bb622f24e757')
    pieces_loc = (By.ID, '04de4690-ee29-4256-a87d-14cb1bd3e2b3')
    remark_loc = (By.ID, '228acf9a-7a59-4b25-8083-9d680bf8cd30')
    save_loc = (By.ID, '8efb2576-7bb8-4af6-b7db-02b19a3db488')
    weight_loc = (By.NAME, '24e628fa-f288-4424-8635-2d393ae529af')
    allweight_loc = (By.ID, '469b31cc-046f-4842-b82d-b2e725b5520a')
    preweight_loc = (By.ID, 'a643fade-6279-412c-9930-7bf52d4a6687')
    flightService_loc = (By.ID, '0ca0917a-d1bf-4e49-b7c0-7224f60081f5')
    menu1_loc = (By.PARTIAL_LINK_TEXT, '收货段')
    menu2_loc = (By.LINK_TEXT, '收货')
    table_loc = (By.ID, '07f19511-22e8-4579-824f-ec06d98ad514-non-body')

    def __init__(self):
        self.client = MongoClient('192.168.1.79', 27017, connect=False)  # 防止出现no servers found yet错误
        db = self.client.LdxSmart
        self.packageItem = db.packageItem
        self.productInfo = db.productInfo
        self.productCustomer = db.productCustomer
        self.freightInfo = db.freightInfo
        self.accountInfo = db.accountInfo
        self.charging = db.charging
        self.productCustomer = db.productCustomer
        self.freightInfo = db.freightInfo

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
        time.sleep(3)

    #   输入客户代码回车
    def cus_code_enter(self, driver, cus_code):
        try:
            driver.find_element(*self.customerCode_loc).clear()
            driver.find_element(*self.customerCode_loc).send_keys(cus_code)
            time.sleep(2)
        except Exception as e:
            print e
        driver.find_element(*self.customerCode_loc).send_keys(Keys.ENTER)
        time.sleep(2)

    #   输入客户名称回车
    def cus_name_enter(self, driver, cus_name):
        try:
            driver.find_element(*self.customerName_loc).clear()
            driver.find_element(*self.customerName_loc).send_keys(cus_name)
        except Exception as ms:
            print ms
        time.sleep(2)
        driver.find_element(*self.customerName_loc).send_keys(Keys.ENTER)
        time.sleep(2)

    #   输入客户代码,悬浮3秒,选择客户
    def cus_code_move(self, driver, cus_code):
        driver.find_element(*self.customerCode_loc).send_keys(cus_code)
        time.sleep(1)
        driver.find_element(*self.customerCode_loc).click()
        time.sleep(1)
        try:
            ActionChains(driver).move_to_element(*self.customerCode_loc).perform()
            time.sleep(3)
            select.Select(driver.find_element(*self.customerTip_loc)).select_by_index(0)
        except:
            print '客户列表未出现'

    #   选择产品
    def product_select(self, driver, index):
        try:
            select.Select(driver.find_element(*self.product_loc)).select_by_index(index)
        except Exception as e:
            print e
        time.sleep(2)

    #   选择货物类型
    def cargotype_select(self, driver, cargoType):
        try:
            select.Select(driver.find_element(*self.cargoType_loc)).select_by_visible_text(cargoType)
        except Exception as e:
            print e
        time.sleep(2)

    #   选择航空服务
    def flightService_select(self, driver, service):
        try:
            select.Select(driver.find_element(*self.flightService_loc)).select_by_visible_text(service)
        except Exception as e:
            print e
        time.sleep(2)

    #   输入单号回车
    def waybillNo_enter(self,driver, waybillNo):
        try:
            driver.find_element(*self.waybillNo_loc).send_keys(waybillNo)
            print "yes"
        except Exception as e:
            print e
        driver.find_element(*self.waybillNo_loc).send_keys(Keys.ENTER)
        time.sleep(2)

    #   输入件数回车
    def pieces_enter(self, driver, pieces):
        try:
            driver.find_element(*self.pieces_loc).clear()
            driver.find_element(*self.pieces_loc).send_keys(pieces)
        except Exception as e:
            print e
        driver.find_element(*self.pieces_loc).send_keys(Keys.ENTER)
        time.sleep(2)

    #   输入备注
    def remark_write(self, driver, remark):
        try:
            driver.find_element(*self.remark_loc).send_keys(remark)
        except Exception as e:
            print e
        time.sleep(2)

    #   输入子单重量
    def weight_write(self, driver, weight):
        try:
            driver.find_element(*self.weight_loc).clear()
            driver.find_element(*self.weight_loc).send_keys(weight)
        except Exception as e:
            print e
        time.sleep(2)

    #   点击保存
    def save_click(self, driver):
        try:
            driver.find_element(*self.save_loc).click()
        except Exception as e:
            print e
        time.sleep(2)

    #   判断单号输入框是否为空
    def waybill_is_null(self, driver):
        value = driver.find_element(*self.waybillNo_loc).get_attribute('value')
        if value.strip():
            return True
        else:
            return False

    #   判断客户名称是否为空
    def name_is_null(self, driver):
        value = driver.find_element(*self.customerName_loc).get_attribute('value')
        if value.strip():
            return False
        else:
            return True

    #   获取产品名称
    def product_is_null(self, driver):
        value = select.Select(driver.find_element(*self.product_loc)).select_by_value("").text
        if value.strip():
            return False
        else:
            return True

    #   获取货物类型
    def cargo_is_null(self, driver):
        value = driver.find_element(*self.cargoType_loc).verifySelectedValue()
        if value.strip():
            return False
        else:
            return True

    #   获取件数
    def pieces_is_null(self, driver):
        value = driver.find_element(*self.pieces_loc).get_attribute('value')
        if value.strip():
            return False
        else:
            return True

    #   取出总重
    def allweight_is_null(self, driver):
        value = driver.find_element(*self.allweight_loc).get_attribute('value')
        if value.strip():
            return False
        else:
            return True

    #   获取列表行数
    def get_table_row(self, driver):
        try:
            # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
            table_tr_list = driver.find_element(*self.table_loc).find_elements(By.TAG_NAME, "tr")
            time.sleep(3)
            t = 0
            for tr in table_tr_list:
                t += 1
            return t
        except Exception as e:
            print e
        time.sleep(3)

    #   计算运费
    def freight_caculate(self, waybill):
        # 获取当前运费和燃油附加费
        waybill_id = self.packageItem.find_one({'waybill_no': waybill})['_id']
        account_id = self.accountInfo.find_one({'waybill_id': waybill_id})['_id']
        freight = self.charging.find_one({'account_id': account_id, 'item': '运费'})['fee']
        fuel_surcharge = self.charging.find_one({'account_id': account_id, 'item': '燃油附加费'})['fee']

        # 获取正确运费和燃油附加费
        customer_id = self.packageItem.find_one({'waybill_no': waybill})['customer_id']
        product_id = self.packageItem.find_one({'waybill_no': waybill})['product_id']
        try:
            #  产品客户有关联,取产品客户关联id
            product_customer_id = self.productCustomer.find_one({'product_id': product_id,
                                                            'customer_id': customer_id})['_id']
        except Exception as e:
            print e
            #  产品客户无关联,取产品的默认id
            product_customer_id = self.productCustomer.find_one({'product_id': product_id,
                                                            'customer_id': None})['_id']

        # 获取结算重量
        account_weight = self.accountInfo.find_one({'waybill_id': waybill_id})['account_weight']
        # 获取货物类型
        now_cargo_type = self.packageItem.find_one({'waybill_no': waybill})['cargo_type']
        cargo_type = 0  # packageItem中cargo_type值与freightInfo中不一致
        if now_cargo_type == 0:
            cargo_type = 1
        else:
            cargo_type = 2

        #  判断freightInfo中是否有货物类型,若无该值则使用默认报价
        ori = []
        des = []
        try:
            for ori_weight in self.freightInfo.find({'productCustomer_id': product_customer_id,
                                                         'cargo_type': cargo_type})['ori_weight']:
                print ori_weight
                ori.append(ori_weight)
            for des_weight in self.freightInfo.find({'productCustomer_id': product_customer_id,
                                                         'cargo_type': cargo_type})['des_weight']:
                print des_weight
                des.append(des_weight)
        except Exception as e:
            print e
            cargo_type = None
            for ori_weight in self.freightInfo.find({'productCustomer_id': product_customer_id}):
                print ori_weight
                ori.append(ori_weight['ori_weight'])
            for des_weight in self.freightInfo.find({'productCustomer_id': product_customer_id}):
                print des_weight
                des.append(des_weight['des_weight'])

        weight = 0
        continue_weight = 0
        account_type = 0
        first_fee = 0
        price = 0
        for i in range(0, len(ori)):
            if ori[i] < account_weight <= des[i]:
                try:
                    account_type = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                              'ori_weight': ori[i], 'des_weight': des[i]
                                                              })['account_type']  # 结算类型
                    first_fee = self.freightInfo.find_one({'productCustomer_id': product_customer_id, 'account_type': 1,
                                                           'cargo_type': cargo_type})['unit_price']  # 首重价格
                    first_weight = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                              'account_type': 1, 'cargo_type': cargo_type})['des_weight']  # 首重
                    continue_weight = account_weight - first_weight
                except Exception as e:
                    print e

                if account_type == 1:  # 首重
                    if first_fee == freight:
                        return True
                    else:
                        return False

                elif account_type == 2:  # 一倍续重
                    weight = math.ceil(continue_weight)  # 续重部分1倍向上取整
                    continue_price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                              'cargo_type': cargo_type, 'account_type': 2
                                                              })['unit_price']  # 1倍续重单价
                    continue_fee = weight * continue_price  # 续重价格
                    all_fee = first_fee + continue_fee
                    if all_fee == freight:
                        return True
                    else:
                        return False

                elif account_type == 3:  # 0.5倍续重

                    multiple = (continue_weight // 1) / 0.5

                    remainder = continue_weight % 1
                    if remainder <= 0.5:
                        multiple += 1
                    else:
                        multiple += 2

                    continue_price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                            'cargo_type': cargo_type, 'account_type': 3})['unit_price']  # 0.5倍续重单价
                    continue_fee = continue_price * multiple  # 续重价格
                    all_fee = first_fee + continue_fee
                    if all_fee == freight:
                        return True
                    else:
                        return False

                elif account_type == 4:  # 单价
                    weight = math.ceil(account_weight)  # 结算重量1倍向上取整
                    try:
                        price = self.freightInfo.find_one({'productCustomer_id': product_customer_id, 'account_type': 4,
                                                           'cargo_type': cargo_type})['unit_price']  # 单价
                    except Exception as e:
                        print e
                    all_fee = weight * price
                    if all_fee == freight:
                        return True
                    else:
                        return False

                elif account_type == 5:  # 固定价格
                    price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                              'cargo_type': cargo_type, 'account_type': 5
                                                              })['unit_price']  # 固定价格
                    if price == freight:
                        return True
                    else:
                        return False

            else:
                print weight


