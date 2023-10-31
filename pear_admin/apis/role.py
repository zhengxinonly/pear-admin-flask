from copy import deepcopy

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


@role_api.get("/role/role_rights/<int:rid>")
def role_rights(rid):
    role: RoleORM = db.session.execute(
        db.select(RoleORM).where(RoleORM.id == rid)
    ).scalar()

    t = request.args.get("type")
    if t == "tree":
        # 1. 获取所有的权限
        rights_all = db.session.execute(db.select(RightsORM)).scalars()
        rights_list = [
            {"id": r.id, "pid": r.pid, "title": r.name, "sort": r.sort}
            for r in rights_all
        ]
        # 2. 获取已有权限 id 集合
        own_rights_set = {r.id for r in role.rights_list}
        # 3. 列表转属性组件
        rights_list.sort(key=lambda item: (item["pid"], item["id"]), reverse=True)
        tree_dict = {}
        for rights_dict in rights_list:  # 遍历子节点
            # 2. 如果当前阶段已经存在于树状表格字典，则是父节点
            if rights_dict["id"] in tree_dict.keys():
                # 将之前的节点添加到父节点之下
                rights_dict["children"] = deepcopy(tree_dict[rights_dict["id"]])
                rights_dict["children"].sort(key=lambda item: item["sort"])
                del tree_dict[rights_dict["id"]]

            # 1. 如果父节点未出现在树状字典里面，就新增子节点列表，否则就追加
            if rights_dict["pid"] not in tree_dict.keys():
                if rights_dict["id"] in own_rights_set:
                    rights_dict["checked"] = True
                tree_dict[rights_dict["pid"]] = [rights_dict]
            else:
                if rights_dict["id"] in own_rights_set:
                    rights_dict["checked"] = True
                tree_dict[rights_dict["pid"]].append(rights_dict)

        return {"code": 0, "data": tree_dict.get(0)}

    return {
        "code": 0,
        "message": "返回角色权限数据成功",
        "data": [rights.json() for rights in role.rights_list],
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
    print(role.rights_list)
    print([r[0] for r in rights_obj_list])
    role.rights_list = [r[0] for r in rights_obj_list]
    role.save()
    print(role.rights_list)
    return {"code": 0, "message": "授权成功"}
