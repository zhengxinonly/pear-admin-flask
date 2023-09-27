from flask import Flask

from configs import config
from pear_admin.extensions import register_extensions
from pear_admin.orms import UserORM


def create_app(config_name="dev"):
    app = Flask("pear-admin-flask")

    app.config.from_object(config[config_name])

    register_extensions(app)

    @app.route("/")
    def index():
        return "hello pear-admin-flask !"

    return app
