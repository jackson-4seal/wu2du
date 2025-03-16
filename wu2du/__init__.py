import os
from flask import Flask

# app = Flask(__name__)

# app.config.from_mapping(
#     SECRET_KEY="dev4",
#     DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
# )

# from wu2du import views

# from wu2du import db

# db.init_app(app)


def create_app(test_config=None):
    # create the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev4",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load normal config when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config otherwise
        app.config.from_mapping(test_config)

    # make sure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .views import views

    app.register_blueprint(views, url_prefix="/")

    from .auth import auth

    app.register_blueprint(auth)

    from wu2du import db

    db.init_app(app)

    from . import lists

    app.register_blueprint(lists.bp)
    app.add_url_rule("/", endpoint="index")

    return app
