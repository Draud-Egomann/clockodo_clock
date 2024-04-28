import re
import os
import json

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