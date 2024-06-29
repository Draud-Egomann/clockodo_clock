def map_json(clockodo_json):
    """
    Transforms a list of clockodo objects containing 'id' and 'name' keys into a new list of dictionaries
    with only these two keys retained.

    Args:
    clockodo_json (list of dict): A list of clockodo objects.

    Returns:
    list of dict: A new list of dictionaries where each dictionary contains only the 'id' and 'name'.
    """
    return [
        {
            "id": item["id"],
            "name": item["name"]
        }
        for item in clockodo_json
    ]

def map_timer_json(data: int):
    """
    Creates a dictionary with a key 'your_timer_id' assigned to the provided data.

    Args:
    data (int): Data to be used as the value for the 'your_timer_id' key in the returned dictionary.

    Returns:
    dict: A dictionary with the key 'your_timer_id' associated with the provided data.
    """
    return {
        'your_timer_id': data
    }