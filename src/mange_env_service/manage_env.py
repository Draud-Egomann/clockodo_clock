import os
import re

def env_values():
    return ['API_KEY', 'EMAIL', 'START_STOP_TIMES', 'SERVICES_ID', 'CUSTOMERS_ID']

def check_env_file():
    env_path = os.path.join('configs', '.env')
    if not os.path.exists(env_path):
        print("No .env file for Clockodo API found")
        create_env_file(env_path)
        return False
    return True

def create_env_file(env_path):
    print("Creating .env file...")
    os.makedirs(os.path.dirname(env_path), exist_ok=True)
    with open(env_path, 'w') as f:
        f.write("API_KEY=your_api_key\n")
        f.write("EMAIL=your_email\n")
        f.write("START_STOP_TIMES=['08:00:00', '17:00:00']\n")
        f.write("SERVICES_ID=your_services_id\n")
        f.write("CUSTOMERS_ID=your_customers_id\n")
    print("The .env file has been created at:", env_path)
    print("Please fill in the required values.")

def check_env_correctness():
    env_path = os.path.join('configs', '.env')
    with open(env_path, 'r') as f:
        env = f.read()

        # Check if all environment variables are present
        api_key_match = re.search(r'API_KEY=(\w+)', env)
        email_match = re.search(r'EMAIL=(\w+)', env)
        start_stop_times_match = re.search(r'START_STOP_TIMES=\[(\d{2}:\d{2}:\d{2}), (\d{2}:\d{2}:\d{2})\]', env)
        services_id_match = re.search(r'SERVICES_ID=(\d+)', env)
        customers_id_match = re.search(r'CUSTOMERS_ID=(\d+)', env)

        env_variables = [api_key_match, email_match, start_stop_times_match, services_id_match, customers_id_match]
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
    # if API_KEY and EMAIL are True
    if value_matches[0] and value_matches[1]:
        user_input = input("Do you want to make a request to the Clockodo API to get the ID values of your services and customers? (y/n)")
        if user_input.lower() == 'y':
            # get_ids_from_api()
            print("Request to the Clockodo API made successfully.")
        return
    print("Please fill in the required values in the .env file and run the script again.")
    return

def get_ids_from_api():
    # Your logic to make a request to the Clockodo API here
    print("Request to the Clockodo API made successfully.")
    return 'your_services_id=123456', 'your_customers_id=123456'