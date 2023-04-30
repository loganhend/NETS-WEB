import os
from flask import render_template
from flask import url_for
from server import app
import logging


if __name__ == "__main__":
    logging.basicConfig(filename='logs.log', level=logging.INFO, filemode='w')
    app.run(debug=True, host='127.0.0.1', port=8080)