from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from wu2du.auth import login_required
from wu2du.db import get_db

bp = Blueprint("blog", __name__)


# SQL IS NOT ACCURATE, SEE wu2du list generation.txt for more
@bp.route("/")
def index():
    db = get_db()
    # get all the lists
    lists = db.execute(
        "SELECT l.id, title, created, author_id"
        " FROM list l JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    # get all the items
    items = db.execute(
        "SELECT i.id, body, complete, list_id"
        " FROM item i JOIN list l ON i.list_id = l.id"
        " ORDER BY complete DESC"
    ).fetchall()
    return render_template("lists/index.html", lists=lists, items=items)
