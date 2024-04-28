def map_json(clockodo_json):
    return [
        {
            "id": item["id"],
            "name": item["name"]
        }
        for item in clockodo_json
    ]

def map_timer_json(data):
    return {
        'your_timer_id': data
    }