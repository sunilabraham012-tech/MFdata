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
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {branch.upper()}_EDW_MF_DATA")

        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {branch.upper()}_EDW_MF_DATA.API_{branch.upper()}")

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {branch.upper()}_EDW_MF_DATA.API_{branch.upper()}.{branch.upper()}_API_LOAD (
                    MF_ID INT AUTOINCREMENT START 1 INCREMENT 1 ORDER,
                    SCHEME_CODE INT,
                    RAW_JSON_DATA VARIANT,
                    LOADED_TIME TIMESTAMP WITH TIME ZONE,
                    LOADED_BY STRING,
                    LOADED_FROM STRING);
            """)

        for row in api_full:
            cursor.execute(
                f"""INSERT INTO {branch.upper()}_EDW_MF_DATA.API_{branch.upper()}.{branch.upper()}_API_LOAD 
                (SCHEME_CODE, RAW_JSON_DATA,LOADED_TIME, LOADED_BY, LOADED_FROM) 
                SELECT %s, PARSE_JSON(%s), CURRENT_TIMESTAMP(), INITCAP(CURRENT_USER), %s""", 

                (row["scheme_code"], json.dumps(row), f"{branch.upper()}_BRANCH")
            )
        connection.commit()
    finally:
        cursor.close()
        connection.close()

    return True
