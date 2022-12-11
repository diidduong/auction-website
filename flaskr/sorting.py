from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import current_app
from werkzeug.exceptions import abort
from datetime import *
from dateutil.relativedelta import *
from dateutil import parser
import calendar
import time
from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("sorting", __name__)


@bp.route("/sorting")
def index():
    """Show all the posts, most recent first."""
    types = [
        {"name":"Time(Most Recent)", "path":"/sorting/mostRecent"}
    ]

    return redirect(url_for("sorting.mostRecent"))

#sort by most recent
@bp.route("/sorting/mostRecent")
def mostRecent():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.price NOT NULL"
        " ORDER BY p.id DESC"
    ).fetchall()
    return render_template("sorting/sorting.html", posts=posts,sortType = "Most Recent")


#sort by oldest first
@bp.route("/sorting/oldest")
def oldest():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.price NOT NULL"
        " ORDER BY p.id ASC"
    ).fetchall()
    return render_template("sorting/sorting.html", posts=posts,sortType = "Oldest")

#sort by price ascending (low to high)
@bp.route("/sorting/priceAsc")
def priceAsc():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.price NOT NULL"
        " ORDER BY p.price ASC"
    ).fetchall()
    return render_template("sorting/sorting.html", posts=posts,sortType = "Price (Ascending)")

#sort by price descending(high to low)
@bp.route("/sorting/priceDesc")
def priceDesc():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.price NOT NULL"
        " ORDER BY p.price DESC"
    ).fetchall()
    return render_template("sorting/sorting.html", posts=posts,sortType = "Price (Descending)")