from data_access_layer.dao import DAO
from employee.EmployeesStats import EmployeesStats
from user.User import User


def initialize():
    DAO.config('./app.config')
    users_json = DAO.load_users()
    porters_count, drivers_count = EmployeesStats.load_employees()

    if porters_count < 50:
        for i in range(porters_count + 1, 51):
            EmployeesStats.add_porter(f'p{i}', set())

    if drivers_count < 50:
        for i in range(drivers_count + 1, 51):
            EmployeesStats.add_driver(f'd{i}', set())


    users_objects = []
    for user in users_json:
        users_objects.append(User(user['user_id'], user['orders']))

    users_count = len(users_objects)
    if users_count < 5:
        for i in range(users_count + 1, 6):
            users_objects.append(User(f'u{i}', []))
    
    return users_objects


users = initialize()
users[2].init_transit_order()

EmployeesStats.store_employees()
DAO.store_users(users)