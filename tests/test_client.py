from src.extractor.client import search_funds, save_to_csv
import snowflake.connector
from dotenv import load_dotenv
import os

def test_search_funds():

    result = search_funds("parag")
    assert result is not None

def test_save_to_csv():

    data = search_funds("parag")
    filename = save_to_csv(data, "data/test_funds.csv")
    assert filename == "data/test_funds.csv"
    assert os.path.exists("data/test_funds.csv")

def test_snowflake_connection():

    load_dotenv()
    connection = snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT CURRENT_USER()")
    result = cursor.fetchone()
    assert result is not None

    cursor.close()
    connection.close()