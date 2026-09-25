# Mutual Fund Data Extractor

A Python-based data extraction project that retrieves mutual fund data from the **GetMFData API**, saves the extracted data to CSV, and optionally loads the data into **Snowflake**.

Snowflake is optional. The project can be used with only the GetMFData API and CSV output.

---

## Features

* Extract mutual fund data using the GetMFData API
* Search multiple mutual funds in one execution
* Retrieve **Direct + Growth** plan data
* Save extracted data to CSV
* Generate CSV filenames based on the current Git branch
* Load extracted data into Snowflake
* Generate Snowflake tables automatically if they do not already exist
* Use branch-specific Snowflake table names
* Store API and Snowflake credentials securely using `.env`
* Handle API timeouts
* Handle API rate limits (`429`)
* Prevent partial output if a fund request fails
* Apply a cooldown between executions
* Run automated tests using `pytest`
* Run tests through GitHub Actions

---

# Project Structure

```text
MFdata/
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
│
├── data/
│   └── .last_run
│
├── src/
│   └── extractor/
│       ├── __init__.py
│       ├── main.py
│       ├── client.py
│       ├── config.py
│       └── snowflake_client.py
│
└── tests/
    └── test_client.py
```

---

# How the Project Works

```text
                 GetMFData API
                       │
                       ▼
                Search Funds
                       │
                       ▼
              Collect API Data
                       │
                       ▼
             Did every request
                 succeed?
                  /     \
                NO       YES
                │         │
                ▼         ▼
              Stop      Save CSV
                          │
                          ▼
                 Snowflake configured?
                       /       \
                     NO         YES
                     │           │
                     ▼           ▼
                   Finish   Create table
                            if necessary
                                 │
                                 ▼
                           Insert data
```

---

# 1. Requirements

Make sure you have:

* Python 3.13
* Git
* A GetMFData API key

Snowflake is optional.

---

# 2. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project:

```bash
cd MFdata
```

---

# 3. Create a Virtual Environment

Create the virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

You should see:

```text
(venv) PS E:\Python\MFdata>
```

---

# 4. Install Dependencies

Install all required packages:

```powershell
pip install -r requirements.txt
```

The project uses packages including:

* `requests` — API requests
* `python-dotenv` — loads environment variables from `.env`
* `pytest` — automated testing
* `snowflake-connector-python` — connects Python to Snowflake

---

# 5. Environment Variables

Create a `.env` file in the project root:

```text
MFdata/
├── .env
├── src/
└── ...
```

Add the GetMFData configuration:

```env
API_BASE_URL=https://getmfdata.com
API_KEY=your_api_key
```

---

## Snowflake Configuration — Optional

If you want to load the extracted data into Snowflake, add:

```env
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

If you do not have a Snowflake account, these variables are not required.

The API → CSV functionality will still work.

---

# 6. Protect `.env`

The `.env` file contains credentials and should not be committed to Git.

Add this to `.gitignore`:

```text
.env
```

Never commit:

* API keys
* Snowflake passwords
* Snowflake credentials

---

# 7. Running the Extractor

The project is run as a Python module.

From the project root:

```powershell
python -m src.extractor.main
```

The program searches for the configured funds and collects their data.

---

# 8. All-or-Nothing Extraction

The project does not save partial data.

For example, if the program searches for:

```text
parag
hdfc
axis
kotak
icici
navi
Edelweiss
JioBlackRock
Mirae
```

and all requests succeed:

```text
All API requests successful
        ↓
Collect all data
        ↓
Save CSV
        ↓
Load Snowflake if configured
```

If any request fails:

```text
One API request fails
        ↓
Stop extraction
        ↓
Do not save output
```

This prevents incomplete data from being written to the output.

---

# 9. CSV Output

The CSV filename is generated using the current Git branch.

For example:

### `main` branch

```text
data/full_data_main.csv
```

### `dev` branch

```text
data/full_data_dev.csv
```

This makes it easy to identify which branch generated the file.

---

# 10. API Error Handling

The project handles API failures.

## Timeout

If an API request takes longer than the configured timeout:

```text
Request timed out after 10 seconds.
```

The extraction stops.

## Rate Limit

If the API returns HTTP `429`:

```text
Too many requests. Rate limit reached.
```

The extraction stops instead of creating a partial output.

---

# 11. Cooldown Mechanism

The project uses a cooldown mechanism to prevent immediate repeated executions.

The last execution time is stored in:

```text
data/.last_run
```

The current cooldown is:

```python
COOLDOWN_SECONDS = 60
```

If the program is run again before the cooldown period has passed, the program waits before continuing.

---

# 12. Snowflake — Optional

Snowflake is an optional destination for the extracted data.

### Without Snowflake

```text
GetMFData API
      ↓
Extract data
      ↓
Save CSV
      ↓
Finish
```

### With Snowflake

```text
GetMFData API
      ↓
Extract data
      ↓
Save CSV
      ↓
Connect to Snowflake
      ↓
Create table if necessary
      ↓
Insert data
```

The program checks whether Snowflake credentials are available.

If:

```text
SNOWFLAKE_USER
```

is available, the Snowflake load is attempted.

If it is not available, Snowflake loading is skipped.

---

# 13. Snowflake Table Creation

The project automatically creates the required table if it does not already exist.

The equivalent SQL is:

```sql
CREATE TABLE IF NOT EXISTS MFDATA_DB.API_DEV.<BRANCH>_API_LOAD (
    MF_ID INT AUTOINCREMENT START 1 INCREMENT 1,
    SCHEME_CODE INT,
    RAW_JSON_DATA VARIANT,
    LOADED_TIME TIMESTAMP WITH TIME ZONE,
    LOADED_BY STRING,
    LOADED_FROM STRING
);
```

For example, when running from the `main` branch:

```text
MFDATA_DB.API_DEV.MAIN_API_LOAD
```

When running from the `dev` branch:

```text
MFDATA_DB.API_DEV.DEV_API_LOAD
```

### What does `IF NOT EXISTS` do?

If the table already exists:

```text
Table exists
     ↓
Do nothing
     ↓
Use existing table
```

If the table does not exist:

```text
Table does not exist
     ↓
Create table
```

It does not delete or recreate an existing table.

---

# 14. Snowflake Table Columns

| Column          | Description                                       |
| --------------- | ------------------------------------------------- |
| `MF_ID`         | Automatically generated record ID                 |
| `SCHEME_CODE`   | Mutual fund scheme code                           |
| `RAW_JSON_DATA` | Complete API record stored as Snowflake `VARIANT` |
| `LOADED_TIME`   | Timestamp when the record was loaded              |
| `LOADED_BY`     | Snowflake user who loaded the record              |
| `LOADED_FROM`   | Branch from which the data was loaded             |

---

# 15. Loading JSON Data

The complete API dictionary is stored in `RAW_JSON_DATA`.

Python converts the dictionary to a JSON string using:

```python
json.dumps(row)
```

Snowflake then converts that JSON string into a `VARIANT` using:

```sql
PARSE_JSON(%s)
```

The flow is:

```text
Python dictionary
       ↓
json.dumps()
       ↓
JSON string
       ↓
PARSE_JSON()
       ↓
Snowflake VARIANT
```

---

# 16. SQL Placeholders

The Snowflake INSERT uses `%s` placeholders.

Example:

```python
cursor.execute(
    """
    INSERT INTO table_name
    (SCHEME_CODE, RAW_JSON_DATA, LOADED_TIME, LOADED_BY, LOADED_FROM)
    SELECT %s,
           PARSE_JSON(%s),
           CURRENT_TIMESTAMP(),
           INITCAP(CURRENT_USER),
           %s
    """,
    (
        row["scheme_code"],
        json.dumps(row),
        f"{branch.upper()}_BRANCH"
    )
)
```

The three `%s` placeholders correspond to the three Python values in the same order:

```text
First %s
    ↓
row["scheme_code"]

Second %s
    ↓
json.dumps(row)

Third %s
    ↓
f"{branch.upper()}_BRANCH"
```

`CURRENT_TIMESTAMP()` and `CURRENT_USER` are generated by Snowflake.

---

# 17. Snowflake Connection

Python connects to Snowflake using:

```python
snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA")
)
```

A cursor is then created:

```python
cursor = connection.cursor()
```

The cursor is used to execute SQL statements.

---

# 18. Testing

The project uses `pytest`.

Run the tests:

```powershell
pytest -v
```

The tests cover functionality such as:

* API extraction
* CSV creation
* Snowflake connection when Snowflake credentials are available

Snowflake testing can be skipped when Snowflake credentials are not configured.

---

# 19. Updating Requirements

If you install a new Python package, make sure the virtual environment is activated.

For example:

```powershell
pip install snowflake-connector-python
```

Then update `requirements.txt`:

```powershell
pip freeze > requirements.txt
```

Another developer can then install the same dependencies with:

```powershell
pip install -r requirements.txt
```

---

# 20. Git Workflow

Development can be performed using Git branches.

Example:

```text
main
 │
 └── dev
```

Create a development branch:

```powershell
git checkout -b dev
```

After making changes:

```powershell
git add .
git commit -m "Add Snowflake integration"
git push origin dev
```

A Pull Request can then be created to merge the changes into `main`.

---

# 21. GitHub Actions

The project uses GitHub Actions to automatically run tests.

The workflow performs:

```text
Push code
    ↓
Checkout repository
    ↓
Set up Python
    ↓
Install requirements
    ↓
Run pytest
```

Credentials required by GitHub Actions should be stored using **GitHub Secrets** rather than directly in the workflow file.

---

# 22. Quick Start — Without Snowflake

A developer who does not have Snowflake can run:

```powershell
git clone <repository-url>

cd MFdata

python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```env
API_BASE_URL=https://getmfdata.com
API_KEY=your_api_key
```

Run tests:

```powershell
pytest -v
```

Run the extractor:

```powershell
python -m src.extractor.main
```

The output will be:

```text
data/full_data_<branch>.csv
```

---

# 23. Quick Start — With Snowflake

Follow the same setup steps above.

Then add the Snowflake credentials to `.env`:

```env
API_BASE_URL=https://getmfdata.com
API_KEY=your_api_key

SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=your_database
SNOWFLAKE_SCHEMA=your_schema
```

Run:

```powershell
pytest -v
```

Then:

```powershell
python -m src.extractor.main
```

The application will:

```text
GetMFData API
      ↓
Extract funds
      ↓
Save CSV
      ↓
Connect to Snowflake
      ↓
Create branch table if it doesn't exist
      ↓
Insert extracted records
```

---

# Security

Never commit `.env` or credentials to GitHub.

Use:

* `.env` for local development
* GitHub Secrets for GitHub Actions

Keep API keys and Snowflake passwords private.
