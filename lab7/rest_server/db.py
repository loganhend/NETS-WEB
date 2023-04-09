import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import json


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    db = sqlite3.connect('server.db')
    db.row_factory = sqlite3.Row

    print("get_db()")

    return db

def get_cursor():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    db = get_db()
    sql = db.cursor()

    print("get_cursor()")

    return sql


def init_database():
    db = get_db()
    with open('schema.sql', 'r') as file:
        sql_script = file.read()
    db.executescript(sql_script)
    fill_database()
    db.commit()

def fill_database():
    fill_seasons()
    fill_series()
    fill_crew()
    fill_characters()

def fill_seasons():
    # Open the JSON file
    with open('package.json', 'r') as f:
        seasons_data = json.load(f)

    db = get_db()

    # Insert each record into the database
    for season in seasons_data:
        print(season)
        num = season['num']
        info = season['info']
        name = season['name']
        filename = season['filename']

        db.execute(
            "INSERT OR IGNORE INTO seasons (img, name, info, num) VALUES (?,?,?,?)",
            (filename, name, info, num)
        )
    db.commit()

def fill_series():
    # Open the JSON file
    with open('episodes.json', 'r') as f:
        data = json.load(f)

    db = get_db()

    # Insert each record into the database
    for record in data:
        print(record)
        date = record['date']
        directed_by = record['directed_by']
        written_by = record['written_by']
        season = record['season']
        num = record['num']
        info = record['info']
        name = record['name']
        filename = record['filename']

        # Insert the record into the database
        db.execute(
            "INSERT OR IGNORE INTO episodes (img,name,info,num,date_released,directed_by,written_by,season_id)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (filename, name, info, num, date, directed_by, written_by, season),
        )
        db.commit()

def fill_crew():
    # Open the JSON file
    with open('crew.json', 'r') as f:
        data = json.load(f)

    db = get_db()

    # Insert each record into the database
    for record in data:
        name = record['name']
        info = record['info']
        filename = record['filename']
        db.execute(
            "INSERT OR IGNORE INTO people (img, name, info) VALUES (?, ?, ?)",
            (filename, name, info,)
        )
    db.commit()

def get_actor(name):
    actor_id = (
        get_db()
        .execute(
            "SELECT people.id, people.name"
            " FROM people"
            " WHERE people.name = ?",
            (name,),
        ).fetchone()
    )
    return actor_id

def fill_characters():
    # Open the JSON file
    with open('characters.json', 'r') as f:
        characters_data = json.load(f)

    db = get_db()

    # Insert each record into the database
    for character in characters_data:
        # Get the ID of the actor from the database
        actor_id = get_actor(character['actor'])['id']

        # Insert the record into the characters table
        db.execute(
            "INSERT OR IGNORE INTO characters (img, name, info, played_by) VALUES (?,?,?,?)",
            (character['filename'], character['name'], character['info'], actor_id,)
        )
        db.commit()
