import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import json

from db import get_db

def get_user(username):
    user = (
        get_db()
        .execute(
            "SELECT users.name, users.password, users.id"
            " FROM users"
            " WHERE users.name = ?",
            (username,),
        ).fetchone()
    )
    if user is None:
        abort(404, "Season id {0} doesn't exist.".format(s_id))

    rows = (dict(user))

    json_string = json.dumps(rows)
    return json_string

def get_all_episodes():
    db = get_db()
    episodes = db.execute(
        "SELECT episodes.id, episodes.img, episodes.name, episodes.num, seasons.num as season"
        " FROM episodes"
        " INNER JOIN seasons on episodes.season_id = seasons.id"
        " ORDER BY episodes.num "
    ).fetchall()

    rows = []
    for row in episodes:
        rows.append(dict(row))

    json_string = json.dumps(rows)
    return json_string

def get_all_seasons():
    db = get_db()
    seasons = db.execute(
        "SELECT seasons.id, seasons.name, seasons.num, seasons.img"
        " FROM seasons"
        " ORDER BY seasons.num "
    ).fetchall()

    rows = []
    for row in seasons:
        rows.append(dict(row))

    json_string = json.dumps(rows)
    return json_string

def get_all_characters():
    db = get_db()
    characters = db.execute(
        "SELECT characters.id, characters.name, characters.img"
        " FROM characters"
        " ORDER BY characters.name "
    ).fetchall()

    rows = []
    for row in characters:
        rows.append(dict(row))

    json_string = json.dumps(rows)
    return json_string

def get_all_crew():
    db = get_db()
    crew = db.execute(
        "SELECT people.id, people.name, people.img"
        " FROM people"
        " ORDER BY people.name "
    ).fetchall()

    rows = []
    for row in crew:
        rows.append(dict(row))

    json_string = json.dumps(rows)
    return json_string

## EPISODE ###

def get_episode(ep_id):
    """ Get episode from the db by id. """

    episode = (
        get_db()
        .execute(
            "SELECT episodes.id, episodes.img, episodes.name, episodes.num, episodes.info, episodes.date_released, episodes.written_by, episodes.directed_by, seasons.num as season"
            " FROM episodes"
            " INNER JOIN seasons on seasons.id = episodes.season_id"
            " WHERE episodes.id = ?",
            (ep_id,),
        ).fetchone()
    )
    if episode is None:
        abort(404, "Episode id {0} doesn't exist.".format(ep_id))

    rows = (dict(episode))

    json_string = json.dumps(rows)
    return json_string

def edit_episode(data, ep_id):
    name = data.get("name")
    info = data.get("info")
    num = data.get("num")
    directed_by = data.get("directed_by")
    written_by = data.get("written_by")
    date = data.get("date")

    # Update the episode info in the database
    db = get_db()
    db.execute(
        "UPDATE episodes SET name = ?, info = ?, num = ?, directed_by = ?, written_by = ?, date_released = ? WHERE id = ?",
        (name, info, num, directed_by, written_by, date, ep_id)
    )
    db.commit()

def add_episode(data):
    name = data["name"]
    info = data["info"]
    num = data["num"]
    directed_by = data["directed_by"]
    written_by = data["written_by"]
    date = data["date"]
    season = data["season"]
    img = data["filename"]

    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO episodes (img,name,info,num,date_released,directed_by,written_by,season_id)"
        " VALUES (?,?,?,?,?,?,?,?)",
        (img, name, info, num, date, directed_by, written_by, season),
    )
    db.commit()

def delete_episode(ep_id):
    db = get_db()
    db.execute(
        "DELETE FROM episodes WHERE id = ?",
        (ep_id,)
    )
    db.commit()

## SEASON ###

def get_season(s_id):
    """ Get episode from the db by id. """

    season = (
        get_db()
        .execute(
            "SELECT seasons.id, seasons.name, seasons.num, seasons.info, seasons.img"
            " FROM seasons"
            " WHERE seasons.id = ?",
            (s_id,),
        ).fetchone()
    )
    if season is None:
        abort(404, "Season id {0} doesn't exist.".format(s_id))

    rows = (dict(season))

    json_string = json.dumps(rows)
    return json_string

def edit_season(data, s_id):
    name = data.get("name")
    info = data.get("info")
    num = data.get("num")

    # Update the episode info in the database
    db = get_db()
    db.execute(
        "UPDATE seasons SET name = ?, info = ?, num = ? WHERE id = ?",
        (name, info, num, s_id)
    )
    db.commit()

def add_season(data):
    name = data["name"]
    info = data["info"]
    num = data["num"]
    img = data["filename"]

    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO seasons (img, name, info, num) VALUES (?,?,?,?)",
        (img, name, info, num)
    )
    db.commit()

def delete_season(s_id):
    db = get_db()
    print(s_id)
    db.execute(
        "DELETE FROM episodes WHERE season_id = ?",
        (s_id,)
    )
    db.execute(
        "DELETE FROM seasons WHERE id = ?",
        (s_id,)
    )
    db.commit()

## CHARACTER ###

def get_character(char_id):
    """ Get episode from the db by id. """

    character = (
        get_db()
        .execute(
            "SELECT characters.id, characters.name, characters.played_by, characters.info, characters.img"
            " FROM characters"
            " WHERE characters.id = ?",
            (char_id,),
        ).fetchone()
    )
    if character is None:
        abort(404, "Character id {0} doesn't exist.".format(char_id))

    rows = (dict(character))

    json_string = json.dumps(rows)
    return json_string

def edit_character(data, char_id):
    name = data.get("name")
    info = data.get("info")
    actor = data.get("actor")

    # Update the episode info in the database
    db = get_db()
    db.execute(
        "UPDATE characters SET name = ?, info = ?, played_by = ? WHERE id = ?",
        (name, info, actor, char_id)
    )
    db.commit()

def add_character(data):
    name = data["name"]
    info = data["info"]
    actor = data["actor"]
    img = data["filename"]

    actor_id = get_actor_id(actor)
    if not actor_id:
        db = get_db()
        db.execute(
            "INSERT OR IGNORE INTO people (name) VALUES (?)",
            (actor,),
        )
        db.commit()


    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO characters (img, name, info, played_by) VALUES (?,?,?,?)",
        (img, name, info, get_actor_id(actor)['id'],),
    )
    db.commit()

def delete_character(char_id):
    db = get_db()
    db.execute(
        "DELETE FROM characters WHERE id = ?",
        (char_id,)
    )
    db.commit()

## CREW ###

def get_crew(crew_id):
    crew = (
        get_db()
        .execute(
            "SELECT people.id, people.name, people.info, people.img"
            " FROM people"
            " WHERE people.id = ?",
            (crew_id,),
        ).fetchone()
    )
    if crew is None:
        abort(404, "Crew member id {0} doesn't exist.".format(crew_id))

    rows = (dict(crew))

    json_string = json.dumps(rows)
    return json_string

def edit_crew(data, crew_id):
    name = data.get("name")
    info = data.get("info")

    db = get_db()
    db.execute(
        "UPDATE people SET name = ?, info = ? WHERE id = ?",
        (name, info, crew_id)
    )
    db.commit()

def add_crew(data):
    name = data["name"]
    info = data["info"]
    img = data["filename"]

    db = get_db()
    db.execute(
        "INSERT OR IGNORE INTO people (img, name, info) VALUES (?, ?, ?)",
        (img, name, info,)
    )
    db.commit()

def delete_crew(crew_id):
    db = get_db()
    db.execute(
        "DELETE FROM people WHERE id = ?",
        (crew_id,)
    )
    db.commit()

### SPECIAL ###

def get_actor_id(name):
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