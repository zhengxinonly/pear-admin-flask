from flask import Flask

from .index import index_bp
from .views import views_bp


def register_views(app: Flask):
    app.register_blueprint(index_bp)
    app.register_blueprint(views_bp)
