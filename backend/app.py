from flask import Flask, jsonify, request
import logging
import config


logging.basicConfig(
    level=getattr(logging, config.LOGGING_MODE),
    format="%(asctime)s.%(msecs)03d-%(levelname)s-%(funcName)s()-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug=True)
