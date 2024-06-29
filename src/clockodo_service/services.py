from decouple import config
import requests

# Load data from .env-file
API_KEY = config('API_KEY')
EMAIL = config('EMAIL')
SUBDOMAIN = config('SUBDOMAIN')

# https://www.clockodo.com/en/api/customers/
start_timer_url = f"https://{SUBDOMAIN}.clockodo.com/api/v2/services"

# define header for request
headers = {
    "X-ClockodoApiKey": API_KEY,
    "X-ClockodoApiUser": EMAIL,
    "X-Clockodo-External-Application": f"Clockodo;{EMAIL}"
}

def env_values_set():
    if not all([API_KEY, EMAIL, SUBDOMAIN]):
        print("Please fill in the required values in the .env file.")
        return False
    return True

def retrieve_data(url):
    """
    Retrieves data from the API URL

    Args:
    url (str): The URL from which to fetch data.

    Returns:
    dict: A clockodo JSON object if the request was successful.
    int: 0 if there was an error or the request fails.
    """
    # if any of the environment variables is empty
    if env_values_set() is False:
        return 0

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error retrieving data from {url}. Status code: {response.status_code}")
        print(response.text)
        return 0
    
def get_services():
    """
    Fetches the list of services from the Clockodo API.

    Returns:
    dict: A JSON object containing the list of services if the API request is successful.
    int: Returns 0 if the API request fails.
    """
    services = retrieve_data(start_timer_url)

    if services != 0:
        print("Services successfully retrieved.")
    return services

def get_service(service_id):
    url = start_timer_url + f"/{service_id}"
    service = retrieve_data(url)

    if service != 0:
        print("Service successfully retrieved.")
    return service

if __name__ == '__main__':
    print(get_services())