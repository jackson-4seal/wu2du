from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from wu2du.auth import login_required
from wu2du.db import get_db

bp = Blueprint("lists", __name__)


# SQL IS NOT ACCURATE, SEE wu2du list generation.txt for more
@bp.route("/")
@bp.route("/<list_id>")
def index(list_id=None):
    db = get_db()
    # get all the lists
    lists = db.execute(
        "SELECT l.id, title, created, author_id"
        " FROM todolist l JOIN user u ON l.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    if len(lists) == 0:
        width = 0
    else:
        width = 100 / len(lists)

    # get all the items
    if list_id is None:
        items = None
    else:
        items = db.execute(
            "SELECT i.id, body, complete, list_id"
            " FROM todoitem i JOIN todolist l WHERE l.id = ?"
            " ORDER BY complete DESC",
            (list_id),
        ).fetchall()

    return render_template(
        "lists/index.html",
        lists=lists,
        items=items,
        width=width,
    )


@bp.route("/createlist", methods=("GET", "POST"))
@login_required
def createlist():
    if request.method == "POST":
        title = request.form["title"]
        error = None

        if not title:
            error = "Title is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO todolist (title, author_id)" " VALUES (?, ?)",
                (title, g.user["id"]),
            )
            db.commit()
            return redirect(url_for("lists.index"))

    return render_template("lists/create.html")


# get_list function to make sure a given list exists when called by update or delete


@bp.route("/<int:list_id>/delete", methods=("POST",))
@login_required
def delete(list_id):
    # get_list(list_id)
    db = get_db()
    db.execute("DELETE FROM todolist WHERE id = ?", (list_id,))
    db.commit()
    return redirect(url_for("lists.index"))
