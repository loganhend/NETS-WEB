from flask import Blueprint
from flask import flash
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from db import get_db
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads

photos = UploadSet('photos', IMAGES)

#bp = Blueprint("btvs", __name__)

app = Flask(__name__, instance_relative_config=True, template_folder='templates')
app.config["UPLOADED_PHOTOS_DEST"] = "static"
configure_uploads(app, photos)

""" 
Fragment functions 
"""


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


""" 
View functions 
"""


@app.route("/")
def index():
    """ View the main page. """

    return render_template("main_page.html")


# 1. EPISODES


@app.route("/episodes")
def view_episodes():
    """ View the episodes in the btvs in alphabetical order. """

    db = get_db()
    episodes = db.execute(
        "SELECT episodes.id, episodes.img, episodes.name, episodes.num, seasons.num as season"
        " FROM episodes"
        " INNER JOIN seasons on episodes.season_id = seasons.id"
        " ORDER BY episodes.num "
    ).fetchall()
    return render_template("btvs/episodes.html", episodes=episodes)


@app.route("/episodes/<int:ep_id>/")
def view_episode(ep_id):
    """ View a single episode and its info in the btvs. """

    episode = get_episode(ep_id)
    return render_template("btvs/episode.html", episode=episode)


@app.route("/episodes/<int:ep_id>/edit", methods=("GET", "POST"))
def edit_episode(ep_id):
    """ Edit episode info. """

    episode = get_episode(ep_id)

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
            db = get_db()
            db.execute(
                "UPDATE episodes SET name = ?, info = ?, num = ?, directed_by = ?, written_by = ?, date_released = ?"
                " WHERE id = ?",
                (name, info, num, directed_by, written_by, date, ep_id)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/edit_episode.html", episode=episode)


@app.route("/add_episode", methods=("GET", "POST"))
def add_episode():
    """ Add new episode. """

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
            db = get_db()
            db.execute(
                "INSERT OR IGNORE INTO episodes (img,name,info,num,date_released,directed_by,written_by,season_id)"
                " VALUES (?,?,?,?,?,?,?,?)",
                (filename, name, info, num, date, directed_by, written_by, season),
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/add_episode.html")


@app.route("/episodes/<int:ep_id>/delete", methods=("POST",))
def delete_episode(ep_id):
    """ Delete an episode from the btvs. """

    get_episode(ep_id)
    db = get_db()
    db.execute(
        "DELETE FROM episodes WHERE id = ?",
        (ep_id,)
    )
    db.commit()
    return redirect(url_for("index"))


# 2. SEASONS


@app.route("/seasons")
def view_seasons():
    """ View the seasons in the btvs in alphabetical order. """

    db = get_db()
    seasons = db.execute(
        "SELECT seasons.id, seasons.name, seasons.num, seasons.img"
        " FROM seasons"
        " ORDER BY seasons.num "
    ).fetchall()
    return render_template("btvs/seasons.html", seasons=seasons)


@app.route("/seasons/<int:s_id>/")
def view_season(s_id):
    """ View a single episode and its info in the btvs. """

    season = get_season(s_id)
    return render_template("btvs/season.html", season=season)


@app.route("/seasons/<int:s_id>/edit", methods=("GET", "POST"))
def edit_season(s_id):
    """ Edit season info. """

    season = get_season(s_id)

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
            db = get_db()
            db.execute(
                "UPDATE seasons SET name = ?, info = ?, num = ? WHERE id = ?",
                (name, info, num, s_id)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/edit_season.html", season=season)


@app.route("/add_season", methods=("GET", "POST"))
def add_season():
    """ Add new season. """

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
            db = get_db()
            db.execute(
                "INSERT OR IGNORE INTO seasons (img, name, info, num) VALUES (?,?,?,?)",
                (filename, name, info, num)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/add_season.html")


@app.route("/episodes/<int:s_id>/delete", methods=("POST",))
def delete_season(s_id):
    """ Delete an episode from the btvs. """

    get_season(s_id)
    db = get_db()
    db.execute(
        "DELETE FROM seasons WHERE id = ?",
        (s_id,)
    )
    db.commit()

    db.execute(
        "DELETE FROM episodes WHERE season_id = ?",
        (s_id,)
    )
    db.commit()
    return redirect(url_for("index"))


# 3. CHARACTERS


@app.route("/characters")
def view_characters():
    """ View the characters in the btvs in alphabetical order. """

    db = get_db()
    characters = db.execute(
        "SELECT characters.id, characters.name, characters.img"
        " FROM characters"
        " ORDER BY characters.name "
    ).fetchall()
    return render_template("btvs/characters.html", characters=characters)


@app.route("/characters/<int:char_id>/")
def view_character(char_id):
    """ View a single character and its info in the btvs. """

    character = get_character(char_id)
    return render_template("btvs/character.html", character=character)


@app.route("/characters/<int:char_id>/edit", methods=("GET", "POST"))
def edit_character(char_id):
    """ Edit character info. """

    character = get_character(char_id)

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
            actor_id = get_actor_id(actor)['id']
            db = get_db()
            db.execute(
                "UPDATE characters SET name = ?, info = ?, played_by = ? WHERE id = ?",
                (name, info, actor_id, char_id)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/edit_character.html", character=character)


@app.route("/add_character", methods=("GET", "POST"))
def add_character():
    """ Add new character. """

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
                (filename, name, info, get_actor_id(actor)['id'],),
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/add_character.html")


@app.route("/characters/<int:char_id>/delete", methods=("POST",))
def delete_character(char_id):
    """ Delete a character from the btvs. """

    get_episode(char_id)
    db = get_db()
    db.execute(
        "DELETE FROM characters WHERE id = ?",
        (char_id,)
    )
    db.commit()
    return redirect(url_for("index"))


# 4. CREW


@app.route("/crew")
def view_crew():
    """ View the crew in the btvs in alphabetical order. """

    db = get_db()
    crew = db.execute(
        "SELECT people.id, people.name, people.img"
        " FROM people"
        " ORDER BY people.name "
    ).fetchall()
    return render_template("btvs/crew.html", crew=crew)


@app.route("/crew/<int:crew_id>/")
def view_crew_member(crew_id):
    """ View a single crew member and its info in the btvs. """

    crew_member = get_crew(crew_id)
    return render_template("btvs/crew_member.html", crew_member=crew_member)


@app.route("/crew/<int:crew_id>/edit", methods=("GET", "POST"))
def edit_crew(crew_id):
    """ Edit crew member info. """

    crew_member = get_crew(crew_id)

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
            db = get_db()
            db.execute(
                "UPDATE people SET name = ?, info = ? WHERE id = ?",
                (name, info, crew_id)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/edit_crew.html", crew_member=crew_member)


@app.route("/add_crew", methods=("GET", "POST"))
def add_crew():
    """ Add new crew member. """

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
            db = get_db()
            db.execute(
                "INSERT OR IGNORE INTO people (img, name, info) VALUES (?, ?, ?)",
                (filename, name, info,)
            )
            db.commit()
            return redirect(url_for("index"))
    return render_template("btvs/add_crew.html")


@app.route("/crew/<int:crew_id>/delete", methods=("POST",))
def delete_crew(crew_id):
    """ Delete a crew member from the btvs. """

    get_episode(crew_id)
    db = get_db()
    db.execute(
        "DELETE FROM people WHERE id = ?",
        (crew_id,)
    )
    db.commit()
    return redirect(url_for("index"))
