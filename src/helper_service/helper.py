import re
import os
import json
import datetime
import random

def randomize_schedule_time(start_time, stop_time):
    # Convert string time to datetime objects
    start_time_obj = datetime.datetime.strptime(start_time, "%H:%M:%S")
    stop_time_obj = datetime.datetime.strptime(stop_time, "%H:%M:%S")
     
    # Add random seconds to start and stop time
    randomized_start_time = start_time_obj + datetime.timedelta(seconds=random.randint(1, 300))
    randomized_stop_time = stop_time_obj + datetime.timedelta(seconds=random.randint(1, 300))
    
    # Format the result as string in "HH:MM:SS" format
    randomized_start_time_str = randomized_start_time.strftime("%H:%M:%S")
    randomized_stop_time_str = randomized_stop_time.strftime("%H:%M:%S")
    
    return randomized_start_time_str, randomized_stop_time_str

def save_json(data, file_name, path=""):
    with open(os.path.join(path, file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def is_valid_regex(pattern, string):
    return re.match(pattern, string) is not None

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