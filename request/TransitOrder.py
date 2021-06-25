import time
from .requests_attributes.Info import LocationInfo, GoodsInfo, FinancialInfo
from .requests_attributes.OrderStat import OrderStat
from handler.ResourceHandler import ResourceHandler

class TransitOrder:
    def __init__(self):
        self.__order_time = time.strftime('%Y-%m-%d %H:%M:%S',
            time.localtime(time.time()))

        self.__location_info = LocationInfo()
        self.__goods_info = GoodsInfo()
        self.__order_stat = OrderStat()
        self.__financial_info = FinancialInfo()

        self.__porters = None
        self.__drivers = None

    def fill_form(self, info_dic):
        if info_dic['form_type'] == 'src_dst':
            self.__location_info.set_loc(info_dic)
        elif info_dic['form_type'] == 'goods_detail':
            self.__goods_info.set_goods(info_dic)
        else:
            exit()

        return

    def book_transit(self, d_time):
        self.__order_stat.set_time(d_time)
        return

    def confirm_deposit(self):
        paid = self.__financial_info.request_payment(self.__location_info, self.__goods_info)
        if not paid:
            exit('\n--error-- not paid\n')

        d_time = self.__order_stat.dispatch_time
        self.__porters, self.__drivers = ResourceHandler.assign_resources(self.__goods_info, d_time, self.__order_stat)
                
        return

    def to_json(self):
        json = dict()
        json['order_time'] = self.__order_time 
        json['location_info'] = self.__location_info.to_json()
        json['goods_info'] = self.__goods_info.to_json()
        json['order_stat'] = self.__order_stat.to_json()
        json['financial_info'] = self.__financial_info.to_json()

        porters_ids = []
        for porter in self.__porters:
            porters_ids.append(porter.to_json()['employee_info']['employee_id'])

        drivers_ids = []
        for driver in self.__drivers:
            drivers_ids.append(driver.to_json()['employee_info']['employee_id'])

        json['porters_ids'] = porters_ids
        json['drivers_ids'] = drivers_ids

        return json
