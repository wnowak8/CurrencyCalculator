"""
Exchange Rate Data Processing Module

This module contains functions for fetching exchange rates data from the NBP API,
sending the data to a PostgreSQL database, and retrieving data from the database
based on a specific currency code.

Functions:
    - get_exchange_rates: Fetch exchange rates data from the NBP API for a specific currency code.
    - send_df_to_db: Retrieve exchange rates data for multiple currency codes and send it to the database.
    - get_record_from_db: Get records from the database where the 'currency' column matches the given value.
    - get_data_by_currency: Retrieve exchange rate data from the database for a specific currency code.
"""
import logging
import os
import requests
import pandas as pd
from dotenv import load_dotenv

from db.db_connector import Connector_DB
from app import config

load_dotenv()


CURRENCY_CODES = ["usd", "eur", "pln"]

connector_db = Connector_DB(
            db_driver=os.environ.get("POSTGRES_DRIVER"),
            db_address=os.environ.get("POSTGRES_HOST"),
            db_port=os.environ.get("POSTGRES_PORT"),
            db_user=os.environ.get("POSTGRES_USER"),
            db_password=os.environ.get("POSTGRES_PASSWORD"),
            db_name=os.environ.get("POSTGRES_DATABASE"),
        )

def get_exchange_rates(currency_code: str):
    """
    Fetch exchange rates data for a specific currency code from the NBP API.

    Args:
        currency_code (str): The currency code (e.g., "usd", "eur", "pln").

    Returns:
        pd.DataFrame or None: DataFrame containing exchange rates data if successful,
                              None if no data is available or an error occurs.
    """
    NBP_URL = f"http://api.nbp.pl/api/exchangerates/rates/C/{currency_code}/?format=json"

    try:
        response = requests.get(NBP_URL)

        if response.status_code == 200:
            data = response.json()
            rates = data.get("rates", [])

            if rates:
                df = pd.DataFrame(rates)
                df["effectiveDate"] = pd.to_datetime(df["effectiveDate"])
                df.drop('no', axis=1, inplace=True)
                df.rename(
                    columns={"effectiveDate": "date"}, inplace=True
                )
                df['currency'] = currency_code
                return df
            else:
                logging.warning("No data in the response.")
        else:
            logging.error(f"Error while fetching data: {response.status_code}")

    except Exception as e:
        logging.error(f"Error during data retrieval: {str(e)}")


def send_df_to_db():
    """
    Retrieve exchange rates data for multiple currency codes and send it to the database.

    Raises:
        Exception: If an error occurs during data processing.
    """
    try:
        for currency_code in CURRENCY_CODES:
            df = get_exchange_rates(currency_code)

            if df is not None:
                logging.debug(f"Data before sending: {df}")
                connector_db.send_df_to_db(table_name=config.TABLE_NAME, df=df)
                logging.info(f"Data for currency {currency_code} successfully sent to the database.")
            else:
                logging.warning(f"No data available for currency with code {currency_code}.")
    except Exception as e:
        logging.error(f"Error occurred during data processing: {str(e)}")


def get_record_from_db(currency_code: str):
    """Get records from the database where the 'currency' column matches the given value.

    Args:
        table_name (str): Name of the table.
        currency_code (str): The value to match in the 'currency' column.

        Returns:
            pd.DataFrame: DataFrame containing records that match the criteria.
        """
    try:
        table = connector_db.get_table(table_name=config.TABLE_NAME)
            
        query = table.select().where(table.c.currency == currency_code)
            
        df = pd.read_sql_query(query, con=connector_db)
        return df
    except Exception as error:
        logging.error(f"Failed to retrieve records from the database: {error}")
        raise


def get_data_by_currency(currency_code):
    """
    Retrieve exchange rate data from the database for a specific currency code.

    Args:
        currency_code (str): The currency code to filter records.

    Returns:
        dict or None: A dictionary representing exchange rate data with keys:
            - "date": Date of the exchange rate.
            - "currency": Currency code.
            - "bid": Bid rate.
            - "ask": Ask rate.
            None if no records are found.
    """
    df = connector_db.get_record_from_db(config.TABLE_NAME, currency_code)

    if not df.empty:
        row = df.iloc[0]
        rate = {
            "date": str(row["date"]),
            "currency": row["currency"],
            "bid": float(row["bid"]),
            "ask": float(row["ask"])
        }
        return rate
    else:
        return None
