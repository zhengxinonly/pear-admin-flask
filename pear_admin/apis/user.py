from datetime import datetime

from flask import Blueprint, request
from flask_sqlalchemy.pagination import Pagination

from pear_admin.extensions import db
from pear_admin.orms import UserORM

user_api = Blueprint("user", __name__)


@user_api.get("/user")
def user_list():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)
    q = db.select(UserORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)

    return {
        "code": 0,
        "message": "获取用户数据成功",
        "data": [item.json() for item in pages.items],
        "count": pages.total,
    }


@user_api.post("/user")
def create_user():
    data = request.get_json()
    if data["id"]:
        del data["id"]
    role = UserORM(**data)
    create_at = data['create_at']
    if create_at:
        role.create_at = datetime.strptime(create_at, '%Y-%m-%d %H:%M:%S')
    role.password = '123456'
    role.save()
    return {"code": 0, "message": "新增用户成功"}


@user_api.put("/user/<int:uid>")
def change_user(uid):
    data = request.get_json()
    del data["id"]

    user_obj = UserORM.query.get(uid)
    for key, value in data.items():
        if key == 'create_at':
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        setattr(user_obj, key, value)
    user_obj.save()
    return {"code": 0, "message": "修改用户信息成功"}


@user_api.delete("/user/<int:rid>")
def del_user(rid):
    user_obj = UserORM.query.get(rid)
    user_obj.delete()
    return {"code": 0, "message": "删除用户成功"}