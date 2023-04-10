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

@app.route("/api/characters")
def get_all_characters_json():
    characters = database.get_all_characters()
    return characters

@app.route("/api/crew")
def get_all_crew_json():
    crew = database.get_all_crew()
    return crew

### EPISODES ###

@app.route("/api/episodes/<int:ep_id>/")
def get_episode(ep_id):
    episode = database.get_episode(ep_id)
    return episode

@app.route("/api/episodes/<int:ep_id>/edit", methods=["PUT"])
def edit_episode(ep_id):
    """ Edit episode info. """

    data = request.get_json()
    database.edit_episode(data, ep_id)

    # Return a success response
    return jsonify({"message": "Episode added to database."}), 200

@app.route("/api/add_episode", methods=["POST"])
def add_episode():
    data = request.json
    database.add_episode(data)

    return jsonify({"message": "Episode added to database."}), 200

@app.route("/api/episodes/<int:ep_id>/delete", methods=["DELETE"])
def delete_episode(ep_id):
    database.delete_episode(ep_id)

    return jsonify({"message": "Episode successfully deleted from the database."}), 200


### SEASONS ###

@app.route("/api/seasons/<int:s_id>/")
def get_season(s_id):
    season = database.get_season(s_id)
    return season

@app.route("/api/seasons/<int:s_id>/edit", methods=["PUT"])
def edit_season(s_id):
    """ Edit episode info. """

    data = request.get_json()
    database.edit_season(data, s_id)

    # Return a success response
    return jsonify({"message": "Season added to database."}), 200

@app.route("/api/add_season", methods=["POST"])
def add_season():
    data = request.json
    database.add_season(data)

    return jsonify({"message": "Season added to database."}), 200

@app.route("/api/seasons/<int:s_id>/delete", methods=["DELETE"])
def delete_season(s_id):
    database.delete_season(s_id)

    return jsonify({"message": "Season successfully deleted from the database."}), 200


### CHARACTERS ###

@app.route("/api/characters/<int:char_id>/")
def get_character(char_id):
    character = database.get_character(char_id)
    return character

@app.route("/api/characters/<int:char_id>/edit", methods=["PUT"])
def edit_character(char_id):
    data = request.get_json()
    database.edit_character(data, char_id)

    # Return a success response
    return jsonify({"message": "Character added to database."}), 200

@app.route("/api/add_character", methods=["POST"])
def add_character():
    data = request.json
    database.add_character(data)

    return jsonify({"message": "Character added to database."}), 200

@app.route("/api/characters/<int:char_id>/delete", methods=["DELETE"])
def delete_character(char_id):
    database.delete_character(char_id)

    return jsonify({"message": "Character successfully deleted from the database."}), 200


### CREW ###

@app.route("/api/crew/<int:crew_id>/")
def get_crew(crew_id):
    crew = database.get_crew(crew_id)
    return crew

@app.route("/api/crew/<int:crew_id>/edit", methods=["PUT"])
def edit_crew(crew_id):
    data = request.get_json()
    database.edit_crew(data, crew_id)

    # Return a success response
    return jsonify({"message": "Crew added to database."}), 200

@app.route("/api/add_crew", methods=["POST"])
def add_crew():
    data = request.json
    database.add_crew(data)

    return jsonify({"message": "Crew added to database."}), 200

@app.route("/api/crew/<int:crew_id>/delete", methods=["DELETE"])
def delete_crew(crew_id):
    database.delete_crew(crew_id)

    return jsonify({"message": "Crew successfully deleted from the database."}), 200