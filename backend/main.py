"""
Flask Application Main Module

This module initializes a Flask web application, configures logging, and defines an endpoint to retrieve
exchange rate data for a specific currency code. It also includes a scheduled job to periodically fetch
exchange rates data and send it to a PostgreSQL database.

Modules:
    - Flask: Web application framework.
    - APScheduler: Advanced Python Scheduler for task scheduling.
    - logging: Python logging module for handling log messages.
    - config: Configuration file for the application.
    - currency_data_processor: Module containing functions for processing exchange rate data.

Endpoints:
    - /rate/<currency_code>: GET endpoint to retrieve exchange rate data for a specific currency code.

Scheduled Job:
    - Fetches exchange rates data and sends it to the database at a specified interval.
"""
from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

import logging
from app import config
from app.currency_data_processor import get_data_by_currency, send_df_to_db


logging.basicConfig(
    level=getattr(logging, config.LOGGING_MODE),
    format="%(asctime)s.%(msecs)03d-%(levelname)s-%(funcName)s()-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

flask_app = Flask(__name__)
scheduler = APScheduler()


@flask_app.route('/rate/<currency_code>', methods=['GET'])
def get_rate(currency_code):
    """
    Get exchange rate data for a specific currency code.

    Args:
        currency_code (str): The currency code to retrieve exchange rate data.

    Returns:
        JSON: JSON response containing exchange rate data with keys:
            - "date": Date of the exchange rate.
            - "currency": Currency code.
            - "bid": Bid rate.
            - "ask": Ask rate.
        If an error occurs, returns JSON with key "error".
    """
    try:
        currency_code = request.args.get('currency_code')
        response_data = get_data_by_currency(currency_code)
        return jsonify(response_data)

    except Exception as error:
        logging.error(f"Failed to process request: {error}")
        return jsonify({"error": "Failed to process request"}), 500


if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=send_df_to_db, trigger="interval", seconds=10)
    scheduler.start()
    flask_app.run(debug=True)
