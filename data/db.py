#coding=utf-8
from pymongo import MongoClient
import re

#建立MongoDB数据库连接
client = MongoClient('192.168.1.168', 27017, connect=False) # 防止出现no servers found yet错误

#连接所需数据库,test为数据库名
db=client.LdxSmart

#连接所用集合，也就是我们通常所说的表，packageItem为表名
collection=db.packageItem

ori = []
des = []
waybill = "20180720002"
freightInfo = db.freightInfo
account = db.accountInfo
productCustomer = db.productCustomer

customer_id = collection.find_one({'waybill_no': waybill})['customer_id']
product_id = collection.find_one({'waybill_no': waybill})['product_id']
product_customer_id = productCustomer.find_one({'product_id': product_id,
                                                     'customer_id': customer_id})['_id']
# print freightInfo.find_one({'productCustomer_id': product_customer_id})['des_weight']


for all in freightInfo.find({'productCustomer_id': product_customer_id}):
    # print all['des_weight']
    des.append(all['des_weight'])
    ori.append(all['ori_weight'])


    for i in range(0, len(ori)):
        try:
            account_type = freightInfo.find_one({'productCustomer_id': product_customer_id,
                                              'ori_weight': ori[i], 'des_weight': des[i], 'cargo_type': None
                                              })['account_type']  # 结算类型
            print account_type
        except Exception as e:
            print e

print len(ori)
# for all in collection.find({'customer_id': customer_id}, {'waybill_no': 1}):
#     print all
    # ori.append(ori_weight['ori_weight'])
# for des_weight in freightInfo.find_one({'productCustomer_id': product_customer_id})['des_weight']:
#     print des_weight
#     des.append(des_weight)

#接下里就可以用collection来完成对数据库表的一些操作

#模糊查询集合中waybill_no含有20180416的waybill_no列
# for all in collection.find({'waybill_no' : re.compile('20180416')}, {'waybill_no': 1}):
#     print all

#获取集合中waybill_no=20180416015对应的state值
# a = collection.find_one({'waybill_no' : '20180416015'})
# print a['state']
#
# #向集合中插入数据
# collection.insert({name:'Tom',age:25,addr:'Cleveland'})
#
# #更新集合中的数据,第一个大括号里为更新条件，第二个大括号为更新之后的内容
# collection.update({Name:'Tom'},{Name:'Tom',age:18})
#
# #删除集合collection中的所有数据
# collection.remove()
#
# #删除集合collection
# collection.drop()

