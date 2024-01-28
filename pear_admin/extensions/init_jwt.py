from flask import redirect
from flask_jwt_extended import JWTManager

from pear_admin.orms.user import UserORM

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserORM.query.filter(UserORM.id == identity).one_or_none()


@jwt.expired_token_loader
def expired_token_callback():
    return {"msg": "token 已过期，请重新登录", "code": -1}, 403


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {"msg": "操作未授权，请重新登录", "code": -1}, 403
