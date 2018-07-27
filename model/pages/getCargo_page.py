# coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import select
from selenium.webdriver.support.wait import WebDriverWait



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
            driver.find_element(*self.customerCode_loc).send_keys(cus_code)
            time.sleep(2)
        except Exception as e:
            print e
        driver.find_element(*self.customerCode_loc).send_keys(Keys.ENTER)
        time.sleep(2)

    #   输入客户名称回车
    def cus_name_enter(self, driver, cus_name):
        try:
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
    def product_select(self, driver, product):
        try:
            select.Select(driver.find_element(*self.product_loc)).select_by_visible_text(product)
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



