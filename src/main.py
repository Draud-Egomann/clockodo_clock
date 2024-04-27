from mange_env_service.manage_env import check_env_file, check_env_correctness, incorrect_env_values

def save_timer_id(timer_id):
    with open('tmp.txt', 'w') as f:
        f.write(timer_id)

def main():
    if not check_env_file():
        print(".env file created. Please fill in the required values and run the script again.")
        print("If you don't know the ID values of your services and customers, enter API_KEY and EMAIL in the .env file and run the script again.")
        return
    
    res = check_env_correctness()
    
    # If any of the environment variables are missing or incorrect
    if not all(res):
        incorrect_env_values(res)

    # Your main logic here

    # Simulating script ending prematurely
    timer_id = 'your_timer_id=[123456]'
    save_timer_id(timer_id)

if __name__ == "__main__":
    main()
