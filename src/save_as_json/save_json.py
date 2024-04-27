import os
import json

def save_json(data, file_name, path=""):
    with open(os.path.join(path, file_name + ".json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)