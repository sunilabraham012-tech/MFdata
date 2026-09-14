import requests

from config import API_BASE_URL, API_KEY


def search_funds(fund):
    url = f"{API_BASE_URL}/api/search"
    headers = {"x-api-key":API_KEY}
    try:
        api_data = requests.get(url,headers=headers, timeout=10, params={"q":fund})
        api_data.raise_for_status()
    except requests.exceptions.Timeout:
        print("Request timed out after 10 seconds.")
        return None
    except requests.exceptions.HTTPError as e:
        print(e)
        print("HTTP Error!!")
        return None
        
    api_result = api_data.json()

    if api_result['error'] is None:
        return api_result['data']
    else:
        print(api_result['error'])
        return None 
    