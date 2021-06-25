import time
import configparser
import json


class User:
    def __init__(self, user_id):
        self.__user_id = user_id
        self.__orders = []
    
    def initTransitOrder(self):
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
        goods_detail['volume'] = input()
        print('Enter the number of workers you require:', end=' ')
        goods_detail['workers_count'] = input()
        goods_detail['form_type'] = 'goods_detail'
        t.fill_form(src_dst)

        print('Enter your desired dispatch time: (yyyy-mm-dd (morning/afternoon/night))', end=' ')
        d_time = input()
        t.book_transit(d_time)

        t.confirm_deposit()

        self.__orders.append(t.to_json())
        # DAO.store_user_requests(self)
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
        paid = self.__financial_info.request_payment()
        if paid:
            d_time = self.__order_stat.dispatch_time
            self.__porters, self.__drivers = ResourceHandler.assign_resources(
                self.__location_info, self.__goods_info, d_time)
                
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
        json['dirvers_ids'] = drivers_ids

        return json


class LocationInfo:
    def __init__(self):
        self.__src_address = None
        self.__dst_address = None
        self.__src_type = None

    def set_loc(self, src_dst):
        assert src_dst['form_type'] == 'src_dst'

        self.__src_address = src_dst['src']
        self.__dst_address = src_dst['dst']
        self.__src_type = src_dst['src_type']

        return

    def to_json(self):
        json = dict()
        json['src_address'] = self.__src_address
        json['dst_address'] = self.__dst_address
        json['src_type'] = self.__src_type

        return json

    @property
    def src_address(self): return self.__src_address

    @property
    def dst_address(self): return self.__dst_address


class GoodsInfo:
    def __init__(self):
        self.__goods_type = None
        self.__goods_volume = None
        self.__workers_count = None

    def set_goods(self, goods_detail):
        assert goods_detail['form_type'] == 'goods_detail'

        self.__goods_type = goods_detail['goods_type']
        self.__goods_volume = goods_detail['volume']
        self.__workers_count = goods_detail['workers_count']

        return

    def to_json(self):
        json = dict()
        json['goods_type'] = self.__goods_type
        json['goods_volume'] = self.__goods_volume
        json['workers_count'] = self.__workers_count

        return json

    @property
    def goods_type(self): return self.__goods_type

    @property
    def goods_volume(self): return self.__goods_volume

    @property
    def workers_count(self): return self.__workers_count


class OrderStat:
    def __init__(self):
        self.__status = 'waiting for deposit'
        self.__dispatch_time = None

    def set_time(self, d_time):
        self.__dispatch_time = d_time
        return

    def set_status(self, stat):
        self.__status = stat
        return

    def to_json(self):
        json = dict()
        json['status'] = self.__status
        json['dispatch_time'] = self.__dispatch_time

        return json

    @property
    def dispatch_time(self): return self.__dispatch_time


class FinancialInfo:
    def __init__(self):
        self.__dep_amount = 0
        self.__dep_percentage = 0.5
        self.__total_price = 0
        self.__dangerous_overcharge = 1.1
        self.__paid = False

    def request_payment(self, loc, goods_detail):
        self.__calc_total_price(loc, goods_detail)
        self.__calc_deposit()
        self.__pay(self.__dep_amount)
        return

    def __calc_deposit(self):
        self.__dep_amount = self.__total_price * self.__dep_percentage
        return

    def __calc_total_price(self, loc, goods_detail):
        self.__total_price = 0
        self.__total_price += goods_detail.goods_volume * 10000
        self.__total_price += goods_detail.workers_count * 20000
        # self.dep_amount += loc.dst_address - loc.src_address  # Overload '-' operator for addresses
        
        if goods_detail.goods_type == 'dangerous':
            self.__total_price *= self.__dangerous_overcharge

        return

    def __pay(self, price):
        # self.paid = SHAPARAK.pay(price)
        self.__paid = True
        return

    def to_json(self):
        self.__dep_amount = 0
        self.__dep_percentage = 0.5
        self.__total_price = 0
        self.__dangerous_overcharge = 1.1
        self.__paid = False

        json = dict()
        json['dep_amount'] = self.__dep_amount
        json['dep_percentage'] = self.__dep_percentage
        json['total_price'] = self.__total_price
        json['dangerous_overcharge'] = self.__dangerous_overcharge
        json['paid'] = self.__paid

        return json
    

    @property
    def paid(self): return self.__paid


class ResourceHandler:

    @staticmethod
    def assign_resources(goods_detail, d_time):
        porters, drivers = EmployeesStats.find_free_workers(goods_detail, d_time)

        for porter in porters:
            porter.assign_task(d_time)

        for driver in drivers:
            driver.assign_task(d_time)
        
        return porters, drivers


class EmployeesStats:
    drivers = []
    porters = []

    @staticmethod
    def find_free_workers(goods_detail, d_time):
        available_porters = []
        available_drivers = []
        porters_needed = goods_detail.workers_count
        drivers_needed = goods_detail.goods_volume / 20 # Each truck has a capacity
                                                        # of 20 cubic meters
        for porter in EmployeesStats.porters:
            if porters_needed == 0:
                break

            if porter.is_available(d_time):
                available_porters.append(porter)
                porters_needed -= 1
        
        for driver in EmployeesStats.drivers:
            if drivers_needed == 0:
                break

            if driver.is_available(d_time):
                available_drivers.append(driver)
                drivers_needed -= 1

        assert (porters_needed == 0) and (drivers_needed == 0)
        return available_porters, available_drivers
        
    @staticmethod
    def add_porter(employee_id, schedule):
        porter = Porter(employee_id, schedule)
        EmployeesStats.porters.append(porter)

        return

    @staticmethod
    def add_driver(employee_id, schedule):
        driver = Driver(employee_id, schedule)
        EmployeesStats.drivers.append(driver)

        return

    @staticmethod
    def load_employees():
        porters_json, drivers_json = DAO.load_employees()

        for porter in porters_json:
            porter_id = porter['employee_info']['employee_id']
            porter_schedule = set(porter['employee_info']['schedule'])
            EmployeesStats.add_porter(porter_id, porter_schedule)

        for driver in drivers_json:
            driver_id = driver['employee_info']['employee_id']
            driver_schedule = set(driver['employee_info']['schedule'])
            EmployeesStats.add_driver(driver_id, driver_schedule)

        return

    @staticmethod
    def store_employees():
        DAO.store_employees(EmployeesStats.porters, EmployeesStats.drivers)

        return


class Driver:
    def __init__(self, employee_id, schedule):
        self.__employee_info = EmployeeInfo(employee_id, schedule)

    def assign_task(self, d_time):
        self.__employee_info.assign_task(d_time)

    def is_available(self, d_time):
        return self.__employee_info.is_available(d_time)

    def to_json(self):
        json = dict()
        json['employee_info'] = self.__employee_info.to_json()
        return json

class Porter:
    def __init__(self, employee_id, schedule):
        self.__employee_info = EmployeeInfo(employee_id, schedule)

    
    def assign_task(self, d_time):
        self.__employee_info.assign_task(d_time)
    
    def is_available(self, d_time):
        return self.__employee_info.is_available(d_time)

    def to_json(self):
        json = dict()
        json['employee_info'] = self.__employee_info.to_json()
        return json


class EmployeeInfo:
    def __init__(self, employee_id, schedule):
        self.__employee_id = employee_id
        self.__schedule = Schedule(schedule)
    
    def assign_task(self, d_time):
        self.__schedule.assign_task(d_time)
    
    def is_available(self, d_time):
        return self.__schedule.is_available(d_time)

    def to_json(self):
        json = self.__schedule.to_json()
        json['employee_id'] = self.__employee_id
        return json


class Schedule:
    def __init__(self, schedule):
        self.__work_schedule = schedule

    def assign_task(self, d_time):
        self.__work_schedule.add(d_time)

    def is_available(self, d_time):
        return d_time not in self.__work_schedule

    def to_json(self):
        json = dict()
        json['schedule'] = list(self.__work_schedule)
        return json

class DAO:

    porters_data_address = None
    drivers_data_address = None
    users_data_address = None


    @staticmethod
    def config_DAO(config_path):

        config_parser = configparser.RawConfigParser()   
        config_parser.read(config_path)

        DAO.drivers_data_address = config_parser.get("EMPLOYEE_DATA", "DRIVERS_DATA")
        DAO.porters_data_address = config_parser.get("EMPLOYEE_DATA", "PORTERS_DATA")

        DAO.users_data_address = config_parser.get("USERS_DATA", "USERS_DATA")

        return

    @staticmethod
    def load_employees():
        assert DAO.porters_data_address != None
        assert DAO.drivers_data_address != None
        assert DAO.users_data_address != None

        porters_file = open(DAO.porters_data_address,)
        porters_json = json.load(porters_file)
        porters_file.close()

        drivers_file = open(DAO.drivers_data_address)
        drivers_json = json.load(drivers_file)
        drivers_file.close()

        # for key, value in porters_json.items():
            # continue

        return porters_json, drivers_json

    
    @staticmethod
    def store_employees(porters, drivers):
        porters_json = []
        for porter in porters:
            porters_json.append(porter.to_json())

        porters_file = open(DAO.porters_data_address, 'w')
        json.dump(porters_json, porters_file, indent=4)
        porters_file.close()

        drivers_json = []
        for driver in drivers:
            drivers_json.append(driver.to_json())

        drivers_file = open(DAO.drivers_data_address, 'w')
        json.dump(drivers_json, drivers_file, indent=4)
        drivers_file.close()

        return


    @staticmethod
    def load_users():
        users_file = open(DAO.users_data_address)
        users_json = json.load(users_file)
        users_file.close()

        return users_json

    @staticmethod
    def store_users(users):
        users_json = []
        for user in users:
            users_json.append(user.to_json())

        users_file = open(DAO.users_data_address, 'w')
        json.dump(users_json, users_file, indent=4)
        users_file.close()

        return


def initialize():
    return


DAO.config_DAO('./app.config')  # necessary
# DAO.load()