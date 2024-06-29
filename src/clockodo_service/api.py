from decouple import config
import requests

# Load data from .env-file
API_KEY = config('API_KEY')
EMAIL = config('EMAIL')
SUBDOMAIN = config('SUBDOMAIN')

# https://www.clockodo.com/en/api/customers/
# https://www.clockodo.com/en/api/services/
base_url = f"https://{SUBDOMAIN}.clockodo.com/api/v2/"

# define header for requests
headers = {
    "X-ClockodoApiKey": API_KEY,
    "X-ClockodoApiUser": EMAIL,
    "X-Clockodo-External-Application": f"Clockodo;{EMAIL}"
}

def retrieve_data(endpoint):
    """
    Retrieves data from the API URL

    Args:
    endpoint (str): The endpoint from which to fetch data.

    Returns:
    dict: A clockodo JSON object if the request was successful.
    int: 0 if there was an error or the request fails.
    """

    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving data from {url}. Status code: {response.status_code}")
        print(response.text)
        return 0

def get_api_data(endpoint):
    """
    Fetches data from a specified endpoint in the Clockodo API.

    Args:
    endpoint (str): The endpoint to fetch the data from.

    Returns:
    dict: A JSON object containing the data if the API request is successful.
    int: Returns 0 if the API request fails.
    """

    data = retrieve_data(endpoint)

    if data != 0:
        print(f"Data successfully retrieved from {endpoint}.")
    return data