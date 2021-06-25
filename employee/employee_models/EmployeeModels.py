
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
