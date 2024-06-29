from clockodo_service.customers_api import get_customers
from clockodo_service.services_api import get_services
from clockodo_mapping_service.mapping import map_json
from helper_service.helper import save_json, is_user_input_within_range, is_valid_regex
from decouple import config
import re

def env_values():
    return ['API_KEY', 'EMAIL', 'SUBDOMAIN', 'SERVICES_ID', 'CUSTOMERS_ID', "VARIABLE_CLOCKING_IN", "WORKING_DAYS", 'SCHEDULES']

def check_env_correctness():
    env_values_list = [config(value) for value in env_values()]

    # Validation checks
    regex_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    regex_value_0 = r'^[1-9]\d*$'
    regex_clocking_in = r'^(True|False)$'
    regex_working_days = r'^\["(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)"(?:,\s*"(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)")*\]$'
    regex_schedule = r'^\[\("(\d{2}:\d{2}:\d{2})", "(\d{2}:\d{2}:\d{2})"\)(?:, \("(\d{2}:\d{2}:\d{2})", "(\d{2}:\d{2}:\d{2})"\))*\]$'

    env_value_matches = [
        isinstance(env_values_list[0], str),
        is_valid_regex(regex_email, env_values_list[1]),
        isinstance(env_values_list[2], str),
        is_valid_regex(regex_value_0, env_values_list[3]),
        is_valid_regex(regex_value_0, env_values_list[4]),
        is_valid_regex(regex_clocking_in, env_values_list[5]),
        is_valid_regex(regex_working_days, env_values_list[6]),
        is_valid_regex(regex_schedule, env_values_list[7])
    ]

    return env_value_matches

def incorrect_env_values(value_matches):
    values = env_values()
    print("Following values are missing or incorrect in the .env file:")
    for i, value in enumerate(value_matches):
        if not value:
            print(f"-  {values[i]}")

    print("Please fill in the required values in the .env file and run the script again.")
    return

def env_write_customer_service(env_path, data_type, env_variable):
    data_id = get_data_from_api(data_type)
    
    if data_id != 0:
        with open(env_path, 'r') as f:
            env = f.read()
            env = re.sub(f'{env_variable}=(\\d+)', f'{env_variable}={data_id}', env)
        with open(env_path, 'w') as f:
            f.write(env)

def get_data_from_api(data_type):
    data_json = fetch_data(data_type)
    data_json = map_json(data_json[data_type])
    
    if len(data_json) > 10:
        print(f"There are too many {data_type} to display. In Data folder, you can find the {data_type}.json file.")
        save_json(data_json, data_type, 'data')
        return 0
    else:
        user_input = ''
        while True:
            print(f"{data_type.capitalize()}:")
            for i, data in enumerate(data_json, start=1):
                print(f"{i}. {data['name']}")
            user_input = input(f"Select the {data_type} you want to use and enter the corresponding number:")
            if is_user_input_within_range(user_input, data_json):
                break
        data_id = data_json[int(user_input) - 1]['id']
        return data_id

def fetch_data(data_type):
    if data_type == 'customers':
        return get_customers()
    elif data_type == 'services':
        return get_services()
    else:
        raise ValueError("Invalid data type")