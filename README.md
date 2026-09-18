# MFdata

A Python-based data extraction pipeline that fetches live Indian mutual fund data (NAVs, scheme details) from the [GetMFData API](https://getmfdata.com) and saves it to CSV.

## What it does

- Searches mutual funds by name via a REST API
- Handles network failures, bad API keys, and rate limits gracefully
- Logs all activity with timestamps and severity levels
- Saves fetched data to CSV for further use
- Automated tests run on every push via GitHub Actions

## Project structure

```
MFdata/
├── src/extractor/
│   ├── config.py      # Loads API credentials from .env
│   ├── client.py       # API client with error handling
│   └── main.py          # Entry point — fetches and saves data
├── tests/
│   └── test_client.py  # Automated tests (pytest)
├── data/                    # Output CSVs (not committed)
├── .github/workflows/
│   └── tests.yml          # CI: runs tests on every push
└── requirements.txt
```

## Setup

1. Clone this repo
   ```
   git clone https://github.com/sunilabraham012-tech/MFdata.git
   cd MFdata
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   API_BASE_URL=https://getmfdata.com
   API_KEY=your_api_key_here
   ```

## Usage

```
python -m src.extractor.main
```

This fetches fund data and saves it to `data/funds.csv`.

## Running tests

```
pytest -v
```

## CI

Every push to `main` automatically triggers a GitHub Actions workflow (`.github/workflows/tests.yml`) that installs dependencies and runs the test suite, using API credentials stored securely as GitHub Secrets.

## Tech stack

- Python 3.13
- `requests` — API calls
- `python-dotenv` — secrets management
- `pytest` — testing
- GitHub Actions — CI