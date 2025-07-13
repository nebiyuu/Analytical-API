# src/data_loader/load_raw_data.py
import json
import os
import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
import logging

# Assuming you have a logger setup in src/utils/logger.py
from src.utils.logger import get_logger

logger = get_logger(__name__)

# --- Configuration ---
RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'kiam')
DB_USER = os.getenv('DB_USER', 'nebiyuessayas01')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'newpass')
RAW_TABLE_NAME = 'raw_telegram_messages' # Name for your raw table

def create_raw_table(conn):
    """Creates the raw table if it doesn't exist."""
    with conn.cursor() as cur:
        create_table_query = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                message_data JSONB,
                loaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """).format(sql.Identifier(RAW_TABLE_NAME))
        cur.execute(create_table_query)
        conn.commit()
    logger.info(f"Table '{RAW_TABLE_NAME}' ensured to exist.")

def load_json_to_db():
    """Loads JSON files from the raw data directory into the PostgreSQL database."""
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        logger.info("Successfully connected to the PostgreSQL database.")

        create_raw_table(conn)

        insert_query = sql.SQL(
            "INSERT INTO {} (message_data) VALUES (%s);"
        ).format(sql.Identifier(RAW_TABLE_NAME))

        files_loaded = 0
        for filename in os.listdir(RAW_DATA_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(RAW_DATA_DIR, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Assuming each JSON file contains a list of messages or a single message object
                        if isinstance(data, list):
                            for message in data:
                                with conn.cursor() as cur:
                                    cur.execute(insert_query, (Json(message),))
                                conn.commit() # Commit after each message for simplicity, batching might be better for large datasets
                                files_loaded += 1
                        elif isinstance(data, dict):
                            with conn.cursor() as cur:
                                cur.execute(insert_query, (Json(data),))
                            conn.commit()
                            files_loaded += 1
                        else:
                            logger.warning(f"Skipping file {filename}: Unexpected JSON structure.")
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON from {filename}: {e}")
                except Exception as e:
                    logger.error(f"Error processing file {filename}: {e}")

        logger.info(f"Finished loading data. {files_loaded} JSON objects/files loaded into '{RAW_TABLE_NAME}'.")

    except Exception as e:
        logger.error(f"Database connection or loading error: {e}")
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")

if __name__ == "__main__":
    load_json_to_db()