def map_customers(customers):
    return {
        "customers": [
            {
                "id": customer["id"],
                "name": customer["name"]
            }
            for customer in customers["customers"]
        ]
    }