from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)


@views_bp.get("/views/rights")
def rights_view():
    return render_template("views/rights/index.html")


@views_bp.get("/views/role")
def role_view():
    return render_template("views/role/index.html")


@views_bp.get("/views/role_rights/<int:rid>")
def role_rights_view(rid):
    return render_template("views/role/role_rights.html", rid=rid)


@views_bp.get("/views/department")
def department_view():
    return render_template("views/department/index.html")


@views_bp.get("/views/user")
def user_view():
    return render_template("views/user/index.html")
