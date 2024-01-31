from flask import Blueprint, request
from flask_sqlalchemy.pagination import Pagination

from pear_admin.extensions import db
from pear_admin.orms import RightsORM, RoleORM

role_api = Blueprint("role", __name__)


@role_api.get("/role")
def role_list():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)
    q = db.select(RoleORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)

    return {
        "code": 0,
        "msg": "获取角色数据成功",
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
    return {"code": 0, "msg": "新增角色成功"}


@role_api.put("/role/<int:rid>")
def change_role(rid):
    data = request.get_json()
    del data["id"]

    role_obj = RoleORM.query.get(rid)
    for key, value in data.items():
        setattr(role_obj, key, value)
    role_obj.save()
    return {"code": 0, "msg": "修改角色权限成功"}


@role_api.delete("/role/<int:rid>")
def del_role(rid):
    role_obj = RoleORM.query.get(rid)
    role_obj.delete()
    return {"code": 0, "msg": "删除角色成功"}


@role_api.get("/role/role_rights/<int:rid>")
def role_rights(rid):
    role: RoleORM = db.session.execute(
        db.select(RoleORM).where(RoleORM.id == rid)
    ).scalar()
    own_rights_list = [r.id for r in role.rights_list]

    return {
        "code": 0,
        "msg": "返回角色权限数据成功",
        "data": own_rights_list,
    }


@role_api.put("/role/role_rights/<int:rid>")
def change_role_rights(rid):
    rights_ids = request.json.get("rights_ids", "")

    rights_list = rights_ids.split(",")
    role: RoleORM = db.session.execute(
        db.select(RoleORM).where(RoleORM.id == rid)
    ).scalar()
    rights_obj_list = db.session.execute(
        db.select(RightsORM).where(RightsORM.id.in_(rights_list))
    ).all()
    role.rights_list = [r[0] for r in rights_obj_list]
    role.save()
    return {"code": 0, "msg": "授权成功"}
