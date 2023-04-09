from flask import Flask, jsonify, request
from flask import url_for
import logging
import os
from db import init_database
import database

app = Flask(__name__, instance_relative_config=True)

######### EPISODES #############

@app.route("/api/episodes")
def get_all_episodes_json():
    episodes = database.get_all_episodes()
    return episodes

@app.route("/api/seasons")
def get_all_seasons_json():
    seasons = database.get_all_seasons()
    return seasons

@app.route("/api/episodes/<int:ep_id>", methods=["PUT"])
def edit_episode_api(ep_id):
    """ Edit episode info. """

    episode = database.get_episode(ep_id)

    data = request.get_json()
    if not data:
        abort(400, "No data provided")

    name = data.get("name")
    info = data.get("info")
    num = data.get("num")
    directed_by = data.get("directed_by")
    written_by = data.get("written_by")
    date = data.get("date")

    error = None
    if not name:
        error = "Name is required."
    elif not info:
        error = "Info is required."
    elif not num:
        error = "Number of episode is required."
    elif not date:
        error = "Date is required."
    elif not directed_by:
        error = "Director is required."
    elif not written_by:
        error = "Writer is required."
    if error is not None:
        abort(400, error)

    db = get_db()
    db.execute(
        "UPDATE episodes SET name = ?, info = ?, num = ?, directed_by = ?, written_by = ?, date_released = ?"
        " WHERE id = ?",
        (name, info, num, directed_by, written_by, date, ep_id)
    )
    db.commit()

    return jsonify({"success": True}), 200