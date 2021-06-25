import configparser
import json


class DAO:

    porters_data_address = None
    drivers_data_address = None
    users_data_address = None


    @staticmethod
    def config(config_path):

        config_parser = configparser.RawConfigParser()   
        config_parser.read(config_path)

        DAO.drivers_data_address = config_parser.get("EMPLOYEE_DATA", "DRIVERS_DATA")
        DAO.porters_data_address = config_parser.get("EMPLOYEE_DATA", "PORTERS_DATA")

        DAO.users_data_address = config_parser.get("USERS_DATA", "USERS_DATA")

        return

    @staticmethod
    def load_employees():
        assert DAO.porters_data_address != None
        assert DAO.drivers_data_address != None
        assert DAO.users_data_address != None

        porters_file = open(DAO.porters_data_address,)
        porters_json = json.load(porters_file)
        porters_file.close()

        drivers_file = open(DAO.drivers_data_address)
        drivers_json = json.load(drivers_file)
        drivers_file.close()

        # for key, value in porters_json.items():
            # continue

        return porters_json, drivers_json

    
    @staticmethod
    def store_employees(porters, drivers):
        porters_json = []
        for porter in porters:
            porters_json.append(porter.to_json())

        porters_file = open(DAO.porters_data_address, 'w')
        json.dump(porters_json, porters_file, indent=4)
        porters_file.close()

        drivers_json = []
        for driver in drivers:
            drivers_json.append(driver.to_json())

        drivers_file = open(DAO.drivers_data_address, 'w')
        json.dump(drivers_json, drivers_file, indent=4)
        drivers_file.close()

        return


    @staticmethod
    def load_users():
        users_file = open(DAO.users_data_address)
        users_json = json.load(users_file)
        users_file.close()

        return users_json

    @staticmethod
    def store_users(users):
        users_json = []
        for user in users:
            users_json.append(user.to_json())

        users_file = open(DAO.users_data_address, 'w')
        json.dump(users_json, users_file, indent=4)
        users_file.close()

        return
