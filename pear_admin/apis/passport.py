from collections import OrderedDict
from copy import deepcopy

from flask import Blueprint, make_response, redirect, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies,
)

from pear_admin.extensions import db
from pear_admin.orms import RightsORM, UserORM

passport_api = Blueprint("passport", __name__)


@passport_api.post("/login")
def login_in():
    data = request.get_json()

    user: UserORM = db.session.execute(
        db.select(UserORM).where(UserORM.username == data["username"])
    ).scalar()

    if not user:
        return {"message": "用户不存在", "code": -1}, 401
    if user.check_password(data["password"]):
        return {"message": "用户密码错误", "code": -1}, 401

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response = make_response({"code": 0, "message": "登录成功"})

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@passport_api.route("/logout", methods=["GET", "POST"])
@jwt_required()
def logout():
    response = make_response(redirect("/login"))
    unset_access_cookies(response)
    unset_refresh_cookies(response)
    return response


@passport_api.get("/menu")
@jwt_required()
def menus_api():
    rights_orm_list = RightsORM.query.filter(RightsORM.type != "auth").all()
    rights_list = [rights_orm.menu_json() for rights_orm in rights_orm_list]
    rights_list.sort(key=lambda x: (x["pid"], x["id"]), reverse=True)

    menu_dict_list = OrderedDict()
    for menu_dict in rights_list:
        if menu_dict["id"] in menu_dict_list.keys():  # 如果当前节点已经存在与字典中
            # 当前节点添加子节点
            menu_dict["children"] = deepcopy(menu_dict_list[menu_dict["id"]])
            menu_dict["children"].sort(key=lambda item: item["sort"])
            # 删除子节点
            del menu_dict_list[menu_dict["id"]]

        if menu_dict["pid"] not in menu_dict_list:
            menu_dict_list[menu_dict["pid"]] = [menu_dict]
        else:
            menu_dict_list[menu_dict["pid"]].append(menu_dict)

    return sorted(menu_dict_list.get(0), key=lambda item: item["sort"])
