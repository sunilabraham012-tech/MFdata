from .client import search_funds, save_to_csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

api_data = search_funds('parag')

if api_data is not None:
    save_csv = save_to_csv(api_data, "data/funds.csv")
    logger.info("Data load successful !!")
else:
    logger.error("API Data failed to fetch")
