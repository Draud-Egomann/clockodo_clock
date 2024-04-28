from clockodo_service.customers import get_customers
from clockodo_service.services import get_services
from clockodo_mapping_service.mapping import map_json
from save_as_json.save_json import save_json
import re

def env_values():
    return ['API_KEY', 'EMAIL', 'SUBDOMAIN', 'START_STOP_TIMES', 'SERVICES_ID', 'CUSTOMERS_ID']

def check_env_correctness(env_path):
    with open(env_path, 'r') as f:
        env = f.read()

        # Check if all environment variables are present
        api_key_match = re.search(r'API_KEY=(\w+)', env)
        email_match = re.search(r'EMAIL=(\w+)', env)
        subdomain_match = re.search(r'SUBDOMAIN=(\w+)', env)
        start_stop_times_match = re.search(r'START_STOP_TIMES=\[(\d{2}:\d{2}:\d{2}), (\d{2}:\d{2}:\d{2})\]', env)
        services_id_match = re.search(r'SERVICES_ID=(\d+)', env)
        customers_id_match = re.search(r'CUSTOMERS_ID=(\d+)', env)

        env_variables = [api_key_match, email_match, subdomain_match, start_stop_times_match, services_id_match, customers_id_match]
        env_value_matches = []

        for env_var in env_variables:
            if not env_var:
                env_value_matches.append(False)
            else:
                env_value_matches.append(True)
        
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
            env = re.sub(f'{env_variable}=(\d+)', f'{env_variable}={data_id}', env)
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

def is_user_input_within_range(user_input, data_list):
    try:
        int_input = int(user_input)
        if int_input < 1 or int_input > len(data_list):
            print("Please enter a number within the range.")
            return False
        return True
    except ValueError:
        print("Please enter a number.")
        return False