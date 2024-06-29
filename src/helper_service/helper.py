import re
import os
import json
import datetime
import random

def calculate_sleep_time(current_time, event_time):
    """
    Calculates the time in seconds between the current time and the next event time.

    Args:
    current_time (datetime.time): The current time.
    event_time (datetime.time): The scheduled event time.

    Returns:
    int: Number of seconds from the current time until the event time. If the event time is earlier in the day, it
         considers the event to be on the next day.
    """
    current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)
    event_datetime = datetime.datetime.combine(datetime.date.today(), event_time)

    if current_datetime > event_datetime:
        event_datetime += datetime.timedelta(days=1)

    time_diff_seconds = (event_datetime - current_datetime).total_seconds()
    return time_diff_seconds

def convert_seconds_to_hhmmss(seconds_diff):
    """
    Converts a number of seconds in seconds into hours, minutes, and seconds.

    Args:
    seconds_diff (int): Number of seconds to convert.

    Returns:
    tuple: A tuple containing hours, minutes, and seconds as integers.

    Example:
    >>> convert_seconds_to_hhmmss(3661)
    (1, 1, 1)
    """
    hours, remainder = divmod(seconds_diff, 3600)
    minutes, seconds = divmod(remainder, 60)

    return int(hours), int(minutes), int(seconds)

def get_sleep_statement(hours, minutes, seconds):
    """
    Formats a string statement indicating how long the program will sleep.

    Args:
    hours (int): Number of hours
    minutes (int): Number of minutes
    seconds (int): Number of seconds

    Returns:
    str: A string describing how long the sleep will last.

    Example:
    >>> get_sleep_statement(2, 30, 45)
    'Sleeping for 2 hours, 30 minutes, and 45 seconds.'

    >>> get_sleep_statement(0, 30, 11)
    'Sleeping for 30 minutes and 11 seconds.'

    >>> get_sleep_statement(0, 0, 5)
    'Sleeping for 5 seconds.'
    """
    parts = []

    if hours > 0:
        parts.append(f"{hours} hours")
    if minutes > 0:
        parts.append(f"{minutes} minutes")
    
    parts.append(f"and {seconds} seconds")

    return "Sleeping for " + ", ".join(parts) + "."

def randomize_schedule_time(start_time, stop_time):
    """
    Randomizes the start and stop times within a range up to 5 minutes.

    Args:
    start_time (str): Start time in "HH:MM:SS" format.
    stop_time (str): Stop time in "HH:MM:SS" format.

    Returns:
    tuple: A tuple containing the randomized start and stop times as strings.

    Example:
    >>> randomize_schedule_time("08:00:00", "18:00:00")
    ('08:04:23', '18:02:57')
    """
    # Convert string time to datetime objects
    start_time_obj = datetime.datetime.strptime(start_time, "%H:%M:%S")
    stop_time_obj = datetime.datetime.strptime(stop_time, "%H:%M:%S")
     
    # Add random seconds (up to 5 minutes) to the start and stop time
    randomized_start_time = start_time_obj + datetime.timedelta(seconds=random.randint(1, 300))
    randomized_stop_time = stop_time_obj + datetime.timedelta(seconds=random.randint(1, 300))
    
    # Format the result as string in "HH:MM:SS" format
    randomized_start_time_str = randomized_start_time.strftime("%H:%M:%S")
    randomized_stop_time_str = randomized_stop_time.strftime("%H:%M:%S")
    
    return randomized_start_time_str, randomized_stop_time_str

def save_json(data, file_name, path=""):
    """
    Saves data as a JSON file in a specified directory.

    Args:
    data (dict): Data to be saved in JSON format.
    file_name (str): The name of the file without extension.
    path (str, optional): The directory path where the file will be saved. Defaults to current directory.
    """
    create_folder(path)

    with open(os.path.join(path, file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def create_folder(path):
    """
    Creates a directory at the path if it does not already exist.
    """
    if not os.path.exists(path):
        os.makedirs(path)

def is_folder_existant(path):
    """
    Checks if a folder exists and returns True if it does, False otherwise.
    """
    return os.path.exists(path)

def is_valid_regex(pattern, string):
    """
    Validates if a string matches a given regex pattern.
    """
    return re.match(pattern, string) is not None

def is_user_input_within_range(user_input, data_list):
    """
    Checks if user input is a valid integer within the range of the given list.

    Args:
    user_input (str): The user input to validate.
    data_list (list): The list to check the range against.

    Returns:
    bool: True if the input is a valid number within the list's range, False otherwise.
    """
    try:
        int_input = int(user_input)
        if int_input < 1 or int_input > len(data_list):
            print("Please enter a number within the range.")
            return False
        return True
    except ValueError:
        print("Please enter a number.")
        return False

def is_today_a_working_day(working_days):
    today = datetime.datetime.today().strftime('%A')  # Gets today's day as a string, e.g. "Monday"
    return today in working_days