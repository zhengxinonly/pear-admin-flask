from flask import Blueprint, render_template

system_bp = Blueprint("system", __name__)


@system_bp.get("/system/<path1>/<path2>")
def system_view(path1, path2):
    return render_template(f"system/{path1}/{path2}")


@system_bp.get("/views/role.html")
def role_view():
    return render_template("system/role/index.html")


@system_bp.get("/views/department.html")
def department_view():
    return render_template("system/department/index.html")


@system_bp.get("/views/user.html")
def user_view():
    return render_template("system/user/index.html")
