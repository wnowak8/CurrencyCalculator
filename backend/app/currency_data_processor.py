import logging
import os
import requests
import pandas as pd
from dotenv import load_dotenv

from db.db_connector import Connector_DB
from app import config

load_dotenv()


CURRENCY_CODES = ["usd", "eur", "pln"]


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
        connector_db = Connector_DB(
            db_driver=os.environ.get("POSTGRES_DRIVER"),
            db_address=os.environ.get("POSTGRES_HOST"),
            db_port=os.environ.get("POSTGRES_PORT"),
            db_user=os.environ.get("POSTGRES_USER"),
            db_password=os.environ.get("POSTGRES_PASSWORD"),
            db_name=os.environ.get("POSTGRES_DATABASE"),
        )

        for code in CURRENCY_CODES:
            df = get_exchange_rates(code)

            if df is not None:
                logging.debug(f"Data before sending: {df}")
                connector_db.send_df_to_db(table_name=config.TABLE_NAME, df=df)
                logging.info(f"Data for currency {code} successfully sent to the database.")
            else:
                logging.warning(f"No data available for currency with code {code}.")
    except Exception as e:
        logging.error(f"Error occurred during data processing: {str(e)}")
