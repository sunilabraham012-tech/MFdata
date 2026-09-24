from .client import search_funds, save_to_csv
from .snowflake_client import save_to_snowflake
import logging
import time
import os
import subprocess

#Used for taking branch name.
branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True
).strip()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

COOLDOWN_FILE = "data/.last_run"
COOLDOWN_SECONDS = 60

def check_cooldown():
    if os.path.exists(COOLDOWN_FILE):
        with open(COOLDOWN_FILE, "r") as f:
            last_run = float(f.read().strip())
        elapsed = time.time() - last_run
        if elapsed < COOLDOWN_SECONDS:
            for remaining in range(60, 0, -1):
                print(f"\rPlease try again after {remaining} seconds",end="",flush=True)
                time.sleep(1)
            return False
    return True

def update_last_run():
    with open(COOLDOWN_FILE, "w") as f:
        f.write(str(time.time()))

def maincall(funds):
    full_data = []

    for fund in funds:
        api_data = search_funds(fund)

        if api_data == 'RATE_LIMIT':
            logger.error(f"Data load Failed because of Rate Limit. ")
            return False

        elif api_data is not None:
            full_data += api_data

        else:
            logger.critical("Something bad happened, Good Luck")
            return False

    save_csv = save_to_csv(full_data, f"data/full_data_{branch}.csv")
    logger.info("Fund Details got extracted and saved as csv")

    try:
        save_to_snowflake(full_data)
        logger.info("Fund Details got loaded into Snowflake")
    except Exception as e:
        logger.error(f"Snowflake load failed: {e}")
        return False   

    return True

if __name__ == '__main__':
    if check_cooldown():
        success = maincall(['parag', 'hdfc', 'axis', 'kotak', 'icici', 'navi','Edelweiss','JioBlackRock','Mirae'])
        if success:
            update_last_run()