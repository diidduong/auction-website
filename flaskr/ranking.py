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

bp = Blueprint("ranking", __name__)


@bp.route("/ranking")
def index():
    """Show all the posts, most recent first."""
    types = [
        {"name":"Top Ask Price", "path":"/ranking/top-ask-price"}
    ]

    return redirect(url_for("ranking.get_top_ask_price"))

# Highest number of posts, frequent seller
@bp.route("/ranking/top-freq-sellers")
def get_top_freq_sellers():
    db = get_db()
    cursor = db.cursor()
    users = cursor.execute(
        "SELECT u.id, u.firstname, u.lastname, p.author_id, COUNT(*)"
        " FROM user u JOIN post p ON u.id = p.author_id"
        " GROUP BY u.id"
        " ORDER BY COUNT(p.author_id) DESC"
    )

    return render_template("ranking/ranking.html", users=users)

# Highest number of posts, frequent bidder
@bp.route("/ranking/top-freq-buyers")
def get_top_freq_buyers():
    db = get_db()
    cursor = db.cursor()
    users = cursor.execute(
        "SELECT u.id, u.firstname, u.lastname, b.author_id, COUNT(*)"
        " FROM user u JOIN bid b ON u.id = b.author_id"
        " GROUP BY u.id"
        " ORDER BY COUNT(b.author_id) DESC"
    )
    return render_template("ranking/ranking.html", users=users)

# Highest purchase
@bp.route("/ranking/top-purchase")
def get_top_purchase():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.best_ask_price NOT NULL"
        " ORDER BY p.best_ask_price DESC"
    ).fetchall()

    return render_template("ranking/ranking.html", posts=posts)

# Highest price
@bp.route("/ranking/top-price")
def get_top_ask_price():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id AND p.price NOT NULL"
        " ORDER BY p.price DESC"
    ).fetchall()

    return render_template("ranking/ranking.html", posts=posts)

