import requests
import traceback

from config import API_BASE_URL, API_KEY


def search_funds(fund):
    url = f"{API_BASE_URL}/api/search"
    headers = {"x-api-key":API_KEY}
    try:
        api_data = requests.get(url,headers=headers, timeout=10, params={"q":fund})
        api_data.raise_for_status()
        api_result = api_data.json()

        if api_result['error'] is None:
            return api_result['data']
        else:
            print(api_result['error'])
            return None 

    except requests.exceptions.Timeout:
        print("Request timed out after 10 seconds.")
        return None
    except requests.exceptions.HTTPError as e:
        traceback.print_exc()
        return None  
    except requests.exceptions.RequestException as e:
        traceback.print_exc()
        return None