# coding:utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support import select
import xlrd
from xlutils.copy import copy

class taiwan_page():

    #定位器
    customerCode_loc = (By.ID, 'f6e783f7-bdfe-44b4-ab88-b99be0d840d2')
    customerName_loc = (By.ID, '9fed341f-01ab-4b61-9541-1f0684c9de7c')
    select_loc = (By.ID, 'e3d3e48a-b723-4584-a867-a1d2754a3a3d')
    upload_loc = (By.ID, '2d84d5c8-5a4b-4a49-944f-e00aa1e7e60eFile')
    menu2_loc = (By.XPATH, '/html/body/div[1]/div[3]/div[1]/div/ul/li[3]/a')
    menu1_loc = (By.XPATH, 'html/body/div[1]/div[1]/div/div[2]/ul/li[4]/a')

    #   打开页面
    def enter(self, driver):
        try:
            driver.find_element(*self.menu1_loc).click()
            time.sleep(3)
            driver.find_element(*self.menu2_loc).click()
            time.sleep(3)
        except Exception as e:
            print e

    #   输入客户名称回车
    def cus_name_enter(self, driver, cus_name):
        try:
            driver.find_element(*self.customerName_loc).send_keys(cus_name)
            driver.find_element(*self.customerName_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    #   输入客户代码回车
    def cus_code_enter(self, driver, cus_code):
        try:
            driver.find_element(*self.customerCode_loc).send_keys(cus_code)
            driver.find_element(*self.customerCode_loc).send_keys(Keys.ENTER)
        except Exception as e:
            print e
        time.sleep(2)

    #   选择模板
    def template_select(self, driver, name):
        try:
            select.Select(driver.find_element(*self.select_loc)).select_by_visible_text(name)
        except Exception as e:
            print e
        time.sleep(2)

    #   上传文件
    def file_upload(self, driver, file_loc):
        try:
            # js = 'document.querySelectorAll("input")[3].style.display="block";'
            js = "var q=document.getElementById(\"2d84d5c8-5a4b-4a49-944f-e00aa1e7e60eFile\");q.style.display=\"block\";"
            driver.execute_script(js)
            driver.find_element(*self.upload_loc).send_keys(file_loc)
        except Exception as e:
            print e
        time.sleep(3)

    #   生成excel文件
    def excel_creat(self):
        try:
            old_excel = xlrd.open_workbook('TWtest3.xls', formatting_info=True)  # 只能用于xls格式
            new_excel = copy(old_excel)
            ws = new_excel.get_sheet(0)
            bill = time.strftime("%Y%m%d", time.localtime())
            line = 1
            for num in range(100, 105):
                waybill = bill + str(num)
                ws.write(line, 0, waybill)
                ws.write(line, 1, waybill)
                line += 1
            new_excel.save('new_TWtest.xls')
        except Exception as e:
            print e
        time.sleep(3)
