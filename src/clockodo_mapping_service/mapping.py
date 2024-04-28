def map_json(clockodo_json):
    return [
        {
            "id": item["id"],
            "name": item["name"]
        }
        for item in clockodo_json
    ]