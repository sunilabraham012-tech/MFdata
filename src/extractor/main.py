from .client import search_funds, save_to_csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def maincall(funds):
    
    for fund in funds:
        api_data = search_funds(fund)

        if api_data is not None:
            save_csv = save_to_csv(api_data, f"data/{fund}.csv")
            logger.info(f"{fund.upper()} Fund Details Loaded into DB")
        else:
            logger.error(f"Data load Failed for {fund} !!")

if __name__ == '__main__':
    maincall(['parag','hdfc','axis','kotak','icici','navi'])

def pass_func():
    pass