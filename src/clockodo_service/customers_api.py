from decouple import config
import requests

# Load data from .env-file
API_KEY = config('API_KEY')
EMAIL = config('EMAIL')
SUBDOMAIN = config('SUBDOMAIN')

# https://www.clockodo.com/en/api/customers/
start_timer_url = f"https://{SUBDOMAIN}.clockodo.com/api/v2/customers"

# define header for request
headers = {
    "X-ClockodoApiKey": API_KEY,
    "X-ClockodoApiUser": EMAIL,
    "X-Clockodo-External-Application": f"Clockodo;{EMAIL}"
}

def retrieve_data(url):
    """
    Retrieves data from the API URL

    Args:
    url (str): The URL from which to fetch data.

    Returns:
    dict: A clockodo JSON object if the request was successful.
    int: 0 if there was an error or the request fails.
    """

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving data from {url}. Status code: {response.status_code}")
        print(response.text)
        return 0

def get_customers():
    """
    Fetches the list of customers from the Clockodo API.

    Returns:
    dict: A JSON object containing the list of customers if the API request is successful.
    int: Returns 0 if the API request fails.
    """
    customers = retrieve_data(start_timer_url)

    if customers != 0:
        print("Customers successfully retrieved.")
    return customers