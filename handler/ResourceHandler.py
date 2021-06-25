from employee.EmployeesStats import EmployeesStats

class ResourceHandler:

    @staticmethod
    def assign_resources(goods_detail, d_time, order_stat):
        porters, drivers = EmployeesStats.find_free_workers(goods_detail, d_time)

        for porter in porters:
            porter.assign_task(d_time)

        for driver in drivers:
            driver.assign_task(d_time)

        order_stat.set_status('registered')
        
        return porters, drivers