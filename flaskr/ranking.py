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

    redirect(url_for("ranking.get_top_ask_price"))

# Highest number of posts, frequent seller
@bp.route("/ranking/top-freq-sellers")
def get_top_freq_sellers():
    return render_template("ranking/ranking.html")

# Highest number of posts, frequent bidder
@bp.route("/ranking/top-freq-buyers")
def get_top_freq_buyers():

    return render_template("ranking/ranking.html")

# Highest purchase
@bp.route("/ranking/top-purchase")
def get_top_purchase():
    return render_template("ranking/ranking.html")

# Highest ask_price
@bp.route("/ranking/top-ask-price")
def get_top_ask_price():
    db = get_db()

    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid, p.image"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY p.created DESC"
    ).fetchall()

    return render_template("ranking/ranking.html", posts=posts)

