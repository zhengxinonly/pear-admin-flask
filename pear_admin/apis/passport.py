from flask import Blueprint

passport_api = Blueprint("passport", __name__)


@passport_api.post("/login")
def login_in():
    return {"message": "登录成功", "code": 0}
