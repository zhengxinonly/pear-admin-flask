from flask import Flask

from .init_db import db, migrate
from .init_script import register_script


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    register_script(app)
