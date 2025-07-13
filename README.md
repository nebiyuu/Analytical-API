# Analytical-API

## Overview
This project is an analytical data pipeline and API for processing, storing, and analyzing Telegram channel messages. It leverages Python for data extraction/loading, PostgreSQL for storage, and dbt for data transformation and analytics.

## Project Structure

```
├── data/                # Raw and processed data
│   └── raw/             # Raw Telegram message files (JSON, images)
├── logs/                # Log files
├── models/              # dbt models (staging, marts)
├── my_project/          # dbt project directory
├── notebook/            # Jupyter notebooks for data exploration
├── src/                 # Source code (scraper, utils)
├── tests/               # dbt and SQL tests
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker setup
├── docker-compose.yml   # Docker Compose setup
├── .env                 # Environment variables
└── README.md            # Project documentation
```

## Features
- **Telegram Scraper**: Collects messages and media from Telegram channels.
- **Data Loader**: Loads raw JSON data into PostgreSQL.
- **dbt Models**: Cleans, transforms, and models data for analytics (staging, marts, dimensions, facts).
- **Testing**: Data quality tests (e.g., no future messages).
- **Jupyter Notebooks**: For data exploration and validation.
- **Logging**: Centralized logging for ETL processes.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd <project-directory>
```

### 2. Environment Variables
Create a `.env` file in the root directory (see sample below):
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=youruser
POSTGRES_PASSWORD=yourpassword
POSTGRES_DB=telegram_db
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
- Ensure PostgreSQL is running and accessible with the credentials in `.env`.
- The ETL scripts will create the required tables automatically.

### 5. Running the Data Loader
```bash
python src/utils/load_raw_to_pg.py
```
This will load all JSON files from `data/raw/` into the `raw_telegram_messages` table.

### 6. Running dbt Models
```bash
cd my_project
dbt run
```
This will build all models (staging, marts, etc.) in your database.

### 7. Running Tests
```bash
cd my_project
dbt test
```

### 8. Using Docker (Optional)
Build and run the project in a containerized environment:
```bash
docker build -t analytical-api .
docker run --env-file .env analytical-api
```

## Notebooks
Jupyter notebooks for data exploration are in the `notebook/` directory. Example: `notebook/load.ipynb` demonstrates loading and inspecting raw Telegram data.

## dbt Models Overview
- **Staging**: Cleans and standardizes raw Telegram messages (`stg_telegram_messages.sql`).
- **Data Marts**: Fact and dimension tables for analytics:
  - `fct_messages.sql`: Fact table for messages
  - `dim_channels.sql`: Channel dimension
  - `dim_dates.sql`: Date dimension
- **Tests**: Example: `no_future_messages.sql` ensures no messages are dated in the future.

## Logging
Logs are written to the `logs/` directory. Logging is configured in `src/utils/logger.py`.

## Requirements
- Python 3.10+
- PostgreSQL
- dbt-core, dbt-postgres
- Telethon, pandas, psycopg2-binary, etc. (see `requirements.txt`)


