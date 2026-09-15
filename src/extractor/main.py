from client import search_funds, save_to_csv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



api_data = search_funds('parag')
# print(api_data)

if api_data is not None:
    save_csv = save_to_csv(api_data, "data/funds.csv")
    logger.info("Data load successful !!")
else:
    logger.error("API Data failed to fetch")




# print(api_data[0].keys())
# print(api_data[1].keys())


# print(len(api_data))

# for fl in range(0, len(api_data)):
#     print(fl)
#     print(api_data[fl].keys())
    # print(fl.keys())





















