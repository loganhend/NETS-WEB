import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    db = sqlite3.connect('server.db')
    db.row_factory = sqlite3.Row
    sql = db.cursor()

    print("get_db()")

    return db


def init_database(app):
    db = get_db()
    with open('schema.sql', 'r') as file:
        sql_script = file.read()
    db.executescript(sql_script)
    db.commit()


