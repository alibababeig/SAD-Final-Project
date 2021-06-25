import time
from data_access_layer.dao import DAO
from employee.EmployeesStats import EmployeesStats
from handler.ResourceHandler import ResourceHandler
from request_attributes.Info import LocationInfo, GoodsInfo, FinancialInfo
from request_attributes.OrderStat import OrderStat

class User:
    def __init__(self, user_id, orders):
        self.__user_id = user_id
        self.__orders = orders
    
    def init_transit_order(self):
        t = TransitOrder()

        src_dst = dict()
        print('Enter your source address:', end=' ')
        src_dst['src'] = input()
        print('Enter your destination address:', end=' ')
        src_dst['dst'] = input()
        print('Enter your source type: (residential/non-residential)', end=' ')
        src_dst['src_type'] = input()
        src_dst['form_type'] = 'src_dst'
        t.fill_form(src_dst)

        goods_detail = dict()
        print('Do you goods involve dangerous stuff such as flamable chemicals? (y/n)', end=' ')
        goods_detail['goods_type'] = 'dangerous' if input() == 'y' else 'safe'
        print('Enter your goods volume in cubic meters:', end=' ')
        goods_detail['volume'] = float(input())
        print('Enter the number of workers you require:', end=' ')
        goods_detail['workers_count'] = int(input())
        goods_detail['form_type'] = 'goods_detail'
        t.fill_form(goods_detail)

        print('Enter your desired dispatch time: (yyyy-mm-dd (morning/afternoon/night))', end=' ')
        d_time = input()
        t.book_transit(d_time)

        t.confirm_deposit()

        self.__orders.append(t.to_json())
        return

    def to_json(self):
        json = dict()
        json['user_id'] = self.__user_id
        json['orders'] = self.__orders

        return json


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


def initialize():
    DAO.config('./app.config')
    users_json = DAO.load_users()
    porters_count, drivers_count = EmployeesStats.load_employees()

    if porters_count < 50:
        for i in range(porters_count + 1, 51):
            EmployeesStats.add_porter(f'p{i}', set())

    if drivers_count < 50:
        for i in range(drivers_count + 1, 51):
            EmployeesStats.add_driver(f'd{i}', set())


    users_objects = []
    for user in users_json:
        users_objects.append(User(user['user_id'], user['orders']))

    users_count = len(users_objects)
    if users_count < 5:
        for i in range(users_count + 1, 6):
            users_objects.append(User(f'u{i}', []))
    
    return users_objects


users = initialize()
users[2].init_transit_order()

EmployeesStats.store_employees()
DAO.store_users(users)