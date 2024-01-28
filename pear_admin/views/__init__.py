from flask import Flask

from .index import index_bp
from .system import system_bp


def register_views(app: Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(system_bp)
