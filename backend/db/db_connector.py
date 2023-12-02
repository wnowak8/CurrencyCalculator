"""
Database Connector Module

This module contains a class, Connector_DB, that serves as a connector to a relational database.
It provides methods for retrieving tables, writing DataFrame records to the database, and initializing
a database engine using SQLAlchemy.

Classes:
    Connector_DB: A database connector class.
"""
import logging
import pandas as pd
from sqlalchemy.orm import registry
from sqlalchemy import create_engine, Table


class Connector_DB:
    def __init__(
        self, db_driver, db_address, db_port, db_name, db_user, db_password
    ):
        """
        Initialize a database connector.

        Args:
            db_driver (str): Database driver.
            db_address (str): Database address.
            db_port (str): Database port.
            db_name (str): Database name.
            db_user (str): Database username.
            db_password (str): Database password.
        """
        self.db_driver = db_driver
        self.db_address = db_address
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        # Default schema for the database
        self.schema = "public"
        # SQLAlchemy engine for connecting to the database
        self.engine = create_engine(
            f"{self.db_driver}://{self.db_user}:{self.db_password}@{self.db_address}:{self.db_port}/{self.db_name}"
        )
        # Mapper registry for the database
        self.mapper_registry = registry()

    def get_table(self, table_name: str):
        """Get a specific table from the database.

        Args:
            table_name (str): Name of the table.

        Returns:
            (Table): Represents a table in the database.
        """
        try:
            return Table(
                table_name,
                self.mapper_registry.metadata,
                autoload=True,
                autoload_with=self.engine,
            )
        except Exception as error:
            logging.error(f"Could not get table {table_name}: {error}")
            raise

    def send_df_to_db(self, table_name: str, df: pd.DataFrame, schema=None):
        """Write records stored in a DataFrame to the database.

        Args:
            table_name (str): Name of the table.
            df (DataFrame): DataFrame with data to send to the database.
            schema (str): Name of the schema (default 'public').
        """
        try:
            logging.info("Trying to send DataFrame to the database")
            schema = schema or self.schema
            df.to_sql(
                name=table_name,
                con=self.engine,
                if_exists="append",
                index=False,
                schema=schema,
            )
            logging.info("Successfully wrote data to the database")
        except Exception as error:
            logging.error(f"Failed to write data to the database: {error}")

