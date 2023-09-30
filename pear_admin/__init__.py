from flask import Flask

from configs import config
from pear_admin.apis import register_apis
from pear_admin.extensions import register_extensions
from pear_admin.orms import UserORM
from pear_admin.views import register_views


def create_app(config_name="dev"):
    app = Flask("pear-admin-flask")

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_apis(app)

    register_views(app)

    return app
