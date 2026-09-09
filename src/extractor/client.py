import requests

from config import API_BASE_URL, API_KEY


def search_funds(fund):
    url = f"{API_BASE_URL}/api/search"
    headers = {"x-api-key":API_KEY}
    api_data = requests.get(url,headers=headers, timeout=10, params={"q":fund})
    return api_data.json()

a = search_funds('hdfc')
print(a)