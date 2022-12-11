from flask import Blue ,Flask
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
import os
import io
from os.path import join, dirname, realpath
UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads')
from flaskr.auth import login_required
from flaskr.db import get_db
bp = Blueprint("blog", __name__)
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg']) 


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 

@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, description, image, price, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY p.created DESC"
    ).fetchall()
    for post in posts:
        x=io.BytesIO(post['image'])
        #post['image']=x
    return render_template("blog/index.html", posts=posts)




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


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == "POST":
        # Get all needed info from the create item form
        title = request.form["title"]
        description = request.form["description"]
        #image = request.form["image"] # use URL, TODO: use binary
        image = request.files['file'] 
        price = request.form["price"] # price is integer
        status = 'available' # status enum available, bidding, sold
        error = None
        if image and allowed_file(image.filename):
            path = os.path.join(UPLOADS_PATH, secure_filename(image.filename))
            image.save(path)
            image1=convertToBinaryData(path)
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
                "INSERT INTO post (title, description, image, price, status, author_id) VALUES (?, ?, ?, ?, ?, ?)",
                (title, description, image1, price, status, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


@bp.route("/<int:id>/update", methods=["GET", "POST"])
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


@bp.route("/<int:id>/delete", methods=["POST"])
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


@bp.route("/<int:post_id>/bid", methods=["POST"])
@login_required
def bid(post_id):
    author_id = g.user["id"]
    amount = request.form["amount"]
    db = get_db()
    
    # Find if there is an existing bid to that post by current user
    bid = db.execute("SELECT id, post_id FROM bid WHERE post_id = ? AND author_id = ?", (post_id, author_id,)).fetchone()
    
    # Create a new bid or update current bid
    if bid is None:
        db.execute("INSERT INTO bid(author_id, post_id, ask_price, status) VALUES (?, ?, ?, ?)", (author_id, post_id, amount, 'sucessful'))
        db.commit()
        bid = db.execute("SELECT id FROM bid WHERE id = ? AND author_id = ?", (post_id, author_id)).fetchone()
    else:
        db.execute("UPDATE bid SET ask_price = ? WHERE id = ?", (amount, bid["id"]))
        db.commit()

    db.execute("UPDATE post SET best_bid_id = ?, best_ask_price = ? WHERE id = ?", (bid["id"], amount, post_id))
    db.commit()

    return redirect(url_for("blog.index"))

@bp.route("/sort/<int:id>", methods=["GET","POST"])
@login_required
def sort(id):
    db = get_db()
    if id==0:#latest first 
        posts = db.execute(
            "SELECT p.id, title, description, image, price, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY p.created DESC"
        ).fetchall()
    elif id==1:#highest price first
        posts = db.execute(
            "SELECT p.id, title, description, image, price, best_ask_price, p.status, p.created, p.author_id, username, u.firstname, u.lastname"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY price DESC"
        ).fetchall()
    return render_template("blog/index.html", posts=posts)