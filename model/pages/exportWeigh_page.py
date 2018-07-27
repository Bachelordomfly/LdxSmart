# coding:utf-8
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class exportWeigh(object):

    menu1_loc = (By.PARTIAL_LINK_TEXT, '出口')
    menu2_loc = (By.LINK_TEXT, '复重')
    waybill_loc = (By.ID, 'e1666a95-8eb1-4dff-85b3-7208377f64af')
    weight_loc = (By.ID, '52c7bf52-0c84-427c-ad43-962fdda7d0b9Value')
    len_loc = (By.NAME, 'ec31691c-0fc1-4967-8b22-9ee21fc90184')
    width_loc = (By.NAME, 'b4bd011a-44b5-4033-9e6c-1c17038f820c')
    height_loc = (By.NAME, 'c19d0fc1-816a-401f-824c-5225f9c188d2')
    save_loc = (By.ID, '6c73196a-c543-48bb-a83e-c1d02bd6c824')

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

    def waybill_enter(self, driver, waybill):
        try:
            driver.find_element(*self.waybill_loc).clear()
            driver.find_element(*self.waybill_loc).send_keys(waybill)
            driver.find_element(*self.waybill_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(3)
        tip1 = u'单号不存在'
        while EC.alert_is_present()(driver):
            result = EC.alert_is_present()(driver)
            if tip1 in result.text:
                result.accept()
                print u'输单查验未成功将单号发出'
                driver.quit()
            else:
                result.accept()
                return

    def weight_change(self, driver):
        try:
            weight = driver.find_element(*self.weight_loc).get_attribute('value')
            driver.find_element(*self.weight_loc).clear()
            we = float(weight) + 2
            driver.find_element(*self.weight_loc).send_keys(str(we))
            print u'子单重量修改为:'+ str(we)
        except Exception as e:
            print e
        time.sleep(2)

    def length_change(self, driver):
        try:
            lenth = driver.find_element(*self.len_loc).get_attribute('value')
            driver.find_element(*self.len_loc).clear()
            l = float(lenth) + 10
            driver.find_element(*self.len_loc).send_keys(str(l))
            print u'子单长度修改为:'+ str(l)
        except Exception as e:
            print e
        time.sleep(2)

    def width_change(self, driver):
        try:
            width = driver.find_element(*self.width_loc).get_attribute('value')
            driver.find_element(*self.width_loc).clear()
            w = float(width) + 10
            driver.find_element(*self.width_loc).send_keys(str(w))
            print u'子单宽度修改为:'+ str(w)
        except Exception as e:
            print e
        time.sleep(2)

    def height_change(self, driver):
        try:
            height = driver.find_element(*self.height_loc).get_attribute('value')
            driver.find_element(*self.height_loc).clear()
            h = float(height) + 10
            driver.find_element(*self.height_loc).send_keys(str(h))
            print u'子单高度修改为:'+ str(h)
        except Exception as e:
            print e
        time.sleep(2)

    def save_click(self, driver):
        try:
            driver.find_element(*self.save_loc).click()
            print "出口复重成功"
        except Exception as e:
            print e
        time.sleep(5)
