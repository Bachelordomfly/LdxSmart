
from pymongo import MongoClient
import math

class caculate_func:

    def __init__(self):
        # self.client = MongoClient('192.168.1.79', 27017, connect=False)  # 防止出现no servers found yet错误
        self.client = MongoClient('47.75.132.197', 27017, connect=False)  # 防止出现no servers found yet错误
        db = self.client.LdxSmart
        self.packageItem = db.packageItem
        self.productInfo = db.productInfo
        self.productCustomer = db.productCustomer
        self.freightInfo = db.freightInfo
        self.accountInfo = db.accountInfo
        self.charging = db.charging
        self.productCustomer = db.productCustomer
        self.freightInfo = db.freightInfo
        self.chargeConfig = db.chargeConfig

    #   获取数据库中运费
    def getFright(self, waybill):
        # 获取已保存的运费
        try:
            waybill_id = self.packageItem.find_one({'waybill_no': waybill})['_id']
            account_id = self.accountInfo.find_one({'waybill_id': waybill_id})['_id']
            freight = self.charging.find_one({'account_id': account_id, 'item': '运费'})['fee']
            return freight
        except Exception as e:
            print(e)
            freight = 0
            return freight

    #   重新计算结算重量，返回计算结果
    def account_weight_caculate(self, waybill):
        waybill_id = self.packageItem.find_one({'waybill_no': waybill})['_id']
        customer_id = self.packageItem.find_one({'waybill_no': waybill})['customer_id']
        product_id = self.packageItem.find_one({'waybill_no': waybill})['product_id']
        delivery_volume = self.packageItem.find_one({'waybill_no': waybill})['delivery_volume']
        weight = self.accountInfo.find_one({'waybill_id': waybill_id})['weight']
        try:
            #  产品客户有关联,取产品客户关联id
            product_customer_id = self.productCustomer.find_one({'product_id': product_id,
                                                                 'customer_id': customer_id})['_id']
            try:
                volume_mode = self.productCustomer.find_one({'_id': product_customer_id})['volume_mode']
                light_parameter = self.productCustomer.find_one({'_id': product_customer_id})['light_parameter']
                account_weight = self.ac_weight(volume_mode, light_parameter, delivery_volume, weight)
                return account_weight

            except Exception as e:
                print(e + u'有产品客户关联，无关联记抛方式和抛重系数，将使用产品默认记抛和抛重')
                pc_id = self.productCustomer.find_one({'product_id': product_id,
                                                                 'customer_id': None})['_id']
                try:
                    volume_mode = self.productCustomer.find_one({'_id': pc_id})['volume_mode']
                    light_parameter = self.productCustomer.find_one({'_id': pc_id})['light_parameter']
                    account_weight = self.ac_weight(volume_mode, light_parameter, delivery_volume, weight)
                    return account_weight
                except Exception as e:
                    print(e + u'有产品客户关联，无关联记抛方式和抛重系数，无产品默认记抛和抛重，将返回...')
                    return 0
        except Exception as e:
            print(e)
            #  产品客户无关联,取产品的默认id
            product_customer_id = self.productCustomer.find_one({'product_id': product_id,
                                                                 'customer_id': None})['_id']
            try:
                volume_mode = self.productCustomer.find_one({'_id': product_customer_id})['volume_mode']
                light_parameter = self.productCustomer.find_one({'_id': product_customer_id})['light_parameter']
                account_weight = self.ac_weight(volume_mode, light_parameter, delivery_volume, weight)
                return account_weight
            except Exception as e:
                print(e + u'无产品客户关联，无关联记抛方式和抛重系数，无产品默认记抛和抛重，将返回...')
                return 0

    #   计算结算重量模块
    def ac_weight(self, volume_mode, light_parameter, delivery_volume, weight):
        if volume_mode == 0:  # 全抛
            ac_weight = delivery_volume / light_parameter
        elif volume_mode == 1:  # 半抛
            ac_weight = delivery_volume / light_parameter / 2
        elif volume_mode == 2:  # 抛大于实
            ac_weight = (delivery_volume / light_parameter + weight) / 2
        elif volume_mode == 3:  # 二八分抛
            ac_weight = (delivery_volume / 6000 - weight) * 0.2 + weight
        if ac_weight > weight:
            account_weight = ac_weight
        else:
            account_weight = weight
        return account_weight

    #   重新计算运费,返回计算结果
    def freight_caculate(self, waybill):
        waybill_id = self.packageItem.find_one({'waybill_no': waybill})['_id']
        # 判断该单号的站点是否有运费的费用配置
        site_id = self.packageItem.find_one({'waybill_no': waybill})['current_site']
        freight_config = self.chargeConfig.find_one({'site_id': site_id, 'charge_item': "运费"})
        freight = 0
        if not freight_config:
            # 获取正确运费和燃油附加费
            customer_id = self.packageItem.find_one({'waybill_no': waybill})['customer_id']
            product_id = self.packageItem.find_one({'waybill_no': waybill})['product_id']
            try:
                #  产品客户有关联,取产品客户关联id
                product_customer_id = self.productCustomer.find_one({'product_id': product_id,
                                                                     'customer_id': customer_id})['_id']
            except Exception as e:
                print(e)
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
            ori_weight_num = self.freightInfo.find({'productCustomer_id': product_customer_id, 'cargo_type': cargo_type})
            if ori_weight_num is None:
                print(u'该货物类型无报价,使用产品客户关联默认报价')
                cargo_type = None
                for ori_weight in self.freightInfo.find({'productCustomer_id': product_customer_id}):
                    ori.append(ori_weight['ori_weight'])

                for des_weight in self.freightInfo.find({'productCustomer_id': product_customer_id}):
                    des.append(des_weight['des_weight'])
            else:
                for ori_weight in self.freightInfo.find(
                        {'productCustomer_id': product_customer_id, 'cargo_type': cargo_type}):
                    ori.append(ori_weight['ori_weight'])

                for des_weight in self.freightInfo.find(
                        {'productCustomer_id': product_customer_id, 'cargo_type': cargo_type}):
                    des.append(des_weight['des_weight'])

            weight = 0
            continue_weight = 0
            account_type = 0
            first_fee = 0
            price = 0
            if len(ori) != 0:
                for i in range(0, len(ori)):
                    if ori[i] < account_weight <= des[i]:
                        try:
                            account_type = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                                      'ori_weight': ori[i], 'des_weight': des[i]
                                                                      })['account_type']  # 结算类型
                            first_fee = \
                                self.freightInfo.find_one({'productCustomer_id': product_customer_id, 'account_type': 1,
                                                       'cargo_type': cargo_type})['unit_price']  # 首重价格
                            first_weight = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                                      'account_type': 1, 'cargo_type': cargo_type})[
                                'des_weight']  # 首重
                            continue_weight = account_weight - first_weight
                        except Exception as e:
                            print(e)

                        if account_type == 1:  # 首重
                            return first_fee

                        elif account_type == 2:  # 一倍续重
                            weight = math.ceil(continue_weight)  # 续重部分1倍向上取整
                            continue_price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                                        'cargo_type': cargo_type, 'account_type': 2
                                                                        })['unit_price']  # 1倍续重单价
                            continue_fee = weight * continue_price  # 续重价格
                            all_fee = first_fee + continue_fee
                            return all_fee

                        elif account_type == 3:  # 0.5倍续重

                            multiple = (continue_weight // 1) / 0.5

                            remainder = continue_weight % 1
                            if remainder <= 0.5:
                                multiple += 1
                            else:
                                multiple += 2

                            continue_price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                                        'cargo_type': cargo_type, 'account_type': 3})[
                                'unit_price']  # 0.5倍续重单价
                            continue_fee = continue_price * multiple  # 续重价格
                            all_fee = first_fee + continue_fee
                            return all_fee
                        elif account_type == 4:  # 单价
                            weight = math.ceil(account_weight)  # 结算重量1倍向上取整
                            try:
                                price = \
                                self.freightInfo.find_one({'productCustomer_id': product_customer_id, 'account_type': 4,
                                                           'cargo_type': cargo_type})['unit_price']  # 单价
                            except Exception as e:
                                print(e)
                            all_fee = weight * price
                            return all_fee

                        elif account_type == 5:  # 固定价格
                            price = self.freightInfo.find_one({'productCustomer_id': product_customer_id,
                                                               'cargo_type': cargo_type, 'account_type': 5
                                                               })['unit_price']  # 固定价格
                            return price

                        else:
                            return 0
                    else:
                        print(u'结算重量不在[' + ori[i] + u',' + des[i] + u'区间内')

        else:
            print(u'该站点无运费的费用配置')
            return 0

    #   重新计算内部运费
    # def internal_freight_caculate(self, waybill):
