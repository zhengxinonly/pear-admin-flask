# -*- coding: utf-8 -*-

from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_pydantic import validate
from flask_sqlalchemy import Pagination

from pear_admin.models import PaginationModel, UserModel, DepartmentModel
from pear_admin.orms import DepartmentORM, RoleORM, UserORM


class UserApi(MethodView):
    @validate()
    def get(self, uid, query: PaginationModel):

        filters = []
        if query.query:
            filters.append(UserORM.username.like("%" + query.query + "%"))

        paginate: Pagination = UserORM.query.filter(*filters).paginate(
            page=query.page, per_page=query.pre_page
        )
        items: list[UserORM] = paginate.items
        return {
            "result": {
                "total": paginate.total,
                "page": paginate.page,
                "pre_page": paginate.per_page,
                "users": [item.json() for item in items],
            },
            "meta": {
                "message": "查询数据成功",
                "status": "success",
            },
        }

    @jwt_required()
    @validate()
    def post(self, body: UserModel):
        user = UserORM()
        user.username = body.username
        user.nickname = body.nickname
        user.password = body.password
        user.mobile = body.mobile
        user.email = body.email
        user.gender = body.gender
        user.education = body.education

        role_ids: str = request.json.get("role_ids")
        role_ids_arr = role_ids.split(",")
        roles = RoleORM.query.filter(RoleORM.id.in_(role_ids_arr)).all()
        user.role = []
        user.role = roles
        user.save_to_db()
        return {
            "meta": {
                "message": "添加数据成功",
                "status": "success",
            },
        }

    @jwt_required()
    @validate()
    def put(self, uid, body: UserModel):
        user = UserORM.find_by_id(uid)
        user.username = body.username
        user.nickname = body.nickname
        if body.password:
            user.password = body.password
        user.mobile = body.mobile
        user.email = body.email
        user.gender = body.gender
        user.education = body.education
        user.state = body.state
        user.save_to_db()

        role_ids: str = request.json.get("role_ids")
        role_ids_arr = role_ids.split(",")
        roles = RoleORM.query.filter(RoleORM.id.in_(role_ids_arr)).all()
        user.role = []
        user.role = roles
        user.save_to_db()
        return {
            "meta": {
                "message": "修改数据成功",
                "status": "success",
            },
        }

    @jwt_required()
    def delete(self, uid):
        if uid in [1, 2, 3]:
            return {
                "meta": {
                    "message": "测试数据禁止删除",
                    "status": "fail",
                },
            }
        user: UserORM = UserORM.find_by_id(uid)
        user.delete_from_db()
        return {
            "meta": {
                "message": "删除数据成功",
                "status": "success",
            },
        }


def user_role(uid):
    roles: list[RoleORM] = RoleORM.query.all()
    if request.method == "GET":
        user: UserORM = UserORM.find_by_id(uid)
        rets = []
        for role in roles:
            if role in user.role:
                rets.append(
                    {
                        "id": role.id,
                        "name": role.name,
                        "desc": role.desc,
                    }
                )
        return {
            "result": {
                "user_role": rets,
            },
            "meta": {
                "message": "查询数据成功",
                "status": "success",
            },
        }
