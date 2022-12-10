from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

def get_bid(id, check_author=True):
    bid = (
        get_db()
        .execute(
            "SELECT id, author_id, created, ask_price, status"
            " FROM bid"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if bid is None:
        abort(404, f"Bid id {id} doesn't exist.")

    if check_author and bid["author_id"] != g.user["id"]:
        abort(403)
    return bid

