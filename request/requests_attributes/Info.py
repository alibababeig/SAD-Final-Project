
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
        print(f'your deposit amount is {self.__dep_amount:,.0f} Tomans. Are you willing to proceed? (y/n)', end=' ')
        if(input() != 'y'):
            exit("\n--error-- user doesn't want to pay us :(\n")

        self.__pay(self.__dep_amount)

        return self.__paid

    def __calc_deposit(self):
        self.__dep_amount = self.__total_price * self.__dep_percentage
        return

    def __calc_total_price(self, loc, goods_detail):
        self.__total_price = 0
        self.__total_price += goods_detail.goods_volume * 10000
        self.__total_price += goods_detail.workers_count * 50000
        # self.dep_amount += loc.dst_address - loc.src_address  # Overload '-' operator for addresses
        
        if goods_detail.goods_type == 'dangerous':
            self.__total_price *= self.__dangerous_overcharge

        return

    def __pay(self, price):
        # self.paid = SHAPARAK.pay(price)
        self.__paid = True
        return

    def to_json(self):
        json = dict()
        json['dep_amount'] = self.__dep_amount
        json['dep_percentage'] = self.__dep_percentage
        json['total_price'] = self.__total_price
        json['dangerous_overcharge'] = self.__dangerous_overcharge
        json['paid'] = self.__paid

        return json
