import os
from flask import render_template
from flask import url_for
import btvs
from btvs import app
from db import init_database
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', level=logging.INFO, filemode='w')
    init_database()
    app.run(debug=True, host='127.0.0.1', port=8080)