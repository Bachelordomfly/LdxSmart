# coding:utf-8
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import select
from selenium.webdriver.common.keys import Keys


class check():
    grid_loc = (By.XPATH, '//*[@id="980ccd2d-faf1-47eb-a6b5-b738340e0855"]/div[1]/div/div[2]')
    #页面
    menu1_loc = (By.PARTIAL_LINK_TEXT, '收货段')
    menu2_loc = (By.LINK_TEXT, '输单查验')
    table_loc = (By.ID, '980ccd2d-faf1-47eb-a6b5-b738340e0855-left-body')
    site_loc = (By.ID, 'c1da30f4-23a5-4f6b-bd15-3608fbefe3fb')
    # send_loc = (By.ID, '65bfe994-a733-4124-998a-f4921f2099db')
    send_loc = (By.XPATH, '//*[@id="65bfe994-a733-4124-998a-f4921f2099db"]')
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
        time.sleep(6)

    def get_table_content(self, driver, queryContent):
        arr = []
        arr1 = []
        try:
            # 按行查询表格的数据，取出的数据是一整行，按空格分隔每一列的数据
            table_tr_list = driver.find_element(*self.table_loc).find_elements(By.TAG_NAME, "tr")
            time.sleep(5)
            for tr in table_tr_list:
                # result = unicode(tr.text, 'GBK').encode('UTF-8')
                arr1 = (tr.text).split(" ")  # 以空格拆分成若干个(个数与列的个数相同)一维列表
                arr.append(arr1)  # 将表格数据组成二维的列表

        except Exception as e:
            print e

        # 循环遍历table数据，确定查询数据的位置
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                if queryContent == arr[i][j]:
                    print("%r坐标为(%r,%r)" % (queryContent, i + 1, j + 1))
                    try:
                        checkbox_xpath = '//*[@id="980ccd2d-faf1-47eb-a6b5-b738340e0855-left-body"]/tbody/tr[' + str(i+1) + ']/td[1]/input'
                        driver.find_element(By.XPATH, checkbox_xpath).click()
                        break

                    except Exception as e:
                        print e
            break
        time.sleep(5)

    def site_select(self, driver, site):
        try:
            select.Select(driver.find_element(*self.site_loc)).select_by_visible_text(site)
        except Exception as e:
            print e
        time.sleep(5)

    def send_click(self, driver):
        try:
            driver.find_element(*self.send_loc).send_keys(Keys.ENTER)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(*self.send_loc)).click()
        except Exception as e:
            print e
        time.sleep(5)
        print "输单查验发送成功"