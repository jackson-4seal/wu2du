from wu2du import create_app

# maybe change to
# from wu2du import create_app

app = create_app()


if __name__ == "__main__":
    app.run()


# def create_app(test_config=None):
#     # create the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY="dev4",
#         DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
#     )

#     if test_config is None:
#         # load normal config when not testing
#         app.config.from_pyfile("config.py", silent=True)
#     else:
#         # load the test config otherwise
#         app.config.from_mapping(test_config)

#     # make sure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # simple test route page
#     @app.route("/hello")
#     def hello():
#         return "Hello, World!"

#     return app
