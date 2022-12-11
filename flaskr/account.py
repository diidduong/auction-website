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

bp = Blueprint("account", __name__)

@bp.route("/account")
@login_required
def index():
    return render_template("account/account.html")


@bp.route("/account/deposit", methods=("GET", "POST"))
@login_required
def deposit():
    if request.method == "POST":
        db = get_db()
        # Get all needed info from the create item form
        amount = request.form.get("amount", type=int)

        # Add amount to total fund
        db.execute("UPDATE user SET total_fund = ? WHERE id = ?", (g.user["total_fund"] + amount, g.user["id"]))
        db.commit()
        flash("Deposit Successful")
        return redirect(url_for("account.index"))

    return render_template("account/deposit.html")

@bp.route("/account/withdrawal", methods=("GET", "POST"))
@login_required
def withdrawal():
    if request.method == "POST":
        db = get_db()
        # Get all needed info from the create item form
        amount = request.form.get("amount", type=int)

        # Alert message if withdraw more than total fund
        if (amount > g.user["total_fund"] - g.user["held_fund"]):
            flash("Insufficient fund for withdrawal.")
            return render_template("account/withdrawal.html")

        # Update fund after withdrawal
        db.execute("UPDATE user SET total_fund = ? WHERE id = ?", (g.user["total_fund"] - amount, g.user["id"]))
        db.commit()
        flash("Withdrawal Successful")
        return redirect(url_for("account.index"))

    return render_template("account/withdrawal.html")