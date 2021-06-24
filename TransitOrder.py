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
        t.book_transit(d_time)

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
        return

class GoodsInfo:
    def __init__(self):
        self.goods_type = None
        self.goods_volume = None
        self.workers_count = None

    def set_goods(self, goods_detail):
        return

class OrderStat:
    def __init__(self):
        self.status = None
        self.dispatch_time = None

    def set_time(self, d_time):
        return

    def set_status(self, stat):
        return

    @property
    def dispatch_time(self): return self.dispatch_time

class FinancialInfo:
    def __init__(self):
        self.dep_amount = None
        self.total_price = None
        self.paid = False

    def request_payment(self, loc, goods_detail):
        return

    def __calc_deposit(self, loc, goods_detail):
        return

    def __calc_total_price(self, loc, goods_detail):
        return

    def __pay(self, price):
        return

class Schedule:
    def __init__(self) -> None:
        pass

class EmployeeInfo:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.shedule = Schedule()


class ResourceHandler:

    @staticmethod
    def assign_resources(loc, goods_detail, d_time):
        return


