from flask import Blueprint

views = Blueprint("views", __name__)


@views.route("/hello")
def hello():
    return "Hello, World!"


@views.route("/about")
def about():
    return "<h1 style='color: red'>About!!!!!!</h1>"
