from flask import Blueprint, request
from flask_sqlalchemy.pagination import Pagination

from pear_admin.extensions import db
from pear_admin.orms import RoleORM

role_api = Blueprint("role", __name__)


@role_api.get("/role")
def role_list():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)
    q = db.select(RoleORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)

    return {
        "code": 0,
        "message": "获取角色数据成功",
        "data": [item.json() for item in pages.items],
        "count": pages.total,
    }


@role_api.post("/role")
def create_role():
    data = request.get_json()
    if data["id"]:
        del data["id"]
    role = RoleORM(**data)
    role.save()
    return {"code": 0, "message": "新增角色成功"}


@role_api.put("/role/<int:rid>")
def change_role(rid):
    data = request.get_json()
    del data["id"]

    role_obj = RoleORM.query.get(rid)
    for key, value in data.items():
        setattr(role_obj, key, value)
    role_obj.save()
    return {"code": 0, "message": "修改角色权限成功"}


@role_api.delete("/role/<int:rid>")
def del_role(rid):
    role_obj = RoleORM.query.get(rid)
    role_obj.delete()
    return {"code": 0, "message": "删除角色成功"}
