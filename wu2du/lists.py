from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from wu2du.auth import login_required
from wu2du.db import get_db

bp = Blueprint("lists", __name__)


# SQL IS NOT ACCURATE, SEE wu2du list generation.txt for more
@bp.route("/")
@bp.route("/<list_id>")
def index(list_id=None):
    # don't display lists if user isn't logged in
    if g.user is None:
        return render_template("base.html")
    
    db = get_db()
    # get all the lists
    lists = db.execute(
        "SELECT l.id, title, created, author_id"
        " FROM todolist l WHERE l.author_id = ?"
        " ORDER BY created DESC",
        (g.user["id"],),
    ).fetchall()
    #first = dict(lists.fetchone())
    #print("first: ")
    

    first = dict(lists[0])
    print(first)
    # firstlist = db.execute(
    #      "SELECT l.id, title, created, author_id"
    #     " FROM todolist l WHERE l.author_id = ?"
    #     " ORDER BY created DESC",
    #     (g.user["id"],),
    # ).fetchone()
    # firstid = firstlist.id

    if len(lists) == 0:
        width = 0
    else:
        width = 100 / len(lists)

    # get all the items
    if list_id == "favicon.ico":
        #print("id was favicon")
        list_id = None
    if list_id is None:
        if lists:
            list_id = first["id"]
        else:
            items = None
    #print(list_id)
    
    if list_id:
        items = db.execute(
            "SELECT i.id, body, complete, list_id"
            " FROM todoitem i WHERE i.list_id = ?"
            " ORDER BY complete DESC",
            (list_id,),
        ).fetchall()
    
    #print(len(items))

    return render_template(
        "lists/index.html",
        lists=lists,
        items=items,
        width=width,
        current_list=list_id,
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
# mainly to make sure user owns the thing theyre trying to modify?

@bp.route("/<int:list_id>/delete", methods=("POST",))
@login_required
def delete(list_id):
    # get_list(list_id)
    db = get_db()
    db.execute("DELETE FROM todolist WHERE id = ?", (list_id,))
    db.commit()
    return redirect(url_for("lists.index"))


@bp.route("/<int:list_id>/listappend", methods=("GET", "POST"))
@login_required
def listappend(list_id):
    if request.method == "POST":
        body = request.form["body"]
        error = None

        if not body:
            error = "body is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute("INSERT INTO todoitem (list_id, complete, body)"
                        "VALUES (?, ?, ?)",
                        (list_id, 0, body)
                    )
            db.commit()
            return redirect(url_for("lists.index", list_id=list_id))

    return render_template("lists/append.html")

@bp.route("/<int:task_id>/<int:list_id>/deletetask", methods=("POST",))
@login_required
def deletetask(task_id, list_id):
    db = get_db()
    db.execute("DELETE FROM todoitem WHERE id = ?", (task_id,))
    db.commit()
    return redirect(url_for("lists.index", list_id=list_id))

# acting weird, sometimes changes the status of a different task
@bp.route("/<int:task_id>/<int:completed>/<int:list_id>/changestatus", methods=("POST",))
@login_required
def changestatus(task_id, completed, list_id):
    new_status = 0 if completed else 1
    db = get_db()
    db.execute("UPDATE todoitem"
               " SET complete = ?"
               " WHERE id = ?",
               (new_status, task_id)
            )
    db.commit()
    return redirect(url_for("lists.index", list_id=list_id))