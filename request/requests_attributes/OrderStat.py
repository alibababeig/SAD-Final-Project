
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
