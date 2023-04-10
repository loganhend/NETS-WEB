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
    url = "http://localhost:8000/api/characters"
    response = urllib.request.urlopen(url)
    characters = json.loads(response.read().decode())
    print(characters)

    return render_template("btvs/characters.html", characters=characters)

@app.route("/crew")
def view_crew():
    url = "http://localhost:8000/api/crew"
    response = urllib.request.urlopen(url)
    crew = json.loads(response.read().decode())
    print(crew)

    return render_template("btvs/crew.html", crew=crew)


### EPISODES ###

@app.route("/episodes/<int:ep_id>/")
def view_episode(ep_id):
    url = "http://localhost:8000/api/episodes/{}/".format(ep_id)
    response = urllib.request.urlopen(url)
    episode = json.loads(response.read().decode())
    print(episode)

    return render_template("btvs/episode.html", episode=episode)

@app.route("/episodes/<int:ep_id>/edit", methods=("GET", "POST"))
def edit_episode(ep_id):
    url = "http://localhost:8000/api/episodes/{}/".format(ep_id)
    response = urllib.request.urlopen(url)
    episode = json.loads(response.read().decode())
    print(episode)

    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        num = request.form["num"]
        directed_by = request.form["directed_by"]
        written_by = request.form["written_by"]
        date = request.form["date"]
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not num:
            error = "Number of episode is required."
        if not date:
            error = "Date is required."
        if not directed_by:
            error = "Director is required."
        if not written_by:
            error = "Writer is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "num": num,
                "directed_by": directed_by,
                "written_by": written_by,
                "date": date,
            }

            url = "http://localhost:8000/api/episodes/{}/edit".format(ep_id)

            response = requests.put(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/edit_episode.html", episode=episode)

@app.route("/add_episode", methods=("GET", "POST"))
def add_episode():
    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        num = request.form["num"]
        directed_by = request.form["directed_by"]
        written_by = request.form["written_by"]
        date = request.form["date"]
        season = request.form["season"]
        # img = request.files.get('img')
        filename = photos.save(request.files['img'])
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not num:
            error = "Number of episode is required."
        if not date:
            error = "Date is required."
        if not directed_by:
            error = "Director is required."
        if not written_by:
            error = "Writer is required."
        if not season:
            error = "Season number is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "num": num,
                "directed_by": directed_by,
                "written_by": written_by,
                "date": date,
                "season": season,
                "filename": filename,
            }

            url = "http://localhost:8000/api/add_episode"

            response = requests.post(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/add_episode.html")

@app.route("/episodes/<int:ep_id>/delete", methods=("POST",))
def delete_episode(ep_id):
    """ Delete an episode from the btvs. """

    url = "http://localhost:8000/api/episodes/{}/".format(ep_id)
    response = urllib.request.urlopen(url)
    episode = json.loads(response.read().decode())
    print(episode)

    url = "http://localhost:8000/api/episodes/{}/delete".format(ep_id)

    response = requests.delete(url)
    if response.status_code == 200:
        print("Episode successfully deleted from server.")
    else:
        print("Error: could not delete episode from server.")

    return redirect(url_for("index"))


    db = get_db()
    db.execute(
        "DELETE FROM episodes WHERE id = ?",
        (ep_id,)
    )
    db.commit()



### SEASONS ###

@app.route("/seasons/<int:s_id>/")
def view_season(s_id):
    url = "http://localhost:8000/api/seasons/{}/".format(s_id)
    response = urllib.request.urlopen(url)
    season = json.loads(response.read().decode())
    print(season)

    return render_template("btvs/season.html", season=season)

@app.route("/seasons/<int:s_id>/edit", methods=("GET", "POST"))
def edit_season(s_id):
    url = "http://localhost:8000/api/seasons/{}/".format(s_id)
    response = urllib.request.urlopen(url)
    season = json.loads(response.read().decode())
    print(season)

    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        num = request.form["num"]
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not num:
            error = "Number of episode is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "num": num,
            }

            url = "http://localhost:8000/api/seasons/{}/edit".format(s_id)

            response = requests.put(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/edit_season.html", season=season)

@app.route("/add_season", methods=("GET", "POST"))
def add_season():
    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        num = request.form["num"]
        # img = request.files.get('img')
        filename = photos.save(request.files['img'])
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not num:
            error = "Number of episode is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "num": num,
                "filename": filename,
            }

            url = "http://localhost:8000/api/add_season"

            response = requests.post(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/add_season.html")

@app.route("/seasons/<int:s_id>/delete", methods=("POST",))
def delete_season(s_id):
    """ Delete an episode from the btvs. """

    url = "http://localhost:8000/api/seasons/{}/".format(s_id)
    response = urllib.request.urlopen(url)
    season = json.loads(response.read().decode())
    print(season)

    url = "http://localhost:8000/api/seasons/{}/delete".format(s_id)

    response = requests.delete(url)
    if response.status_code == 200:
        print("Season successfully deleted from server.")
    else:
        print("Error: could not delete episode from server.")

    return redirect(url_for("index"))



### CHARACTERS ###

@app.route("/characters/<int:char_id>/")
def view_character(char_id):
    url = "http://localhost:8000/api/characters/{}/".format(char_id)
    response = urllib.request.urlopen(url)
    character = json.loads(response.read().decode())
    print(character)

    return render_template("btvs/character.html", character=character)

@app.route("/characters/<int:char_id>/edit", methods=("GET", "POST"))
def edit_character(char_id):
    url = "http://localhost:8000/api/characters/{}/".format(char_id)
    response = urllib.request.urlopen(url)
    character = json.loads(response.read().decode())
    print(character)

    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        actor = request.form["actor"]
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not actor:
            error = "Actor of episode is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "actor": actor,
            }

            url = "http://localhost:8000/api/characters/{}/edit".format(char_id)

            response = requests.put(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/edit_character.html", character=character)

@app.route("/add_character", methods=("GET", "POST"))
def add_character():
    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        actor = request.form["actor"]
        # img = request.files.get('img')
        filename = photos.save(request.files['img'])
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if not actor:
            error = "Actor of episode is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "actor": actor,
                "filename": filename,
            }

            url = "http://localhost:8000/api/add_character"

            response = requests.post(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/add_character.html")

@app.route("/characters/<int:char_id>/delete", methods=("POST",))
def delete_character(char_id):
    url = "http://localhost:8000/api/characters/{}/".format(char_id)
    response = urllib.request.urlopen(url)
    character = json.loads(response.read().decode())
    print(character)

    url = "http://localhost:8000/api/characters/{}/delete".format(char_id)

    response = requests.delete(url)
    if response.status_code == 200:
        print("Character successfully deleted from server.")
    else:
        print("Error: could not delete episode from server.")

    return redirect(url_for("index"))



### CREW ###

@app.route("/crew/<int:crew_id>/")
def view_crew_member(crew_id):
    url = "http://localhost:8000/api/crew/{}/".format(crew_id)
    response = urllib.request.urlopen(url)
    crew_member = json.loads(response.read().decode())
    print(crew_member)

    return render_template("btvs/crew_member.html", crew_member=crew_member)

@app.route("/crew/<int:crew_id>/edit", methods=("GET", "POST"))
def edit_crew(crew_id):
    url = "http://localhost:8000/api/crew/{}/".format(crew_id)
    response = urllib.request.urlopen(url)
    crew_member = json.loads(response.read().decode())
    print(crew_member)

    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
            }

            url = "http://localhost:8000/api/crew/{}/edit".format(crew_id)

            response = requests.put(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/edit_crew.html", crew_member=crew_member)

@app.route("/add_crew", methods=("GET", "POST"))
def add_crew():
    if request.method == "POST":
        name = request.form["name"]
        info = request.form["info"]
        # img = request.files.get('img')
        filename = photos.save(request.files['img'])
        error = None
        if not name:
            error = "Name is required."
        if not info:
            error = "Info is required."
        if error is not None:
            flash(error)
        else:
            data = {
                "name": name,
                "info": info,
                "filename": filename,
            }

            url = "http://localhost:8000/api/add_crew"

            response = requests.post(url, json=data)

            if response.status_code == 200:
                print("Data successfully sent to server.")
            else:
                print("Error: could not send data to server.")

            return redirect(url_for("index"))

    return render_template("btvs/add_crew.html")

@app.route("/crew/<int:crew_id>/delete", methods=("POST",))
def delete_crew(crew_id):
    url = "http://localhost:8000/api/crew/{}/".format(crew_id)
    response = urllib.request.urlopen(url)
    crew_member = json.loads(response.read().decode())
    print(crew_member)

    url = "http://localhost:8000/api/crew/{}/delete".format(crew_id)

    response = requests.delete(url)
    if response.status_code == 200:
        print("Crew successfully deleted from server.")
    else:
        print("Error: could not delete episode from server.")

    return redirect(url_for("index"))