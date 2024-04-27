from mange_env_service.manage_env import check_env_file

def save_timer_id(timer_id):
    with open('tmp.txt', 'w') as f:
        f.write(timer_id)

def main():
    check_env_file()

    # Your main logic here

    # Simulating script ending prematurely
    timer_id = 'your_timer_id=[123456]'
    save_timer_id(timer_id)

if __name__ == "__main__":
    main()
