from request.TransitOrder import TransitOrder

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
