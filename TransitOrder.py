import time


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.orders = []
    
    def initTransitOrder(self):
        t = TransitOrder()

        src_dst = dict()
        print("Enter your source address:", end=' ')
        src_dst['src'] = input()
        print("Enter your destination address:", end=' ')
        src_dst['dst'] = input()
        print("Enter your source type: (residential/non-residential)", end=' ')
        src_dst['src_type'] = input()
        src_dst['form_type'] = 'src_dst'
        t.fill_form(src_dst)

        goods_detail = dict()
        print("Do you goods involve dangerous stuff such as flamable chemicals? (y/n)", end=' ')
        goods_detail['goods_type'] = 'dangerous' if input() == 'y' else 'safe'
        print("Enter your goods volume:", end=' ')
        goods_detail['volume'] = input()
        print("Enter the number of workers you require:", end=' ')
        goods_detail['workers_count'] = input()
        goods_detail['form_type'] = 'goods_detail'
        t.fill_form(src_dst)

        print("Enter your desired dispatch time: (yyyy:mm:dd, hh)", end=' ')
        d_time = input()
        t.book_transit(d_time)  #TODO: Convert d_time to a proper datatype

        t.confirm_deposit()

        self.orders.append(t)
        return


class TransitOrder:
    def __init__(self):
        self.order_time = time.time() #FIXME: yyyy:mm:dd, hh

        self.location_info = LocationInfo()
        self.goods_info = GoodsInfo()
        self.order_stat = OrderStat()
        self.financial_info = FinancialInfo()

        self.porters = None
        self.drivers = None

    def fill_form(self, info_dic):
        if info_dic['form_type'] == 'src_dst':
            self.location_info.set_loc(info_dic)
        elif info_dic['form_type'] == 'goods_detail':
            self.goods_info.set_goods(info_dic)
        else:
            exit()

        return

    def book_transit(self, d_time):
        self.order_stat.set_time(d_time)
        return

    def confirm_deposit(self):
        paid = self.financial_info.request_payment()
        if paid:
            d_time = self.order_stat.dispatch_time
            self.porters, self.drivers = ResourceHandler.assign_resources(
                self.location_info, self.goods_info, d_time)
                
        return


class LocationInfo:
    def __init__(self):
        self.src_address = None
        self.dst_address = None
        self.src_type = None

    def set_loc(self, src_dst):
        assert src_dst['form_type'] == 'src_dst'

        self.src_address = src_dst['src']
        self.dst_address = src_dst['dst']
        self.src_type = src_dst['src_type']

        return

    @property
    def src_address(self): return self.src_address

    @property
    def dst_address(self): return self.dst_address


class GoodsInfo:
    def __init__(self):
        self.goods_type = None
        self.goods_volume = None
        self.workers_count = None

    def set_goods(self, goods_detail):
        assert goods_detail['form_type'] == 'goods_detail'

        self.goods_type = goods_detail['goods_type']
        self.goods_volume = goods_detail['volume']
        self.workers_count = goods_detail['workers_count']

        return

    @property
    def goods_type(self): return self.goods_type

    @property
    def goods_volume(self): return self.goods_volume

    @property
    def workers_count(self): return self.workers_count


class OrderStat:
    def __init__(self):
        self.status = None
        self.dispatch_time = None

    def set_time(self, d_time):
        self.dispatch_time = d_time
        return

    def set_status(self, stat):
        self.status = stat
        return

    @property
    def dispatch_time(self): return self.dispatch_time


class FinancialInfo:
    def __init__(self):
        self.dep_amount = 0
        self.total_price = 0
        self.paid = False

    def request_payment(self, loc, goods_detail):
        self.__calc_total_price(loc, goods_detail)
        self.__calc_deposit(0.5)
        self.__pay(self.dep_amount)

        return

    def __calc_deposit(self, percentage):
        self.dep_amount = self.total_price * percentage
        return

    def __calc_total_price(self, loc, goods_detail):
        self.dep_amount += goods_detail.goods_volume * 10000
        if goods_detail.goods_type == 'dangerous':
            self.dep_amount *= 1.1
        self.dep_amount += goods_detail.workers_count * 20000
        # self.dep_amount += loc.dst_address - loc.src_address  # Overload - operator for address

        return

    def __pay(self, price):
        # self.paid = SHAPARAK.pay(price)
        self.paid = True
        return


class ResourceHandler:

    @staticmethod
    def assign_resources(goods_detail, d_time):
        porters, drivers = EmployeeStats.find_free_workers(goods_detail, d_time)

        for porter in porters:
            porter.assign_task(d_time)

        for driver in drivers:
            driver.assign_task(d_time)
        
        return porters, drivers


class EmployeeStats:
    drivers = []
    porters = []

    @staticmethod
    def find_free_workers(goods_detail, d_time):
        available_porters = []
        available_drivers = []
        porters_needed = goods_detail.workers_count
        drivers_needed = goods_detail.goods_volume / 12 # Each truck has a capacity
                                                        # of 12 cubic meters
        for porter in EmployeeStats.porters:
            if porters_needed == 0:
                break

            if porter.is_available(d_time):
                available_porters.append(porter)
                porters_needed -= 1
        
        for driver in EmployeeStats.drivers:
            if porters_needed == 0:
                break

            if driver.is_available(d_time):
                available_drivers.append(driver)
                drivers_needed -= 1

        assert (porters_needed == 0) and (drivers_needed == 0)
        return available_porters, available_drivers
        
    @staticmethod
    def add_porter(porter):
        EmployeeStats.porters.append(porter)

    @staticmethod
    def add_driver(driver):
        EmployeeStats.drivers.append(driver)


class Driver:
    def __init__(self, employee_id):
        self.employee_info = EmployeeInfo(employee_id)

    def assign_task(self, d_time):
        self.employee_info.assign_task(d_time)


class Porter:
    def __init__(self, employee_id):
        self.employee_info = EmployeeInfo(employee_id)
    
    def assign_task(self, d_time):
        self.employee_info.assign_task(d_time)


class EmployeeInfo:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.schedule = Schedule()
    
    def assign_task(self, d_time):
        self.schedule.assign_task(d_time)


class Schedule:  #TODO: 
    def __init__(self) -> None:
        pass
