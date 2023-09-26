from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "hello pear-admin-flask !"

    return app
