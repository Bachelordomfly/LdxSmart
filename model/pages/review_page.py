# coding:utf-8
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class review(object):

    menu1_loc = (By.LINK_TEXT, '出口')
    menu2_loc = (By.LINK_TEXT, '审单')
    table_loc = (By.ID, 'f22b57d9-7b88-42c9-b2d8-701ac3a315d5-left-body')
    send_loc = (By.ID, '1c9db0d6-ed1f-4cab-b134-d41291c42c1d')

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
                        checkbox_xpath = '//*[@id="f22b57d9-7b88-42c9-b2d8-701ac3a315d5-left-body"]/tbody/tr[' + str(i+1) + ']/td[1]/input'
                        driver.find_element(By.XPATH, checkbox_xpath).click()
                        break

                    except Exception as e:
                        print e
            break
        time.sleep(5)

    def send_click(self, driver):
        try:
            driver.find_element(*self.send_loc).send_keys(Keys.ENTER)
            # WebDriverWait(driver, 10).until(EC.element_to_be_clickable(*self.send_loc)).click()
        except Exception as e:
            print e
        time.sleep(5)
        tip1 = u'存在未打包记录'
        while EC.alert_is_present()(driver):
            result = EC.alert_is_present()(driver)
            if tip1 in result.text:
                result.accept()
                print result.text
                return
            else:
                print result.text
                return
        print "出口审单确认成功"

