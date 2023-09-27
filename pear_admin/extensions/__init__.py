from flask import Flask

from .init_db import db, migrate


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
