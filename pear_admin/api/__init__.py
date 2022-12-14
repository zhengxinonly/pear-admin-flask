# -*- coding: utf-8 -*-
from flask import Blueprint, Flask

from pear_admin.utils.functools import register_rest_api_func

from .auth_api import LoginApi, LogoutApi
from .role_api import PermissionApi, RoleApi, permission_enable, role_permission
from .users_api import UserApi, user_role
from .department_api import DepartmentApi, batch_remove_api


def register_api(app: Flask):
    api = Blueprint("api", __name__, url_prefix="/api/private/v1")
    api.add_url_rule(
        "/login", view_func=LoginApi.as_view("login_api"), methods=["POST"]
    )
    api.add_url_rule(
        "/logout", view_func=LogoutApi.as_view("logout_api"), methods=["POST"]
    )

    register_rest_api_func(api, UserApi, "user_api", "/user/", pk="uid")
    api.add_url_rule(
        "/user/role/<int:uid>", view_func=user_role, methods=["GET", "PUT"]
    )
    register_rest_api_func(api, RoleApi, "role_api", "/role/", pk="rid")

    api.add_url_rule(
        "/role/permission/<int:rid>", view_func=role_permission, methods=["PUT"]
    )
    register_rest_api_func(
        api, PermissionApi, "permission_api", "/permission/", pk="pid"
    )
    api.add_url_rule(
        "/permission/<int:pid>/enable", view_func=permission_enable, methods=["PUT"]
    )

    register_rest_api_func(
        api, DepartmentApi, "department_api", "/department/", pk="did"
    )
    api.add_url_rule(
        "/department/batch_remove", view_func=batch_remove_api, methods=["DELETE"]
    )
    app.register_blueprint(api)
