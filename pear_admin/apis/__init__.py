from flask import Blueprint, Flask

from .passport import passport_api
from .rights import rights_api


def register_apis(app: Flask):
    apis = Blueprint("api", __name__, url_prefix="/api/v1")

    apis.register_blueprint(passport_api)
    apis.register_blueprint(rights_api)

    app.register_blueprint(apis)
