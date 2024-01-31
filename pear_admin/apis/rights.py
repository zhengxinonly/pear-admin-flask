from copy import deepcopy

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from pear_admin.extensions import db
from pear_admin.orms import RightsORM

rights_api = Blueprint("rights", __name__)


@rights_api.get("/rights")
@jwt_required()
def rights_list():
    t = request.args.get("type", default="")
    if t == "tree":  # tree 组件数据，用于权限赋值
        # 1. 获取所有的权限
        rights_all = db.session.execute(db.select(RightsORM)).scalars()
        rights_list = [
            {"id": r.id, "pid": r.pid, "title": r.name, "sort": r.sort}
            for r in rights_all
        ]
        # 2. 获取已有权限 id 集合
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
                tree_dict[rights_dict["pid"]] = [rights_dict]
            else:
                tree_dict[rights_dict["pid"]].append(rights_dict)

        return {"code": 0, "data": tree_dict.get(0)}
    if t == "treetable":  # tree table 数据
        page = request.args.get("page", type=int, default=1)
        per_page = request.args.get("per_page", type=int, default=10)

        q = db.select(RightsORM).where(RightsORM.type == "menu")
        pages = db.paginate(q, page=page, per_page=per_page, error_out=False)

        ret = []

        # 构建树状表格的数据
        for page in pages.items:
            data = page.json()
            data["children"] = []
            for child in page.children:
                child_data = child.json()
                if child.children:
                    child_data["children"] = [
                        sub_child.json() for sub_child in child.children
                    ]
                    child_data["isParent"] = True

                data["children"].append(child_data)
                data["isParent"] = True
            ret.append(data)
        return {"code": 0, "msg": "请求权限数据成功", "count": pages.total, "data": ret}
    return {"code": 0, "msg": "请求权限数据成功，"}


@rights_api.post("/rights")
@jwt_required()
def create_rights():
    data = request.get_json()
    if not data["pid"]:
        data["pid"] = 0
    if not data["sort"]:
        data["sort"] = int(data["sort"])
    rights_obj = RightsORM(**data)
    rights_obj.save()
    return {"code": 0, "msg": "新增权限数据成功"}


@rights_api.put("/rights/<int:rid>")
@jwt_required()
def change_rights(rid):
    data = request.get_json()
    del data["id"]

    rights_obj = RightsORM.query.get(rid)
    for key, value in data.items():
        setattr(rights_obj, key, value)
    rights_obj.save()
    return {"code": 0, "msg": "修改权限数据成功"}


@rights_api.delete("/rights/<int:rid>")
@jwt_required()
def delete_rights(rid):
    rights_obj = RightsORM.query.get(rid)
    rights_obj.delete()
    return {"code": 0, "msg": "删除权限数据成功"}
