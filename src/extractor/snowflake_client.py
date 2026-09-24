import json
import snowflake.connector
from . import config
import logging
import os
import subprocess

#Used for taking branch name.
branch = subprocess.check_output(
    ["git", "branch", "--show-current"],
    text=True
).strip()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def save_to_snowflake(api_full):

    connection = snowflake.connector.connect(
        user=config.user,
        password=config.password,
        account=config.account,
        warehouse=config.warehouse,
        database=config.database,
        schema=config.schema
        )
    cursor = connection.cursor()
    logger.info("Connected to Snowflake")

    cursor.execute("ALTER SESSION SET TIMEZONE = 'Asia/Kolkata';")

    try:
        for row in api_full:
            cursor.execute(
                f"INSERT INTO MFDATA_DB.API_DEV.{branch.upper()}_API_LOAD (SCHEME_CODE, RAW_JSON_DATA,LOADED_TIME, LOADED_BY, LOADED_FROM) SELECT %s, PARSE_JSON(%s), CURRENT_TIMESTAMP(), INITCAP(CURRENT_USER), %s", 
                (row["scheme_code"], json.dumps(row), f"{branch.upper()}_BRANCH")
            )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return True
