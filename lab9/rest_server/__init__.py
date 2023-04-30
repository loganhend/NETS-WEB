import os
from flask import render_template
from flask import url_for
from db import init_database
from REST import app
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='api_logs.log', level=logging.INFO, filemode='w')
    init_database()
    app.run(debug=True, host='127.0.0.1', port=8000)