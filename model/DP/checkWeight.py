from pymongo import MongoClient
import math
import unittest


class check_weight(unittest.TestCase):

    def setUp(self):
        # self.client = MongoClient('192.168.1.79', 27017, connect=False)  # 防止出现no servers found yet错误
        self.client = MongoClient('120.27.198.114', 27017, connect=False)  # 防止出现no servers found yet错误
        db = self.client.LdxSmart
        db.authenticate("ldxsmart", "KDBund0905")
        self.packageItem = db.packageItem
        self.packageItemDetail = db.packageItemDetail
        self.accountInfo = db.accountInfo
        self.waybill = 2018110120

    #   检查台湾面单的收货重量和口岸重量是否正常
    def check_tw_weight(self):
        for i in range(0, 12):
            waybill = str(self.waybill)
            delivery_weight = self.packageItem.find_one({'waybill_no': waybill})['delivery_weight']
            port_weight = self.packageItem.find_one({'waybill_no': waybill})['port_weight']
            waybill_id = self.packageItem.find_one({'waybill_no': waybill})['_id']

            if delivery_weight == port_weight:
                print(waybill + u'packageItem表中收货重量和口岸重量相同')
            else:
                print(waybill + u'packageItem表中收货重量和口岸重量ERROR')

            pt_port_weight = self.packageItemDetail.find_one({'waybill_id': waybill_id})['port_weight']
            pt_delivery_weight = self.packageItemDetail.find_one({'waybill_id': waybill_id})['delivery_weight']

            if pt_port_weight == pt_delivery_weight:
                print(waybill + u'子单表中收货重量和口岸重量相同')
            else:
                print(waybill + u'子单表中收货重量和口岸重量ERROR')

            account_weight = self.accountInfo.find_one({'waybill_id': waybill_id})['account_weight']
            if pt_port_weight == account_weight:
                print(waybill + u'account_weight正常')
            else:
                print(waybill + u'account_weight异常')

            print(u'------------------------------------------------------')
            self.waybill += 1

    def test01(self):
        self.check_tw_weight()

    def tearDown(self):
        # self.driver.close()
        print(self.waybill)

if __name__ == '__main__':
        unittest.main()


