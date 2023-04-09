import sqlite3

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext
import json

from db import get_db


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
    return episode

def get_season(season_id):
    """ Get season from the db by id. """

    season = (
        get_db()
        .execute(
            "SELECT seasons.id, seasons.name, seasons.num, seasons.info, seasons.img"
            " FROM seasons"
            " WHERE seasons.id = ?",
            (season_id,),
        ).fetchone()
    )
    if season is None:
        abort(404, "Season id {0} doesn't exist.".format(season_id))
    return season

def get_character(char_id):
    """ Get character from the db by id. """

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
    return character

def get_crew(crew_id):
    """ Get crew member from the db by id. """

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
    return crew

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