from clockodo_service.customers import get_customers
from clockodo_service.services import get_services
from clockodo_mapping_service.mapping import map_customers
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

def env_write_customer_service(env_path):
    customer_id = get_customers_from_api()

    if customer_id != 0:
        with open(env_path, 'r') as f:
            env = f.read()
            env = re.sub(r'CUSTOMERS_ID=(\d+)', f'CUSTOMERS_ID={customer_id}', env)
        with open(env_path, 'w') as f:
            f.write(env)

    services_id = get_services_from_api()

    if services_id != 0:
        with open(env_path, 'r') as f:
            env = f.read()
            env = re.sub(r'SERVICES_ID=(\d+)', f'SERVICES_ID={services_id}', env)
        with open(env_path, 'w') as f:
            f.write(env)

def get_customers_from_api():
    customers_json = get_customers()
    
    if customers_json['paging']['count_items'] > 10:
        print("There are too many customers to display. In Data folder, you can find the customers.json file.")
        maped_customer = map_customers(customers_json)
        save_json(maped_customer, 'customers', 'data')
        return 0
    else:
        user_input = ''
        while True:
            print("Customers:")
            for i, customer in customers_json['customers']:
                print(f"{i}. {customer['name']}")
            user_input = input("Select the customer you want to use and enter the corresponding number:")
            if is_user_input_within_range(user_input, customers_json['customers']) is True:
                break
        customer_id = customers_json['customers'][int(user_input) - 1]['id']
        return customer_id

def get_services_from_api():
    services_json = get_services()
    
    if len(services_json['services']) > 10:
        print("There are too many services to display. In Data folder, you can find the services.json file.")
        save_json(services_json, 'services', 'data')
        return 0
    else:
        user_input = ''
        while True:
            print("Services:")
            for i, service in services_json['services']:
                print(f"{i}. {service['name']}")
            user_input = input("Select the service you want to use and enter the corresponding number:")
            if is_user_input_within_range(user_input, services_json['services']) is True:
                break
        service_id = services_json['services'][int(user_input) - 1]['id']
        return service_id

def is_user_input_within_range(input, range):
    try:
        int_input = int(input)
        if int_input < 1 or int_input > len(range):
            print("Please enter a number within the range.")
            return False
        return True
    except ValueError:
        print("Please enter a number.")
        return False