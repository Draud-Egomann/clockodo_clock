from helper_service.helper import save_json, randomize_schedule_time
from clockodo_mapping_service.mapping import map_timer_json
from helper_service.helper import calculate_sleep_time, convert_seconds_to_hhmmss, get_sleep_statement, is_today_a_working_day
from decouple import config
import requests
import datetime
import atexit
import time
import json

# load data from .env-file
API_KEY = config('API_KEY')
EMAIL = config('EMAIL')
SUBDOMAIN = config('SUBDOMAIN')
SCHEDULES = config('SCHEDULES')
SERVICES_ID = config('SERVICES_ID')
CUSTOMERS_ID = config('CUSTOMERS_ID')
VARIABLE_CLOCKING_IN = config('VARIABLE_CLOCKING_IN')
WORKING_DAYS = config('WORKING_DAYS')

start_timer_url = f"https://{SUBDOMAIN}.clockodo.com/api/v2/clock"

# define header for request
headers = {
    "X-ClockodoApiKey": API_KEY,
    "X-ClockodoApiUser": EMAIL,
    "X-Clockodo-External-Application": f"Clockodo;{EMAIL}"
}

def get_current_timer_id():
    """
    Retrieves the current timer Id from the temporary JSON file.

    Returns:
    int: The current timer Id if available, or 0 not.
    """
    # Load data from JSON file
    try:
        with open('data/tmp.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return 0
    
    # Extract and return the timer id
    return data.get('your_timer_id')

def reset_current_timer_id():
    """
    Resets the current timer Id to 0.
    """
    data = get_current_timer_id()

    data = map_timer_json(0)
    save_json(data, 'tmp', 'data')

def save_current_timer_id():
    """
    Gets the current running timer from the API and saves its Id locally.

    Returns:
    int or None: Returns None if successful, or 0 if the request failed.
    """
    response = requests.get(start_timer_url, headers=headers)

    if response.status_code == 200:
        print("Timer successfully retrieved.")
        json = map_timer_json(response.json()['running']['id'])
        save_json(json, 'tmp', 'data')
    else:
        print(f"Error retrieving timer. Status code: {response.status_code}")
        print(response.text)
        return 0

# POST request to start the timer
def start_timer():
    """
    Starts a timer through a POST request to the API and saves the timer Id locally.
    """
    data = {
        'services_id': SERVICES_ID,
        'customers_id': CUSTOMERS_ID,
    }

    response = requests.post(start_timer_url, headers=headers, data=data)
    if response.status_code == 200:
        print("Timer successfully started.")
        save_current_timer_id()
    else:
        print(f"Error starting timer. Status code: {response.status_code}")
        print(response.text)

# POST request to stop the current timer
def stop_timer():
    """
    Stops the current timer through a DELETE request to the API.
    """
    timer_id = get_current_timer_id() # get the current timer id

    if timer_id == 0:
        print("No timer running.")
        return # If the clock is not running return

    response = requests.delete(start_timer_url + f"/{timer_id}", headers=headers)
    if response.status_code == 200:
        print("Timer successfully stopped.")
        reset_current_timer_id()
    else:
        print(f"Error stopping timer. Status code: {response.status_code}")
        print(response.text)

def clock():
    """
    Controls the clocking behavior based on predefined start and stop times, handling timer start and stop accordingly.

    This function loops indefinitely, checking current time against scheduled times and managing the timer based on these times.
    """
    schedules = eval(SCHEDULES)

    while True:
        if not is_today_a_working_day(WORKING_DAYS):
            print("Today is not a working day. Sleeping until tomorrow.")
            time.sleep(86400)  # Sleep for one day
            continue

        current_time = datetime.datetime.now().time()
        min_time_diff = float('inf')

        for start_time, stop_time in schedules:
            if VARIABLE_CLOCKING_IN == "True":
                start_time, stop_time = randomize_schedule_time(start_time, stop_time)

            start_datetime = datetime.datetime.strptime(start_time, "%H:%M:%S").time()
            stop_datetime = datetime.datetime.strptime(stop_time, "%H:%M:%S").time()

            if start_datetime <= current_time <= stop_datetime:

                # only start the timer if it is not already running
                if get_current_timer_id() == 0:
                    start_timer()

                # loop until the stop time is reached
                while current_time < stop_datetime:
                    current_time = datetime.datetime.now().time()

                    time_diff_seconds = calculate_sleep_time(current_time, stop_datetime)
                    min_time_diff = min(min_time_diff, time_diff_seconds)
                    hours, minutes, seconds = convert_seconds_to_hhmmss(min_time_diff)
                    sleep_statement = get_sleep_statement(hours, minutes, seconds)
                    
                    print(sleep_statement)
                    time.sleep(min_time_diff if min_time_diff != float('inf') else 60)

                # stop the timer only if it is running
                if get_current_timer_id() != 0:
                    stop_timer()
            else:
                time_diff_seconds = calculate_sleep_time(current_time, start_datetime)
                min_time_diff = min(min_time_diff, time_diff_seconds)

        hours, minutes, seconds = convert_seconds_to_hhmmss(min_time_diff)
        sleep_statement = get_sleep_statement(hours, minutes, seconds)

        print(sleep_statement)
        time.sleep(min_time_diff if min_time_diff != float('inf') else 60)

def on_exit():
    """
    Ensures the timer is stopped when the script exits. Registered with atexit to trigger on script termination.
    """
    # stop the timer only if it is running
    if get_current_timer_id() != 0:
        stop_timer()

# register exit-hook
atexit.register(on_exit)