from flask import Blueprint
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads
import requests
import urllib.request
import json

photos = UploadSet('photos', IMAGES)

app = Flask(__name__, instance_relative_config=True, template_folder='templates')
app.config["UPLOADED_PHOTOS_DEST"] = "static"
configure_uploads(app, photos)

@app.route("/")
def index():
    """ View the main page. """

    return render_template("main_page.html")


@app.route("/episodes")
def view_episodes():
    """ View the episodes in the btvs in alphabetical order. """

    url = "http://localhost:8000/api/episodes"
    response = urllib.request.urlopen(url)
    episodes = json.loads(response.read().decode())
    print(episodes)

    return render_template("btvs/episodes.html", episodes=episodes)

@app.route("/seasons")
def view_seasons():
    """ View the episodes in the btvs in alphabetical order. """

    url = "http://localhost:8000/api/seasons"
    response = urllib.request.urlopen(url)
    seasons = json.loads(response.read().decode())
    print(seasons)

    return render_template("btvs/seasons.html", seasons=seasons)

@app.route("/characters")
def view_characters():
    pass

@app.route("/crew")
def view_crew():
    pass


### EPISODES ###

@app.route("/episodes/<int:ep_id>/")
def view_episode(ep_id):
    pass

@app.route("/episodes/<int:ep_id>/edit", methods=("GET", "POST"))
def edit_episode(ep_id):
    pass

@app.route("/add_episode", methods=("GET", "POST"))
def add_episode():
    pass

@app.route("/episodes/<int:ep_id>/delete", methods=("POST",))
def delete_episode(ep_id):
    pass


### SEASONS ###

@app.route("/seasons/<int:s_id>/")
def view_season(s_id):
    pass

@app.route("/seasons/<int:s_id>/edit", methods=("GET", "POST"))
def edit_season(s_id):
    pass

@app.route("/add_season", methods=("GET", "POST"))
def add_season():
    pass

@app.route("/episodes/<int:s_id>/delete", methods=("POST",))
def delete_season(s_id):
    pass


### CHARACTERS ###

@app.route("/characters/<int:char_id>/")
def view_character(char_id):
    pass

@app.route("/characters/<int:char_id>/edit", methods=("GET", "POST"))
def edit_character(char_id):
    pass

@app.route("/add_character", methods=("GET", "POST"))
def add_character():
    pass

@app.route("/characters/<int:char_id>/delete", methods=("POST",))
def delete_character(char_id):
    pass


### CREW ###

@app.route("/crew/<int:crew_id>/")
def view_crew_member(crew_id):
    pass

@app.route("/crew/<int:crew_id>/edit", methods=("GET", "POST"))
def edit_crew(crew_id):
    pass

@app.route("/add_crew", methods=("GET", "POST"))
def add_crew():
    pass

@app.route("/crew/<int:crew_id>/delete", methods=("POST",))
def delete_crew(crew_id):
    pass