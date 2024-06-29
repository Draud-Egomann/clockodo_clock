import os

def create_env_file():
    env_path = os.path.join(os.getcwd(), '.env')

    if os.path.exists(env_path):
        print(f'.env file already exists at {env_path}')
        return

    env_content = """API_KEY=your_api_key_here
EMAIL=your_email_here
SUBDOMAIN=my
SERVICES_ID=0
CUSTOMERS_ID=0
RANDOM_CLOCKING_IN=True
WORKING_DAYS=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
START_STOP_TIMES=[("08:00:00", "12:00:00"), ("13:00:00", "17:00:00")]"""

    with open(env_path, 'w') as file:
        file.write(env_content)
    print(f'.env file created at {env_path}')

if __name__ == "__main__":
    create_env_file()