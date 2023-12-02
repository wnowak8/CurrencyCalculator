from flask import Flask, jsonify, request
from flask_apscheduler import APScheduler

import logging
from app import config
from app.currency_data_processor import send_df_to_db


logging.basicConfig(
    level=getattr(logging, config.LOGGING_MODE),
    format="%(asctime)s.%(msecs)03d-%(levelname)s-%(funcName)s()-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

flask_app = Flask(__name__)
scheduler = APScheduler()

if __name__ == '__main__':
    scheduler.add_job(id = 'Scheduled Task', func=send_df_to_db, trigger="interval", seconds=10)
    scheduler.start()
    flask_app.run(debug=True)
