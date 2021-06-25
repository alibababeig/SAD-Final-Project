import math
from data_access_layer.dao import DAO
from .employee_models.EmployeeModels import Driver, Porter

class EmployeesStats:
    drivers = []
    porters = []

    @staticmethod
    def find_free_workers(goods_detail, d_time):
        available_porters = []
        available_drivers = []
        porters_needed = goods_detail.workers_count
        drivers_needed = math.ceil(goods_detail.goods_volume / 20) # Each truck has a capacity
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

        return len(EmployeesStats.porters), len(EmployeesStats.drivers)

    @staticmethod
    def store_employees():
        DAO.store_employees(EmployeesStats.porters, EmployeesStats.drivers)

        return

