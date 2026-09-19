import requests
import traceback
import logging
import csv
from .config import API_BASE_URL, API_KEY

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

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
            logger.error(f"API Error: {api_result['error']}")
            return None 

    except requests.exceptions.Timeout:
        logger.error("Request timed out after 10 seconds.")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTPError: {e}")
        return None  
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return None

def save_to_csv(data, filename):
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames= data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    return filename