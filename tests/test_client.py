from src.extractor.client import search_funds, save_to_csv
import os

def test_search_funds():
    result = search_funds("parag")
    assert result is not None


def test_save_to_csv():
    data = search_funds("parag")
    filename = save_to_csv(data, "data/test_funds.csv")
    assert filename == "data/test_funds.csv"
    assert os.path.exists("data/test_funds.csv")


