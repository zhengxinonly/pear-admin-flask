from flask import Blueprint, Flask

from .passport import passport_api


def register_apis(app: Flask):
    apis = Blueprint("api", __name__, url_prefix="/api/v1")

    apis.register_blueprint(passport_api)

    app.register_blueprint(apis)
