from flask import Flask

from .index import index_bp


def register_views(app: Flask):
    app.register_blueprint(index_bp)
