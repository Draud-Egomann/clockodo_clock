import os

def check_env_file():
    env_path = os.path.join('configs', '.env')
    print(env_path)
    if not os.path.exists(env_path):
        print("No .env file for Clockodo API found")
        create_env_file(env_path)

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
