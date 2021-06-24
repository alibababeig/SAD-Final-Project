import time


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.orders = []
    
    def initTransitOrder(self):
        t = Transit()

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


class Transit:
    def __init__(self):
        self.order_time = time.time()

    def fill_form(self, info_dic):

        return

    def book_transit(self, d_time):
        return

    def confirm_deposit(self):
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

class FinancalInfo:
    def __init__(self, loc, goods_detail):
        self.dep_amount = None
        self.total_price = None
        self.paid = False

    def check_payment(self):
        return

    def calc_deposit(self, loc, goods_detail):
        return

    def calc_total_price(self, loc, goods_detail):
        return

    def request_payment(self, price):
        return

class Schedule:
    def __init__(self) -> None:
        pass

class EmployeeInfo:
    def __init__(self, employee_id):
        self.employee_id = employee_id
        self.shedule = Schedule()
