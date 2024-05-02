from flask import Blueprint, request
from flask_sqlalchemy.pagination import Pagination

from pear_admin.extensions import db
from pear_admin.orms import DepartmentORM

department_api = Blueprint("department", __name__, url_prefix="/department")


@department_api.get("/")
def department_list():
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("limit", default=10, type=int)

    q = db.select(DepartmentORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)

    return {
        "code": 0,
        "msg": "获取部门数据成功",
        "data": [item.json() for item in pages.items],
        "count": pages.total,
    }


@department_api.post("/")
def create_department():
    data = request.get_json()
    if data.get("id"):
        del data["id"]
    department = DepartmentORM(**data)
    department.save()
    return {"code": 0, "msg": "新增部门成功"}


@department_api.put("/")
@department_api.put("/<int:rid>")
def change_department(rid=None):
    data = request.get_json()
    rid = data["id"]
    del data["id"]

    department_obj = DepartmentORM.query.get(rid)
    for key, value in data.items():
        setattr(department_obj, key, value)
    department_obj.save()
    return {"code": 0, "msg": "修改部门成功"}


@department_api.delete("/<int:rid>")
def del_department(rid):
    department_obj = DepartmentORM.query.get(rid)
    department_obj.delete()
    return {"code": 0, "msg": "删除删除成功"}


@department_api.get("/treetable")
def get_list_as_treetable():
    q = db.select(DepartmentORM)
    q = q.where(DepartmentORM.pid == 0)
    dept_orm_list = db.session.execute(q).scalars()
    ret = []
    for child in dept_orm_list:
        child_data = child.json()
        child_data["children"] = []
        if child.children:
            child_data["isParent"] = True
        for son in child.children:
            son_data = son.json()
            child_data["children"].append(son_data)
        ret.append(child_data)
    return {"code": 0, "message": "请求权限数据成功", "data": ret}
