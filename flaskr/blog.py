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

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, JobExecutionEvent
bp = Blueprint("blog", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, description, image, price, duration, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname, p.disabledBid"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY p.created DESC"
    ).fetchall()

    return render_template("blog/index.html", posts=posts)

"""
@bp.route("/test-apscheduler", methods=("GET",))
def test_apscheduler():
    print('testing scheduler...')
    current_app.apscheduler.add_job(
        func=test_scheduler,
        trigger="interval",
        seconds=5,
        id="test scheduler",
        name="test scheduler",
        replace_existing=True
    )
    return render_template("blog/index.html")
"""

@bp.route("/get-apscheduler", methods=("GET",))
def test_apscheduler():
    print('getting scheduler...')
    print(current_app.apscheduler.get_jobs())
    return render_template("blog/index.html")


#@bp.route("/timer-for-bid", methods=("GET",))
#def bidTime_apscheduler(duration):
#    print('testing timing with scheduler...')
#    current_app.apscheduler.add_job(
#        func=bidTime_scheduler,
#        trigger="date",
#        seconds=duration,
#        id="bidTime-scheduler",
#       name="bidTime-scheduler",
#        replace_existing=True
#    )
#    return render_template("blog/index.html")    




def get_post(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, description, created, author_id, username, u.firstname, u.lastname"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        # Get all needed info from the create item form
        title = request.form["title"]
        description = request.form["description"]
        image = request.form["image"] # use URL, TODO: use binary
        price = request.form["price"] # price is integer
        duration = int(request.form["duration"]) #time in seconds
        disabledBid = 0 # used for disable bids for post
        status = 'available' # status enum available, bidding, sold
        error = None

        # Validate input before putting to db
        if not title:
            error = "Title is required."
        elif not price.isnumeric():
            error = "Enter price as integer"
        
        # alert error if bad input or save to db if valid input
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, description, image, price, duration, disabledBid, status, author_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (title, description, image, price, duration, disabledBid,status, g.user["id"]),
            )
            db.commit()

            #grabbing post that was just made
            post = db.execute(
                "SELECT p.id,duration "
                " FROM post p "
                " ORDER BY p.id DESC "
                " LIMIT 1 ",
            ).fetchone()
            
            jobId = "expiring_post_" + str(post['id'])
            expiration_date = datetime.now() + relativedelta(hours=0, minutes=0, seconds=duration)

            current_app.apscheduler.add_job(
                func=expiring_post,
                trigger="date",
                id=jobId,
                name=jobId,
                replace_existing=True,
                run_date=expiration_date,
                args=[post["id"], current_app._get_current_object()]
            )
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == "POST":
        # Get all needed info from the update item form
        title = request.form["title"]
        description = request.form["description"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, description = ? WHERE id = ?", (title, description, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)


@bp.route("/<int:id>/delete", methods=("POST",))
@login_required
def delete(id):
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()
    return redirect(url_for("blog.index"))


@bp.route("/<int:post_id>/bid", methods=("POST",))
@login_required
def bid(post_id):
    author_id = g.user["id"]
    amount = request.form.get("amount", type=int)
    db = get_db()
    
    # Get user current info, eg. available fund
    user = db.execute("SELECT * FROM user WHERE id = ?", (author_id,)).fetchone()
    total_fund = user["total_fund"] if user["total_fund"] else 0
    held_fund = user["held_fund"] if user["held_fund"] else 0
    available_fund = total_fund - held_fund

    # Find post
    post = db.execute("SELECT * FROM post WHERE id = ?", (post_id,)).fetchone()

    # Check if the post is still available
    disabledBid = post['disabledBid']
    if disabledBid:
        flash("Item is sold")
        return redirect(url_for("blog.index"))


    # Check if bid is higher than current one (price/best_ask_price)
    current_ask_price = post["best_ask_price"] if post["best_ask_price"] else post["price"]
    if (amount <= current_ask_price):
        flash('Please place higher bid then current one.')
        return redirect(url_for("blog.index"))

    # Check to see enough fund to place bid
    if (total_fund is None or total_fund == 0) or (available_fund < amount):
        flash('Not enough fund. Deposit more please!')
        return redirect(url_for("blog.index"))

    # Find if there is an existing bid to that post by current user
    bid = db.execute("SELECT * FROM bid WHERE post_id = ? AND author_id = ?", (post_id, author_id,)).fetchone()

    # Create a new bid or update current bid
    if bid is None:
        # Put an amount of fund on hold for the bid
        new_held_fund = held_fund + amount
        db.execute("UPDATE user SET held_fund = ? WHERE id = ?", (new_held_fund, author_id))
        db.commit()

        # Create a bid of current user if not exist 
        db.execute("INSERT INTO bid(author_id, post_id, ask_price, status) VALUES (?, ?, ?, ?)", (author_id, post_id, amount, 'sucessful'))
        db.commit()
        bid = db.execute("SELECT id FROM bid WHERE id = ? AND author_id = ?", (post_id, author_id)).fetchone()
    else:
        # If current user has highest bid, don't need to make a higher bid
        if (bid["id"] == post["best_bid_id"]):
            flash("You're having a highest bid. Don't need to place higher.")

        # Remove old holding fund on this bid and replace by new ammount
        new_held_fund = held_fund - bid["ask_price"] + amount
        db.execute("UPDATE user SET held_fund = ? WHERE id = ?", (new_held_fund, author_id))
        db.commit()

        db.execute("UPDATE bid SET ask_price = ? WHERE id = ?", (amount, bid["id"]))
        db.commit()

    # Update post best current bid
    db.execute("UPDATE post SET best_bid_id = ?, best_ask_price = ? WHERE id = ?", (bid["id"], amount, post_id))
    db.commit()

    # Notify all other bidder that they are outbid

    return redirect(url_for("blog.index"))


def test_scheduler():
    msg = 'Scheduler run!'
    print(msg)

def expiring_post(postID, cApp):
    with cApp.app_context():
        msg = 'bidScheduler run!'
        db = get_db()
        print(msg)
        # getting duration 
        print("Disabling bids")
        update = db.execute("UPDATE post SET disabledBid = ? ,status= ? WHERE id = ?", (1, "Not Available", postID))
        db.commit()
        print(" need notify winning bid")
        print("stopping job...")
        cApp.apscheduler.subscribe(listener_post, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    
def listener_post(event):
    print(f"Received {event.__class__.__name__}")
    #TODO : get all users based on post  and notify all user here